from flask import Flask, request, jsonify, abort
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

if __name__ == '__main__':
    app.run(port=5003, debug=True)