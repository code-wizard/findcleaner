from django.urls import path, include
from .api import NewCategory,NewService,AllServices

app_name = 'services'

urlpatterns = [
    path('new-category/', NewCategory.as_view()),
    path('new-service/', NewService.as_view()),
    path('all-services',AllServices.as_view())
]