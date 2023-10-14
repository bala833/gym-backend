import json
import os
import razorpay
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .constats import PaymentStatus

from payrazor.models import RazorpayPayment

# Get Razorpay Key id and secret for authorizing razorpay client.
# RAZOR_KEY = os.getenv('RAZORPAY_KEY', None)
# RAZOR_SECRET = os.getenv('RAZORPAY_SECRET', None)

RAZOR_KEY = 'rzp_test_XEfwHTjtpjeM4A'
RAZOR_SECRET = 'wMVScYvLNRAusjtamR16vsCQ'

# Creating a Razorpay Client instance.
razorpay_client = razorpay.Client(auth=(RAZOR_KEY, RAZOR_SECRET))


class PaymentView(APIView):
    """
    APIView for Creating Razorpay Order.
    :return: list of all necessary values to open Razorpay SDK
    """

    http_method_names = ('post',)
    permission_classes = ([])

    @staticmethod
    def post(request, *args, **kwargs):

        # Take Order Id from frontend and get all order info from Database.
        # order_id = request.data.get('order_id', None)

        # Here We are Using Static Order Details for Demo.
        # name = "Swapnil Pawar"
        # amount = 10

        data = request.data


        # Create Order
        razorpay_order = razorpay_client.order.create(
            {"amount": int(data['amount']* 100), "currency": "INR", "payment_capture": "1"}
        )

        # Save the order in DB
        order = RazorpayPayment.objects.create(
            name=data['name'], amount=data['amount'], provider_order_id=razorpay_order["id"]
        )

        data = {
            "name" : data['name'],
            "merchantId": RAZOR_KEY,
            "amount": data['amount'],
            "currency" : 'INR' ,
            "orderId" : razorpay_order["id"],
            }

        # save order Details to frontend
        return Response(data, status=status.HTTP_200_OK)

class CallbackView(APIView):
    
    """
    APIView for Verifying Razorpay Order.
    :return: Success and failure response messages
    """
    permission_classes = ([])

    @staticmethod
    def post(request, *args, **kwargs):

        # getting data form request
        response = request.data.dict()

        """
            if razorpay_signature is present in the request 
            it will try to verify
            else throw error_reason
        """
        if "razorpay_signature" in response:

            # Verifying Payment Signature
            data = razorpay_client.utility.verify_payment_signature(response)

            # if we get here True signature
            if data:
                payment_object = RazorpayPayment.objects.get(provider_order_id = response['razorpay_order_id'])                # razorpay_payment = RazorpayPayment.objects.get(order_id=response['razorpay_order_id'])
                payment_object.status = PaymentStatus.SUCCESS
                payment_object.payment_id = response['razorpay_payment_id']
                payment_object.signature_id = response['razorpay_signature']          
                payment_object.save()

                return Response({'status': 'Payment Done'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'Signature Mismatch!'}, status=status.HTTP_400_BAD_REQUEST)

        # Handling failed payments
        else:
            print(response, "error came check")
            error_code = response['error[code]']
            error_description = response['error[description]']
            error_source = response['error[source]']
            error_reason = response['error[reason]']
            error_metadata = json.loads(response['error[metadata]'])
            razorpay_payment =   RazorpayPayment.objects.get(provider_order_id=error_metadata['order_id'])
            razorpay_payment.payment_id = error_metadata['payment_id']
            razorpay_payment.signature_id = "None"
            razorpay_payment.status = PaymentStatus.FAILURE
            razorpay_payment.save()

            error_status = {
                'error_code': error_code,
                'error_description': error_description,
                'error_source': error_source,
                'error_reason': error_reason,
            }

            return Response({'error_data': error_status}, status=status.HTTP_401_UNAUTHORIZED)






            