from django.db import models
from customers.models import FcServiceRequest
from uuid import uuid4
from django.contrib.auth import get_user_model

User = get_user_model()

status = (("pending", "Pending"),("paid", "Paid"), ("cancelled", "Cancelled"))
EarningStatus = (("pending", "Pending"),("initiated", "Initiated"),("recieved", "Recieved"))


class DefaultCardBillingInfo(models.Model):
    """
        Keep track of model to limit oine record of it as is_default = True
    """
    model_name = models.CharField(max_length=64, unique=True)
    record_id = models.IntegerField() # id of the record for isdefault

    def __unicode__(self):
        return u'Model %s record %d for %s' % (self.model_name, self.record_id)


class FcBillingInfo(models.Model):
    class Billing_Status:
        PAID = status[1][0]
        PENDING = status[0][0]
        CANCELLED = status[2][0]
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    billing_reference = models.CharField(max_length=255, null=True)
    billing_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=125,choices=status,default='pending')
    service_request = models.ForeignKey(FcServiceRequest, on_delete=models.DO_NOTHING, related_name="service_billing", null=True)
    billing_info = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def amount_to_charge(self):
        return self.service_request.total_amount


class FcCustomerCardsDetails(models.Model):
    user = models.ForeignKey(User, related_name='my_card_details', on_delete=models.DO_NOTHING, null=True)
    authorization_code = models.CharField(max_length=255)
    bin = models.CharField(max_length=255, null=True)
    brand = models.CharField(max_length=255, null=True)
    signature = models.CharField(max_length=255, null=True)
    country_code = models.CharField(max_length=255, null=True)
    last4 = models.CharField(max_length=255, null=True)
    exp_month = models.CharField(max_length=255, null=True)
    exp_year = models.CharField(max_length=255, null=True)
    channel = models.CharField(max_length=255, null=True)
    card_type = models.CharField(max_length=255, null=True)
    bank = models.CharField(max_length=255, null=True)
    reusable = models.BooleanField(default=True)
    default = None #models.BooleanField(default=False)
    status = models.CharField(max_length=125, default='active')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    billing_info = models.OneToOneField(FcBillingInfo, on_delete=models.CASCADE, related_name="billing_card_detail", null=True)

    def is_default(self):
        if self.default == None:
            try:
                default = DefaultCardBillingInfo.objects.get(model_name=self.__name__)
            except DefaultCardBillingInfo.DoesNotExist:
                default = None
        return self.id == default.record_id

    def remove_card(self):
        self.is_deleted = True
        if DefaultCardBillingInfo.objects.filter(model_name=self.__class__.__name__).exists():
            default = DefaultCardBillingInfo.objects.get(model_name=self.__class__.__name__)
            default.delete()
        self.save()
        return

    def set_default(self):
        try:
            default_rec = DefaultCardBillingInfo.objects.get(model_name=self.__class__.__name__)
        except DefaultCardBillingInfo.DoesNotExist:
            DefaultCardBillingInfo.objects.create(model_name=self.__class__.__name__, record_id=self.id)
        else:
            if default_rec.record_id != self.id:
                default_rec.record_id = self.id
                default_rec.save()
        # self.default_no = self
        return


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

