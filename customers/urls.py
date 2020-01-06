from django.urls import path, include
from customers import api

app_name = "customers"

urlpatterns = [
    path('search-providers', api.FcSearchProviders.as_view()),
    path('login/', api.FcCustomerLoginView.as_view()),
    path('signup/', api.FcCustomerRegisterView.as_view()),
    path('schedule/', api.NewServiceRequestSchedule.as_view()),
    path('request/<request_id>', api.UpdateRequestView.as_view()),
]

