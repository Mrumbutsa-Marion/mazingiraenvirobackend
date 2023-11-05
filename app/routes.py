# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db = SQLAlchemy(app)

# # Import models
# from models import User, Role, Organization, Donation, Story, Beneficiary, Inventory, Reminder

# # Define routes

# @app.route('/')
# def index():
#     return 'Welcome to the donation platform!'

# # Routes for users
# @app.route('/users', methods=['GET'])
# def get_users():
#     users = User.query.all()
#     result = []
#     for user in users:
#         result.append({
#             'id': user.id,
#             'username': user.username,
#             'email': user.email
#         })
#     return jsonify(result)

# @app.route('/users', methods=['POST'])
# def create_user():
#     data = request.json
#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')

#     if not username or not email or not password:
#         return jsonify({'error': 'Missing required fields'}), 400

#     # Check if the user already exists
#     existing_user = User.query.filter_by(email=email).first()
#     if existing_user:
#         return jsonify({'error': 'User with the provided email already exists'}), 409

#     # Create the user
#     new_user = User(username=username, email=email, password=password)
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'User created successfully'}), 201

# # Routes for organizations
# @app.route('/organizations', methods=['GET'])
# def get_organizations():
#     organizations = Organization.query.all()
#     result = []
#     for organization in organizations:
#         result.append({
#             'id': organization.id,
#             'name': organization.name,
#             'description': organization.description
#         })
#     return jsonify(result)

# @app.route('/organizations', methods=['POST'])
# def create_organization():
#     data = request.json
#     name = data.get('name')
#     description = data.get('description')

#     if not name or not description:
#         return jsonify({'error': 'Missing required fields'}), 400

#     # Create the organization
#     new_organization = Organization(name=name, description=description)
#     db.session.add(new_organization)
#     db.session.commit()

#     return jsonify({'message': 'Organization created successfully'}), 201

# # Routes for donations
# @app.route('/donations', methods=['POST'])
# def create_donation():
#     data = request.json
#     organization_id = data.get('organization_id')
#     amount = data.get('amount')
#     donation_type = data.get('donation_type')
#     anonymous = data.get('anonymous')

#     if not organization_id or not amount or not donation_type:
#         return jsonify({'error': 'Missing required fields'}), 400

#     # Check if the organization exists
#     organization = Organization.query.get(organization_id)
#     if not organization:
#         return jsonify({'error': 'Organization not found'}), 404

#     # Create the donation
#     new_donation = Donation(amount=amount, donation_type=donation_type, anonymous=anonymous)
#     organization.donations.append(new_donation)
#     db.session.commit()

#     return jsonify({'message': 'Donation created successfully'}), 201

# # Routes for stories
# @app.route('/stories', methods=['GET'])
# def get_stories():
#     stories = Story.query.all()
#     result = []
#     for story in stories:
#         result.append({
#             'id': story.id,
#             'title': story.title,
#             'content': story.content
#         })
#     return jsonify(result)

# @app.route('/stories', methods=['POST'])
# def create_story():
#     data = request.json
#     title = data.get('title')
#     content = data.get('content')

#     if not title or not content:
#         return jsonify({'error': 'Missing required fields'}), 400

#     # Create the story
#     new_story = Story(title=title, content=content)
#     db.session.add(new_story)
#     db.session.commit()

#     return jsonify({'message': 'Story created successfully'}), 201

# # Routes for beneficiaries
# @app.route('/beneficiaries', methods=['GET'])
# def get_beneficiaries():
#     beneficiaries = Beneficiary.query.all()
#     result = []
#     for beneficiary in beneficiaries:
#         result.append({
#             'id': beneficiary.id,
#             'name': beneficiary.name,
#             'description': beneficiary.description
#         })
#     return jsonify(result)

# @app.route('/beneficiaries', methods=['POST'])
# def create_beneficiary():
#     data = request.json
#     name = data.get('name')
#     description = data.get('description')

#     if not name or not description:
#         return jsonify({'error': 'Missing required fields'}), 400

# from flask import Flask
# from flask_restful import Api, Resource, reqparse
# from flask_sqlalchemy import SQLAlchemy
# from models import User, Organization, Donation, Story, Beneficiary, Inventory

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db = SQLAlchemy(app)
# api = Api(app)

# class UserResource(Resource):
#     def get(self):
#         users = User.query.all()
#         result = [{
#             'id': user.id,
#             'username': user.username,
#             'email': user.email
#         } for user in users]
#         return result

