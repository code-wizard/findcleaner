from .base import BaseClass

class BillingCustomer(BaseClass):
    def create_customer(self, data):
        path = "/customer"
        response = self.make_request('POST', path, json=data)
        # return self.result_format(response)
        if response.status_code >= 400:
            return None
        return response.json()['data']['customer_code']


    def get_customer(self, customer_email):
        path = "/customer/{}".format(customer_email)
        response = self.make_request('GET', path)
        return self.result_format(response)


class Transaction(BaseClass):

    def initialize_transaction(self, kwargs):

        path = "/transaction/initialize"

        json_data = {
            'reference': kwargs['reference'],
            'email': kwargs['email'],
            'amount': kwargs['amount'] ,
            # 'callback_url': kwargs['callback_url']
        }
        response = self.make_request('POST', path, json=json_data)
        return self.result_format(response)

    def recurrent_charge(self, **kwargs):

        path = "/transaction/charge_authorization"
        json_data = {
            'authorization_code': kwargs['authorization_code'],
            'email': kwargs['email'],
            'amount': kwargs['amount']
        }
        response = self.make_request('POST', path, json=json_data)
        return self.result_format(response)


