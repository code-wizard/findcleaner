from django.contrib.postgres.fields import ArrayField
from django.db import models
from accounts.models import FcUser,FcAddress
from django.utils.translation import ugettext_lazy as _
from services.models import FcService
from providers.models import FcProviderServices
from django.db.models import Sum

status = (("new", "New"),("accepted", "Accepted"), ("ongoing", "Ongoing"),("cancel", "Cancelled"),
          ("completed", "Completed"), ("paid", "Paid"))
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
    class FcRequestStatus:
        NEW = status[0][0]
        ACCEPTED = status[1][0]
        ONGOING = status[2][0]
        CANCELLED = status[3][0]
        COMPLETED = status[4][0]
        PAID = status[5][0]

    service = models.ForeignKey(FcService, on_delete=models.CASCADE, related_name='service_requests', null=True)
    service_provider = models.ForeignKey(FcProviderServices, on_delete=models.SET_NULL,
                                         related_name="provider_service_request", null=True)
    customer = models.ForeignKey(FcCustomer, on_delete=models.SET_NULL, related_name="customer", null=True)
    address = models.CharField(max_length=255, null=True)
    coords = ArrayField(models.FloatField(null=True), size=2, null=True)
    requirement_description = models.TextField(_('Service Requirement'), max_length=500, null=True, blank=True)
    service_required_on = models.DateTimeField(_('Service requested On'), null=True, blank=True, max_length=20)
    # expected_start_time = models.TimeField(_('Expected Start Time'), null=True, blank=True)
    expected_hours_to_complete = models.CharField(_('Expected Complete hours'),max_length=500, null=True, blank=True)
    total_amount = models.FloatField(_('Amount'),max_length=120, null=True, blank=True)
    status = models.CharField(_('Status'),max_length=120,default='new', choices=status)
    payment_mode = models.CharField(_('Payment Mode'),choices=payment_mode, default='cash',max_length=500, null=True, blank=True)
    service_deliver_on = models.DateField(_('Service Delivered on'),max_length=500, null=True, blank=True)
    no_of_pets = models.PositiveIntegerField(default=0, null=True)
    no_of_toilets = models.PositiveIntegerField(default=0, null=True)
    no_of_spaces = models.PositiveIntegerField(default=0, null=True)
    no_of_rooms = models.PositiveIntegerField(default=0, null=True)
    no_of_cleaners = models.PositiveIntegerField(default=0, null=True)
    cleaning_products = models.CharField(null=True, max_length=3)
    cleaning_equipment = models.CharField(null=True, max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}-{}".format(self.service.service, self.service_provider.provider.name)
        # return "{}-{}".format(self.service.service, self.service_provider.provider.name)

    def get_service_name(self):
        return self.service.service


    class Meta:
        db_table = "fc_service_request"
        verbose_name = _("Service Request")
        ordering = ('-created_at', )

    def get_customer_name(self):
        return self.customer.user.get_full_name()

        # my_service_requests = self.service_provider # FcServiceRequest.objects.filter(service_provider=service_provider_obj)
        # print('my_service_requests',my_service_requests)
        # completed_service = # my_service_requests.filter(status='completed')
        #
        # my_revenue = 0 if completed_service == None else completed_service.aggregate(Sum('total_amount'))[
        #     'total_amount__sum']
        #
        # return my_revenue

