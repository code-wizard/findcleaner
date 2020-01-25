# version = django.get_version().split(".")
# if int(version[0]) >= 2:
#     from django.urls import re_path as url
# else:
#     from django.conf.urls import url
#
# from django.views.decorators.csrf import csrf_exempt

from . import views
from django.urls import path
from billing.api import billing_api

app_name = "billing"

urlpatterns = [
    path("new-customer", views.new_customer, name='new_customer'),
    # path("charge", views.charge, name='charge_customer'),
    path('new-billing',billing_api.NewBillingView.as_view(),name='new_billing'),
]
