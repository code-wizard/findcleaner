from rest_framework import serializers
from .models import FcBillingInfo,FcProviderEearningInfo,FcCustomerCardsDetails
from customers.models import FcServiceRequest
from billing.utils import load_lib
from uuid import uuid4
from django.db import transaction


class FcBillingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcBillingInfo
        fields = '__all__'
        read_only_fields = ('billing_reference','status',)


class FcEarningInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcProviderEearningInfo
        fields = '__all__'
        # read_only_fields = ('reference','status',)


class FcCustomerCardsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcCustomerCardsDetails
        fields = '__all__'
        # read_only_fields = ('reference','status',)


class FcInitiateCustomerPaymentInfoSerializer(serializers.Serializer):
    service_request = serializers.CharField(read_only=False)
    account_number = serializers.CharField(read_only=False)
    bank_code = serializers.CharField(read_only=False)

    def save(self, **kwargs):
        service_request = self.validated_data.get('service_request')

        if not FcServiceRequest.objects.filter(id=service_request).exists():
            raise serializers.ValidationError("Service request with this id not found")
        with transaction.atomic():
            service_request_obj = FcServiceRequest.objects.get(id=service_request)
            customer = service_request_obj.customer

            if not FcBillingInfo.objects.filter(service_request=service_request_obj).exists():
                raise serializers.ValidationError("Customer is yet to make payment for this service. Try again later")

            if service_request_obj.status !=  FcServiceRequest.FcRequestStatus.COMPLETED:
                raise serializers.ValidationError("This service has not been completed yet, payment can not be initiated")

            PaystackAPI = load_lib()
            paystack_instance = PaystackAPI()

            new_transfer_ctx = {
                "type": "nuban",
                "name": customer.user.get_full_name(),
                "account_number": self.validated_data.get("account_number"),
                "bank_code":self.validated_data.get("bank_code"),
                "description":"payment for {0} service rendered to {1}".format(service_request_obj.get_service_name(),service_request_obj.get_customer_name())
            }
            # print('new_transfer_ctx',new_transfer_ctx)
            recipient_code = paystack_instance.new_transfer_reciepient(new_transfer_ctx)

            if not isinstance(recipient_code, str):
                raise serializers.ValidationError(recipient_code)

            transfer_ctx = {
                "amount": service_request_obj.total_amount,
                "recipient":recipient_code,
                "reference": str(uuid4())}

            transfer_response = paystack_instance.initiate_transfer(transfer_ctx)
            if not isinstance(transfer_response, str):
                raise serializers.ValidationError(transfer_response)

            earning_obj = FcProviderEearningInfo.objects.create(**self.validated_data,
                                                                service_request=service_request_obj,
                                                                reference=transfer_ctx.get("transfer_ctx"))

            return earning_obj
