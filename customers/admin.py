from django.contrib import admin
from .models import FcCustomer,FcServiceRequest

admin.site.register(FcCustomer)
admin.site.register(FcServiceRequest)