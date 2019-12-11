from rest_framework import serializers
from accounts.models import FcUser
from customers.models import FcServiceRequest
from .models import FcSystemSettings

class DashBoardUsersViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcUser
        fields = ('username','first_name','last_name','account_type','email','phone_number',)


class DashBoardActiveSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcServiceRequest
        fields = '__all__'


class FcSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcSystemSettings
        fields = '__all__'