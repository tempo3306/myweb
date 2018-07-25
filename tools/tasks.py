from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery import task, Task
from .utils import send_control_email
from bid.models import Identify
from celery.schedules import crontab
from myweb import celery_app
from tools.getdata.get_daipai import daipaihui_newdata

@task
def confirm_email(email):
    mail_sent = send_control_email(email)
    return mail_sent


@task
def reset_email(email):
    mail_sent = send_control_email(email, send_type='forget')
    return mail_sent

@task
def send_identify_email(email):
    mail_sent = send_control_email(email, send_type='send_once_identify_code')
    return mail_sent


##还原激活码登录状态
@task
def reset_identify_code(identify_code):
    import time
    try:
        import time
        time.sleep(60 * 5)  ##登录或keep 5分钟后将软件重置
        identify = Identify.objects.get(identify_code=identify_code)
        identify.uuuid  = 'none'
        identify.save()
    except:
        pass


class CallbackTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass




