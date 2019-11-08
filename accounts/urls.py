from django.urls import include, path, re_path
from accounts import api

app_name = "accounts"

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('signup/', api.FcRegisterView.as_view())
]

