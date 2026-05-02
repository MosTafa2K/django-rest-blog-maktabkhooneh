import time
from celery import shared_task


@shared_task
def send_email_task():
    time.sleep(2)
    print("EMail has been sent :)")


@shared_task
def happy_birthday():
    print("Happy Birthday to you :)")
