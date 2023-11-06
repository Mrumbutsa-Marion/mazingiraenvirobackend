# paypal_routes.py

from flask import Blueprint, request,Flask
from models import Payment,db  # Import your Payment model
#from app import create_app
paypal_bp = Blueprint('paypal', __name__)




app = Flask(__name__)

@paypal_bp.route('/callback', methods=['POST'])
def paypal_callback():
       # Assume you have received the PayPal response in the 'paypal_response' variable
    paypal_response = request.get_json()

    payment = Payment()
    payment.donor_user_id = "<user_id>" # Assign the user ID associated with the payment
    payment.organization_id = "<organization_id>"  # Assign the organization ID
    payment.amount = paypal_response['amount']  
    payment.payment_method = 'PayPal'  # Assuming the payment was made using PayPal
    payment.date = paypal_response['date']  # Extract and assign the payment date
    payment.transaction_id = paypal_response['transaction_id']  # Extract and assign the transaction ID
    payment.status = paypal_response['status']  # Extract and assign the payment status
    payment.is_anonymous = False  # Set the anonymity based on your logic

      # Save the payment details to the database
    db.session.add(payment)
    db.session.commit()

    return "Payment details saved successfully"


@paypal_bp.route('/payment-details', methods=['GET'])
def get_payment_details():
    # Retrieve payment details from the database or any other data source
    payment_details = {
        'donor_user_id': "<user_id>",
        'organization_id': "<organization_id>",
        'amount': 10.0,
        'payment_method': 'PayPal',
        'date': '2023-11-06',
        'transaction_id': '123456789',
        'status': 'Completed',
        'is_anonymous': False
    }

    return jsonify(payment_details)

if __name__ == '__main__':
    app.run()

   
    