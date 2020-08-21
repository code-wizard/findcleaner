from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from services.models import FcService
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from core.utils import calculate_provider_distance

PROVIDER_TYPES = (('individual', 'Individual'), ('agency', 'Agency'))
PROVIDER_STATUS = (('active', 'Active'), ('disabled', 'disabled'))
FcUser = get_user_model()


class FcProvider(models.Model):
    class FcProviderStatus:
        ACTIVE = PROVIDER_STATUS[0][0]
        DISABLED = PROVIDER_STATUS[1][0]

    name = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(FcUser, on_delete=models.SET_NULL, related_name="provider_info", null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    coords = ArrayField(models.FloatField(null=True), size=2, null=True)
    type = models.CharField(choices=PROVIDER_TYPES, default='individual', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=PROVIDER_STATUS, max_length=8, default='disabled')

    def __str__(self):
        if self.name:
            return self.name
        return f"{self.user.first_name} {self.user.last_name}"

    def get_name(self):
        firsname = self.user.first_name
        lastname = self.user.last_name
        return "{} {}".format(firsname, lastname)

    def get_phone(self):
        return self.user.phone_number


    class Meta:
        db_table = "fc_provider"
        verbose_name = _("Provider")


class FcProviderServices(models.Model):
    service = models.ForeignKey(FcService, on_delete=models.SET_NULL, related_name="service_provider", null=True)
    provider = models.ForeignKey(FcProvider, on_delete=models.SET_NULL, related_name="my_services", null=True)
    # billing_rate = models.CharField(max_length=255, blank=True, null=True)
    # experience = models.CharField(max_length=255, blank=True, null=True)
    service_description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        try:
            return "{}-{}".format(self.provider.name, self.service.service() )
        except:
            return "{}".format(self.provider.name)

    def get_service_name(self):
        try:
            return self.service.service 
        except:
            return None

    def get_billing_rate(self):
        billing_rate = self.service.agency_base_price if self.provider.type == 'agency' else self.service.individual_base_price
        return billing_rate


    def get_my_ratings(self):
        service_request = self.provider_service_request.first()
        if service_request:
            print('service_request', service_request)
            # rating = FcRating.objects.all() #filter(rated=obj.provider.user.id).aggregate(Avg('rating_score'))
            # return rating
            return service_request.request_ratings.all().values('rating_score','review','date_rated')
        return 'No review yet'

    def get_provider_review(self):
        service_request = self.provider_service_request.first()
        print('service_request', service_request)
        if service_request:
            return service_request.request_ratings.all().values('user__first_name','review','date_rated')
        return 'No review yet'

    def get_name(self):
        # firsname = self.provider.user.first_name
        # lastname = self.provider.user.last_name
        return "{0}".format(self.provider.name)

    def get_provider_distance(self,lat, lng):
        provider_coods = self.provider.coords
        if provider_coods:
            dist_in_km = calculate_provider_distance((float(-provider_coods[0]), float(provider_coods[1])),
                                                 (-float(lat),float(lng)))
            return dist_in_km

        # provider hasnt fill his address info (coords)
        return 'Unknown location'

    class Meta:
        db_table = "fc_provider_services"
        verbose_name = _("Provider Service")
