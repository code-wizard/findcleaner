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
