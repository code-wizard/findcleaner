from rest_framework.views import APIView
from accounts import serializers
from rest_framework.response import Response
from allauth.account.utils import send_email_confirmation
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
            return Response("Unable to send activation email please enrsure you entered a valid email",
                            status=status.HTTP_400_BAD_REQUEST)
        return Response("success")

