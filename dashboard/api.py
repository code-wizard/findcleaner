from rest_framework import permissions, viewsets,generics,filters,status,views
from .serializers import DashBoardUsersViewSerializer,UsersViewSerializer,DashBoardActiveSessionSerializer,FcSettingsSerializer
from accounts.models import FcUser
from customers.models import FcServiceRequest
from core import pagination
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import FcSystemSettings
from core.permissions import IsCustomer,IsProvider,IsStaff
import datetime


class AllUsers(generics.ListAPIView):
    """
    Endpoint that list all user infos, it also support ordering and searching
    by passing the keyword "query={search parameter}"
    """
    serializer_class = DashBoardUsersViewSerializer
    permission_classes = (IsStaff,)
    pagination_class = pagination.CustomPageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('account_type','username','phone_number', 'first_name','last_name','email')
    ordering = ('account_type',)  # Default ordering

    def get_queryset(self):
        qs = FcUser.objects.filter(is_superuser=False)
        qs = qs.filter(Q(account_type=FcUser.FcAccountType.CUSTOMER) |Q(account_type=FcUser.FcAccountType.PROVIDER) ).order_by('-created_at')
        # qs = FcUser.objects.filter(is_superuser=False).order_by('-created_at')
        query = self.kwargs.get('query')
        if query:
            qs = qs.filter(Q(first_name=query)|
                                                  Q(last_name=query))
        return qs


class AllUsers_NoPgaination(generics.ListAPIView):
    serializer_class = DashBoardUsersViewSerializer
    permission_classes = (IsStaff,)

    def get_queryset(self):
        qs = FcUser.objects.filter(is_superuser=False)
        qs = qs.filter(
            Q(account_type=FcUser.FcAccountType.CUSTOMER) | Q(account_type=FcUser.FcAccountType.PROVIDER)).order_by(
            '-created_at')
        query = self.kwargs.get('query')
        if query:
            qs = qs.filter(Q(first_name=query)|
                                                  Q(last_name=query))
        return qs


class UserUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
        This endpoint allow both POST,GET and DELETE request by passing the username
        of the desired user to perform the operation on
        """
    serializer_class = UsersViewSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def get_object(self):
        query = self.kwargs.get("username")
        user = get_object_or_404(FcUser,username=query,is_superuser=False)
        return user


class TransactionView(generics.RetrieveUpdateDestroyAPIView):
    """
        You can retrieve,update and destroy transaction details by passing id
        of the trasaction as a keyword "service_id={}"
        """
    serializer_class = DashBoardActiveSessionSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def get_object(self):
        query = self.kwargs.get("service_id")
        transaction = get_object_or_404(FcServiceRequest,id=query)
        return transaction


class AllTransactionView(generics.ListAPIView):
    """
    List all trasaction, to get active or ongoing trasaction, pass
    the keyword "status={completed,ongoing...}"
     """
    serializer_class = DashBoardActiveSessionSerializer
    pagination_class = pagination.CustomPageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('service_required_on','payment_mode','status','requirement_description','service_deliver_on','customer__user__first_name','service_provider__provider__user__first_name')
    ordering = ('service_required_on','service_deliver_on','service_provider__provider__user__first_name')  # Default ordering
    permission_classes = (permissions.IsAuthenticated,)

    # queryset = FcServiceRequest.objects.all()

    def get_queryset(self):
        qs = FcServiceRequest.objects.all().order_by('-created_at')
        status = self.kwargs.get('status')
        if status:
            print('status here')
            qs = qs.filter(Q(status=status))
        return qs


class FilterTransactionView(generics.ListAPIView):
    """
    List all trasaction, to get active or ongoing trasaction, pass
    the keyword "status={completed,ongoing...}"
     """
    serializer_class = DashBoardActiveSessionSerializer
    pagination_class = pagination.CustomPageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('service_required_on','payment_mode','status','requirement_description','service_deliver_on','customer__user__first_name','service_provider__provider__user__first_name')
    ordering = ('service_required_on','service_deliver_on','service_provider__provider__user__first_name')  # Default ordering
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        qs = FcServiceRequest.objects.all().order_by('-created_at')
        from_date = self.kwargs.get('from_date')
        to_date = self.kwargs.get('to_date')
        if from_date and to_date:
            try:
                qs = qs.filter(service_deliver_on__gte=datetime.datetime.strptime(from_date,'%Y-%m-%d'),
                               service_deliver_on__lte=datetime.datetime.strptime(to_date,'%Y-%m-%d'))
            except:
                return qs
        return qs


class ActiveSession(generics.ListAPIView):
    """
    Use this endpoint to search or list some transaction based
    on customer name or description of the service
    """
    serializer_class = DashBoardActiveSessionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('service_required_on', 'payment_mode', 'status', 'requirement_description', 'service_deliver_on',
                     'customer__user__first_name', 'service_provider__provider__user__first_name')
    ordering = (
    'service_required_on', 'service_deliver_on', 'service_provider__provider__user__first_name')  # Default ordering
    permission_classes = (permissions.IsAuthenticated,)


    def get_queryset(self):
            qs = FcServiceRequest.objects.filter(status='ongoing').order_by('-created_at')
            query = self.kwargs.get('query')
            if query:
                qs = qs.filter(Q(requirement_description=query)|
                                                      Q(customer__user__first_name=query))
            return qs


class ActiveSessionNoPagination(generics.ListAPIView):
    """
    Use this endpoint to search or list some transaction based
    on customer name or description of the service
    """
    serializer_class = DashBoardActiveSessionSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        qs = FcServiceRequest.objects.filter(status='ongoing').order_by('-created_at')
        query = self.kwargs.get('query')
        if query:
            qs = qs.filter(Q(requirement_description=query)|
                                                  Q(customer__user__first_name=query))
        return qs


class FcSettingView(generics.RetrieveUpdateAPIView):
    """
    This is for system pricing and default currency settings.
    support only GET,PATCH request.
    """
    serializer_class = FcSettingsSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def get_object(self):
        obj_settings = FcSystemSettings.objects.first()
        return obj_settings