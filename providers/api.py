from django.contrib.auth import get_user_model
from rest_auth.views import LoginView

from providers import serializers
from .models import FcProviderServices
from accounts.serializers import FcUserDetailsSerializer
from rest_framework.generics import CreateAPIView,ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import  APIView
from customers.models import FcServiceRequest
from django.db.models import Sum
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import FcProvider
from accounts.serializers import FcLoginSerializer
from core.permissions import IsCustomer,IsProvider,IsStaff
from rest_framework import filters,status
from core import pagination


User = get_user_model()


class FcProviderLoginView(LoginView):
    """
    Use this endpoint to login as a provider by providing your email and password
    """
    serializer_class = FcLoginSerializer

    def get_response(self):
        serializer_class = self.get_response_serializer()
        data = {
            'user': self.user,
            'token': self.token
        }
        serializer = serializer_class(instance=data, context={'request': self.request})

        provider = serializers.FcProviderSerializer(self.user.provider_info).data
        return Response({"user": serializer.data, 'provider': provider}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request, 'account_type': User.FcAccountType.PROVIDER})
        self.serializer.is_valid(raise_exception=True)

        # update_last_login(None, request.user)
        self.login()
        if self.user.provider_info.status == FcProvider.FcProviderStatus.DISABLED:
            return Response('Your account is under review. Please contact admin', status=401)
        return self.get_response()


class FcProviderRegisterView(APIView):
    """
    provider signup endpoint. pass a list of services to services_info field
    in the format below

    [{"service_id":1,"billing_rate":2500,
    "service_description":"description"},
    {"service_id":2,"billing_rate":2300,
    "service_description":"good service"}]
    """
    serializer_class = serializers.FcProviderSignUpSerializer

    def post(self, request):
        try:
            data = request.data.dict()
        except:
            data = request.data
        print('data',data)
        # data["coords"] = [9434034,-4343]
        serializer = self.serializer_class(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'success'})


class FcNewProviderService(CreateAPIView):
    """
    Use this end point to add service to provider by passing service ID
    """
    serializer_class = serializers.FcProviderServicesSerializer
    # permission_classes = (IsProvider,)

    def perform_create(self, serializer):
        user = self.request.user
        provider = get_object_or_404(FcProvider, user=user)
        return serializer.save(provider=provider)


class FcProviderServiceList(ListAPIView):
    """
    Get a list of providers who have signed up for the specified service,
    by passing the service id.
    """
    serializer_class = serializers.FcProviderServicesSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        service_id = self.kwargs.get('service_id')
        return FcProviderServices.objects.filter(service__id=service_id)


class FcProviderSummaryDashboard(APIView):
    """
        Logged in provider can use this endpoint to show summary of all his transaction
    """
    def get(self,request):
        user = self.request.user
        provider = user.provider_info
        # print('provider',provider)
        # provider_service_request
        try:
            myservices = provider.my_services.all()
            service_provider_obj = myservices.first()
            my_service_requests = FcServiceRequest.objects.filter(service_provider=service_provider_obj)
            completed_service = my_service_requests.filter(status='completed')
            total_service = myservices.count()
            cancelled_service = my_service_requests.filter(status='cancel').count()
            schedule_service = my_service_requests.filter(status='accepted').count()
            my_revenue = 0 if completed_service == None else completed_service.aggregate(Sum('total_amount'))['total_amount__sum']
        except AttributeError:
            total_service = 0
            cancelled_service = 0
            schedule_service = 0
            my_revenue = 0
        dashbooard_summary = {
            'total_service':total_service,
            'cancelled_service':cancelled_service,
            'schedule_service':schedule_service,
            'my_revenue': 0 if my_revenue == None else my_revenue
        }

        result = serializers.FcProviderDashboard(dashbooard_summary).data
        return Response(result)


class FcMyServiceRequest(ListAPIView):
    """
    View all logged in provider request.
    """
    serializer_class = serializers.FcServiceRequestSerializer
    permission_classes = (IsProvider,)

    def get_queryset(self):
        user = self.request.user
        provider = user.provider_info
        # myservices = provider.my_services.all()
        # service_provider_obj = myservices.first()
        my_service_requests = FcServiceRequest.objects.filter(service_provider__provider=provider)
        return my_service_requests


class FcRequestByStatus(ListAPIView):
    """
        View List of request based and filter by request status. which can be
        new, accepted, ongoing, cancel and completed

    """
    serializer_class = serializers.FcServiceRequestSerializer

    def get_queryset(self):
        status = self.kwargs.get('status')
        user = self.request.user

        provider = user.provider_info

        myservices = provider.my_services.all()
        service_provider_obj = myservices.first()
        if status == 'all':
            my_service_requests = FcServiceRequest.objects.filter(service_provider=service_provider_obj.pk)
        else:
            my_service_requests = FcServiceRequest.objects.filter(service_provider=service_provider_obj.pk, status=status)
        return my_service_requests


# class FcProvideEarningView()

class FcProviderEarnings(ListAPIView):
    serializer_class = serializers.FcServiceRequestEarningsSerializer
    # permission_classes = (IsProvider,)
    pagination_class = pagination.CustomPageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('service__service',)
    ordering = ('service__service',)  # Default ordering

    def get_queryset(self):
        user = self.request.user
        user = get_object_or_404(User,id=user.id)
        provider = user.provider_info

        myservices = provider.my_services.all()
        service_provider_obj = myservices.first()
        history_earnings = FcServiceRequest.objects.filter(service_provider=service_provider_obj.pk)
        return history_earnings

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        my_revenue = qs.aggregate(Sum('total_amount'))[
            'total_amount__sum']

        serializer  = self.get_serializer(qs, many=True)
        response_data = {"total_earning":my_revenue, "result":serializer.data}
        return Response(response_data)


class FcProviderServiceList(ListAPIView):
    serializer_class = serializers.FcProviderServicesSerializer
    permission_classes = (IsProvider,)

    def get_queryset(self):
        user = self.request.user
        provider = get_object_or_404(FcProvider, user=user)
        my_services = FcProviderServices.objects.filter(provider=provider)
        return my_services


class FcUpdateProviderServiceView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.FcProviderServicesSerializer
    # permission_classes = (IsProvider,)

    def get_object(self):
        user = self.request.user
        provider = get_object_or_404(FcProvider, user=user)

        provider_service_id = self.kwargs.get('provider_service_id')
        p_services = get_object_or_404(FcProviderServices,provider = provider,id=provider_service_id)
        return p_services