from flask import Flask, request, jsonify,Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from models import db, User, Role, Story, Donation, Beneficiary, Organization, Inventory, Reminder
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import secrets
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime
import paypalrestsdk
from paypalrestsdk import Payment

def create_app():

    app = Flask(__name__)
    

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mazingira.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    #swagger configs
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Mazingira Application"
    }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


    db.init_app(app)
    migrate = Migrate(app, db)

    CORS(app)

    secret_key = secrets.token_hex(16)
    app.config['SECRET_KEY'] = secret_key

    return app

app = create_app()

# Define a WTForms class for user signup
class SignupForm(FlaskForm):
    user_name = StringField('user_name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

# Define a WTForms class for user login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

@app.route('/')
def home():
    return "Welcome to my app"

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json

    user_name = data.get('user_name')
    email = data.get('email')
    password = data.get('password')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User with this email already exists'}), 409

    hashed_password = generate_password_hash(password)

    new_user = User(user_name=user_name, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful'})

# Organizations
@app.route('/organizations', methods=['GET'])
def get_organizations():
    organizations = Organization.query.all()

    organization_data = [
        {
            "id": organization.id,
            "image_url": organization.image_url,
            "name": organization.name,
            "description": organization.description,
            "contact_information": organization.contact_information,
            "status": organization.status,
            "isAdminApproved": organization.isAdminApproved
        }
        for organization in organizations
    ]

    return jsonify(organization_data)

@app.route('/organizations/<int:organization_id>', methods=['GET'])
def get_organization(organization_id):
    organization = Organization.query.get(organization_id)

    if organization is None:
        return jsonify({"error": "Organization not found"}), 404

    organization_data = {
        "id": organization.id,
        "image_url": organization.image_url,
        "name": organization.name,
        "description": organization.description,
        "contact_information": organization.contact_information,
        "status": organization.status,
        "isAdminApproved": organization.isAdminApproved
    }

    return jsonify(organization_data)
@app.route('/stories', methods=['GET'])
def get_stories():
    stories = Story.query.all()
    serialized_stories = []
    for story in stories:
        serialized_story = {
            'organization_id': story.organization_id,
            'title': story.title,
            'content': story.content,
            'images': story.images,
            'date_created': story.date_created.isoformat()
        }
        serialized_stories.append(serialized_story)
    return jsonify(serialized_stories)

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": "AXr0WUl_Ss7nwdTPK5VWRa3lju-Yq1AN7KYQjnjefMrLugfR123C6dqDHUXZcoZnJskjb772FQWF8knc",
    "client_secret": "EFfQwjU9_3CJn75_dbaMVZPalhVlgPqoqpRESMO5I7bQW3rsp8byQx6Vq4K4EDGjIH_TMAQ67zYnm_hw"
})
@app.route('/callback', methods=['POST'])
def create_payment():
       
    payment_data = request.get_json()
    # Create a new payment instance using the PayPal SDK
    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": str(payment_data['amount']),
                "currency": "USD" 
            }
        }],
        "redirect_urls": {
            "return_url": "http://example.com/return",
            "cancel_url": "http://example.com/cancel"
        }
    })

    # Create the payment using the PayPal SDK
    if payment.create():
        # Save the payment details to the database
        payment_model = Payment()
        payment_model.donor_user_id = payment_data['donor_user_id']
        payment_model.organization_id = payment_data['organization_id']
        payment_model.amount = payment_data['amount']
        payment_model.payment_method = "PayPal"
        payment_model.date = datetime.utcnow()
        payment_model.transaction_id = payment['id']
        payment_model.status = payment['state']
        payment_model.is_anonymous = payment_data['is_anonymous']

        db.session.add(payment_model)
        db.session.commit()

        return "Payment created successfully"
    else:
        return "Payment creation failed"





@app.route('/payment-details', methods=['GET'])
def get_payment_details():
    # Retrieve payment details from the database 
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
    app.run(port=5003, debug=True)