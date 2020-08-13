from django.db.models.signals import pre_save
from .models import FcServiceRequest
from django.dispatch import receiver
import datetime

@receiver(pre_save, sender = FcServiceRequest)
def notifiy_provider(sender, instance, created, **kwargs):
    if created:
        print('creating new request')
    print('updating service request')
    provider = instance.service_provider
    if instance.status == FcServiceRequest.FcRequestStatus.COMPLETED:
        print('service request is completed')
        if not instance.service_billing:
            print('bill customer now')

    if instance.action == "start" and instance.start_time is None:

        print('starting the service')
        instance.start_time = datetime.datetime.now()
        instance.save()


# def trigger_complet ed_service(pre_save, sender=FcServiceRequest):