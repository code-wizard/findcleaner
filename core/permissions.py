from rest_framework import permissions
import logging
logger = logging.getLogger(__name__)


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.account_type.lower() == 'customer'
        return False


class IsProvider(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.account_type.lower() == 'provider'
        return False


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff
        return False
