from rest_framework import serializers
from .models import FcServiceRequest


class FcServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcServiceRequest
        fields = '__all__'
        read_only_fields = ['customer','status']



