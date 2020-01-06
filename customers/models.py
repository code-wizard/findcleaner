from django.contrib.postgres.fields import ArrayField
from django.db import models
from accounts.models import FcUser,FcAddress
from django.utils.translation import ugettext_lazy as _
from services.models import FcService
from providers.models import FcProviderServices

status = (("new", "New"),("accepted", "Accepted"), ("ongoing", "Ongoing"),("cancel", "Cancelled"), ("completed", "Completed"))
payment_mode = (("cash", "Cash"), ("card", "Card"), ("bank_transfer", "Bank Transfer"))


class FcCustomer(models.Model):
    user = models.ForeignKey(FcUser, on_delete=models.SET_NULL, related_name="customer_info", null=True)
    address = models.ForeignKey(FcAddress, on_delete=models.CASCADE, related_name="customer_address",null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fc_customer"
        verbose_name = _("Customer")

    def get_name(self):
        firsname = self.user.first_name
        lastname = self.user.last_name
        return "{} {}".format(firsname, lastname)


class FcServiceRequest(models.Model):
    service = models.ForeignKey(FcService, on_delete=models.CASCADE, related_name='service_requests', null=True)
    service_provider = models.ForeignKey(FcProviderServices, on_delete=models.SET_NULL,
                                         related_name="provider_service_request", null=True)
    customer = models.ForeignKey(FcCustomer, on_delete=models.SET_NULL, related_name="customer", null=True)
    address = models.CharField(max_length=255, null=True)
    coords = ArrayField(models.FloatField(null=True), size=2, null=True)
    requirement_description = models.TextField(_('Service Requirement'), max_length=500, null=True, blank=True)
    service_required_on = models.DateField(_('Service requested On'), null=True, blank=True, max_length=20)
    # expected_start_time = models.TimeField(_('Expected Start Time'), null=True, blank=True)
    expected_hours_to_complete = models.CharField(_('Expected Complete hours'),max_length=500, null=True, blank=True)
    total_amount = models.FloatField(_('Amount'),max_length=120, null=True, blank=True)
    status = models.CharField(_('Status'),max_length=120,default='new', choices=status)
    payment_mode = models.CharField(_('Payment Mode'),choices=payment_mode, default='cash',max_length=500, null=True, blank=True)
    service_deliver_on = models.DateField(_('Service Delivered on'),max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fc_service_request"
        verbose_name = _("Service Request")

    def get_customer_name(self):
        return self.customer.user.get_full_name()

