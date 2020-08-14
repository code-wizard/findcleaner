from rest_framework import serializers
from .models import FcRating
from .models import FcServiceRequest
from django.shortcuts import get_object_or_404
from accounts.serializers import FcUserDetailsSerializer
from providers.serializers import FcServiceRequestSerializer


class FcRatingSerializer(serializers.ModelSerializer):
    user_detail = FcUserDetailsSerializer(read_only=True, source="user")
    service_request_detail = FcServiceRequestSerializer(read_only=True, source="service_request")

    class Meta:
        model = FcRating
        exclude = ('is_active','is_deleted',)
        read_only_fields = ('user','rated','provider_service',)

    def validate(self, attrs):
        if FcRating.objects.filter(user=attrs.get('user'),service_request=attrs.get('service_request')).exists():
            raise serializers.ValidationError("sorry, This user has already review the said service request.")

        service_request_obj = get_object_or_404(FcServiceRequest, id=attrs.get('service_request').id)
        # FcServiceRequest.objects.filter()
        if service_request_obj.status != 'cancel' and service_request_obj.status != 'completed' and service_request_obj.status != 'paid':
            raise serializers.ValidationError("You can only review completed or cancelled task."
                                              " This task is {0}".format(service_request_obj.status))

        return attrs
        

    def create(self, validated):
        user = self.context.get('user')
        service_request = validated.get('service_request')
        rated = service_request.customer.user
        if rated == user:
            rated = service_request.service_provider.provider.user

        rating = FcRating.objects.create(**validated, user=user,provider_service=service_request.service_provider,
                                        rated=rated)
        rating.save()                                        
        return validated
        

class FcRatingUpdateSerializer(serializers.ModelSerializer):
    user = FcUserDetailsSerializer(read_only=True)
    service_request = FcServiceRequestSerializer(read_only=True)

    class Meta:
        model = FcRating
        exclude = ('is_active','is_deleted')
        read_only_fields = ('user','service_request',)


