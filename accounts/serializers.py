from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from accounts.models import FcUser
from rest_auth.serializers import PasswordResetSerializer
from accounts.forms import PasswordResetForm
from accounts import models as auth_models
from django.conf import settings
from django.db import transaction
from customers.models import FcCustomer
from providers.models import FcProvider
from django.utils.translation import ugettext_lazy as _
from allauth.account.utils import send_email_confirmation

UserModel = get_user_model()


class FcLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg)

        return user


    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = self._validate_email(email, password)

        # Did we get back an active user?
        if user:

            if not user.is_active:
                msg = _('User account is disabled.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg)

        # check if a customer is trying to login into the provider app

        if self.context.get('account_type') == 'provider' and user.account_type == 'customer':
            raise serializers.ValidationError(_('You are not allowed to access this section of FindCleaner'))

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))


        attrs['user'] = user
        return attrs


class FcPasswordResetSerializer(PasswordResetSerializer):
    """
        Serializer for requesting a password reset e-mail.
    """
    # phone = serializers.CharField()
    email = serializers.EmailField(required=False)
    password_reset_form_class = PasswordResetForm

    def validate_email(self, email):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)
        elif not auth_models.Fc.objects.filter(email=email).exists():
                raise serializers.ValidationError("Invalid email")
        return email

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


class FcRegisterSerializer(serializers.ModelSerializer):
    # with transaction.atomic():
    email = serializers.EmailField(max_length=255, write_only=False)
    password = serializers.CharField(max_length=1000, write_only=True)
    # username = serializers.CharField(max_length=255, write_only=False)
    first_name = serializers.CharField(max_length=255, write_only=False)
    last_name = serializers.CharField(max_length=255, write_only=False)
    phone_number = serializers.CharField(max_length=255, write_only=False)

    def validate_email(self, email):
        if FcUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        return email

    def validate_username(self,username):
        if FcUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("This username has already been taken")
        return username

    def create(self, validated_data):
        with transaction.atomic():
            first_name = validated_data.get("first_name","")
            last_name = validated_data.get("last_name","")
            account_type = validated_data.get("account_type","")
            is_staff = validated_data.get("is_staff",False)
            user = FcUser.objects.create(
                username=validated_data.get("email"),
                email=validated_data.get("email"),
                phone_number=validated_data.get("phone_number",""),
                first_name = first_name,
                is_active = validated_data.get("is_active", True),
                last_name = last_name,
                is_staff = is_staff,
                account_type = account_type
            )
            user.set_password(validated_data.get("password"))
            user.raw_password = validated_data.get("password")
            user.save()

            # if account_type == 'customer':
            #     customer_info = FcCustomer.objects.create(user=user)
            #     customer_info.save()
            # else:
            #     provider_info = FcProvider.objects.create(user=user)
            #     provider_info.save()

            # request = self.context.get("request")
            print('before sending mail')
            # send_email_confirmation(request, user, True)
            print('after sending mail')

            return user

    class Meta:
        model = FcUser
        read_only_field = ('account_type')
        fields = ("email","first_name","last_name","is_staff","phone_number","password")


class FcUserDetailsSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField(read_only=True)

    def get_user_type(self,obj):
        return obj.get_user_type()

    def validate_username(self, username):
        try:
            if auth_models.FcUser.objects.filter(~Q(pk=self.context.get("request").user.id),
                                                 username__iexact=username).exists():
                raise serializers.ValidationError("User with this Username already exists.")
        except:
            ''' catch error while creating bulk user, request object is not passed'''
            if auth_models.FcUser.objects.filter(username__iexact=username).exists():
                raise serializers.ValidationError("User with this Username already exists.")

        return username

    class Meta:
        model = auth_models.FcUser
        read_only_fields = ('is_staff','is_superuser','is_active','email','username',)
        fields = ('id', 'username',"first_name","last_name",
                  'email', 'is_active','user_type', "date_joined","is_staff")