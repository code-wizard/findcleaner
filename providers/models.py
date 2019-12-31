from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from accounts.models import FcUser,FcAddress
from services.models import FcService
from django.utils.translation import ugettext_lazy as _
# from customers.models import FcCustomer

PROVIDER_TYPES = (('individual', 'Individual'), ('Agency', 'Agency'))
PROVIDER_STATUS = (('active', 'Active'), ('disabled', 'disabled'))

class FcProvider(models.Model):
    class FcProviderStatus:
        ACTIVE = PROVIDER_STATUS[0][0]
        DISABLED = PROVIDER_STATUS[1][0]

    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    user = models.OneToOneField(FcUser, on_delete=models.SET_NULL, related_name="provider_info", null=True)
    address = models.CharField(max_length=255)
    coords = ArrayField(models.IntegerField(), size=2)
    type = models.CharField(choices=PROVIDER_TYPES, default='individual', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=PROVIDER_STATUS, max_length=8, default='disabled')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "fc_provider"
        verbose_name = _("Provider")


class FcProviderServices(models.Model):
    service = models.ForeignKey(FcService, on_delete=models.SET_NULL, related_name="service_provider", null=True)
    provider = models.ForeignKey(FcProvider, on_delete=models.SET_NULL, related_name="my_services", null=True)
    billing_rate = models.CharField(max_length=255, blank=True, null=True)
    experience = models.CharField(max_length=255, blank=True, null=True)
    service_description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_service_name(self):
        return self.service.service

    def get_name(self):
        firsname = self.provider.user.first_name
        lastname = self.provider.user.last_name
        return "{0} {1}".format(firsname, lastname)


    class Meta:
        db_table = "fc_provider_services"
        verbose_name = _("Provider Service")


