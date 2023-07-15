from flask import Blueprint
from init import db
from models.user import User, UserSchema
from models.tour import Tour, tours_schema
from controllers.tourist_controller import tourists_bp
from controllers.tourguide_controller import tourguides_bp
from flask_jwt_extended import jwt_required
from controllers.decorator import authorise_as_admin
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

users_bp = Blueprint('users', __name__)
users_bp.register_blueprint(tourists_bp, url_prefix='/tourists')
users_bp.register_blueprint(tourguides_bp, url_prefix='/tourguides')

# User route for getting all users (full info access) - Admin only 
@users_bp.route('/users')
@jwt_required()
@authorise_as_admin
def get_all_users():
    # Fetch all users from the database
    stmt = db.select(User).order_by(User.id.asc())
    users = db.session.scalars(stmt)
    # Return users in the response, excluding passwords
    return UserSchema(many=True, exclude=['password']).dump(users)

# User route for getting one user (full info access) - admin only
@users_bp.route('/users/<int:id>')
@jwt_required()
@authorise_as_admin
def get_one_user(id):
    # Find the user with id=id
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    # If the user exists, return the user in the response
    if user:
        return UserSchema(exclude=['password']).dump(user), 201
    # If the user does not exist, return the error message
    else: 
        return {'error' : f'User not found with id {id}'}, 404

# User route for deleting one user - Admin only
@users_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_one_card(id):
    try:
        # Find the user with id=id
        stmt = db.select(User).filter_by(id=id)
        user = db.session.scalar(stmt)
        # If the user exists, delete the user and commit to database
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': f'User {user.username} has been deleted successfully.'}
        # If the user does not exist, return the error message
        else:
            return {'error' : f'User not found with id {id}'}, 404
        
    # Error handling for integrity error when an existing booking is still linked to the tour
    # which is also linked to a tour guide user
    except IntegrityError as err: 
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error' : f'The user can not be deleted due to an existing related booking. Please cancel the related booking before deleting the user.'}, 409

# Tour route for getting all tours with existing bookings - Admin only
@users_bp.route('/users/tours')
@jwt_required()
@authorise_as_admin
def get_all_tours():
    # Fetch all tours from the database
    stmt = db.select(Tour).order_by(Tour.from_date.asc())
    tours = db.session.scalars(stmt)
    # Return all tours in the response
    return tours_schema.dump(tours)

