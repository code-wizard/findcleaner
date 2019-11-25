from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from allauth.utils import build_absolute_uri

class AccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self,client_domain, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        url = reverse(
            "accounts:confirm_email",
            args=[emailconfirmation.key])
        ret = build_absolute_uri(
            request,
            url)
        return ret

    def confirm_email(self, request, email_address):
        """
        Marks the email address as confirmed on the db
        """
        email_address.verified = True
        email_address.set_as_primary(conditional=True)
        email_address.save()

        u = get_user_model().objects.get(pk=email_address.user.id)
        u.is_active = True
        u.save()

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        user_default_password = request.session.pop('default_password',None)
        client_domain = request.session.pop('client_domain',None)

        current_site = get_current_site(request)
        activate_url = self.get_email_confirmation_url(client_domain,
            request,
            emailconfirmation)
        ctx = {
            "user_password": user_default_password,
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": emailconfirmation.key
        }
        if signup:
            email_template = 'authentication/email/activate_email'
        else:
            email_template = 'authentication/email/activate_email'
        self.send_mail(email_template,
                       emailconfirmation.email_address.email,
                       ctx)
