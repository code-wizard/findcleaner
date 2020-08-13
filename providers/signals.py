from django.db.models.signals import pre_save
from customers.models import FcServiceRequest
from django.dispatch import receiver
from datetime import datetime

@receiver(pre_save, sender = FcServiceRequest)
def notifiy_provider(sender, instance, **kwargs):
    # if created:
    #     print('creating new request')
    print('updating service request')
    provider = instance.service_provider
    if instance.status == FcServiceRequest.FcRequestStatus.COMPLETED:
        print('service request is completed')
        # if instance.service_billing is None:
        #     print('bill customer now')

    if instance.action == "accept" and instance.start_time is None:
        instance.status = FcServiceRequest.FcRequestStatus.ACCEPTED

    if instance.action == "reject" and instance.start_time is None:
        instance.status = FcServiceRequest.FcRequestStatus.CANCELLED
        # instance.save()

    if instance.action == "start" and instance.start_time is None:
        instance.start_time = datetime.now()
        instance.status = FcServiceRequest.FcRequestStatus.ONGOING
        # instance.save()

    if instance.action == "stop" and instance.start_time is not None:
        instance.end_time = datetime.now()

        start_time = datetime.strptime(instance.start_time, '%Y-%m-%d %H:%M:%S.%f')
        duration =  (instance.end_time - start_time).total_seconds() / 60
        instance.duration = f"{duration} minutes"
        instance.status = FcServiceRequest.FcRequestStatus.COMPLETED
        # instance.save()


# def trigger_complet ed_service(pre_save, sender=FcServiceRequest):