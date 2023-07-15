from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema, otherUserSchema, user_schema
from models.tour import Tour, tours_schema
from models.tour_booking import TourBooking, tour_bookings_schema
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from controllers.decorator import authorise_as_tourguide
from sqlalchemy.sql import and_

tourguides_bp = Blueprint('tourguides', __name__)

# Tour guide route for getting one tour guide account (full info access) - account owner only
@tourguides_bp.route('/<int:user_id>')
@jwt_required()
def get_one_tourguide_account(user_id):
    # Find the user with id=user_id in the database
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
   
    # If the user exists and is active
    if user and user.is_active == True:

        # If the user who is currently logged in is not the tour guide account owner
        if str(user.id) != get_jwt_identity():
            # Return the user account in the response,
            # the otherUserSchema is used for returning the user account in which sensitive data is excluded,
            # excluding tour_bookings because a tour guide does not own any booking
            return otherUserSchema(exclude=['tour_bookings']).dump(user)
        
        # Else, return the account in the response,
        # the UserSchema is used for returning the user account with full info,
        # excluding password because it is already hashed and stored in the database, not supposed to send back to the client
        return UserSchema(exclude=['password','tour_bookings']).dump(user)
    
    # If the user does not exist, return the error message
    else:
        return {'error' : f'User not found with id {user_id}.'}, 404

# Tour guide route for updating a tour guide account - account owner only
@tourguides_bp.route('/<int:user_id>', methods=['PUT','PATCH'])
@jwt_required()
@authorise_as_tourguide
def update_tourguide_account(user_id):
    try:
        # Load data from the request using schema to include data validation 
        body_data = user_schema.load(request.get_json(), partial=True)

        # Find the user with id=user_id
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)

        # If the user exists
        if user:
            # If the user who is currently logged in is not account owner, return the error message
            if str(user.id) != get_jwt_identity():
                return {'error' : 'Only the account owner can update account.'}, 403
            
            # If the user is account owner, update database with the data from the request
            user.username = body_data.get('username') or user.username
            if body_data.get('password'):
                user.password=bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8') or user.password
            user.email = body_data.get('email') or user.email
            user.f_name = body_data.get('f_name') or user.f_name
            user.l_name = body_data.get('l_name') or user.l_name
            user.dob = body_data.get('dob') or user.dob
            user.gender = body_data.get('gender') or user.gender
            user.spoken_language = body_data.get('spoken_language') or user.spoken_language
            user.description = body_data.get('description') or user.description
            user.phone = body_data.get('phone') or user.phone
            user.identity_doc_type = body_data.get('identity_doc_type') or user.identity_doc_type
            user.identity_doc_ID = body_data.get('identity_doc_ID') or user.identity_doc_ID
            if body_data.get('is_active') == False:
                user.is_active = False
            else:
                user.is_active = True

            # Commit to the database
            db.session.commit()
            # Return the updated account in the response
            return UserSchema(exclude=['password','tour_bookings']).dump(user)
        
        # If the user does not exist, return the error message
        else:
            return {'error' : f'User not found with id {user_id}.'}, 404
    
    # Error handling for phone number or identity document ID already in use
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error' : f'The {err.orig.diag.constraint_name} is already in use'}, 409


# Tour guide route for getting all tour guides (limited info access) - Other users
@tourguides_bp.route('/')
@jwt_required()
def get_all_tourguide():
    # Find in the database the user who has role_id=3 (role ID for tour guides) and is active
    stmt = db.select(User).filter_by(role_id=3, is_active=True).order_by(User.username.asc())
    users = db.session.scalars(stmt)
    # Return the users in the response with schema used for limited infor access
    return otherUserSchema(many=True, exclude=['tour_bookings']).dump(users)


# Tour guide route for getting all tours with booking info - Tours owner only
@tourguides_bp.route('/<int:user_id>/tours')
@jwt_required()
@authorise_as_tourguide
def get_all_tourguide_tours(user_id):

    # Find all tours that belong to the tour guide with id=user_id
    stmt = db.select(Tour).filter(Tour.user_id==user_id).order_by(Tour.from_date.asc())
    tours = db.session.scalars(stmt)

    # Check if the tour guide who is currently logged in is the owner of tours
    if str(user_id) != get_jwt_identity():
        # If not, return error message
        return {'error': f'Unauthorized to view all tours info of user with id {user_id}.'}, 403
    # If yes, return tours in the response
    return tours_schema.dump(tours)

# Tour guide route for viewing a tour guides's all tour bookings - related tour guide only
@tourguides_bp.route('/<int:user_id>/tourbookings')
@jwt_required()
@authorise_as_tourguide
def get_all_touguide_bookings(user_id):

    # Find all bookings that link to the tour guide with id=user_id
    stmt = db.select(TourBooking).join(Tour).filter(Tour.user_id==user_id)
    bookings = db.session.scalars(stmt)
    
    # Check if the tour guide who is currently logged in is the owner of tours
    if str(user_id) != get_jwt_identity():
        # If not, return error message
        return {'error': f'Unauthorized to view bookings of user with id {user_id}.'}, 403
    # If yes, return tour bookings in the response
    return tour_bookings_schema.dump(bookings)


# Tour guide route for getting one tourist (limited info access) - Tour guide only
# Only applied to the tourist who has booked the tours of the tour guide
@tourguides_bp.route('/<int:tourguide_id>/<int:tourist_id>')
@jwt_required()
@authorise_as_tourguide
def get_one_tourist(tourguide_id, tourist_id):

    # Find the targeted tourist with id=tourist_id
    user_stmt = db.select(User).filter_by(id=tourist_id)
    user = db.session.scalar(user_stmt)

    # Find the booking of the targeted tourist, which links to the tour guide with id=tourguide_id
    booking_stmt = db.select(TourBooking).join(Tour).join(User).filter(and_(TourBooking.user_id==tourist_id, User.id==tourguide_id))
    booking = db.session.scalar(booking_stmt)

    # If the booking exists
    if booking:
        # If not the tour guide who has the booking that links to the target tourist, return error message
        if str(tourguide_id) != get_jwt_identity():
            return {'error': f'Unauthorized to view tourist account with id {tourist_id}.'}, 403
        
        # If the tour guide has a booking that links to the target tourist
        # Return the tourist account with limitted info
        # return the targeted tourist, excluding tours and tour_bookings
        # because tourists have no tours and they might have bookings of other tours, which should not be all shown up
        return otherUserSchema(exclude=['tours','tour_bookings']).dump(user)
    
    # If the booking does not exist
    else:
        return {'error' : f'User not found with id {tourist_id}.'}, 404


    
