# -*- coding: utf-8 -*-
from alipay import AliPay
# from alipay import ISVAlipay
import os.path
BASE = os.path.dirname(os.path.abspath(__file__))
app_private_key = open(os.path.join(BASE, "key/app_private_key.pem"))
alipay_public_key = open(os.path.join(BASE, "key/alipay_public_key.pem"))

app_private_key_string = app_private_key.read()
alipay_public_key_string = alipay_public_key.read()

alipay = AliPay(
    appid="2018062460380864",
    app_notify_url="http://www.getsms.club/alipay/success",  # 默认回调url
    app_private_key_string=app_private_key_string,
    alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    sign_type="RSA2", # RSA 或者 RSA2
    debug=True  # 默认False
)


# If you don't know what ISV is, then forget about what I mentioned below
# either app_auth_code or app_auth_token should not be None

# isv_alipay = ISVAliPay(
#     appid="",
#     app_notify_url=None,  # 默认回调url
#     app_private_key_srting="",
#     alipay_public_key_string="", # alipay public key, do not use your public key!
#     sign_type="RSA", # RSA or RSA2
#     debug=False,  # False by default,
#     app_auth_code=None,
#     app_auth_token=None
# )


# 如果你是Python 2用户（考虑考虑升级到Python 3吧），请确保非ascii的字符串为utf8编码：
# For Python 2 users(you should really think about Python 3), making sure non-ascii strings are utf-8 encoded
subject = u"充值1元".encode("utf8")

# Pay via Web，open this url in your browser: https://openapi.alipay.com/gateway.do? + order_string
order_string = alipay.api_alipay_trade_page_pay    (
    out_trade_no="201611111",
    total_amount=0.01,
    subject=subject,
    return_url="http://www.getsms.club/accounts/profile",
    notify_url="http://www.getsms.club/alipay/success" # this is optional
)

# url =  'https://openapi.alipaydev.com/gateway.do?' + order_string
url = 'https://openapi.alipay.com/gateway.do?' + order_string
print url