from rest_framework import serializers
from accounts.models import FcUser
from customers.models import FcServiceRequest
from .models import FcSystemSettings
from providers.serializers import FcProviderServicesSerializer
from customers.serializers import FcServiceRequestSerializer,FcCustomerSerializer
from services.serializers import ServiceSerializer
from rating.serializers import FcRatingUpdateSerializer


class DashBoardUsersViewSerializer(serializers.Serializer):
    def to_representation(self, obj):
        id = obj.get_platform_id()
        return {
            'username' : obj.username,
            'first_name' : obj.first_name,
            'last_name': obj.last_name,
            'account_type': obj.account_type,
            obj.account_type+'_id':id,
            'email': obj.email,
            'phone_number': obj.phone_number
        }



class RatedUsersViewSerializer(serializers.Serializer):
    def to_representation(self, obj):
        id = obj.get_platform_id()
        rating = FcRatingUpdateSerializer(obj.get_ratings()).data
        return {
            'username' : obj.username,
            'first_name' : obj.first_name,
            'last_name': obj.last_name,
            'account_type': obj.account_type,
            obj.account_type+'_id':id,
            'rating':rating,
            'email': obj.email,
            'phone_number': obj.phone_number
        }


class UsersViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = FcUser
        fields = ('username','first_name','last_name','account_type','email','phone_number',)


class DashBoardActiveSessionSerializer(serializers.ModelSerializer):
    service_provider = FcProviderServicesSerializer(read_only=True)
    customer = FcCustomerSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    def get_customer(self,obj):
        return obj.get_customer_name()

    class Meta:
        model = FcServiceRequest
        fields = '__all__'


class FcSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcSystemSettings
        fields = '__all__'