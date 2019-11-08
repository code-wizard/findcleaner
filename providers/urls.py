from .api import (NewProviderService,
                  ProviderSummaryDashboard,
                  MyServiceRequest,
                  ProviderServiceList,
                  RequestByStatus)

from django.urls import path, include

app_name = "providers"

urlpatterns = [
        path('new-service/', NewProviderService.as_view()),
        path('summary/',ProviderSummaryDashboard.as_view()),
        path('all-request/',MyServiceRequest.as_view()),
        path('request/<status>', RequestByStatus.as_view()),
        path('<service_id>/providers', ProviderServiceList.as_view()),

]