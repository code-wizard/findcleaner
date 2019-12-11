from django.db import models
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _


class FcSystemSettings(models.Model):
    default_currency = models.CharField(_('Default Currency'),max_length=500, null=True, blank=True, default='Naira')
    service_base_price = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0000'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fc_settings"
        verbose_name = _("Settings")





