from __future__ import absolute_import, unicode_literals
import random
from celery.decorators import task

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


@task(name="sum_two_numbers")
def add(x, y):
    return x + y

@task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    return total

@task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)


@task(name="send_mail")
def send_email_(title,template_path,to,context={}):

    msg_plain = render_to_string(f"{template_path}.txt", context)
    msg_html = render_to_string(f"{template_path}.html", context)
    
    send_mail(
        title,
        msg_plain,
        getattr(settings,'DEFAULT_FROM_EMAIL','no-reply@findcleaner.net'),
        [to],
        html_message=msg_html,
    )
    return None