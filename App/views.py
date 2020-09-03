import uuid

from alipay import AliPay, ISVAliPay
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from AXF.settings import MEDIA_KEY_PREFIX, ALIPAY_APPID, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY
from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, AXFUser, Cart, Order, \
    OrderGoods
from App.views_constant import *
from App.views_helper import send_email_activate, get_total_price


def home(request):
    '''
    :param request:
    :return:
    '''
    main_wheels = MainWheel.objects.all()

    main_navs = MainNav.objects.all()

    main_mustbuys = MainMustBuy.objects.all()

    main_shops = MainShop.objects.all()

    main_shop0_1 = main_shops[0:1]

    main_shop1_3 = main_shops[1:3]

    main_shop3_7 = main_shops[3:7]

    main_shop7_11 = main_shops[7:11]

    main_shows = MainShow.objects.all()

    data = {
        'title': '首页',
        'main_wheels': main_wheels,
        'main_navs': main_navs,
        'main_mustbuys': main_mustbuys,
        'main_shop0_1': main_shop0_1,
        'main_shop1_3': main_shop1_3,
        'main_shop3_7': main_shop3_7,
        'main_shop7_11': main_shop7_11,
        'main_shows': main_shows,
    }

    return render(request, 'main/home.html', context=data)


def market(request):
    return redirect(reverse('axf:market_with_params', kwargs={
        "typeid": 104749,
        "childcid": 0,
        "order_rule": "0",
    }))


def market_with_params(request, typeid, childcid, order_rule):
    ''''''
    foodtypes = FoodType.objects.all()

    goods_list = Goods.objects.filter(categoryid=typeid)

    if childcid == ALL_TYPE:
        pass
    else:
        goods_list = goods_list.filter(childcid=childcid)

    if order_rule == ORDER_TOTAL:
        pass
    elif order_rule == ORDER_PRICE_UP:
        goods_list = goods_list.order_by('price')
    elif order_rule == ORDER_PRICE_DOWN:
        goods_list = goods_list.order_by('-price')
    elif order_rule == ORDER_SALE_UP:
        goods_list = goods_list.order_by('productnum')
    elif order_rule == ORDER_SALE_DOWN:
        goods_list = goods_list.order_by('-productnum')

    foodtype = foodtypes.get(typeid=typeid)
    '''
    全部分类:0 #饮用水:103550  #茶饮/咖啡:103554 #功能饮料:103553 #酒类:103555
             #果汁饮料:103551 #碳酸饮料:103552  #整箱购:104503
             #植物蛋白:104489 #进口饮料:103556
    '''
    foodtypechildname = foodtype.childtypenames
    foodtypechildname_list = foodtypechildname.split('#')
    foodtype_childname_list = []

    for foodtypechildname in foodtypechildname_list:
        foodtype_childname_list.append(foodtypechildname.split(':'))

    order_rule_list = [
        ['综合排序', ORDER_TOTAL],
        ['价格升序', ORDER_PRICE_UP],
        ['价格降序', ORDER_PRICE_DOWN],
        ['销量升序', ORDER_SALE_UP],
        ['销量降序', ORDER_SALE_DOWN],
    ]

    # 添加功能：如果登陆 商品数量显示已添加数量
    #         未登陆   显示0
    user_id = request.session.get('user_id')
    cart_dict = {}
    cart_list = []
    if user_id:
        cart_objs = Cart.objects.filter(c_user_id=user_id)
        for cart in cart_objs:
            cart_dict[cart.c_goods_id] = cart.c_goods_num
            cart_list.append(cart.c_goods_id)

    data = {
        'title': '闪购',
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'typeid': int(typeid),
        'foodtype_childname_list': foodtype_childname_list,
        'childcid': childcid,
        'order_rule_list': order_rule_list,
        'order_rule_view': order_rule,
        'cart_dict': cart_dict,
        'cart_list': cart_list,
    }
    return render(request, 'main/market.html', context=data)


from django.template.defaulttags import register


# 新增管道方法，单纯方便上面函数，日后提取出来
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def cart(request):
    carts = Cart.objects.filter(c_user=request.user)
    is_all_select = not carts.filter(c_is_select=False).exists()
    total_price = get_total_price(request.user)
    data = {
        'title': '购物车',
        'carts': carts,
        'is_all_select': is_all_select,
        'total_price': total_price,
    }

    return render(request, 'main/cart.html', context=data)


