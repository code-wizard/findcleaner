from django.contrib import admin
from .models import FcUser,FcAddress
# Register your models here.

admin.site.register(FcUser)
admin.site.register(FcAddress)