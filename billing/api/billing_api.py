from billing.models import FcBillingInfo
from billing.serializers import FcBillingInfoSerializer
from rest_framework.generics import CreateAPIView
from customers.models import FcServiceRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from billing.utils import load_lib
from accounts.serializers import FcUserDetailsSerializer
from uuid import uuid4
from django.http import JsonResponse


class NewBillingView(APIView):
    serializer_class = FcBillingInfoSerializer

    def get_object(self, service_request_id):
        service_request = get_object_or_404(FcServiceRequest,id=service_request_id)
        return service_request

    def post(self,request):
        serializer = self.serializer_class(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        service_request_id = serializer.validated_data['service_request'].id
        service_request = self.get_object(service_request_id)

        customer_user_info = service_request.customer.user

        customer_info = FcUserDetailsSerializer(customer_user_info).data

        PaystackAPI = load_lib()
        paystack_instance = PaystackAPI()

        context = {
            "reference": str(uuid4()),
            "email": customer_info['email'],
            "amount": service_request.total_amount
        }
        data = paystack_instance.charge_customer(context)
        serializer.save(billing_reference=context['reference'])
        return JsonResponse({"data": data})


def verify_payment(request,billing_reference):
    refrence_code = billing_reference
    PaystackAPI = load_lib()
    paystack_instance = PaystackAPI()
    response = paystack_instance.verify_payment(refrence_code)

    # check if payment has been made,
    if response[0]:
        billing_info = get_object_or_404(FcBillingInfo,billing_reference=billing_reference)
        billing_info.status = billing_info.Billing_Status.PAID
        billing_info.save()

        context = {
            'status':'Successful',
            'message': response[1]
        }
        return JsonResponse(context)

    return JsonResponse(response)



