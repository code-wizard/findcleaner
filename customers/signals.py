from django.db.models.signals import pre_save
from .models import FcServiceRequest
from django.dispatch import receiver


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

    # if instance.status == FcServiceRequest.FcRequestStatus.ONGOING and instance.start_time is None:
        # set start time here
        # instance.start_time =


# def trigger_complet ed_service(pre_save, sender=FcServiceRequest):