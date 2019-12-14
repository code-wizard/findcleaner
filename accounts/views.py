from allauth.account.views import EmailConfirmationHMAC
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from django.views.generic.base import TemplateResponseMixin, View

#
# class MmConfirmEmailView(ConfirmEmailView):
#     template_name = "authentication/account_activate_confirm.html"
#
#
#
# confirm_email = MmConfirmEmailView.as_view()




class FcConfirmEmailView(TemplateResponseMixin, View):
    template_name = "authentication/account_activate_confirm.html"

    def get(self, *args, **kwargs):
        # context = {"domain":connection.tenant.domain_url}
        return self.render_to_response()


account_confirm = FcConfirmEmailView.as_view()



class ConfirmEmailView(APIView):
    template_name = "authentication/account_activate_confirm.html"
    permission_classes = ()

    def get_object(self, queryset=None):
        key = self.kwargs.get('key') #['key']
        print('key',key)
        emailconfirmation = EmailConfirmationHMAC.from_key(key)
        return emailconfirmation


    def post(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        if confirmation:
            confirmation.confirm(self.request)
            status = "Activated"
        else:
            status = 'Error'

        return Response({"status": status})

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        if confirmation:
            confirmation.confirm(self.request)
            status = "Activated"
        else:
            status = 'Error'

        return Response({"status": status})

confirm_email = ConfirmEmailView.as_view()
