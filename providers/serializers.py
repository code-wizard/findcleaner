from .models import FcServiceProvider
from rest_framework import serializers
from customers.models import FcServiceRequest


class FcServiceProviderSerializer(serializers.ModelSerializer):
    service_name = serializers.SerializerMethodField(read_only=True)

    def get_service_name(self,obj):
        return obj.get_service_name()

    class Meta:
        model = FcServiceProvider
        fields = '__all__'
        read_only_fields = ('provider',)


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
