from random import Random  # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from account.models import EmailVerifyRecord  # 邮箱验证model
from myweb.settings import EMAIL_FROM  # setting.py添加的的配置信息
from myweb.settings import DEBUG
import time



# 生成随机字符串
def random_str(randomlength=12):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def random_num(randomlength=6):
    str = ''
    chars = '0123456789'
    random = Random()
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 发送邮件
def send_control_email(email, send_type="register", **kwargs):
    # 初始化为空
    email_title = ""
    email_body = ""
    # 如果为注册类型
    if send_type == "register":
        email_record = EmailVerifyRecord()
        # 将给用户发的信息保存在数据库中
        code = random_str(10)
        email_record.code = code
        email_record.email = email
        email_record.send_type = send_type
        email_record.save()
        # email_title = "你好"
        # email_body = "明天请参会"
        email_title = "沪牌一号注册激活链接"
        if DEBUG:
            email_body = "您在注册沪牌一号的账号，请点击下面的链接激活你的账号: http://127.0.0.1:8000/account/active/{0}/".format(code)
        else:
            email_body = "您在注册沪牌一号的账号，请点击下面的链接激活你的账号: https://hupai.pro/account/active/{0}/".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == "forget":
        code = random_num(6)  # 纯数字验证码
        email_record = EmailVerifyRecord.objects.filter(email=email)[0]
        if not email_record:
            email_record = EmailVerifyRecord()
        email_record.code = code
        email_record.send_type = 'forget'
        email_record.save()
        email_title = "沪牌一号找回密码"
        email_body = "您在找回沪牌一号的密码，验证码为: {0}".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "send_once_identify_code":
        from bid.models import Identify_code
        identify_code = random_str(randomlength=6)  ##生成6位数的随机验证码
        Identify_code.objects.create(identify_code, )


##上传文件控制
def handle_uploaded_file(f):
    file_name = ""
    import os, time
    try:
        path = "media/editor" + time.strftime('/%Y/%m/%d/%H/%M/%S/')
        if not os.path.exists(path):
            os.makedirs(path)
            file_name = path + f.name
            destination = open(file_name, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
    except Exception as e:
        print(e)

    return file_name


def handle_fileupload(file, p):  ##file: request.FILES['file']    p: MEDIA下的文件夹名
    import os
    from myweb.settings import MEDIA_ROOT
    try:
        fname = file.name  # 获取文件名
        # 验证文件扩展名
        filename, extention = os.path.splitext(fname)
        rand_str = random_str(8)
        newname = r'{0}/{1}{2}'.format(p, rand_str, extention)
        path = '{0}{1}'.format(MEDIA_ROOT, newname)
        with open(path, 'wb+') as fil:
            for chunk in file.chunks():  # 分块写入文件
                fil.write(chunk)
        return newname
    except:
        return None


##初始化软件
# {"0": ["0", 40.0, 700, 0, 0.5, 55.8, true, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# "1": ["1", 35.0, 300, 0, 0.0, 48.0, true, 50.0, 700, 100, 0.4, 56.0, true, 0, 0, 0, 0, 0, 0, 0],
# "2": ["2", 40.0, 500, 0, 0.0, 53.0, 100, 0.6, 54.0, 200, 0.5, 56.0, 56.5, 0, 0, 0, 0, 0, 0, 0],
# "3": ["3", 40.0, 500, 0, 0.5, 46.0, true, 51.0, 700, 0, 0.0, 54.4, 100, 0.6, 55.6, 100, 0.5, 56.5, 57.5, 0],
# "4": [4, 48.0, 700], "yanzhengma_scale": true,
# "strategy_description": "\u5355\u67aa\u7b56\u7565 \u667a\u80fd\u63d0\u4ea4",
# "strategy_type": "2", "enter_on": true}

def init_variable():
    ##用于计算 最低成交价位置
    data = {}
    data['px_relative'] = 118  # 查找出来位置反算相对位置
    data['py_relative'] = 1
    ##计算时间位置
    data['px_timerelative'] = 94
    data['py_timerelative'] = 3

    ## 相对于最低成交价位置
    #   ## 0:加价  1：出价 2：提交  3：刷新   4 ：确认   5：价格输入框    6:验证码输入框     7：取消
    data['P_relative2'] = [[647, -98], [650, 8], [400, 89], [396, 16], [505, 68], [562, 8], [585, 8], [586, 86]]
    P_relative2 = data['P_relative2']
    data['Position_frame'] = [[0, 0] for i in range(len(P_relative2))]
    ## 限定截图位置
    data['refresh_area_relative'] = [396 - 150, 11 - 100, 396 + 150, 11 + 100]
    data['confirm_area_relative'] = [505 - 80, 68 - 50, 505 + 80, 68 + 50]
    data['yan_confirm_area_relative'] = [205 - 80, 68 - 50, 405 + 80, 68 + 50]
    data['Pos_controlframe_relative'] = [192 - 344, 514 - 183]
    data['Pos_yanzhengma_relative'] = [-277, - 65, - 97, + 45]  # 验证码所在位置
    data['Pos_yanzhengmaframe_relative'] = [297, - 283]  # 验证码框放置位置
    ##返回正确的时间
    nowtime = get_timebase()
    data['timebase_str'] = nowtime[0]
    data['target_time'] = nowtime[1]
    data['final_time'] = nowtime[2]

    return data


'''
target_time 11:30:1 策略还原的时间戳
final_time  11:29:56.5 智能出价的戴上时间
'''


def get_timebase():
    currenttime = time.time()
    timebase_str = time.strftime("%Y-%m-%d", time.localtime(currenttime))
    target_str = "{0} 11:30:1".format(timebase_str)
    finaltime_str = "{0} 11:29:56".format(timebase_str)
    target_time = time.mktime(time.strptime(target_str, "%Y-%m-%d %H:%M:%S"))  ##时间戳
    final_time = time.mktime(time.strptime(finaltime_str, "%Y-%m-%d %H:%M:%S")) + 0.5  ##时间戳
    return (timebase_str, target_time, final_time)
