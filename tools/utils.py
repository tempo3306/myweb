from random import Random # 用于生成随机码
from django.core.mail import send_mail # 发送邮件模块
from account.models import EmailVerifyRecord # 邮箱验证model
from myweb.settings import EMAIL_FROM  # setting.py添加的的配置信息

# 生成随机字符串
def random_str(randomlength=12):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


# 发送邮件
def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    # 将给用户发的信息保存在数据库中
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    # 初始化为空
    email_title = ""
    email_body = ""
    # 如果为注册类型
    if send_type == "register":
        # email_title = "你好"
        # email_body = "明天请参会"
        email_title = "沪牌一号注册激活链接"
        email_body = "您在注册沪牌一号的账号，请点击下面的链接激活你的账号: https://hupai.pro/account/active/{0}/".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass