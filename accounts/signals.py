from allauth.account.utils import send_email_confirmation
from django.dispatch import Signal, receiver

send_confirmation_email = Signal(providing_args=['request', 'user', 'signup'])


@receiver(send_confirmation_email)
def send_email(sender, request, user, signup=False, **kwargs):
    send_email_confirmation(request, user, signup)