from flask import Blueprint, request
from init import db
from models.tour import Tour
from models.tour_booking import TourBooking, tour_booking_schema
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.decorator import authorise_as_tourist, admin_user_ID
from sqlalchemy.sql import and_

tour_bookings_bp=Blueprint('tour_bookings', __name__)

# Tour booking route for viewing a tour booking - tour booking owner and tour owner only
@tour_bookings_bp.route('/<int:booking_id>')
@jwt_required()
def get_one_tourbooking(tour_id, booking_id):

    # Find the tour with id=tour_id
    tour_stmt = db.select(Tour).filter_by(id=tour_id)
    tour = db.session.scalar(tour_stmt)

    # Find the booking that links to the tour, matching it with booking_id 
    booking_stmt = db.select(TourBooking).join(Tour).filter(and_(TourBooking.id==booking_id, Tour.id==tour_id))
    tour_booking = db.session.scalar(booking_stmt)
    
    # If the tour and related tour booking exist
    # Only the tourist and tour guide involved in this tour booking can view the booking
    if tour and tour_booking:
        if str(tour_booking.user_id) == get_jwt_identity() or str(tour.user_id) == get_jwt_identity():

            # If no conflicts with authorised users,
            # and the tour has matching booking with id=booking id, return the booking in the response
            return tour_booking_schema.dump(tour_booking)
        
        # If unauthorised users, return the error message
        else:
            return {'error': 'Only the tourist and tour guide relating to this tour booking can view.'}, 403
    
    # If the tour and related tour booking does not exist, return the error message
    else: 
        return {'error' : f'Tour not found with id {tour_id} or Tour booking not found with id {booking_id}.'}, 404


# Tour booking route for creating a tour booking - tourist only
@tour_bookings_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_as_tourist
def create_tourbooking(tour_id):
    # Load booking data from the request using schema to include data validation
    body_data = tour_booking_schema.load(request.get_json())

    # Find the tour with id=tour_id
    tour_stmt = db.select(Tour).filter_by(id=tour_id)
    tour = db.session.scalar(tour_stmt)

    # Check the user who is currently logged in 
    # and match with user who has a current booking linked to the tour with id=tour_id
    current_user_id = get_jwt_identity()
    user_stmt = db.select(User).join(TourBooking).join(Tour).filter(and_(TourBooking.user_id==current_user_id, Tour.id==tour_id))
    user = db.session.scalar(user_stmt)

    # If the tour exists and is available
    if tour and tour.is_available == True:

        # Preventing booking duplicates by checking
        # if the current user already had a booking linked to the tour, return the error message
        if user:
            return {'error' : f'You have existing booking with tour of id {tour_id}.'}, 409
        
        # If no existing booking, create a new Booking model instance with data passed in from the request
        tour_booking = TourBooking(
            tourist_number=body_data.get('tourist_number'),
            preferred_language=body_data.get('preferred_language'),
            extra_request=body_data.get('extra_request'),
            user_id = get_jwt_identity(),
            tour=tour 
        )

        # Add and commit new booking to the database
        db.session.add(tour_booking)
        db.session.commit()

        # Return the new booking in the response
        return tour_booking_schema.dump(tour_booking), 201
    
    # If tour does not exist or unavailable, return the error message
    else:
        return {'error' : f'Tour not found with id {tour_id}.'}, 404


# Tour booking route for updating a tour booking - tour booking owner only
@tour_bookings_bp.route('/<int:booking_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_booking(tour_id, booking_id):
    # Load booking data from the request using schema to include data validation
    body_data = tour_booking_schema.load(request.get_json(), partial=True)

    # Find the tour with id=tour_id
    tour_stmt = db.select(Tour).filter_by(id=tour_id)
    tour = db.session.scalar(tour_stmt)

    # Find the booking that links to the tour, matching it with booking_id 
    booking_stmt = db.select(TourBooking).join(Tour).filter(and_(TourBooking.id==booking_id, Tour.id==tour_id))
    tour_booking = db.session.scalar(booking_stmt)

    # If the tour and related tour booking exists
    if tour and tour_booking:
        # Check if the user who is currently logged in is the booking owner
        if str(tour_booking.user_id) != get_jwt_identity():
            # If not, return the error message
            return {'error': 'Only the owner of the tour booking can edit.'}, 403
        
        # If it is the booking owner, update the database with the new data from the request
        tour_booking.tourist_number=body_data.get('tourist_number') or tour_booking.tourist_number
        tour_booking.preferred_language=body_data.get('preferred_language') or tour_booking.preferred_language
        tour_booking.extra_request=body_data.get('extra_request') or tour_booking.extra_request

        # Commit to the database
        db.session.commit()
        # Return the updated booking in the response
        return tour_booking_schema.dump(tour_booking)
    
    # If the tour has no matching tour booking with id=booking_id, return the error message
    else:
        return {'error' : f'Tour not found with id {tour_id} or Tour booking not found with id {booking_id}.'}, 404

# Tour booking route for deleting a tour booking - tourist only
@tour_bookings_bp.route('/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def delete_one_booking(tour_id, booking_id):

    # Find the tour with id=tour_id
    tour_stmt = db.select(Tour).filter_by(id=tour_id)
    tour = db.session.scalar(tour_stmt)

    # Find the booking that links to the tour, matching it with booking_id 
    booking_stmt = db.select(TourBooking).join(Tour).filter(and_(TourBooking.id==booking_id, Tour.id==tour_id))
    tour_booking = db.session.scalar(booking_stmt)

    # If the tour and related tour booking exist
    if tour and tour_booking:

        # Check if the user who is currently logged in is the booking owner or admin user
        if str(tour_booking.user_id) == get_jwt_identity() or get_jwt_identity() == admin_user_ID():
            # If yes, delete the booking and commit to database
            db.session.delete(tour_booking)
            db.session.commit()
            return {'message' : f'Tour booking {tour_booking.id} deleted successfully.'}
        # If not, return the error message
        else:
            return {'error': 'Only the owner of the tour booking can delete.'}, 403

    # If the tour has no matching tour booking with id=booking_id, return the error message
    else:
        return {'error' : f'Tour not found with id {tour_id} or Tour booking not found with id {booking_id}.'}, 404