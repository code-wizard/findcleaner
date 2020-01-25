from django.shortcuts import redirect, reverse
from django.http import JsonResponse
from django.views.generic import RedirectView
# Create your views here.
from . import settings
# from .signals import payment_verified
from .utils import load_lib
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.validators import ValidationError

def new_customer(request):
    PaystackAPI = load_lib()
    paystack_instance = PaystackAPI()
    email = "walex@yahoo.com"
    first_name = "Will"
    last_name = "Smith"
    phone = "88765895243"
    context = {
        "email":email,
        "first_name":first_name,
        "last_name": last_name,
        "phone": phone
    }

    if paystack_instance.get_customer(email)[0]:
        response = paystack_instance.new_customer(context)
    # billing_code = response
    return JsonResponse({'status': 'Success'}, status=200)


class FailedView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        if settings.PAYSTACK_FAILED_URL == 'paystack:failed_page':
            return reverse(settings.PAYSTACK_FAILED_URL)
        return settings.PAYSTACK_FAILED_URL


def success_redirect_view(request, order_id):
    url = settings.PAYSTACK_SUCCESS_URL
    if url == 'paystack:success_page':
        url = reverse(url)
    return redirect(url, permanent=True)


def failure_redirect_view(request, order_id):
    url = settings.PAYSTACK_FAILED_URL
    if url == 'paystack:failed_page':
        url = reverse(url)
    return redirect(url, permanent=True)


class SuccessView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        if settings.PAYSTACK_SUCCESS_URL == 'paystack:success_page':
            return reverse(settings.PAYSTACK_SUCCESS_URL)
        return settings.PAYSTACK_SUCCESS_URL