import hashlib

from django.core.mail import send_mail
from django.http import request
from django.template import loader

from AXF.settings import EMAIL_HOST_USER, SERVER_HOST, SERVER_PORT
from App.models import Cart


def hash_str(source):
    return hashlib.new('sha512', source.encode('utf-8')).hexdigest()


def send_email_activate(username, email, u_token):
    # 名称
    subject = '{} Activate email'.format(username)
    # 内容
    message = 'hello'

    data = {
        'username': username,
        'activate_url': 'http://{}:{}/axf/activate/?u_token={}'.format(SERVER_HOST, SERVER_PORT, u_token)
    }

    html_message = loader.get_template('user/activate.html').render(data)

    # 源
    from_email = EMAIL_HOST_USER
    # 发送列表
    recipient_list = [email]

    send_mail(
        # 名称
        subject=subject,
        # 内容
        # message='XXX',
        message=message,
        # 源
        from_email=from_email,
        # 发送列表
        recipient_list=recipient_list,
        html_message=html_message,
    )


# 根据用户id筛选cart返回总价
def get_total_price(user_id):
    carts = Cart.objects.filter(c_user=user_id).filter(c_is_select=True)

    total = 0

    for cart in carts:
        total = total + cart.c_goods_num * cart.c_goods.price
    # 保留2位小数 自动四舍五入
    return format(total, '.2f')
