from rest_framework import permissions, viewsets,generics,filters,status,views
from .serializers import FcServiceRequestSerializer
from providers.models import FcServiceProvider
from core import pagination
from providers.serializers import FcServiceProviderSerializer
from django.db.models import Q


class NewServiceRequestSchedule(generics.CreateAPIView):
    serializer_class = FcServiceRequestSerializer


class NewRequestView(generics.ListAPIView):
    """
       Search employee by passing 'search' = 'fieldname' as url param, you can pass firstname, lastname, middlename or employee username.
       This view also support ordering of fields by passing 'ordering' = 'fieldname'
    """
    serializer_class = FcServiceProviderSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    pagination_class = pagination.CustomPageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('service__service', 'service_description')
    ordering = ('service__service',)  # Default ordering

    def get_queryset(self):
        qs = FcServiceProvider.objects.all()
        query = self.kwargs.get('query')
        if query:
            qs = qs.filter(Q(service__service__icontains=query)|
                                                  Q(service_description__icontains=query))
        return qs