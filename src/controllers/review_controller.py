from flask import Blueprint, request
from init import db
from models.tour import Tour
from models.review import Review, review_schema, reviews_schema
from models.user import User
from models.tour_booking import TourBooking
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.decorator import authorise_as_tourist, admin_user_ID
from datetime import date
from sqlalchemy.sql import and_

reviews_bp = Blueprint('reviews', __name__)

# Review route for getting all reviews of a tour
@reviews_bp.route('/')
def get_all_reviews():
    # Fetch all reviews in the database
    stmt = db.select(Review).order_by(Review.date_created.asc())
    reviews = db.session.scalars(stmt)
    # Return all tours in the reponse
    return reviews_schema.dump(reviews)

# Review route for posting a review - tourist only
# Only the tourist who has booke the tour can review
@reviews_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_as_tourist
def create_review(tour_id):
    # Load review data from the request using schema to include data validation
    body_data = review_schema.load(request.get_json())

    # Find tour with id=tour_id
    tour_stmt = db.select(Tour).filter_by(id=tour_id)
    tour = db.session.scalar(tour_stmt)

    # Check the user who is currently logged in 
    # and match with user who has a booking linked to the tour with id=tour_id
    current_user_id = get_jwt_identity()
    user_stmt = db.select(User).join(TourBooking).join(Tour).filter(and_(Tour.id==tour_id, TourBooking.user_id==current_user_id))
    user = db.session.scalar(user_stmt)

    # If the tour exists
    if tour:

        # If not the user who has a booking linked to the tour, return error message
        if not user:
            return {'error' : f'Unauthorized to review tour with id {tour_id}.'}
        
        # Else, create a new instance of Review class and passed in data from request body
        review = Review(
            rating=body_data.get('rating'),
            message=body_data.get('message'),
            user_id = get_jwt_identity(),
            tour=tour
        )

        # Add and commit new review to database
        db.session.add(review)
        db.session.commit()

        # Respond to the client with new review
        return review_schema.dump(review), 201
    
    # If the tour does not exist, return error message
    else:
        return {'error' : f'Tour not found with id {tour_id}.'}, 404


# Review route for deleting a review - review owner and admin only
@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(tour_id, review_id):

    # Find the review which has id=review_id and is linked to the tour with id=tour_id
    stmt = db.select(Review).join(Tour).filter(and_(Tour.id==tour_id, Review.id==review_id))
    review = db.session.scalar(stmt)

    # If the review exists
    if review:
        # If the user who currently logged in is the review owner or admin user
        if str(review.user_id) == get_jwt_identity() or get_jwt_identity() == admin_user_ID():

            # Delete the review and commit 
            db.session.delete(review)
            db.session.commit()
            return {'message' : f'Review {review.id} deleted successfully.'}
        
        # If the user is not the review owner or admin user, return error message
        else:
            return {'error': 'Only the owner of the review can delete.'}, 403
    
    # If the review does not exist
    else:
        return {"error": f"Review not found with id {review_id}."}, 404
    

# Review route for editing a review - review owner only
@reviews_bp.route('/<int:review_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_review(tour_id, review_id):

    # Load the review from the request using schema to include data validation
    body_data = review_schema.load(request.get_json())
    # Find the review which has id=review_id and is linked to the tour with id=tour_id
    stmt = db.select(Review).join(Tour).filter(and_(Tour.id==tour_id, Review.id==review_id))
    review = db.session.scalar(stmt)
    
    # If the review exists
    if review:

        # If the user who currently logged in is not the review owner, return error message
        if str(review.user_id) != get_jwt_identity():
            return {'error': 'Only the owner of the review can edit.'}, 403
        
        # If the user is the review owner
        # Get the data from the request and commit 
        review.rating=body_data.get('rating') or review.rating
        review.message=body_data.get('message') or review.message
        review.date_created=date.today()
        db.session.commit()

        # Return updated review
        return review_schema.dump(review)

# If the review does not exist, return error message
    else:
        return {'error': f'Review not found with id {review_id}.'}, 404