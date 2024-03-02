from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .consumers import WSConsumer


# @shared_task(bind=True)
# def print_test(self):
#     for i in range(10):
#         print(i)
#     return "Hello, World!"


@shared_task(bind=True)
def print_test(self):
    WSConsumer()
    