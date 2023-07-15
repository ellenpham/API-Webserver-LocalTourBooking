from flask import Blueprint, request
from init import db
from models.tour import Tour, TourSchema, tour_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.decorator import authorise_as_tourguide, admin_user_ID
from controllers.tourbooking_controller import tour_bookings_bp
from controllers.review_controller import reviews_bp
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

tours_bp = Blueprint('tours', __name__, url_prefix='/tours')
tours_bp.register_blueprint(tour_bookings_bp, url_prefix='/<int:tour_id>/tourbookings')
tours_bp.register_blueprint(reviews_bp, url_prefix='/<int:tour_id>/reviews')


# Tour route for getting all tours - all users
@tours_bp.route('/')
def get_all_tours():
    # Fetch all tours from the database
    stmt = db.select(Tour).order_by(Tour.from_date.asc())
    tours = db.session.scalars(stmt)

    # Return all tours in the response, excluding tour booking because this info cannot be publicly disclosed
    return TourSchema(many=True, exclude=['tour_bookings']).dump(tours)

# Tour route for getting one tour - all users
@tours_bp.route('/<int:tour_id>')
def get_one_tour(tour_id):
    # Find the tour with id=tour_id in the database
    stmt = db.select(Tour).filter_by(id=tour_id)
    tour = db.session.scalar(stmt)

    # If the tour exists, return the tour, exluding any related tour bookings
    if tour:
        return TourSchema(exclude=['tour_bookings']).dump(tour)
    # If the tour does not exist, return error message
    else:
        return {'error': f'Tour not found with id {tour_id}'}, 404

# Tour route for searching tour by country (using searching with query strings)
@tours_bp.route('/search')
def search_tours():
    # Find in the database for the tour that has the content of the query string
    stmt = db.select(Tour).filter_by(country=request.args.get('country'))
    tours = db.session.scalars(stmt)

    # Return the tour with queried info in the reponse body
    return TourSchema(many=True, exclude=['tour_bookings']).dump(tours)

# Tour route for creating a tour - tour guide only
@tours_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_as_tourguide
def create_tour():
    # Load data from the request using schema to include data validation
    body_data = tour_schema.load(request.get_json())

    # Create a new Tour model instance with provided data from the request
    tour = Tour(
        country=body_data.get('country'),
        tour_name=body_data.get('tour_name'),
        description=body_data.get('description'),
        from_date=body_data.get('from_date'),
        to_date=body_data.get('to_date'),
        tourist_capacity=body_data.get('tourist_capacity'),
        is_private=body_data.get('is_private'),
        price=body_data.get('price'),
        user_id=get_jwt_identity()
    )

    # Add and commit the new tour to the database
    db.session.add(tour)
    db.session.commit()
    # Return the new tour in the response
    return tour_schema.dump(tour)

# Tour route for updating a tour - tour owner only
@tours_bp.route('/<int:tour_id>', methods=['PUT','PATCH'])
@jwt_required()
def update_one_tour(tour_id):
    # Load data from the request using schema for data validation
    body_data = tour_schema.load(request.get_json(), partial=True)
    # Find the tour with id=tour_id
    stmt = db.select(Tour).filter_by(id=tour_id)
    tour = db.session.scalar(stmt)

    # If the tour exists
    if tour:

        # If the user who is currently logged in is not the tour owner, return the error message
        if str(tour.user_id) != get_jwt_identity():
            return {'error': 'Only the owner of the tour can edit.'}, 403
        
        # Else, get the tour details with the provided data from the request
        tour.country=body_data.get('country') or tour.country
        tour.tour_name=body_data.get('tour_name') or tour.tour_name
        tour.description=body_data.get('description') or tour.description
        tour.from_date=body_data.get('from_date') or tour.from_date
        tour.to_date=body_data.get('to_date') or tour.to_date
        tour.tourist_capacity=body_data.get('tourist_capacity') or tour.tourist_capacity
        tour.is_private=body_data.get('is_private') or tour.is_private
        tour.price=body_data.get('price') or tour.price
        # If the value of is_available is false, update the false value in the database
        if body_data.get('is_available') == False:
            tour.is_available = False
        # Else, update the true value in the database
        else:
            tour.is_available = True

        # Commit the changes
        db.session.commit()
        # # Return the updated tour in the response
        return tour_schema.dump(tour)
    
    # If the tour does not exist, return the error message
    else: 
        return {"error" : f"Tour not found with id {tour_id}"}, 404

# Tour route for deleting a tour - tour owner only
@tours_bp.route('/<int:tour_id>', methods=['DELETE'])
@jwt_required()
def delete_one_tour(tour_id):
    try: 
        # Find the tour with id=tour_id
        stmt = db.select(Tour).filter_by(id=tour_id)
        tour = db.session.scalar(stmt)

        # If the tour exists
        if tour:
            # If the user who is currently logged in is the tour owner or admin user
            if str(tour.user_id) == get_jwt_identity() or get_jwt_identity() == admin_user_ID():
                # Delete the tour and commit to the database
                db.session.delete(tour)
                db.session.commit()
                return {'message' : f'Tour {tour.id} deleted successfully.'}
            # If not the tour owner or admin user, return the error message
            else:
                return {'error': 'Only the owner of the tour can delete.'}, 403
        # If the tour does not exist, return the error message
        else:
            return {"error": f"Tour not found with id {tour_id}."}, 404
        
    # Error handling for integrity error when there is still an existing booking linked to the tour
    except IntegrityError as err: 
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error' : f'The tour can not be deleted as it has been booked. Please cancel the related booking before deleting the tour.'}, 409