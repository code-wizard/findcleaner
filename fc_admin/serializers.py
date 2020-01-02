from rest_framework import serializers
from fc_admin.models import FcAdmin
from accounts.serializers import FcRegisterSerializer
from django.db import transaction
from accounts.signals import send_confirmation_email
from accounts.serializers import FcUserDetailsSerializer


class FcAdminSignupSerializer(FcRegisterSerializer):

    def create(self,validated_data):
        with transaction.atomic():
            validated_data['is_active'] = False
            validated_data['account_type'] = FcAdmin.FcAdminRole.ADMIN
            validated_data['is_staff'] = True
            user = super(FcAdminSignupSerializer, self).create(validated_data)
            staff_info = FcAdmin.objects.create(user=user,role=validated_data.get('role'))
            staff_info.save()
            request = self.context.get('request')
            send_confirmation_email.send(sender=FcAdmin,request=request,user=user, signup=True)
            return user

    class Meta:
        model = FcAdmin
        read_only_fields = ('user',)

        fields = '__all__'


class FcAdminSerializer(serializers.ModelSerializer):
    user = FcUserDetailsSerializer(read_only=False)

    class Meta:
        model = FcAdmin
        fields = ('role','is_deleted','user')
        # read_only_fields = ['is_active',]