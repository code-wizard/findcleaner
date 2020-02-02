from  django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
User = get_user_model()


class EmailAuthBackend(object):
    """
    A custom accounts backend. Allows users to log in using their email address.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Authentication method
        """
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None

