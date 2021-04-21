from paypalpayoutssdk.payouts import PayoutsPostRequest
from paypalhttp import HttpError
from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment


# Creating Access Token for Sandbox
client_id = "AZSXZCVOuntZ2_B98xdE74TfFl0nSxKx5uCl97ag78Mqf7Gk6PkA1iSpnYwoi7J9SFqoV15f4GcCpPAM"
client_secret = "ENmegYyriCvCxHSoqEaTygXkWDwyG6ZoRzoapUJlQ9ySjVcK-XpoLlWhvi40PlyS2GkCPC7eSVhIp6VA"
# Creating an environment
environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
client = PayPalHttpClient(environment)

# Construct a request object and set desired parameters
# Here, PayoutsPostRequest() creates a POST request to /v1/payments/payouts
body = {
    "sender_batch_header": {
        "recipient_type": "EMAIL",
        "email_message": "SDK payouts test txn",
        "note": "Enjoy your Payout!!",
        "sender_batch_id": "Test_SDK_2",
        "email_subject": "This is a test transaction from SDK"
    },
    "items": [{
        "note": "Your 1$ Payout!",
        "amount": {
            "currency": "USD",
            "value": "1.00"
        },
        "receiver": "sb-zs0j85931255@personal.example.com",
        "sender_item_id": "Test_txn_1"
    }]
}

request = PayoutsPostRequest()
request.request_body(body)

try:
    # Call API with your client and get a response for your call
    response = client.execute(request)
    # If call returns body in response, you can get the deserialized version from the result attribute of the response
    batch_id = response.result.batch_header.payout_batch_id
    print(batch_id);
except IOError as ioe:
    print(ioe);
    if isinstance(ioe, HttpError):
        # Something went wrong server-side
        print(ioe.status_code);