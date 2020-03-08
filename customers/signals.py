from django.db.models.signals import pre_save
from .models import FcServiceRequest
from django.dispatch import receiver


@receiver(pre_save, sender = FcServiceRequest)
def notifiy_provider(sender, instance, **kwargs):
    print('updating service request')
    provider = instance.service_provider
    if instance.status == FcServiceRequest.FcRequestStatus.COMPLETED:
        print('service request is completed')
        if not instance.service_billing:
            print('bill customer now')


# def trigger_complet ed_service(pre_save, sender=FcServiceRequest):