from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema, user_schema
from models.tour_booking import TourBooking, tour_bookings_schema
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from controllers.decorator import authorise_as_tourist

tourists_bp = Blueprint('tourists', __name__)

# Tourist route for getting one tourist account (full info access) - account owner only 
@tourists_bp.route('/<int:user_id>')
@jwt_required()
@authorise_as_tourist
def get_one_tourist_account(user_id):
    # Find in the database the user who has id=user_id
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    # If the user exists
    if user:
        # If the user who is currenly logged in is not the account owner, return error message
        if str(user.id) != get_jwt_identity():
            return {'error' : 'Only the account owner can have a full access to the account.'}, 403
        
        # Else, return the user account in the response,
        # excluding description and tours because tourists do not own any tour and need no description
        # excluding password because it should not be returned to the client
        return UserSchema(exclude=['password', 'description', 'tours']).dump(user)
    
    # If the user does not exist, return the error message
    else:
        return {'error' : f'User not found with id {user_id}.'}, 404


# Tourist route for updating a tourist account - account owner only
@tourists_bp.route('/<int:user_id>', methods=['PUT','PATCH'])
@jwt_required()
@authorise_as_tourist
def update_tourist_account(user_id):
    try:
        # Load the data from the request using schema to include data validation
        body_data = user_schema.load(request.get_json(), partial=True)

        # Find in the database the user who has id=user_id
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)

        # If the user exists
        if user:
            # If the user who is currenly logged in is not the account owner, return error message
            if str(user.id) != get_jwt_identity():
                return {'error' : 'Only the account owner can update account.'}, 403
            
            # If the user is the account owner, update the database with data from the request
            user.username = body_data.get('username') or user.username
            if body_data.get('password'):
                user.password=bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8') or user.password
            user.email = body_data.get('email') or user.email
            user.f_name = body_data.get('f_name') or user.f_name
            user.l_name = body_data.get('l_name') or user.l_name
            user.dob = body_data.get('dob') or user.dob
            user.gender = body_data.get('gender') or user.gender
            user.spoken_language = body_data.get('spoken_language') or user.spoken_language
            user.phone = body_data.get('phone') or user.phone
            user.identity_doc_type = body_data.get('identity_doc_type') or user.identity_doc_type
            user.identity_doc_ID = body_data.get('identity_doc_ID') or user.identity_doc_ID
            if body_data.get('is_active') == False:
                user.is_active = False
            else:
                user.is_active = True

            # Commit to the database
            db.session.commit()
            # Return the user account in the response
            return UserSchema(exclude=['password', 'description', 'tours']).dump(user)
        
        # If the user does not exist, return the error message
        else:
            return {'error' : f'User not found with id {user_id}.'}, 404
    
    # Error handling for phone number or identity document ID already in use
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error' : f'The {err.orig.diag.constraint_name} is already in use.'}, 409

 
# Tourist route for getting a tourist's all tour bookings - related tourist only
@tourists_bp.route('<int:user_id>/tourbookings')
@jwt_required()
@authorise_as_tourist
def get_all_tourist_bookings(user_id):
    
    # Find all bookings that belong to the tourist with id=user_id
    stmt = db.select(TourBooking).filter(TourBooking.user_id==user_id)
    bookings = db.session.scalars(stmt)
    
    # If the user who is currenly logged in is not the bookings owner, return error message
    if str(user_id) != get_jwt_identity():
        return {'error': f'Unauthorized to view bookings of user with id {user_id}.'}, 403
    # Else, return the bookings in the response
    return tour_bookings_schema.dump(bookings)

