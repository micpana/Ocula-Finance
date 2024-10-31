import os
import requests
import json
import time
from pytz import timezone
from datetime import datetime
from settings import platform_name

# oxapay credentials **********************************************************************************************************************
oxapay_merchant_api_key = os.environ.get('OXAPAY_MERCHANT_API_KEY')
# *****************************************************************************************************************************************

# initiate payment ************************************************************************************************************************
def oxapay_payment(amount, description, order_id, user_email):
    url = 'https://api.oxapay.com/merchants/request'
    data = {
        'merchant': oxapay_merchant_api_key, # api key
        'amount': amount, # amount to be paid
        'currency': 'USD', # currency symbol, for the invoice to be calculated in a specific currency
        'lifeTime': 15, # expiration time for the payment link, in minutes
        'feePaidByPayer': 0, # 0 merchant, 1 payer
        'underPaidCover': 2.5, # accepted % difference between the requested and paid amount
        'callbackUrl': '', # url where payment information will be sent
        'returnUrl': 'https://oculafinance.com/dashboard', # url where the payer will be redirected after a successful payment
        'description': description, # description / order details
        'orderId': order_id, # unique order id for system reference
        'email': user_email # payer's email for reporting purposes
    }

    response = requests.post(url, data=json.dumps(data))
    response_json = response.json()
    print(response_json)

    # result code ... indicates the outcome of the request
    result = response_json['result']
    # message ... contains additional information about the result of the request
    message = response_json['message']
    # track id ... unique identifier for the payment session in the OxaPay payment gateway
    track_id = response_json['trackId']
    # paylink ... payment page link associated with the generated track ID
    paylink = response_json['payLink']

    # transaction initiation status
    if result == 100: # successful operation
        transaction_initiation_successful = True
    else:
        transaction_initiation_successful = False

    # return transaction_initiation_successful, track_id and paylink
    return transaction_initiation_successful , track_id, paylink
# *****************************************************************************************************************************************

# check transaction status, only to be called if the transaction was initiated successfully ***********************************************
def oxapay_status(track_id):
    url = 'https://api.oxapay.com/merchants/inquiry'
    data = {
        'merchant': oxapay_merchant_api_key,
        'trackId': track_id
    }
    response = requests.post(url, data=json.dumps(data))
    response_json = response.json()
    print(response_json)

    # result ... result code indicates the success or failure of the request
    result = response_json['result']
    # message ... message providing additional information about the result
    message = response_json['message']
    # status ... current status of the payment (e.g., \"New,\" \"Waiting,\" \"Confirming,\" \"Paid,\" \"Expired,\" etc.)
    status = response_json['status']
    # network ... blockchain network on which the payment was made
    if status == 'Paid': network = response_json['network']
    else: network = None

    # transaction status check status
    if result == 100: # successful operation
        transaction_status_check_successful = True
    else:
        transaction_status_check_successful = False

    # return transaction_status_check_successful, status, and network
    return transaction_status_check_successful, status, network
# *****************************************************************************************************************************************

# testing (to be commented out after testing) *********************************************************************************************
# transaction_initiation_successful, track_id, paylink = oxapay_payment(
#     10.00, # amount
#     'Monthly Subscription', # description
#     'michaelmudimbu@gmail.com-73828723', # order id
#     'michaelmudimbu@gmail.com' # user email
# )
# print('Transaction initiated successfully:', transaction_initiation_successful, '| Track ID:', track_id, '| Paylink:', paylink)
# if transaction_initiation_successful == True:
#     time.sleep(10)
#     transaction_status_check_successful, status, network = oxapay_status(track_id)
#     print('Transaction status check successful:', transaction_status_check_successful, '| Payment status:', status, '| Blockchain network:', network)
# *****************************************************************************************************************************************