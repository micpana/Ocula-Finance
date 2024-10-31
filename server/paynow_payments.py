import os
from paynow import Paynow
import time
from settings import one_usd_to_zwg

# paynow credentials **********************************************************************************************************************
# USD ***************************************************************************************************************************
usd_integration_id = os.environ.get('PAYNOW_USD_INTEGRATION_ID')
usd_integration_key = os.environ.get('PAYNOW_USD_INTEGRATION_KEY')
# *******************************************************************************************************************************
# ZWG ***************************************************************************************************************************
zwg_integration_id = os.environ.get('PAYNOW_ZWG_INTEGRATION_ID')
zwg_integration_key = os.environ.get('PAYNOW_ZWG_INTEGRATION_KEY')
# *******************************************************************************************************************************
# *****************************************************************************************************************************************

# initiate payment ************************************************************************************************************************
def paynow_payment(purpose, item, user_email, payment_method, payment_phonenumber, amount, currency): # currency -> USD / ZWG
    # integration id
    integration_id = usd_integration_id if currency == 'USD' else zwg_integration_id

    # integration key
    integration_key = usd_integration_key if currency == 'USD' else zwg_integration_key

    # if currency is ZWG, convert USD amount to ZWG
    if currency == 'ZWG': amount = amount * one_usd_to_zwg()

    # create an instance of the Paynow class optionally setting the result and return url(s)
    paynow = Paynow(
        integration_id, # integration id
        integration_key, # integration key
        'https://oculafinance.com',
        'https://oculafinance.com'
    )

    # create a new payment passing in the reference for that payment (e.g invoice id, or anything that you can use to identify the transaction and the user's email address
    payment = paynow.create_payment(purpose, user_email)

    # you can then start adding items to the payment
    payment.add(item, amount)

    # save the response from paynow in a variable
    response = paynow.send_mobile(payment, payment_phonenumber, payment_method) # only ecocash and onemoney are supported

    # transaction initiation status
    transaction_initiation_successful = response.success

    if transaction_initiation_successful == True:
        # get the poll url (used to check the status of a transaction). You might want to save this in your DB
        poll_url = response.poll_url
        # get the instructons
        instructions = response.instructions
    else:
        # set poll url to None
        poll_url = None
        # set instructions to None
        instructions = None

    # return transaction_initiation_successful and poll_url
    return transaction_initiation_successful, poll_url
# *****************************************************************************************************************************************

# check transaction status, only to be called if a the transaction was initiated successfully *********************************************
def paynow_status(poll_url, currency):
    # integration id
    integration_id = usd_integration_id if currency == 'USD' else zwg_integration_id

    # integration key
    integration_key = usd_integration_key if currency == 'USD' else zwg_integration_key

    # create an instance of the Paynow class optionally setting the result and return url(s)
    paynow = Paynow(
        integration_id, # integration id
        integration_key, # integration key
        'https://oculafinance.com',
        'https://oculafinance.com'
    )

    # check the status of the transaction with the specified poll url ... now you see why you need to save that url ;-)
    status = paynow.check_transaction_status(poll_url)

    if status.paid :
        # Yay! Transaction was paid for. Update transaction?
        print('Paid')
    else :
        # Handle that
        print('Not paid')

    # payments status ... sent / paid / cancelled
    payment_status = status.status

    # return payment status
    return payment_status
# *****************************************************************************************************************************************

# testing (to be commented out after testing) *********************************************************************************************
# currency = 'USD'
# amount = 10.00
# if currency == 'ZWG': amount = amount * one_usd_to_zwg()
# transaction_initiation_successful, poll_url = paynow_payment(
#     'Subscription', # purpose
#     'MonthlyPackage', # item
#     'michaelmudimbu@gmail.com', # user email ... use account email for sandbox tests
#     'ecocash', # payment method
#     '0782464219', # payment phonenumber ... for sandbox tests, use phonenumbers on https://developers.paynow.co.zw/docs/test_mode.html
#     amount, # amount
#     currency # currency ... USD / ZWG
# )
# print('Transaction initiated successfully:', transaction_initiation_successful, '| Poll url:', poll_url)
# if transaction_initiation_successful == True:
#     time.sleep(60)
#     payment_status = paynow_status(poll_url, currency)
#     print('Payment status:', payment_status)
# *****************************************************************************************************************************************