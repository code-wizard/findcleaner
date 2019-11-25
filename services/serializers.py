from rest_framework import serializers
from .models import FcServiceCategory, FcService


class NewCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FcServiceCategory
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self,obj):
        return obj.get_category_name()

    class Meta:
        model = FcService
        fields = '__all__'

