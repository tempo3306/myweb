from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery import task, Task
from .utils import send_register_email

@task
def confirm_email(email):
    mail_sent = send_register_email(email)
    return mail_sent





class CallbackTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


@task(base=CallbackTask)  # this does the trick
def add(x, y):
    return x + y