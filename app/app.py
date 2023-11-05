from flask import Flask, request, jsonify
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


if __name__ == '__main__':
    app.run(port=5003, debug=True)