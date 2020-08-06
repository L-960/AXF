# constant

ALL_TYPE = "0"

'''
排序规则 order
'''
ORDER_TOTAL = "0"
ORDER_PRICE_UP = "1"
ORDER_PRICE_DOWN = "2"
ORDER_SALE_UP = "3"
ORDER_SALE_DOWN = "4"

'''
HTTP_CODE
'''
HTTP_USER_EXIST = 901
HTTP_OK = 200

# ORDER_STATUS订单相关
# 已下单未付款
ORDER_STATUS_NOT_PAY = 1
# 已下单已付款未发货
ORDER_STATUS_NOT_SEND = 2
# 已下单已付款已发货未收货
ORDER_STATUS_NOT_RECEIVE = 3
# 已下单已付款已发货已收货未确认
# 已下单已付款已发货已收货已确认未评价
# 已下单已付款已发货已收货已确认已评价未追评
# 已下单已付款已发货已收货已确认已评价
# 申请售后
# 退货
# 换货
# 返修
