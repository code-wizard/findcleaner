from django.urls import path
from dashboard import api


app_name = "dashboard"

urlpatterns = [
    path('users/', api.AllUsers.as_view()),
    path('users/all', api.AllUsers_NoPgaination.as_view()),
    path('rated-users/all', api.AllRatedUsers.as_view()),
    path('active-session/', api.ActiveSession.as_view()),
    path('active-session/all', api.ActiveSessionNoPagination.as_view()),
    path('user/<user_email>', api.UserUpdateDeleteView.as_view()),
    path('all-transaction/', api.AllTransactionView.as_view()),
    path('transactions/<from_date>/<to_date>', api.FilterTransactionView.as_view()),
    path('transaction/<service_id>', api.TransactionView.as_view()),
    path('settings/', api.FcSettingView.as_view()),
]


