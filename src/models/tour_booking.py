from init import db, ma 
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

# Tour booking model
class TourBooking(db.Model):
    __tablename__ = "tour_bookings"

    id = db.Column(db.Integer, primary_key=True)
    tourist_number = db.Column(db.Integer, nullable=False)
    preferred_language = db.Column(db.String(100), nullable=False)
    extra_request = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)

    user = db.relationship('User', back_populates='tour_bookings')
    tour = db.relationship('Tour', back_populates='tour_bookings')

# Tour booking schema
class TourBookingSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['username', 'email', 'role'])
    tour = fields.Nested('TourSchema', only=['user', 'tour_name'])

    # Tourist number validation
    tourist_number = fields.Integer(required=True)

    # Preferred language validation
    preferred_language = fields.String(required=True, validate=And(
        Length(min=2, error="Preferred language must have at least 2 characters."),
        Regexp("^[a-zA-Z, ]+$", error="Preferred language can contain only letters and space, multiple languages are separated by comma.")
    ))

    # Extra request validation
    extra_request = fields.String(validate=Length(min=5, error="Extra request does not have enough information. Please add more."))

    class Meta:
        fields = ('id', 'tourist_number', 'preferred_language', 'extra_request', 'user', 'tour')
        ordered = True

tour_booking_schema = TourBookingSchema()
tour_bookings_schema = TourBookingSchema(many=True)