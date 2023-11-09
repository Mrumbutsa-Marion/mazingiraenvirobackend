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
from flask_login import current_user
from flask_admin import AdminIndexView, Admin, expose
from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime
import paypalrestsdk
from paypalrestsdk import Payment



def create_app():

    app = Flask(__name__)
    

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///environment.db'
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

    class MyAdminIndexView(AdminIndexView):
        @expose("/")
        def index(self):
         return super(MyAdminIndexView,self).index()
        
        

    admin = Admin(app, name='Mazingira', template_mode='bootstrap4', index_view=MyAdminIndexView(
    name="Dashboard", menu_icon_type="fa", menu_icon_value="fa-dashboard"
    ))

    class OrganizationAdminView(ModelView):
        column_list = ('name', 'description', 'contact_information', 'status', 'isAdminApproved')
        form_columns = ('name', 'description', 'contact_information', 'status', 'isAdminApproved')
        column_searchable_list = ('name', 'description')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    class ReviewAdminView(ModelView):
        column_list = ('id', 'name', 'description', 'contact_information', 'image_url', 'status')
        can_edit = False
        can_create = False
        column_filters = ['status', 'isAdminApproved']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    class ApprovalAdminView(ModelView):
       def on_model_change(self, form, model, is_created):
        if is_created:
            model.status = 'Approved'
            model.isAdminApproved = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    class RejectionAdminView(ModelView):
       def on_model_change(self, form, model, is_created):
        if is_created:
            model.status = 'Rejected'

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()


    # Add Flask-Admin views for the models
    admin.add_view(ModelView(User, db.session, name="Users", menu_icon_type="fa", menu_icon_value="fa-solid fa-users"))
    admin.add_view(ModelView(Role, db.session, menu_icon_type="fa", menu_icon_value="fa-solid fa-user-tie"))
    admin.add_view(ModelView(Story, db.session))
    admin.add_view(ModelView(Donation, db.session, menu_icon_type="fa", menu_icon_value="fa-solid fa-circle-dollar-to-slot"))
    admin.add_view(ModelView(Beneficiary, db.session, menu_icon_type="fa", menu_icon_value="fa-solid fa-hands-holding-child"))
    admin.add_view(ModelView(Organization, db.session, menu_icon_type="fa", menu_icon_value="fa-solid fa-database"))
    admin.add_view(ReviewAdminView(Organization, db.session, name='Applications', endpoint='review_applications', category="Applications"))
    admin.add_view(ApprovalAdminView(Organization, db.session, name='Approve', endpoint='approve_application', category="Applications"))
    admin.add_view(RejectionAdminView(Organization, db.session, name='Reject', endpoint='reject_application', category="Applications"))
    admin.add_view(ModelView(Inventory, db.session, menu_icon_type="fa", menu_icon_value="fa-solid fa-tree"))
    admin.add_view(ModelView(Reminder, db.session))
  


   


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
    role_name = data.get('role')  # Extract the role from the request data

    if not user_name:
        return jsonify({'message': 'User name is required'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User with this email already exists'}), 409

    hashed_password = generate_password_hash(password)

    # Check if the provided role exists in the database
    role = Role.query.filter_by(name=role_name).first()

    if not role:
        role = Role(name=role_name)
        db.session.add(role)
        db.session.commit()

        return jsonify({'message': 'Role not found'}), 404

    new_user = User(user_name=user_name, email=email, password=hashed_password, role_id=role.id)

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

@app.route('/organizations/<int:org_id>', methods=['DELETE'])
def delete_organization(org_id):
    organization = Organization.query.get(org_id)
    if organization is None:
        return jsonify({'error': 'Organization not found'}), 404

    try:
        db.session.delete(organization)
        db.session.commit()
        return jsonify({'message': 'Organization deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Unable to delete organization', 'details': str(e)}), 500


#-------------------routes for organisattion application-------------------
@app.route('/apply', methods=['POST'])
def apply():
     data = request.json
     new_organization = Organization(
        name=data.get('name'),
        description=data.get('description'),
        contact_information=data.get('contact_information'),
        image_url=data.get('image_url'),
        status='Pending',
        isAdminApproved=False
     )
     db.session.add(new_organization)
     db.session.commit()
     return jsonify({"message": "Application submitted successfully!"}), 201

@app.route('/admin/review', methods=['GET'])
def review_applications():
    pending_orgs = Organization.query.filter_by(isAdminApproved=False).all()
    pending_orgs_json = [
        {
            'id': org.id,
            'name': org.name,
            'description': org.description,
            'contact_information': org.contact_information,
            'image_url': org.image_url,
            'status': org.status
        } for org in pending_orgs
    ]
    return jsonify(pending_orgs_json)

@app.route('/admin/approve/<int:org_id>', methods=['POST'])
def approve_application(org_id):
    org = Organization.query.get_or_404(org_id)
    org.status = 'Approved'
    org.isAdminApproved = True
    db.session.commit()
    return jsonify({"message": "Organization approved successfully!"}), 200

@app.route('/admin/reject/<int:org_id>', methods=['POST'])
def reject_application(org_id):
    org = Organization.query.get_or_404(org_id)
    org.status = 'Rejected'
    db.session.commit()
    return jsonify({"message": "Organization rejected successfully!"}), 200
   

#----------------------------------------------------------------------------------------

        #donations

@app.route('/donations', methods=['GET']) #admin and organization
def get_donations():
    organization_id = request.args.get('organization_id')
    if organization_id:
        donations = Donation.query.filter_by(organization_id=organization_id).all()
    else:
        donations = Donation.query.all()
    donations_list = [{
        'id': donation.id,
        'donor_user_id': donation.donor_user_id,
        'organization_id': donation.organization_id,
        'amount': str(donation.amount),
        'donation_type': donation.donation_type,
        'anonymous': donation.anonymous,
        'date': donation.date.isoformat(),
        'transaction_id': donation.transaction_id
    } for donation in donations]
    return jsonify(donations_list), 200


@app.route('/donations/<int:donation_id>', methods=['GET']) 
def get_donation(donation_id):
    donation = Donation.query.get_or_404(donation_id, description="Donation not found")
    donation_dict = {
        'id': donation.id,
        'donor_user_id': donation.donor_user_id,
        'organization_id': donation.organization_id,
        'amount': str(donation.amount),
        'donation_type': donation.donation_type,
        'anonymous': donation.anonymous,
        'date': donation.date.isoformat(),
        'transaction_id': donation.transaction_id
    }
    return jsonify(donation_dict), 200


@app.route('/donations/<int:donation_id>', methods=['PUT']) #admin only
def update_donation(donation_id):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    donation = Donation.query.get(donation_id)
    if not donation:
        abort(404, description="Donation not found")
    
    data = request.get_json()
    
    donation.amount = data.get('amount', donation.amount)
    donation.donation_type = data.get('donation_type', donation.donation_type)
    donation.anonymous = data.get('anonymous', donation.anonymous)

    if 'date' in data:
        try:
            donation.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            abort(400, description="Invalid date format. Please use 'YYYY-MM-DD' format.")

    try:
        db.session.commit()
        return jsonify(donation.repr()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500

@app.route('/donations/<int:donation_id>', methods=['DELETE']) #admin only
def delete_donation(donation_id):
    donation = Donation.query.get_or_404(donation_id, description="Donation not found")
    db.session.delete(donation)
    db.session.commit()
    return jsonify({'message': 'Donation deleted successfully'}), 200

    #beneficiaries
@app.route('/beneficiaries', methods=['GET']) #admin and organization
def get_beneficiaries():
    beneficiaries = Beneficiary.query.all()
    beneficiaries_list = [{
        'id': beneficiary.id,
        'organization_id': beneficiary.organization_id,
        'name': beneficiary.name,
        'description': beneficiary.description,
        'inventory_received': beneficiary.inventory_received
    } for beneficiary in beneficiaries]

    return jsonify(beneficiaries_list), 200

@app.route('/beneficiaries/<int:beneficiary_id>', methods=['GET']) #admin and organization
def get_beneficiary(beneficiary_id):
    beneficiary = Beneficiary.query.get_or_404(beneficiary_id)
    beneficiary_data = {
        'id': beneficiary.id,
        'organization_id': beneficiary.organization_id,
        'name': beneficiary.name,
        'description': beneficiary.description,
        'inventory_received': beneficiary.inventory_received
    }

    return jsonify(beneficiary_data), 200    

@app.route('/beneficiaries', methods=['POST']) #organisation only
def create_beneficiary():
    data = request.json
    organization_id = data.get('organization_id')

    if not organization_id or not isinstance(organization_id, int):
        return jsonify({'error': 'Invalid organization_id'}), 400

    organization = Organization.query.get(organization_id)
    if not organization:
        return jsonify({'error': 'Organization not found'}), 404

    beneficiary = Beneficiary(
        organization_id=organization_id,
        name=data.get('name'),
        description=data.get('description'),
        inventory_received=data.get('inventory_received')
    )

    db.session.add(beneficiary)
    try:
        db.session.commit()
        return jsonify({'beneficiary_id': beneficiary.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/beneficiaries/<int:beneficiary_id>', methods=['PUT']) #organisation only
def update_beneficiary(beneficiary_id):
    data = request.json
    beneficiary = Beneficiary.query.get(beneficiary_id)

    if not beneficiary:
        return jsonify({'error': 'Beneficiary not found'}), 404

    organization_id = data.get('organization_id')
    if organization_id:
        organization = Organization.query.get(organization_id)
        if not organization:
            return jsonify({'error': 'Organization not found'}), 404
        beneficiary.organization_id = organization_id

    name = data.get('name')
    if name:
        beneficiary.name = name

    description = data.get('description')
    if description:
        beneficiary.description = description

    inventory_received = data.get('inventory_received')
    if inventory_received:
        beneficiary.inventory_received = inventory_received

    try:
        db.session.commit()
        return jsonify({'message': 'Beneficiary updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


    

@app.route('/beneficiaries/<int:beneficiary_id>', methods=['DELETE']) #organisation only
def delete_beneficiary(beneficiary_id):
    beneficiary = Beneficiary.query.get_or_404(beneficiary_id)
    db.session.delete(beneficiary)
    db.session.commit()

    return jsonify({'message': 'Beneficiary deleted successfully'}), 200    
 
 #inventory routes
@app.route('/inventory', methods=['GET'])
def get_inventory():
    inventory_items = Inventory.query.all()
    return jsonify([{
        'id': item.id,
        'beneficiary_id': item.beneficiary_id,
        'description': item.description,
        'quantity': item.quantity,
        'date_received': item.date_received.strftime('%Y-%m-%d')
    } for item in inventory_items]), 200  
  
@app.route('/inventory/<int:inventory_id>', methods=['GET'])
def get_inventory_item(inventory_id):
    inventory_item = Inventory.query.get_or_404(inventory_id)
    return jsonify({
        'id': inventory_item.id,
        'beneficiary_id': inventory_item.beneficiary_id,
        'description': inventory_item.description,
        'quantity': inventory_item.quantity,
        'date_received': inventory_item.date_received.strftime('%Y-%m-%d')
    }), 200

@app.route('/inventory', methods=['POST'])
def add_inventory():
    new_inventory = Inventory(
        beneficiary_id=request.json['beneficiary_id'],
        description=request.json['description'],
        quantity=request.json['quantity'],
        date_received=datetime.strptime(request.json['date_received'], '%Y-%m-%d') if request.json.get('date_received') else datetime.utcnow()
    )
    db.session.add(new_inventory)
    db.session.commit()
    return jsonify(new_inventory.id), 201

@app.route('/inventory/<int:inventory_id>', methods=['PUT'])
def update_inventory(inventory_id):
    inventory_item = Inventory.query.get_or_404(inventory_id)
    data = request.json
    if 'description' in data:
        inventory_item.description = data['description']
    if 'quantity' in data:
        inventory_item.quantity = data['quantity']
    if 'date_received' in data:
        inventory_item.date_received = datetime.strptime(data['date_received'], '%Y-%m-%d')
    
    db.session.commit()
    return jsonify({
        'id': inventory_item.id,
        'beneficiary_id': inventory_item.beneficiary_id,
        'description': inventory_item.description,
        'quantity': inventory_item.quantity,
        'date_received': inventory_item.date_received.strftime('%Y-%m-%d')
    }), 200

@app.route('/inventory/<int:inventory_id>', methods=['DELETE'])
def delete_inventory(inventory_id):
    inventory_item = Inventory.query.get_or_404(inventory_id)
    db.session.delete(inventory_item)
    db.session.commit()
    return jsonify({'message': 'Inventory deleted'}), 200

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
    app.run(port=5001, debug=True)