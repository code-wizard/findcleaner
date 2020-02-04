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
        # fields = '__all__'
        exclude = ('created_at','updated_at')


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
                                                      type=validated_data.get('type'),
                                                      name=validated_data.get('name'),
                                                      coords=coords)


            provider_info.save()
            print('Save info')

            # create provider services
            if services_info:
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
                  'coords','services_info', 'name', 'address', 'city', 'state', 'type')


class FcProviderServicesSerializer(serializers.ModelSerializer):
    service_name = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    distance = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)
    address = serializers.SerializerMethodField(read_only=True)
    service_image = serializers.SerializerMethodField(read_only=True)

    def get_service_image(self, obj):
        request = self.context.get('request')
        avatar = obj.get_service_avatar().url
        return request.build_absolute_uri(avatar)

    def get_address(self, obj):
        return obj.provider.address

    def get_distance(self,obj):
        lat = self.context.get("lat")
        lng = self.context.get("lng")
        if not lat or not lng:
            lat = 0.0
            lng = 0.0
        return obj.get_provider_distance(lat, lng)

    def get_rating(self, obj):
        return obj.get_my_ratings()

    def get_name(self,obj):
        return obj.get_name()

    def get_service_name(self,obj):
        return obj.get_service_name()

    class Meta:
        model = FcProviderServices
        fields = '__all__'
        # exclude = ('provider',)
        # read_only_fields = ('provider',)


class FcProviderDashboard(serializers.Serializer):
    total_service = serializers.IntegerField(read_only=True)
    cancelled_service = serializers.IntegerField(read_only=True)
    schedule_service = serializers.IntegerField(read_only=True)
    my_revenue = serializers.IntegerField(read_only=True)


class FcServiceRequestSerializer(serializers.ModelSerializer):
    service_name = serializers.SerializerMethodField(read_only=True)
    customer_name = serializers.CharField(source="customer.user.get_full_name", read_only=True)
    billing_rate = serializers.CharField(source="service_provider.billing_rate", read_only=True)

    def get_service_name(self, obj):
        return obj.get_service_name()

    class Meta:
        model = FcServiceRequest
        # fields = '__all__'
        exclude = ('created_at','updated_at')
        read_only_fields = ['service_provider','customer','status']


class FcServiceRequestEarningsSerializer(serializers.ModelSerializer):
    service_name = serializers.SerializerMethodField(read_only=True)

    def get_service_name(self, obj):
        return obj.get_service_name()

    class Meta:
        model = FcServiceRequest
        fields = ('service_name','service_required_on','total_amount','created_at','status',)

