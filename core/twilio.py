from django.conf import settings
from twilio.rest import Client

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


class TwilioSMS(object):

    def send_otp(self, to, channel="sms"):
        if channel not in ("sms", "voice"):
            channel = "sms"
        try:
            verification = client.verify \
                .services(settings.VERIFICATION_SID) \
                .verifications \
                .create(to=to, channel=channel)
                
            return verification.sid
        except:
            return None

    def check_verification(self, phone, code):
        service = settings.VERIFICATION_SID

        try:
            verification_check = client.verify \
                .services(service) \
                .verification_checks \
                .create(to=phone, code=code)

            if verification_check.status == "approved":

                return True, "Your phone number has been verified! Please login to continue."

            else:
                return False, "The code you provided is incorrect. Please try again."
        except Exception as e:
            return False, "Error validating code: {}".format(e)