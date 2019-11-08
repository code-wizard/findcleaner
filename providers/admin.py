from django.contrib import admin
from .models import FcProvider,FcServiceProvider

admin.site.register(FcProvider)
admin.site.register(FcServiceProvider)
