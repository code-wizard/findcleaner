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


class EarningProvider(BaseClass):

    def new_transfer_recipient(self, data):
        path = "/transferrecipient"
        response = self.make_request('POST', path, json=data)
        # return self.result_format(response)
        if response.status_code >= 400:
            return response.json()
        return response.json()['data']['recipient_code']

    def initiate_transfer(self,data):
        path = "/transfer"
        response = self.make_request('POST', path, json=data)
        # return self.result_format(response)
        if response.status_code >= 400:
            return response.json()
        return response.json()['data']

    def verify_transfer(self,data):
        path = "/transfer/verify/reference"
        response = self.make_request('GET', path, json=data)
        if response.status_code >= 400:
            return response.json()
        return response.json()['data']


class BankInfo(BaseClass):

    def get_bank_list(self):
        path = "/bank"
        response = self.make_request('GET', path)
        if response.status_code >= 400:
            return response.json()
        return response.json()['data']


class Transaction(BaseClass):

    def verify_result(self, response, **kwargs):
        if response.status_code == 200:
            result = response.json()
            data = result["data"]
            amount = kwargs.get("amount")
            if amount:
                if data["amount"] == int(amount):
                    return True, result["message"]
                return False, data["amount"]
            return True, result["message"], data

        if response.status_code >= 400:
            return False, "Could not verify transaction"

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

    def verify_payment(self,code, **kwargs):
        path = "/transaction/verify/{}".format(code)
        response = self.make_request("GET", path)
        return self.result_format(response)

    def charge_authorization(self, kwargs):

        path = "/transaction/charge_authorization"
        json_data = {
            'authorization_code': kwargs['authorization_code'],
            'email': kwargs['email'],
            'amount': kwargs['amount']
        }
        response = self.make_request('POST', path, json=json_data)
        return self.result_format(response)




