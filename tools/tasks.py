from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery import task, Task
from .utils import send_control_email
from bid.models import Identify
from celery.schedules import crontab
from myweb import celery_app as app
from tools.getdata.get_daipai import daipaihui_newdata
from datetime import timedelta


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



#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     from celery.schedules import crontab
#     from tools.getdata.get_daipai import daipaihui_newdata
#     # Calls test('hello') every 10 seconds.
#     # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#     #
#     # # Calls test('world') every 30 seconds
#     # sender.add_periodic_task(30.0, test.s('world'), expires=10)
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#
#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab( minute='*/1'),
#         daipaihui_newdata.s(),
#     )

from celery.schedules import crontab
app.conf.timezone = 'Asia/Shanghai'

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tools.getdata.get_daipai.daipaihui_newdata',
        'schedule': crontab( minute='*/3'),
        # 'schedule': 30,
        # 'args': (16, 16)
    },
}


'''
##重试
@app.task(bind=True, default_retry_delay=300, max_retries=5)
def my_task_A():
    try:
        print("doing stuff here...")
    except SomeNetworkException as e:
        print("maybe do some clenup here....")
        self.retry(e)
'''
