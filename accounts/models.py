from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin
from django.utils import timezone
# from rating.models import FcRating
import os

account_types = (("customer", "Customer"), ("provider", "Service Provider"), ('admin', 'Admin'))

def avatar_upload_path(instance, filename):
    filename, ext = os.path.splitext(filename)
    filename = "{0}{1}".format(int(timezone.now().timestamp()), ext)
    return "user/upload/avatar/{0}".format(filename)


class FcUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email), username=username
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,username, email, password):
        super_user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.is_active = True
        super_user.save(using=self._db)
        return super_user


class FcUser(AbstractBaseUser, PermissionsMixin):
    class FcAccountType:
        CUSTOMER = account_types[0][0]
        PROVIDER = account_types[1][0]
        ADMIN = account_types[2][0]

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']
    email = models.EmailField(_('email address'), max_length=254, unique=True, db_index=True)
    username = models.CharField(_('username'), max_length=500, blank=True, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    avatar = models.ImageField(upload_to=avatar_upload_path, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    account_type = models.CharField(_('Account Type'), default='customer', max_length=500, choices=account_types)

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))

    is_superuser = models.BooleanField(_('super status'), default=False,
                                       help_text=_('Designates whether the user can log into this admin '
                                                   'site.'))

    is_active = models.BooleanField(_('active'), default=False,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = FcUserManager()

    def get_user_type(self):
        return self.account_type

    def get_platform_id(self): # platform id means provider id or customer id
        try:
            if self.account_type == 'customer':
                return self.customer_info.first().id
            else:
                self.provider_info.first().id
        except:
            return 'admin'


    class Meta:
        db_table = "fc_user"
        verbose_name = _("User")
        verbose_name_plural = _('Users')

    def get_ratings(self):
        ratings = self.my_created_rating.first()
        # print('ratings',ratings)
        # ratings = FcRating.objects.get(service_request__service_provider__provider__user=self)
        return ratings

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)


class FcAddress(models.Model):
    # user_id = models.ForeignKey(FcUser, on_delete=models.SET_NULL, related_name="customer_info", null=True)
    country = models.CharField(max_length=255,null=True,blank=True)
    state = models.CharField(max_length=255,null=True,blank=True)
    area = models.CharField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    lat = models.CharField(max_length=255,null=True,blank=True)
    lng = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fc_address"
        verbose_name = _("Address")
