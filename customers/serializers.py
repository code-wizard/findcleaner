from rest_framework import serializers
from .models import FcServiceRequest
from .models import FcCustomer
from accounts.serializers import FcRegisterSerializer
from accounts.signals import send_confirmation_email
from accounts.models import FcUser
from services.serializers import ServiceSerializer
from providers.serializers import FcProviderServicesSerializer


class FcCustomerSignUpSerializer(FcRegisterSerializer):

    def create(self, validated_data):
        validated_data["account_type"] = FcUser.FcAccountType.CUSTOMER
        user = super(FcCustomerSignUpSerializer, self).create(validated_data)
        customer_info = FcCustomer.objects.create(user=user)
        customer_info.save()
        request = self.context.get("request")
        send_confirmation_email.send(sender=FcCustomer, request=request, user=user, signup=True)
        return user

#
# class FcServiceRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FcServiceRequest
#         fields = '__all__'
#         read_only_fields = ['customer','status']
#
#

class FcCreateServiceRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FcServiceRequest
        fields = '__all__'


class FcServiceRequestSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_provider = FcProviderServicesSerializer(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    customer_user_id = serializers.IntegerField(source="customer.user.id", read_only=True)

    def get_name(self, obj):
        return obj.get_customer_name()

    class Meta:
        model = FcServiceRequest
        fields = '__all__'
        # exclude = ('user','address')
        read_only_fields = ['customer',]


class FcCustomerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    # name = serializers.SerializerMethodField(read_only=True)
    #
    def get_name(self, obj):
        return obj.get_name()

    class Meta:
        model = FcCustomer
        # fields = '__all__'
        exclude = ('created_at','updated_at')
        # read_only_fields = ['customer','status']



