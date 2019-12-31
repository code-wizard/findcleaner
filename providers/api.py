from django.contrib.auth import get_user_model
from rest_auth.views import LoginView

from .serializers import FcProviderServicesSerializer,FcProviderDashboard,\
    FcServiceRequestSerializer,FcProviderSignUpSerializer, FcProviderSerializer
from .models import FcProviderServices
from accounts.serializers import FcUserDetailsSerializer
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.views import  APIView
from customers.models import FcServiceRequest
from django.db.models import Sum
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import FcProvider
from accounts.serializers import FcLoginSerializer
User = get_user_model()
from rest_framework import permissions, status
from core.permissions import IsCustomer,IsProvider,IsStaff


class FcProviderLoginView(LoginView):
    serializer_class = FcLoginSerializer

    def get_response(self):
        serializer_class = self.get_response_serializer()
        data = {
            'user': self.user,
            'token': self.token
        }
        serializer = serializer_class(instance=data, context={'request': self.request})

        provider = FcProviderSerializer(self.user.provider_info).data
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
    serializer_class = FcProviderSignUpSerializer

    def post(self, request):
        data = request.data.dict()
        data["coords"] = [9434034,-4343]
        serializer = self.serializer_class(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'success'})

class NewProviderService(CreateAPIView):
    """
    Use this end point to add service to provider by passing service ID
    """
    serializer_class = FcProviderServicesSerializer
    # permission_classes = (IsProvider,)

    def perform_create(self, serializer):
        user = self.request.user
        provider = get_object_or_404(FcProvider, user=user)
        return serializer.save(provider=provider)


class ProviderServiceList(ListAPIView):
    """
    Get a list of providers who have signed up for the specified service,
    by passing the service id.
    """
    serializer_class = FcProviderServicesSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        service_id = self.kwargs.get('service_id')
        return FcProviderServices.objects.filter(service__id=service_id)



class ProviderSummaryDashboard(APIView):
    """
        Logged in provider can use this endpoint to show summary of all his transaction
    """
    def get(self,request):
        user = self.request.user
        provider = user.provider_info.all().first()
        # print('provider',provider)
        # provider_service_request
        try:
            myservices = provider.my_services.all()
            print('myservices',myservices)
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
        print('my_revenue',my_revenue)
        dashbooard_summary = {
            'total_service':total_service,
            'cancelled_service':cancelled_service,
            'schedule_service':schedule_service,
            'my_revenue':my_revenue
        }

        result = FcProviderDashboard(dashbooard_summary).data
        return Response(result)


class MyServiceRequest(ListAPIView):
    """
    View all logged in provider request.
    """
    serializer_class = FcServiceRequestSerializer
    # permission_classes = (IsProvider,)

    def get_queryset(self):
        # print('get here')
        user = self.request.user
        # print('user',user)

        provider = user.provider_info.all().first()
        # print('provider',provider)
        myservices = provider.my_services.all()
        service_provider_obj = myservices.first()
        my_service_requests = FcServiceRequest.objects.filter(service_provider=service_provider_obj)
        return my_service_requests


class RequestByStatus(ListAPIView):
    """
        View List of request based and filter by request status. which can be
        new, accepted, ongoing, cancel and completed

    """
    serializer_class = FcServiceRequestSerializer

    def get_queryset(self):
        status = self.kwargs.get('status')
        user = self.request.user

        provider = user.provider_info.all().first()

        myservices = provider.my_services.all()
        service_provider_obj = myservices.first()
        my_service_requests = FcServiceRequest.objects.filter(service_provider=service_provider_obj,status=status)
        return my_service_requests






