from django.db import models
from django.utils.translation import ugettext_lazy as _
# from customers.models import FcCustomer
# from providers.models import FcProvider
# from providers.models import FcServiceProvider
import os


# class FcServiceCategory(models.Model):
#     category = models.CharField(max_length=255, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = "fc_service_category"
#         verbose_name = _("Service Category")

    # def __str__(self):
    #     try:
    #         return "{}".format(self.category)
    #     except:
    #         return str(self.id)

def service_upload_path(instance, filename):
    filename, ext = os.path.splitext(filename)
    # filename = "{0}{1}".format(int(timezone.now().timestamp()), ext)
    filename = "{0}{1}".format(instance.service, ext)
    return "services/{0}".format(filename)


class FcService(models.Model):
    service_category = models.CharField(max_length=120, null=True,blank=True, default='general')
    # category = models.ForeignKey(FcServiceCategory, on_delete=models.SET_NULL, related_name="services", null=True)
    service = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to=service_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    agency_base_price = models.FloatField(default=0)
    individual_base_price = models.FloatField(default=0)

    class Meta:
        db_table = "fc_service"
        verbose_name = _("Service")

    def get_category_name(self):
        try:
            return self.service_category
        except:
            return 'unkown category'

    def __str__(self):
        try:
            return "{}".format(self.service)
        except:
            return str(self.id)

