from django.contrib.auth import get_user_model
from rest_auth.views import LoginView
from rest_framework import permissions,generics,filters,status,views
from rest_framework.response import Response
from rest_framework.views import APIView
from customers.models import FcHelp

from .serializers import FcServiceRequestSerializer, FcCustomerSignUpSerializer, FcCreateServiceRequestSerializer
from providers.models import FcProviderServices
from .models import FcCustomer
from core import pagination
from providers.serializers import FcProviderServicesSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from customers.models import FcServiceRequest
from core.permissions import IsCustomer,IsProvider,IsStaff
from accounts.serializers import FcLoginSerializer
from billing.utils import load_lib
from uuid import uuid4
from billing.models import FcCustomerCardsDetails,DefaultCardBillingInfo,FcBillingInfo
from django.http import JsonResponse
from core.mail_utils import send_email_

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
    serializer_class = FcCreateServiceRequestSerializer
    permission_classes = (IsCustomer,)

    def perform_create(self, serializer): 
        user = self.request.user
        customer = get_object_or_404(FcCustomer, user=user)

        return serializer.save(customer=customer)

    def get_queryset(self):
        user = self.request.user
        customer = user.customer_info.first()
        requests = FcServiceRequest.objects.filter(customer=customer)
        return requests

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # customer = get_object_or_404(FcCustomer, user=self.request.user)

        context.update({
            'user':self.request.user
        })
        return context


class FcSearchProviders(generics.ListAPIView):
    """
        initiate a new request by getting list of providers who have signed up for the passed service_id,
        passs the following as url param: service_id, neighborhood and locality and customer_coords as (lat,lng)
    """
    serializer_class = FcProviderServicesSerializer
    # permission_classes = (IsCustomer,)
    pagination_class = pagination.CustomPageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('service__service', 'service_description')
    ordering = ('service__service',)  # Default ordering

    def get_queryset(self):
        qs = FcProviderServices.objects.all()
        service_id = self.request.GET.get("service_id",None)
        if service_id:
            qs = qs.filter(service_id=service_id)
        
        neighborhood = self.request.GET.get("neighborhood","")
        locality = self.request.GET.get("locality","")
        qs = qs.filter(Q(provider__address__icontains=neighborhood) & Q(provider__address__icontains=locality))
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'lat': self.request.GET.get("lat"),
            'lng': self.request.GET.get("lng")
        })
        return context


class UpdateRequestView(generics.RetrieveUpdateAPIView):
    serializer_class = FcServiceRequestSerializer
    # permission_classes = (IsCustomer,)
    # queryset = FcServiceRequest.objects.all()

    def get_object(self):
        query = self.kwargs.get('request_id')
        request_obj = get_object_or_404(FcServiceRequest,id=query)
        return request_obj

    def patch(self, request,*args, **kwargs):
        serializer = self.serializer_class(self.get_object(),data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        service_request = self.get_object()
        # check for service request status
        if request.data.get('status') == FcServiceRequest.FcRequestStatus.COMPLETED:
            customer_info = service_request.customer.user
            PaystackAPI = load_lib()
            paystack_instance = PaystackAPI()

            context = {
                "reference": str(uuid4()),
                "email": customer_info.email,
                "amount": service_request.total_amount
            }
            customer_cardss = FcCustomerCardsDetails.objects.filter(user=self.request.user,is_deleted=False).values('id').distinct()
            # fetch default card detail
            auth_code = DefaultCardBillingInfo.objects.get(record_id__in=customer_cardss, model_name='FcCustomerCardsDetails').id

            # check if the customer card details exists with the auth_code
            if auth_code:
                context.update({'authorization_code': auth_code})
                res = paystack_instance.recurrent_charge(context)
                return JsonResponse({"data": res})  # payment is being made here

            # if not charge as a new customer
            # this will return authorization url where payment can be made
            data = paystack_instance.charge_customer(context)
            FcBillingInfo.objects.get_or_create(service_request=service_request,billing_reference=context['reference'])
            return JsonResponse({"data": data})
        return Response(serializer.data)


class FcCancelServiceRequestView(APIView):
    serializer_class = FcServiceRequestSerializer

    def get_object(self):
        query = self.kwargs.get('request_id')
        request_obj = get_object_or_404(FcServiceRequest, id=query)
        return request_obj

    def patch(self, request,*args, **kwargs):
        serializer = self.serializer_class(self.get_object(),data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(status=FcServiceRequest.FcRequestStatus.CANCELLED)
        return Response(serializer.data)


class FcCustomerServiceHistoryViews(generics.ListAPIView):
    """
        get customer task history by passing the customer username. if status is passed. it will be filtered
        based on that else it will show only completed tasks. status can be (new,completed,ongoing,accepted,cancel)
    """
    serializer_class = FcServiceRequestSerializer
    # permission_classes = (IsCustomer,)
    # queryset = FcServiceRequest.objects.all()

    def get_queryset(self):
        # user_id = self.kwargs.get("user_id")
        user = self.request.user #get_object_or_404(User,id=user_id)
        status = self.request.GET.get('status','completed')
        # history_tasks = FcServiceRequest.objects.filter(customer=user.customer_info.first(),status=status)
        history_tasks = FcServiceRequest.objects.filter(customer=user.customer_info.first())
        return history_tasks


class FcHelpAPIView(APIView):

    def get(self, request):
        help = FcHelp.objects.filter()[0]
        return Response(dict(phone=help.phone, email=help.email))