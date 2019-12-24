from rest_framework import permissions, viewsets,generics,filters,status,views
from .serializers import DashBoardUsersViewSerializer,DashBoardActiveSessionSerializer,FcSettingsSerializer
from accounts.models import FcUser
from customers.models import FcServiceRequest
from core import pagination
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import FcSystemSettings


class AllUsers(generics.ListAPIView):
    """
    Endpoint that list all user infos, it also support ordering and searching
    by passing the keyword "query={search parameter}"
    """
    serializer_class = DashBoardUsersViewSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    pagination_class = pagination.CustomPageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('account_type','username', 'first_name','last_name','email')
    ordering = ('first_name',)  # Default ordering

    def get_queryset(self):
        qs = FcUser.objects.all()
        # print(qs.first().__class__)
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
    serializer_class = DashBoardUsersViewSerializer

    def get_object(self):
        query = self.kwargs.get("username")
        user = get_object_or_404(FcUser,username=query)
        return user


class TransactionView(generics.RetrieveUpdateDestroyAPIView):
    """
        You can retrieve,update and destroy transaction details by passing id
        of the trasaction as a keyword "service_id={}"
        """
    serializer_class = DashBoardActiveSessionSerializer

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
    # queryset = FcServiceRequest.objects.all()

    def get_queryset(self):
        qs = FcServiceRequest.objects.all()
        status = self.kwargs.get('status')
        if status:
            qs = qs.filter(Q(status=status))
        return qs




class ActiveSession(generics.ListAPIView):
    """
    Use this endpoint to search or list some transaction based
    on customer name or description of the service
    """
    serializer_class = DashBoardActiveSessionSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    pagination_class = pagination.CustomPageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    # search_fields = ('account_type','username', 'first_name','last_name','email')
    # ordering = ('first_name',)  # Default ordering

    def get_queryset(self):
        qs = FcServiceRequest.objects.filter(status='ongoing')
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

    def get_object(self):
        obj_settings = FcSystemSettings.objects.first()
        return obj_settings