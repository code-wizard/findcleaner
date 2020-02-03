from providers import api
from django.urls import path, include

app_name = "providers"

urlpatterns = [
        path('login/', api.FcProviderLoginView.as_view()),
        path('signup/', api.FcProviderRegisterView.as_view()),
        path('new-service/', api.FcNewProviderService.as_view()),
        path('my-services/', api.FcProviderServiceList.as_view()),
        path('my-service-update/<provider_service_id>', api.FcUpdateProviderServiceView.as_view()),
        path('summary/',api.FcProviderSummaryDashboard.as_view()),
        path('all-request/',api.FcMyServiceRequest.as_view()),
        path('request/<status>', api.FcRequestByStatus.as_view()),
        path('my-earnings/', api.FcProviderEarnings.as_view()),
        path('<service_id>/providers', api.FcProviderServiceList.as_view()),

]

