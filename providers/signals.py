from django.db.models.signals import pre_save
from customers.models import FcServiceRequest
from django.dispatch import receiver
from datetime import datetime
from accounts.tasks import send_email_


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
        # send mail to customer 
        customer_email = instance.customer.user.email
        phone = instance.provider.get_phone()
        provider_name = provider.name
        customer_name = instance.customer.get_name()
        ctx = {'customer_name':customer_name, 'provider_name':provider_name, 'phone':phone}

        send_email_.delay('Service Schedule','customers/service_schedule',customer_email, ctx)


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
        duration =  (instance.end_time - start_time).total_seconds() / 60 # duation in mins
        instance.duration = f"{duration} minutes"
        instance.status = FcServiceRequest.FcRequestStatus.COMPLETED
        # calculate the amount
        billing_rate = instance.service_provider.billing_rate
        charge = round((float(billing_rate)/60) * duration,2)
        instance.total_amount = charge
        # send the notification to customer to make payment
        # instance.save()
    
    instance.action = None


# def trigger_complet ed_service(pre_save, sender=FcServiceRequest):