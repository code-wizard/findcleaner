from rest_framework import permissions

from billing.models import FcBillingInfo,FcProviderEearningInfo,FcCustomerCardsDetails
from billing import serializers
from rest_framework.generics import CreateAPIView, RetrieveAPIView,ListAPIView
from customers.models import FcServiceRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from billing.utils import load_lib
from accounts.serializers import FcUserDetailsSerializer
from uuid import uuid4
from django.http import JsonResponse
from rest_framework.validators import ValidationError
from core.permissions import IsProvider
from rest_framework import filters
from core import pagination
from django.contrib.auth import get_user_model

User = get_user_model()


class FcCustomerCardsDetailsView(ListAPIView):
    serializer_class = serializers.FcCustomerCardsDetailsSerializer
    permission_classes = (IsProvider,)
    pagination_class = pagination.CustomPageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('bank',)
    ordering = ('created_at',)  # Default ordering

    def get_queryset(self):
        user = self.request.user
        cards = FcCustomerCardsDetails.objects.filter(user=user)
        return cards


class NewBillingView(APIView):
    serializer_class = serializers.FcBillingInfoSerializer
    # permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, service_request_id):
        service_request = get_object_or_404(FcServiceRequest,id=service_request_id)
        return service_request

    def post(self,request):
        serializer = self.serializer_class(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        service_request_id = serializer.validated_data['service_request'].id
        service_request = self.get_object(service_request_id)

        if not service_request.status == FcServiceRequest.FcRequestStatus.COMPLETED:
            raise ValidationError("Error!!! You can only make payment for completed service.")

        customer_user_info = service_request.customer.user

        customer_info = FcUserDetailsSerializer(customer_user_info).data

        PaystackAPI = load_lib()
        paystack_instance = PaystackAPI()

        context = {
            "reference": str(uuid4()),
            "email": customer_info['email'],
            "amount": service_request.total_amount
        }
        auth_code = self.request.GET.get("authorization_code")

        # check if the customer card details exists with the auth_code
        if FcCustomerCardsDetails.objects.filter(authorization_code=auth_code,user=self.request.user).exists():
            context.update({'authorization_code':auth_code})
            res = paystack_instance.recurrent_charge(context)
            return JsonResponse({"data": res})

        # if not charge as a new customer
        data = paystack_instance.charge_customer(context)
        serializer.save(billing_reference=context['reference'])
        return JsonResponse({"data": data})


def all_banks_list(request):
    PaystackAPI = load_lib()
    paystack_instance = PaystackAPI()
    response = paystack_instance.get_bank_list_api()
    return JsonResponse({"banks":response})


def verify_payment(request, billing_reference):
    refrence_code = billing_reference
    PaystackAPI = load_lib()
    paystack_instance = PaystackAPI()
    response = paystack_instance.verify_payment(refrence_code)
    # check if payment has been made,
    if response[2]['status'] == 'success':
        payment_info_from_paystack = response[2]['authorization']

        billing_info = get_object_or_404(FcBillingInfo,billing_reference=billing_reference)
        billing_info.status = billing_info.Billing_Status.PAID
        billing_info.save()
        FcCustomerCardsDetails.objects.get_or_create(**payment_info_from_paystack,billing_info=billing_info,user=request.user)

        context = {
            'status':200,
            'message': "Payment has been made successfully"
        }
        return JsonResponse(context)
    return JsonResponse({
        "status": response[0],
        "message": response[2]
    })


class FcEarningRequestView(CreateAPIView):
    serializer_class = serializers.FcInitiateCustomerPaymentInfoSerializer
    queryset = FcProviderEearningInfo.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        service_request_id = serializer.validated_data['service_request']
        if not FcServiceRequest.objects.filter(id=service_request_id).exists():
            raise ValidationError("Service request not found with this ID")

        serializer.save(service_request=service_request_id)
        return JsonResponse({"status":"successfully done"})


class FcEarningInfo(RetrieveAPIView):
    serializer_class = serializers.FcEarningInfoSerializer

    def get_object(self):
        query = self.kwargs.get('service_request_id')
        service_request = get_object_or_404(FcServiceRequest, id=query)
        return service_request


def verify_transfer(request,reference):
    refrence_code = reference
    PaystackAPI = load_lib()
    paystack_instance = PaystackAPI()
    response = paystack_instance.verify_transfer(refrence_code)

    return JsonResponse({"response":response})
