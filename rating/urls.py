from providers import api
from django.urls import path, include
from .api import FcRatingView,FcRatingUpdateView,GetUserRatingView


app_name = "rating"

urlpatterns = [
    path('new',FcRatingView.as_view()),
    path('update/<rating_id>', FcRatingUpdateView.as_view()),
    path('user/<user_id>', GetUserRatingView.as_view()),
]