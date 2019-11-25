from django.urls import include, path, re_path
from accounts import api
from accounts import views


app_name = "accounts"

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path("confirm-email/<key>/", views.confirm_email, name="confirm_email"),
    path("accounts/confirmed/", views.account_confirm, name="account_confirm"),
    path("accounts/resend-confirm-email/", api.FcResendActivationEmailAPIView.as_view(), name="resend_account_confirm"),
    path('accounts/', include('allauth.urls')),
    path('signup/', api.FcRegisterView.as_view())
]
