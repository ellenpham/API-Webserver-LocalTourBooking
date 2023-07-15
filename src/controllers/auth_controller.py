from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema, user_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Route for user register
@auth_bp.route('/register', methods=['POST'])
def auth_register():
    try:
        # Load data from the request using schema to include data validation
        body_data = user_schema.load(request.get_json())

        # Create a new User model instance from the user info
        # Username, email, password and role_id are required for registration
        user = User() # Instance of the User class
        user.username = body_data.get('username')
        user.email = body_data.get('email')
        user.role_id = body_data.get('role_id')
        if body_data.get('password'):
            user.password=bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        
        # Add new user to database after all input are validated and commit to database
        db.session.add(user)
        db.session.commit()
        
        # If the user registers as tourist (role_id=2)
        # Return to the response body with new registration data, excluding password and tours
        # because tourists have no tour - tours will be nested in tour bookings
        if user.role_id == 2:
            return UserSchema(exclude=['password', 'tours']).dump(user), 201
        
        # If the user registers as tour guide (role_id=3)
        # Return to the response body with new registration data, excluding password and tour bookings
        # because tour guides have no separated tour booking field - tour bookings will be nested in tours 
        elif user.role_id == 3:
            return UserSchema(exclude=['password', 'tour_bookings']).dump(user), 201
    
    # Error handling for unique violation of username or email adress 
    # And not null violation for all required attributes/fields
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error' : 'Username or email address is already in use.'}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error' : f'The {err.orig.diag.column_name} is required for registration.'}, 409

# Route for user login
@auth_bp.route('/login', methods=['POST'])
def auth_login():

    # Load data from the request
    body_data = request.get_json()
    
    # Check users by username
    stmt = db.select(User).filter_by(username=body_data.get('username'))
    user = db.session.scalar(stmt)

    # If username and password are correct, return username and role ID with granted token
    # else return error message for incorrect email or password
    try: 
        if user and bcrypt.check_password_hash(user.password, body_data.get('password')):
            token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
            return {'username' : user.username, 'token' : token, 'role_id' : user.role_id}
        else:
            return {'error' : 'Incorrect email or password. Please check again.'}, 401

    # Error handling for missing field when logging in 
    except Exception:
        return {'error' : f'Invalid request format. Please check again.'}
    