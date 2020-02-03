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
    # path("new-customer", billing_api.new_customer, name='new_customer'),
    path("verify_payment/<billing_reference>", billing_api.verify_payment, name='verify_payment'),
    path('new-billing',billing_api.NewBillingView.as_view(),name='new_billing'),
    path('supported-bank-list', billing_api.all_banks_list, name='bank-list'),
    path('claim-earning', billing_api.FcEarningRequestView.as_view(), name='claim-earning'),
    path('earning_info/<service_request_id>', billing_api.FcEarningInfo.as_view(), name='earning-info'),
    path('verify-transfer/<reference>', billing_api.verify_transfer, name='verify-transfer'),
]