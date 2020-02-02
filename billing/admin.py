from django.contrib import admin
from billing.models import FcBillingInfo,FcProviderEearningInfo

admin.site.register(FcBillingInfo)
admin.site.register(FcProviderEearningInfo)