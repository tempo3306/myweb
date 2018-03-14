from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery import task, Task
from .utils import send_control_email

@task
def confirm_email(email):
    mail_sent = send_control_email(email)
    return mail_sent


@task
def reset_email(email):
    mail_sent = send_control_email(email, send_type='forget')
    return mail_sent


class CallbackTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass

