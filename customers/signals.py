from django.db.models.signals import pre_save
from .models import FcServiceRequest
from django.dispatch import receiver


@receiver(pre_save, sender = FcServiceRequest)
def notifiy_provider(sender, instance, **kwargs):
    provider = instance.service_provider
