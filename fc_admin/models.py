from django.db import models
from django.contrib.auth import get_user_model


STAFF_ACCOUNT_TYPE = (('admin','Admin'),('staff','Staff'),('manager','Manager'))
FcUser = get_user_model()


class FcAdmin(models.Model):
    class FcAdminRole:
        ADMIN = STAFF_ACCOUNT_TYPE[0][0]
        MANAGER = STAFF_ACCOUNT_TYPE[1][0]
        STAFF = STAFF_ACCOUNT_TYPE[2][0]

    user = models.ForeignKey(FcUser, on_delete=models.DO_NOTHING, related_name ='staff_info')
    role = models.CharField(max_length=60, choices=STAFF_ACCOUNT_TYPE, default='staff')
    # created_by = models.ForeignKey("fc_admin.FcStaff", related='my_created_users')
