from django.db import models
from django.contrib.auth import get_user_model


STAFF_ACCOUNT_TYPE = (('admin','Admin'),('staff','Staff'),('manager','Manager'))
FcUser = get_user_model()


class FcAdminManager(models.Manager):
    def get_query_set(self):
        return self.filter(is_deleted=False,user__is_staff=True)

    # def get_object(self):
    #     return self.model.objects.get(pk=self.request.user.pk, is_deleted=False)
    #

class FcAdmin(models.Model):
    class FcAdminRole:
        ADMIN = STAFF_ACCOUNT_TYPE[0][0]
        MANAGER = STAFF_ACCOUNT_TYPE[1][0]
        STAFF = STAFF_ACCOUNT_TYPE[2][0]

    user = models.ForeignKey(FcUser, on_delete=models.DO_NOTHING, related_name ='staff_info')
    role = models.CharField(max_length=60, choices=STAFF_ACCOUNT_TYPE, default='staff')
    is_deleted = models.BooleanField(default=False)
    # created_by = models.ForeignKey("fc_admin.FcStaff", related='my_created_users')
    objects = FcAdminManager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.user.is_active = False
        self.save()

    # class Meta:
    #     db_table = "fc_admin"
    #     verbose_name = _("Staff")