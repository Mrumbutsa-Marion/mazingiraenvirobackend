# paypal_routes.py
from datetime import datetime
from flask import Blueprint, request,Flask,jsonify
from models import Payment,db  # Import your Payment model
#from app import create_app
paypal_bp = Blueprint('paypal', __name__)




app = Flask(__name__)

@paypal_bp.route('/callback', methods=['POST'])
def paypal_callback():
       # Assume you have received the PayPal response in the 'paypal_response' variable
    paypal_response = request.get_json()

    payment = Payment()
    payment.donor_user_id = "<user_id>" # Assign the user ID 
    payment.organization_id = "<organization_id>"  # Assign the organization ID
    payment.amount = paypal_response['amount']  
    payment.payment_method = 'PayPal'  
    payment.date = paypal_response['date']  
    payment.transaction_id = paypal_response['transaction_id']  
    payment.status = paypal_response['status']  
    payment.is_anonymous = False  # Set the anonymity based on your logic

      # Save the payment details to the database
    db.session.add(payment)
    db.session.commit()

    return "Payment details saved successfully"


@paypal_bp.route('/payment-details', methods=['GET'])
def get_payment_details():
    # Retrieve payment details from the database or any other data source
    payment_details = [
    {
        "donor_user_id": 1,
        "organization_id": 1,
        "amount": 100.00,
        "payment_method": "Credit Card",
        "date": datetime.utcnow(),
        "transaction_id": "ABC123",
        "status": "success",
        "is_anonymous": False
    },
    {
        "donor_user_id": 2,
        "organization_id": 2,
        "amount": 50.00,
        "payment_method": "PayPal",
        "date": datetime.utcnow(),
        "transaction_id": "456",
        "status": "pending",
        "is_anonymous": True
    },
    {
        "donor_user_id": 3,
        "organization_id": 3,
        "amount": 200.00,
        "payment_method": "Bank Transfer",
        "date": datetime.utcnow(),
        "transaction_id": "GHI79",
        "status": "failed",
        "is_anonymous": False
    },
    {
        "donor_user_id": 4,
        "organization_id": 4,
        "amount": 75.00,
        "payment_method": "Credit Card",
        "date": datetime.utcnow(),
        "transaction_id": "JK012",
        "status": "success",
        "is_anonymous": False
    },
    {
        "donor_user_id": 5,
        "organization_id": 5,
        "amount": 150.00,
        "payment_method": "PayPal",
        "date": datetime.utcnow(),
        "transaction_id": "MN345",
        "status": "success",
        "is_anonymous": True
    },
    {
        "donor_user_id": 6,
        "organization_id": 1,
        "amount": 75.00,
        "payment_method": "Credit Card",
        "date": datetime.utcnow(),
        "transaction_id": "PQR68",
        "status": "success",
        "is_anonymous": False
    },
    {
        "donor_user_id": 7,
        "organization_id": 2,
        "amount": 100.00,
        "payment_method": "PayPal",
        "date": datetime.utcnow(),
        "transaction_id": "STU01",
        "status": "success",
        "is_anonymous": True
    },
    {
        "donor_user_id": 8,
        "organization_id": 5,
        "amount": 50.00,
        "payment_method": "Bank Transfer",
        "date": datetime.utcnow(),
        "transaction_id": "VWX34",
        "status": "pending",
        "is_anonymous": False
    },
    {
        "donor_user_id": 9,
        "organization_id": 6,
        "amount": 200.00,
        "payment_method": "Credit Card",
        "date": datetime.utcnow(),
        "transaction_id": "YZ567",
        "status": "failed",
        "is_anonymous": False
    },
    {
        "donor_user_id": 10,
        "organization_id": 7,
        "amount": 150.00,
        "payment_method": "PayPal",
        "date": datetime.utcnow(),
        "transaction_id": "BC890",
        "status": "success",
        "is_anonymous": True
    },
    {
        "donor_user_id": 11,
        "organization_id": 8,
        "amount": 80.00,
        "payment_method": "Credit Card",
        "date": datetime.utcnow(),
        "transaction_id": "EFG",
        "status": "success",
        "is_anonymous": False
    }

]
    return jsonify(payment_details)

if __name__ == '__main__':
    app.run()

   
    