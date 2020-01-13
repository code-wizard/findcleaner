from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from services.models import FcService
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from core.utils import calculate_provider_distance

PROVIDER_TYPES = (('individual', 'Individual'), ('Agency', 'Agency'))
PROVIDER_STATUS = (('active', 'Active'), ('disabled', 'disabled'))
FcUser = get_user_model()


class FcProvider(models.Model):
    class FcProviderStatus:
        ACTIVE = PROVIDER_STATUS[0][0]
        DISABLED = PROVIDER_STATUS[1][0]

    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    user = models.OneToOneField(FcUser, on_delete=models.SET_NULL, related_name="provider_info", null=True)
    address = models.CharField(max_length=255)
    coords = ArrayField(models.FloatField(null=True), size=2, null=True)
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
    # experience = models.CharField(max_length=255, blank=True, null=True)
    service_description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return   "{}-{}".format(self.provider.name, self.service.get_category_name())

    def get_service_name(self):
        return self.service.service

    def get_name(self):
        # firsname = self.provider.user.first_name
        # lastname = self.provider.user.last_name
        return "{0}".format(self.provider.name)

    def get_provider_distance(self,lat, lng):
        provider_coods = self.provider.coords
        dist_in_km = calculate_provider_distance((float(-provider_coods[0]), float(provider_coods[1])),
                                                 (-float(lat),float(lng)))
        return dist_in_km




    class Meta:
        db_table = "fc_provider_services"
        verbose_name = _("Provider Service")

#
# class FcProviderRating(models.Model):
#     user
#     rating = models.IntegerField(max=5)
#     provider
#     service

