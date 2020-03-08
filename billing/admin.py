from django.contrib import admin
from billing.models import FcBillingInfo,FcProviderEearningInfo,FcCustomerCardsDetails, DefaultCardBillingInfo

admin.site.register(FcBillingInfo)
admin.site.register(FcProviderEearningInfo)
admin.site.register(FcCustomerCardsDetails)
admin.site.register(DefaultCardBillingInfo)

