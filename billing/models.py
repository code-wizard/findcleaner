from django.db import models
from customers.models import FcServiceRequest
from uuid import uuid4


class FcBillingInfo(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    billing_reference = models.CharField(max_length=255, null=True)
    billing_date = models.DateTimeField(auto_now_add=True)
    service_request = models.OneToOneField(FcServiceRequest, on_delete=models.DO_NOTHING, related_name="service_billing", null=True)
    billing_info = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def amount_to_charge(self):
        return self.service_request.total_amount