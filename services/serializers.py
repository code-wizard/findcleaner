from rest_framework import serializers
from .models import FcServiceCategory, FcService


class NewCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FcServiceCategory
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcService
        fields = '__all__'

