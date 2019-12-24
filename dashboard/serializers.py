from rest_framework import serializers
from accounts.models import FcUser
from customers.models import FcServiceRequest
from .models import FcSystemSettings
from providers.serializers import FcServiceProviderSerializer
from customers.serializers import FcServiceRequestSerializer
from services.serializers import ServiceSerializer

class DashBoardUsersViewSerializer(serializers.Serializer):
    def to_representation(self, obj):
        id = obj.get_platform_id()
        print('id',id)
        return {
            'username' : obj.username,
            'first_name' : obj.first_name,
            'last_name': obj.last_name,
            'account_type': obj.account_type,
            obj.account_type+'_id':id,
            'email': obj.email,
            'phone_number': obj.phone_number
        }

# class DashBoardUsersViewSerializer(serializers.ModelSerializer):
#     platform_id = serializers.SerializerMethodField(read_only=True)
#
#     def get_platform_id(self,obj):
#         return "sample"
#
#     class Meta:
#         model = FcUser
#         fields = ('username','first_name','last_name','account_type','platform_id','email','phone_number',)


class DashBoardActiveSessionSerializer(serializers.ModelSerializer):
    service_provider = FcServiceProviderSerializer(read_only=True)
    customer = FcServiceRequestSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    class Meta:
        model = FcServiceRequest
        fields = '__all__'


class FcSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcSystemSettings
        fields = '__all__'