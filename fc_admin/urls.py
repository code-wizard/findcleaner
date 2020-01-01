from fc_admin import api
from django.urls import path

app_name = "fc_admin"

urlpatterns = [
        path('login/', api.FcAdminLoginView.as_view()),
        path('signup/', api.FcAdminRegisterView.as_view()),
        path('users/', api.FcAdminListView.as_view()),
        path('update/<staff_id>', api.FcAdminUpdateView.as_view()),
]