def mine(request):
    user_id = request.session.get('user_id')

    data = {
        'title': '我的',
        'is_login': False,
    }

    if user_id:
        user = AXFUser.objects.get(pk=user_id)
        data['username'] = user.u_username
        data['icon'] = MEDIA_KEY_PREFIX + user.u_icon.url
        data['is_login'] = True
        data['order_not_pay'] = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_PAY).count()
        data['order_not_receive'] = Order.objects.filter(o_user=user).filter(
            o_status__in=[ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_SEND]).count()
    else:
        pass

    return render(request, 'main/mine.html', context=data)


def learn(request):
    return redirect('axf:home')


def register(request):
    if request.method == "GET":
        data = {
            'title': '注册',
        }
        return render(request, 'user/register.html', context=data)

    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        icon = request.FILES.get('icon')

        # password = hash_str(password)
        password = make_password(password)

        user = AXFUser()
        user.u_username = username
        user.u_password = password
        user.u_email = email
        user.u_icon = icon

        user.save()

        # 用户完成注册，发送邮件激活

        # 函数用于将10进制整数转换成16进制，以字符串形式表示。
        # 将uuid转换为字符串
        u_token = uuid.uuid4().hex
        # 需要配置缓存
        cache.set(u_token, user.id, timeout=60 * 60 * 24)

        send_email_activate(username, email, u_token)

        return redirect(reverse('axf:login'))


def login(request):
    if request.method == "GET":

        data = {
            'title': '登陆',
        }

        error_message = request.session.get('error_message')

        if error_message:
            del request.session['error_message']
            # request.user.delete()
            data['error_message'] = error_message

        return render(request, 'user/login.html', context=data)

    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        users = AXFUser.objects.filter(u_username=username)
        if users.exists():
            user = users.first()

            if check_password(password, user.u_password):

                if user.is_active:
                    request.session['user_id'] = user.id
                    # request.user = user
                    return redirect(reverse('axf:mine'))
                else:
                    print('激活失败')
                    request.session['error_message'] = 'not activate'
                    return redirect(reverse('axf:login'))

            else:
                print('密码错误')
                request.session['error_message'] = 'password error'
                return redirect(reverse('axf:login'))
        print('用户不存在')
        request.session['error_message'] = 'user is not exist'
        return redirect(reverse('axf:login'))


def check_user(request):
    username = request.GET.get('username')
    users = AXFUser.objects.filter(u_username=username)
    data = {
        'status': HTTP_OK,
        'msg': 'user can use',
    }
    if users.exists():
        data['status'] = HTTP_USER_EXIST
        data['msg'] = 'user already'
    else:
        pass

    return JsonResponse(data=data)


def logout(request):
    request.session.flush()
    return redirect(reverse('axf:mine'))


def activate(request):
    u_token = request.GET.get('u_token')
    user_id = cache.get(u_token)
    if user_id:
        # 只能激活一次 再次点击失效
        cache.delete(u_token)

        user = AXFUser.objects.get(pk=user_id)
        user.is_active = True
        user.save()
        return redirect(reverse('axf:login'))
    return None


def add_to_cart(request):
    goodsid = request.GET.get('goodsid')
    carts = Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid)

    if carts.exists():
        cart_obj = carts.first()
        cart_obj.c_goods_num = cart_obj.c_goods_num + 1
    else:
        cart_obj = Cart()
        cart_obj.c_goods_id = goodsid
        cart_obj.c_user = request.user
    cart_obj.save()

    data = {
        'status': 200,
        'msg': 'success',
        'c_goods_num': cart_obj.c_goods_num,
    }

    return JsonResponse(data=data)


def sub_to_cart(request):
    goodsid = request.GET.get('goodsid')
    carts = Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid)
    data = {}
    if carts.exists():
        cart_obj = carts.first()
        if cart_obj.c_goods_num > 0:
            cart_obj.c_goods_num = cart_obj.c_goods_num - 1
            data['status'] = 200
            data['msg'] = 'success'
            data['c_goods_num'] = cart_obj.c_goods_num
            cart_obj.save()
    else:
        data['status'] = 302
        data['msg'] = '不能再少了！'
        data['c_goods_num'] = 0

    return JsonResponse(data=data)


def change_cart_state(request):
    user_id = request.session.get('user_id')
    cart_id = request.GET.get('cartid')

    cart_obj = Cart.objects.get(pk=cart_id)

    cart_obj.c_is_select = not cart_obj.c_is_select

    cart_obj.save()

    is_all_select = not Cart.objects.filter(c_user=request.user).filter(c_is_select=False).exists()

    data = {
        'status': 200,
        'msg': 'change ok',
        'c_is_select': cart_obj.c_is_select,
        'is_all_select': is_all_select,
        'total_price': get_total_price(user_id)
    }

    return JsonResponse(data=data)


