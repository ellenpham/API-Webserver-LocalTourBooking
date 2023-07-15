from init import db, ma 
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, OneOf
from datetime import date

# Tour model
class Tour(db.Model):
    __tablename__ = "tours"

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(50), nullable=False)
    tour_name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    tourist_capacity = db.Column(db.String)
    is_private = db.Column(db.Boolean)
    price = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='tours')
    tour_bookings = db.relationship('TourBooking', back_populates='tour') # no need cascade = 'all, delete', assuming that tours cannot be deleted if it is still linked to a tour booking
    reviews = db.relationship('Review', back_populates='tour', cascade='all, delete')

# Tour schema
class TourSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['username', 'email', 'role'])
    tour_bookings = fields.List(fields.Nested("TourBookingSchema", exclude=["tour"]))
    reviews = fields.List(fields.Nested('ReviewSchema', exclude=['tour']))

    # Country validation
    country = fields.String(required=True, validate=And(
        Length(min=2, error="Country must have at least 2 characters."),
        Regexp("^[a-zA-Z]+$", error="Country must only contain letters.")
    ))

    # Tour name validation
    tour_name = fields.String(required=True, validate=Length(min=10, max=200, error="Tour name must have a minimum of 10 characters and maximum of 200 character."))

    # Description validation
    description = fields.String(required=True, validate=Length(min=5, error="Description does not have enough information. Please add more."))

    # Date validation
    from_date = fields.Date(required=True, format='%d-%m-%Y', default=date.today())
    to_date = fields.Date(required=True, format='%d-%m-%Y', default=date.today())

    # Tourist capacity validation
    tourist_capacity = fields.String(validate=Length(min=1, error="Tourist capacity must have at least 1 character.")) 

    # is_private validation
    is_private = fields.Boolean(validate=OneOf([1,0], error="Invalid input! Please try again."))

    # Price validation
    price = fields.Float(required=True)
    
    # is_available validation
    is_available = fields.Boolean(validate=OneOf([1,0], error="Invalid input! Please try again."))

    class Meta:
        fields = ('id', 'country', 'tour_name', 'description', 'from_date', 'to_date', 'tourist_capacity', 'is_private', 'price', 'is_available', 'user', 'tour_bookings', 'reviews')
        ordered = True

tour_schema = TourSchema()
tours_schema = TourSchema(many=True)