#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('username', required=True)
#         parser.add_argument('email', required=True)
#         parser.add_argument('password', required=True)
#         data = parser.parse_args()

#         username = data['username']
#         email = data['email']
#         password = data['password']

#         if not username or not email or not password:
#             return {'error': 'Missing required fields'}, 400

#         existing_user = User.query.filter_by(email=email).first()
#         if existing_user:
#             return {'error': 'User with the provided email already exists'}, 409

#         new_user = User(username=username, email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit()

#         return {'message': 'User created successfully'}, 201

# api.add_resource(UserResource, '/users')

# class OrganizationResource(Resource):
#     def get(self):
#         organizations = Organization.query.all()
#         result = [{
#             'id': organization.id,
#             'name': organization.name,
#             'description': organization.description
#         } for organization in organizations]
#         return result

#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('name', required=True)
#         parser.add_argument('description', required=True)
#         data = parser.parse_args()

#         name = data['name']
#         description = data['description']

#         if not name or not description:
#             return {'error': 'Missing required fields'}, 400

#         new_organization = Organization(name=name, description=description)
#         db.session.add(new_organization)
#         db.session.commit()

#         return {'message': 'Organization created successfully'}, 201

# api.add_resource(OrganizationResource, '/organizations')

# class DonationResource(Resource):
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('organization_id', type=int, required=True)
#         parser.add_argument('amount', type=float, required=True)
#         parser.add_argument('donation_type', required=True)
#         parser.add_argument('anonymous', type=bool)
#         data = parser.parse_args()

#         organization_id = data['organization_id']
#         amount = data['amount']
#         donation_type = data['donation_type']
#         anonymous = data['anonymous']

#         if not organization_id or not amount or not donation_type:
#             return {'error': 'Missing required fields'}, 400

#         organization = Organization.query.get(organization_id)
#         if not organization:
#             return {'error': 'Organization not found'}, 404

#         new_donation = Donation(amount=amount, donation_type=donation_type, anonymous=anonymous)
#         organization.donations.append(new_donation)
#         db.session.commit()

#         return {'message': 'Donation created successfully'}, 201

# api.add_resource(DonationResource, '/donations')

# class StoryResource(Resource):
#     def get(self):
#         stories = Story.query.all()
#         result = [{
#             'id': story.id,
#             'title': story.title,
#             'content': story.content
#         } for story in stories]
#         return result

#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('title', required=True)
#         parser.add_argument('content', required=True)
#         data = parser.parse_args()

#         title = data['title']
#         content = data['content']

#         if not title or not content:
#             return {'error': 'Missing required fields'}, 400

#         new_story = Story(title=title, content=content)
#         db.session.add(new_story)
#         db.session.commit()

#         return {'message': 'Story created successfully'}, 201

# api.add_resource(StoryResource, '/stories')

# class BeneficiaryResource(Resource):
#     def get(self):
#         beneficiaries = Beneficiary.query.all()
#         result = [{
#             'id': beneficiary.id,
#             'name': beneficiary.name,
#             'description': beneficiary.description
#         } for beneficiary in beneficiaries]
#         return result

#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('name', required=True)
#         parser.add_argument('description', required=True)
#         data = parser.parse_args()

#         name = data['name']
#         description = data['description']

#         if not name or not description:
#             return {'error': 'Missing required fields'}, 400

#         new_beneficiary = Beneficiary(name=name, description=description)
#         db.session.add(new_beneficiary)
#         db.session.commit()

#         return {'message': 'Beneficiary created successfully'}, 201

# api.add_resource(BeneficiaryResource, '/beneficiaries')

# class InventoryResource(Resource):
#     def get(self):
#         inventories = Inventory.query.all()
#         result = [{
#             'id': inventory.id,
#             'description': inventory.description,
#             'quantity': inventory.quantity
#         } for inventory in inventories]
#         return result

#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('description', required=True)
#         parser.add_argument('quantity', type=int, required=True)
#         data = parser.parse_args()

#         description = data['description']
#         quantity = data['quantity']

#         if not description or not quantity:
#             return {'error': 'Missing required fields'}, 400

#         new_inventory = Inventory(description=description, quantity=quantity)
#         db.session.add(new_inventory)
#         db.session.commit()

#         return {'message': 'Inventory created successfully'}, 201

# api.add_resource(InventoryResource, '/inventories')

# if __name__ == '__main__':
#     app.run()
from flask import Flask, jsonify
from models import db, Story

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mazingira.db'
db.init_app(app)

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

if __name__ == '__main__':
    app.run(debug=True)