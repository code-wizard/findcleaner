from django.contrib.auth import get_user_model
from rest_auth.views import LoginView
from rest_framework import permissions, viewsets,generics,filters,status,views
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import FcServiceRequestSerializer, FcCustomerSignUpSerializer
from providers.models import FcProviderServices
from .models import FcCustomer
from core import pagination
from providers.serializers import FcProviderServicesSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from customers.models import FcServiceRequest
from core.permissions import IsCustomer,IsProvider,IsStaff
from accounts.serializers import FcLoginSerializer

User = get_user_model()

class FcCustomerLoginView(LoginView):

    serializer_class = FcLoginSerializer

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request, 'account_type': User.FcAccountType.CUSTOMER})
        self.serializer.is_valid(raise_exception=True)

        # update_last_login(None, request.user)
        self.login()
        return self.get_response()


class FcCustomerRegisterView(APIView):
    serializer_class = FcCustomerSignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class NewServiceRequestSchedule(generics.ListCreateAPIView):
    """
    Schedule a new request by passing the provider id selcted from
    search providers/ endpoint
    """
    serializer_class = FcServiceRequestSerializer
    # permission_classes = (IsCustomer,)

    def perform_create(self, serializer):
        user = self.request.user
        customer = get_object_or_404(FcCustomer, user=user)
        return serializer.save(customer=customer)

    def get_queryset(self):
        user = self.request.user
        print(user.customer_info.first())
        customer = user.customer_info.first()
        requests = FcServiceRequest.objects.filter(customer=customer)
        return requests


class FcSearchProviders(generics.ListAPIView):
    """
        initiate a new request by searching for provider who have specified
         a service or description of a service. pass query = "specified keyword"
    """
    serializer_class = FcProviderServicesSerializer
    # permission_classes = (IsCustomer,)
    pagination_class = pagination.CustomPageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('service__service', 'service_description')
    ordering = ('service__service',)  # Default ordering

    def get_queryset(self):
        qs = FcProviderServices.objects.all()
        query = self.kwargs.get('query')
        if query:
            qs = qs.filter(Q(service__service__icontains=query)|
                                                  Q(service_description__icontains=query))
        return qs


class UpdateRequestView(generics.RetrieveUpdateAPIView):
    serializer_class = FcServiceRequestSerializer
    # permission_classes = (IsCustomer,)
    # queryset = FcServiceRequest.objects.all()

    def get_object(self):
        query = self.kwargs.get('request_id')
        request_obj = get_object_or_404(FcServiceRequest,id=query)
        return request_obj


