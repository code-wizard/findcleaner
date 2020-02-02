from django.urls import include, path, re_path
from accounts import api
from accounts import views
from rest_auth.views import PasswordResetConfirmView

app_name = "accounts"

urlpatterns = [
    # path('customer-login/', api.FcCustomerLoginView.as_view(), name="customer-login"),
    path('rest-auth/', include('rest_auth.urls')),
    path('password/reset/confirm/<uidb64>/<key>', PasswordResetConfirmView.as_view(),
    name='auth_password_reset_confirm'),
    path("confirm-email/<key>/", views.confirm_email, name="confirm_email"),
    path("accounts/confirmed/", views.account_confirm, name="account_confirm"),
    path("accounts/resend-confirm-email/", api.FcResendActivationEmailAPIView.as_view(), name="resend_account_confirm"),
    path('accounts/', include('allauth.urls')),
    path('signup/', api.FcRegisterView.as_view())
]
