from django.urls import path, include
from .api import NewRequestView,NewServiceRequestSchedule,UpdateRequestView

app_name = "customers"

urlpatterns = [
    path('new-request/', NewRequestView.as_view()),
    path('schedule/', NewServiceRequestSchedule.as_view()),
    path('request/<request_id>', UpdateRequestView.as_view()),
]

