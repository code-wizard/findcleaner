from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from .serializers import NewCategorySerializer,ServiceSerializer
from services.models import FcService

class NewCategory(CreateAPIView):
    serializer_class = NewCategorySerializer


class NewService(CreateAPIView):
    serializer_class = ServiceSerializer


class AllServices(ListAPIView):
    serializer_class = ServiceSerializer
    queryset = FcService.objects.all()

# class ServiceDetail(RetrieveAPIView):
    # serializer_class =

