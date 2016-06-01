from twilio.rest import TwilioRestClient

account = os.environ['TWILIO_ACCOUNT_SID']
token = os.environ['TWILIO_AUTH_TOKEN']
client = TwilioRestClient(account, token)

message = client.messages.create(to="+17076960691", from_="+15555555555",
                                 body="Hello there!")