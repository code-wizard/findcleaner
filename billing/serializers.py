from rest_framework import serializers
from .models import FcBillingInfo


class FcBillingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcBillingInfo
        fields = '__all__'
        read_only_fields = ('billing_reference',)