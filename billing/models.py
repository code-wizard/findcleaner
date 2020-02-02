from django.db import models
from customers.models import FcServiceRequest
from uuid import uuid4


status = (("pending", "Pending"),("paid", "Paid"), ("cancelled", "Cancelled"))
EarningStatus = (("pending", "Pending"),("initiated", "Initiated"),("recieved", "Recieved"))


class FcBillingInfo(models.Model):
    class Billing_Status:
        PAID = status[1][0]
        PENDING = status[0][0]
        CANCELLED = status[2][0]
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    billing_reference = models.CharField(max_length=255, null=True)
    billing_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=125,choices=status,default='pending')
    service_request = models.OneToOneField(FcServiceRequest, on_delete=models.DO_NOTHING, related_name="service_billing", null=True)
    billing_info = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def amount_to_charge(self):
        return self.service_request.total_amount


class FcProviderEearningInfo(models.Model):
    class Status:
        PENDING = status[0][0]
        INITIATED = status[1][0]
        RECIEVED = status[2][0]
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    reference = models.CharField(max_length=255, null=True, blank=True)
    billing_info = models.OneToOneField(FcBillingInfo, on_delete=models.CASCADE, null=True)
    remarks = models.CharField(max_length=255, null=True, default="successful transaction")
    service_request = models.OneToOneField(FcServiceRequest, on_delete=models.DO_NOTHING, related_name="service_earning", null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=125,choices=EarningStatus,default='pending')
    updated_at = models.DateTimeField(auto_now=True)

