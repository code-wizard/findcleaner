from django.contrib import admin
from .models import FcCustomer,FcServiceRequest, FcHelp

admin.site.register(FcCustomer)
admin.site.register(FcServiceRequest)
admin.site.register(FcHelp)