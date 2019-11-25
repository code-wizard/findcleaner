from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin
from django.utils import timezone

account_types = (("customer", "Customer"), ("provider", "Service Provider"))


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email), username=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        super_user = self.create_user(
            email,
            password=password,
        )
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.save(using=self._db)
        return super_user


class FcUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    email = models.EmailField(_('email address'), max_length=254, unique=True, db_index=True)
    username = models.CharField(_('username'), max_length=500, blank=True, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
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

    objects = MyUserManager()

    def get_user_type(self):
        return self.account_type

    class Meta:
        db_table = "fc_user"
        verbose_name = _("User")
        verbose_name_plural = _('Users')


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
