from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


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

    # DEFAULT_FROM_EMAIL = "FindCleaner <no-reply@findcleaner.net>"
 