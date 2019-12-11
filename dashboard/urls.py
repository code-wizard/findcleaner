from django.urls import path
from dashboard import api


app_name = "dashboard"

urlpatterns = [
    path('users/', api.AllUsers.as_view()),
    path('active-session/', api.ActiveSession.as_view()),
    path('user/<username>', api.UserUpdateDeleteView.as_view()),
    path('all-transaction/', api.AllTransactionView.as_view()),
    path('transaction/<service_id>', api.TransactionView.as_view()),
    path('settings/', api.FcSettingView.as_view()),
]

