from .serializers import FcAdminSignupSerializer,FcAdminSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_auth.views import LoginView
from accounts.serializers import FcLoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from fc_admin.models import FcAdmin
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions, viewsets,generics,filters,status,views
from core import pagination

FcUser = get_user_model()


class FcAdminLoginView(LoginView):
    serializer_class = FcLoginSerializer

    def get_response(self):
        serializer_class = self.get_response_serializer()
        data = {
            'user': self.user,
            'token': self.token
        }
        serializer = serializer_class(instance=data, context={'request': self.request})
        staff = get_object_or_404(FcAdmin,user=self.user)

        return Response({"user": serializer.data,"staff":staff.role}, status=status.HTTP_200_OK)


    def post(self, request):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context = {'request':request,
                                                         'account_type': FcUser.FcAccountType.ADMIN})
        self.serializer.is_valid(raise_exception=True)

        self.login()
        if not self.user.is_staff:
            return Response('You are not authorized to access this endpoint. Contact admin', status=401)
        return self.get_response()


class FcAdminRegisterView(APIView):
    serializer_class = FcAdminSignupSerializer

    def post(self, request):
        # print('request',request.data)
        try:
            data = request.data.dict()
        except:
            data = request.data
        serializer = self.serializer_class(data=data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data)


class FcAdminListView(generics.ListAPIView):
    serializer_class = FcAdminSerializer
    pagination_class = pagination.CustomPageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('role','user__first_name','user__last_name','user__email','user__is_active')
    ordering = ('role','user__first_name','user__last_name')
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = FcAdmin.objects.filter(is_deleted=False,user__is_staff=True).order_by('-user__created_at')


class FcAdminUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FcAdminSerializer

    def get_object(self):
        id = self.kwargs.get('staff_id')
        staff = get_object_or_404(FcAdmin,user__id = id,is_deleted=False)
        return staff

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response({'message':'deleted'})


