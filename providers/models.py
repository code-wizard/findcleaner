from django.db import models
from accounts.models import FcUser,FcAddress
from services.models import FcService
from django.utils.translation import ugettext_lazy as _
# from customers.models import FcCustomer


class FcProvider(models.Model):
    user = models.ForeignKey(FcUser, on_delete=models.SET_NULL, related_name="provider_info", null=True)
    address = models.ForeignKey(FcAddress, on_delete=models.CASCADE, related_name="provider_address",null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fc_provider"
        verbose_name = _("Provider")


class FcServiceProvider(models.Model):
    service = models.ForeignKey(FcService, on_delete=models.SET_NULL, related_name="service_provider", null=True)
    provider = models.ForeignKey(FcProvider, on_delete=models.SET_NULL, related_name="my_services", null=True)
    billing_rate = models.CharField(max_length=255, blank=True, null=True)
    experience = models.CharField(max_length=255, blank=True, null=True)
    service_description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_service_name(self):
        return self.service.service


    class Meta:
        db_table = "fc_service_provider"
        verbose_name = _("Service Provider")