def add_shopping(request):
    user_id = request.session.get('user_id')
    cart_id = request.GET.get('cartid')
    cart_obj = Cart.objects.get(pk=cart_id)
    cart_obj.c_goods_num = cart_obj.c_goods_num + 1
    cart_obj.save()

    data = {
        'status': 200,
        'msg': 'success',
        'c_goods_num': cart_obj.c_goods_num,
        'total_price': get_total_price(user_id),
    }

    return JsonResponse(data=data)


def sub_shopping(request):
    user_id = request.session.get('user_id')
    cartid = request.GET.get("cartid")

    cart_obj = Cart.objects.get(pk=cartid)

    data = {
        'status': 200,
        'msg': 'ok',
    }

    if cart_obj.c_goods_num > 1:
        cart_obj.c_goods_num = cart_obj.c_goods_num - 1
        cart_obj.save()
        data['c_goods_num'] = cart_obj.c_goods_num
    else:
        cart_obj.delete()
        data['c_goods_num'] = 0

    data['total_price'] = get_total_price(user_id)

    return JsonResponse(data=data)


def all_select(request):
    user_id = request.session.get('user_id')
    cart_list = request.GET.get('cart_list')

    cart_list = cart_list.split("#")

    carts = Cart.objects.filter(id__in=cart_list)

    for cart_obj in carts:
        cart_obj.c_is_select = not cart_obj.c_is_select
        cart_obj.save()

    data = {
        'status': 200,
        'msg': 'ok',
        'total_price': get_total_price(user_id),
    }

    return JsonResponse(data=data)


# 生成订单
def make_order(request):
    user_id = request.session.get('user_id')
    user = AXFUser.objects.get(pk=user_id)
    # 获取用户订单中已选择商品
    carts = Cart.objects.filter(c_user=user).filter(c_is_select=True)

    order = Order()

    order.o_user = user

    order.o_price = get_total_price(user_id)

    order.save()

    for cart_obj in carts:
        # 生成订单商品
        ordergoods = OrderGoods()
        ordergoods.o_order = order
        ordergoods.o_goods_num = cart_obj.c_goods_num
        ordergoods.o_goods = cart_obj.c_goods
        ordergoods.save()
        cart_obj.delete()

    data = {
        "status": 200,
        "msg": 'ok',
        'order_id': order.id
    }

    return JsonResponse(data)


def order_detail(request):
    order_id = request.GET.get('orderid')

    order = Order.objects.get(pk=order_id)

    data = {
        'title': "订单详情",
        'order': order
    }

    return render(request, 'order/order_detail.html', context=data)


def order_list_not_pay(request):
    user_id = request.session.get('user_id')
    user = AXFUser.objects.get(pk=user_id)

    orders = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_PAY)

    data = {
        'title': '订单列表',
        'orders': orders
    }

    return render(request, 'order/order_list_not_pay.html', context=data)


def payed(request):
    data = {
        "status": 200,
        'msg': 'payed success',
    }
    order_id = request.GET.get("orderid")

    order = Order.objects.get(pk=order_id)

    order.o_status = ORDER_STATUS_NOT_SEND

    order.save()

    return JsonResponse(data)


def alipay(request):
    # 构建支付的客户端  AlipayClient
    alipay_client = AliPay(
        appid=ALIPAY_APPID,
        app_notify_url=None,  # 默认回调url
        app_private_key_string=APP_PRIVATE_KEY,
        alipay_public_key_string=ALIPAY_PUBLIC_KEY,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        #2、sign_type设置错误
        # 检查代码中sign_type的值是否正确，规则如下：
        #
        # （1）私钥为1024位长度，sign_type=RSA
        #
        # （2）私钥为2048位长度或者证书方式，sign_type=RSA2
        #
        # 注：2018年1月5日后创建的应用只支持RSA2的格式；
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=False  # 默认False
    )
    # 使用Alipay进行支付请求的发起

    # 主题
    subject = "i9 20核系列 RTX2080"

    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay_client.api_alipay_trade_page_pay(
        out_trade_no="120",  # 订单编号
        total_amount=100,  # 付款金额
        subject=subject,
        return_url="https://127.0.0.1/axf/home/",  # 交易成功后回调地址
        notify_url="http://www.baidu.com"  # 通知地址，接受付款信息，可选, 不填则使用默认notify url
    )

    # 客户端操作
    # 支付宝网关
    return redirect(to="https://openapi.alipaydev.com/gateway.do?" + order_string)
