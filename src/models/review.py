from init import db, ma 
from marshmallow import fields
from marshmallow.validate import Length, Range
from datetime import date

# Review model
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_created= db.Column(db.Date, default=date.today())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)

    user = db.relationship('User', back_populates='reviews')
    tour = db.relationship('Tour', back_populates='reviews')

# Review schema
class ReviewSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['username', 'role'])
    tour = fields.Nested('TourSchema', only=['tour_name', 'user'])

    # Rating validation
    rating = fields.Integer(required=True, validate=Range(1,5))

    # Message validation
    message = fields.String(required=True, validate=Length(min=5, error='Message does not have enough information. Please add more.'))

    class Meta:
        fields = ('id', 'rating', 'message', 'date_created', 'user', 'tour')
        ordered = True

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)