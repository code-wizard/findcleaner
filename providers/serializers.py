from django.db import transaction

from accounts.serializers import FcRegisterSerializer, FcUserDetailsSerializer
from .models import FcProviderServices, FcProvider
from rest_framework import serializers
from customers.models import FcServiceRequest
from accounts.models import FcUser
from .models import FcProvider
from accounts.signals import send_confirmation_email


# class FcServiceProviderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FcProvider
#         fields = '__all__'

class FcProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = FcProvider
        fields = '__all__'


class FcProviderSignUpSerializer(FcRegisterSerializer):
    services_info = serializers.JSONField(read_only=False, default=list)
    # user = FcUserDetailsSerializer(read_only=True)
    # services = serializers.JSONField()

    def create(self, validated_data):
        with transaction.atomic():
            validated_data["is_active"] = False
            validated_data["account_type"] = FcUser.FcAccountType.PROVIDER
            services_info = validated_data.get('services_info')
            user = super(FcProviderSignUpSerializer, self).create(validated_data)
            coords = validated_data.get("coords")
            provider_info = FcProvider.objects.create(user=user,
                                                      state=validated_data.get('state'),
                                                      city=validated_data.get('city'),
                                                      address=validated_data.get('address'),
                                                      name=validated_data.get('name'),
                                                      coords=coords)


            provider_info.save()

            # create provider services
            FcProviderServices.objects.bulk_create(
                [FcProviderServices(service_id=service["service_id"],
                                   billing_rate = service["billing_rate"],
                                   service_description=service["service_description"],
                                   provider=provider_info)
                 for service in eval(services_info)])

            request = self.context.get("request")
            send_confirmation_email.send(sender=FcProvider, request=request, user=user, signup=True)
            return user

    class Meta:
        model = FcProvider
        fields = ('email', 'first_name', 'last_name', 'phone_number','password',
                  'coords','services_info', 'name', 'address', 'city', 'state')



class FcProviderServicesSerializer(serializers.ModelSerializer):
    service_name = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)

    def get_name(self,obj):
        return obj.get_name()

    def get_service_name(self,obj):
        return obj.get_service_name()

    class Meta:
        model = FcProviderServices
        # fields = '__all__'
        exclude = ('provider',)
        # read_only_fields = ('provider',)


class FcProviderDashboard(serializers.Serializer):
    total_service = serializers.IntegerField(read_only=True)
    cancelled_service = serializers.IntegerField(read_only=True)
    schedule_service = serializers.IntegerField(read_only=True)
    my_revenue = serializers.IntegerField(read_only=True)



class FcServiceRequestSerializer(serializers.ModelSerializer):
    service_name = serializers.SerializerMethodField(read_only=True)

    def get_service_name(self, obj):
        return obj.get_service_name()

    class Meta:
        model = FcServiceRequest
        fields = '__all__'
        read_only_fields = ['service_provider','customer','status']
