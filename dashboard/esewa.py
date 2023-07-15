import requests
from dashboard.models import Payment

def initiate_esewa_payment(payment_id, callback_url):
    # Retrieve the payment object based on the payment ID
    payment = Payment.objects.get(id=payment_id)

    # Set up the request payload
    payload = {
        'amt': payment.amt,
        'pdc': '',
        'psc': '',
        'txAmt': '',
        'tAmt': payment.amt,
        'pid': payment_id,
        'su': callback_url,
        'fu': callback_url,
    }

    # Make a POST request to the eSewa payment API
    response = requests.post('https://uat.esewa.com.np/epay/main', data=payload)

    # Check the response and return the necessary data to handle the payment process
    if response.status_code == 200:
        # Parse the response data (e.g., extract the token)
        token = ...  # Extract the token from the response
        # Redirect the user to the eSewa payment page using the token
        redirect_url = f'https://uat.esewa.com.np/epay/transrec?pid={payment_id}&scd=epay_payment'
        return redirect_url
    else:
        # Handle the error case
        return None
