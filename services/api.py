from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from .serializers import NewCategorySerializer,ServiceSerializer
from services.models import FcService

class NewCategory(CreateAPIView):
    """
    Add new service category
    """
    serializer_class = NewCategorySerializer


class NewService(CreateAPIView):
    """
    Add new service endpioint
    """
    serializer_class = ServiceSerializer


class AllServices(ListAPIView):
    """
    List all services
    """
    serializer_class = ServiceSerializer
    queryset = FcService.objects.all()

# class ServiceDetail(RetrieveAPIView):
    # serializer_class =

