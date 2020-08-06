from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^market/', views.market, name='market'),
    url(r'^marketwithparams/(?P<typeid>\d+)/(?P<childcid>\d+)/(?P<order_rule>\d+)/', views.market_with_params,
        name='market_with_params'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^check_user/', views.check_user, name='check_user'),

    url(r'^logout/', views.logout, name='logout'),

    url(r'^activate/', views.activate, name='activate'),

    # 测试
    # url(r'^sendemail/', views.send_email, name='send_email'),
    # 添加减少商城商品market
    url(r'^addtocart/', views.add_to_cart, name='addtocart'),
    url(r'^subtocart/', views.sub_to_cart, name='subtocart'),

    url(r'^changecartstate/', views.change_cart_state, name='change_cart_state'),

    # 购物车商品操作
    url(r'^addshopping/', views.add_shopping, name='add_shopping'),
    url(r'^subshopping/', views.sub_shopping, name='sub_shopping'),

    url(r'^allselect/', views.all_select, name='all_select'),
    # 生成订单
    url(r'^makeorder/', views.make_order, name='make_order'),

    url(r'^orderdetail/', views.order_detail, name='order_detail'),

    # url(r'^orderlistnotpay/', views.order_list_not_pay, name='order_list_not_pay'),
]
