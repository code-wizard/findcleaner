from rest_framework import serializers
from .models import FcServiceRequest
from .models import FcCustomer

class FcServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcServiceRequest
        fields = '__all__'
        read_only_fields = ['customer','status']



class FcServiceRequestSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)

    def get_name(self, obj):
        return obj.get_customer_name()

    class Meta:
        model = FcServiceRequest
        fields = '__all__'
        # exclude = ('user','address')
        read_only_fields = ['customer','status']


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



