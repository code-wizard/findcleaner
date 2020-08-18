from rest_auth.views import LoginView
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from accounts import serializers
from rest_framework.response import Response
from allauth.account.utils import send_email_confirmation
from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import FcUser
from accounts.serializers import FcUserSerializer
from accounts.utils import format_number
from core.twilio import TwilioSMS
from dashboard.serializers import UsersViewSerializer

User = get_user_model()


class FcRegisterView(APIView):
    serializer_class = serializers.FcRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class FcResendActivationEmailAPIView(APIView):

    def get(self, request):
        try:
            user = User.objects.get(email=request.query_params.get("email"))

            send_email_confirmation(request, user, True)
        except:
            return Response("Unable to send activation email please ensure you entered a valid email",
                            status=status.HTTP_400_BAD_REQUEST)
        return Response("success")


class UserUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
        This endpoint allow both POST,GET and DELETE request by passing the username
        of the desired user to perform the operation on
        """
    serializer_class = FcUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user = get_object_or_404(FcUser, pk=self.kwargs.get("id"))
        return user
 

class FcValidatePhone(APIView):
    # serializer_class = serializers.FcPhoneSerializer

    def get(self, request, **kwargs):
        phone = format_number(kwargs.get("phone"))
        if User.objects.filter(phone_number=phone).exists():
            return Response("Account already registered with this phone number", status=status.HTTP_400_BAD_REQUEST)

        twilio_response = TwilioSMS().send_otp(to=phone)
        if not twilio_response:
            return Response({"status":"error", "message":"an error occured. Try after some time"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response("success", status=status.HTTP_200_OK)


class FcVerfiyOTP(APIView):
    # serializer_class = serializers.FcVerifyOtpSerializer

    def post(self, request):
        phone = format_number(request.data.get("phone"))
        _, message = TwilioSMS().check_verification(phone, request.data.get("code"))
        if not _:
            return Response("Invalid OTP", status=status.HTTP_400_BAD_REQUEST)
        return Response(message)


class FcVerifyPhoneForPasswordReset(APIView):
    # serializer_class = serializers.FcPhoneSerializer

    def get(self, request, **kwargs):
        phone = format_number(kwargs.get("phone"))
        if not User.objects.filter(phone_number=phone).exists():
            return Response("User account not found. You can sign up instead", status=status.HTTP_400_BAD_REQUEST)

        twilio_response = TwilioSMS().send_otp(to=phone)
        if not twilio_response:
            return Response({"status":"error", "message":"an error occured. Try after some time"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response("success", status=status.HTTP_200_OK)


class ResetPasswordView(APIView):

    def post(self, request):
        phone = self.request.data.get("phone")
        password = self.request.data.get("password")
        try:
            user = User.objects.get(phone_number=phone)
            user.set_password(password)
            user.save()
        except:
            return Response("error", status=status.HTTP_404_NOT_FOUND)

        return Response("success", status=status.HTTP_200_OK)