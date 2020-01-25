import hmac
import hashlib
import requests
import importlib
# from . import api
from billing.api import transaction


class PaystackAPI(object):
    def __init__(self, django=True, **kwargs):
        if django:
            from . import settings

            self.public_key = kwargs.get("public_key", settings.PAYSTACK_PUBLIC_KEY)
            self.secret_key = kwargs.get("secret_key", settings.PAYSTACK_SECRET_KEY)
            self.base_url = kwargs.get("base_url", settings.PAYSTACK_API_URL)
        else:
            for key, value in kwargs.items():
                setattr(self, key, value)
        self.transaction_api = transaction.Transaction(self.make_request)
        self.customer_api = transaction.BillingCustomer(self.make_request)
        # self.transfer_api = transaction.Transfer(self.make_request, self.async_make_request)
        # self.webhook_api = transaction.Webhook(self.secret_key)
        # self.subscription_api = transaction.PlanAndSubscription(self.make_request)

    def make_request(self, method, path, **kwargs):
        options = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "DELETE": requests.delete,
        }
        url = "{}{}".format(self.base_url, path)
        headers = {
            "Authorization": "Bearer {}".format(self.secret_key),
            "Content-Type": "application/json",
        }
        return options[method](url, headers=headers, **kwargs)

    async def async_make_request(self, method, path, session, **kwargs):
        options = {
            "GET": session.get,
            "POST": session.post,
            "PUT": session.put,
            "DELETE": session.delete,
        }
        url = "{}{}".format(self.base_url, path)
        headers = {
            "Authorization": "Bearer {}".format(self.secret_key),
            "Content-Type": "application/json",
        }
        return await options[method](url, headers=headers, **kwargs)


    def new_customer(self, data):
        return self.customer_api.create_customer(data)

    def get_customer(self,cust_email):
        return self.customer_api.get_customer(cust_email)

    def charge_customer(self, data):
        return self.transaction_api.initialize_transaction(data)



def load_lib(config=None):
    """
    dynamically import the paystack module to use
    """
    from . import settings

    config_lib = config or settings.PAYSTACK_LIB_MODULE
    module = importlib.import_module(config_lib)
    return module.PaystackAPI


def generate_digest(data):
    from . import settings

    return hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode("utf-8"), msg=data, digestmod=hashlib.sha512
    ).hexdigest()  # request body hash digest
