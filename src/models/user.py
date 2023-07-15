from init import db, ma
from marshmallow import fields, EXCLUDE
from marshmallow.validate import Length, And, Regexp, OneOf
from datetime import date

VALID_ROLE_ID = (1, 2, 3) # 1 for Admin, 2 for Tourist, 3 for Tour Guide
VALID_GENDER = ("male", "female", "others")
VALID_IDENTITY_DOC_TYPE = ("passport", "driver license", "identity card")

# User Model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    f_name = db.Column(db.String(50))
    l_name = db.Column(db.String(50))
    date_created= db.Column(db.Date, default=date.today())
    dob = db.Column(db.Date)
    gender = db.Column(db.String)
    spoken_language= db.Column(db.String)
    description = db.Column(db.Text)
    phone = db.Column(db.String(15), unique=True)
    identity_doc_type = db.Column(db.String)
    identity_doc_ID = db.Column(db.String, unique=True)
    is_active = db.Column(db.Boolean, default=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    role = db.relationship('UserRole', back_populates='users')
    tours = db.relationship('Tour', back_populates='user', cascade='all, delete')
    tour_bookings = db.relationship('TourBooking', back_populates='user') # no need for cascade='all,delete', assuming an user cannot be deleted if there's still an existing tour booking
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete')

# User Schema for returning objects to authorized users with full info access
class UserSchema(ma.Schema):
    role = fields.Nested('UserRoleSchema', only=['name'])
    tours = fields.List(fields.Nested('TourSchema', exclude=['user']))
    tour_bookings = fields.List(fields.Nested('TourBookingSchema', exclude=['user']))

    # Username validation
    username = fields.String(required=True, validate=And(
        Length(min=5, error="Username must have at least 5 characters."),
        Regexp("^[a-zA-Z0-9_.-]+$", error="Username can contain only letters, numbers and the following special characters: dot(.), underscore (_) or dash (-)")
    ))

    # Email validation
    email = fields.Email(required=True, 
    error_messages = {
        "required" : "Email is a mandatory field.",
        "invalid": "Invalid email address! Please check again."})

    # Password validation
    password = fields.String(required=True, validate=And(
        Length(min=5, error="Username must have at least 5 characters."),
        Regexp('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).*$', error='Password must include at least one uppercase letter, one lowercase letter, one digit and one special character.')
    ))

    # Role ID validation 
    role_id = fields.Integer(required=True, validate=OneOf(VALID_ROLE_ID, error="Invalid value! Please enter Role ID 2 for Tourist. Role ID 3 for Tour Guide."))

    # DOB validation
    dob = fields.Date(format='%d-%m-%Y', error_messages = {
        "invalid": "Invalid date input! Please use the following format dd-mm-yy."})

    # Name validation
    f_name = fields.String(validate=And(
        Length(min=2, error="First name must have at least 2 characters."),
        Regexp("^[a-zA-Z ]+$", error="First name can contain only letters and space.")
    ))
    
    l_name = fields.String(validate=And(
        Length(min=2, error="Last name must have at least 2 characters."),
        Regexp("^[a-zA-Z ]+$", error="Last name can contain only letters and space.")
    ))

    # Gender validation
    gender = fields.String(validate=OneOf(VALID_GENDER, error="Invalid input for gender! Please try again."))

    # Spoken language validation
    spoken_language = fields.String(validate=And(
        Length(min=2, error="Spoken language must have at least 2 characters."),
        Regexp("^[a-zA-Z, ]+$", error="Spoken language can contain only letters and space, multiple languages are separated by comma.")
    ))

    # Description validation
    description = fields.String(validate=Length(min=5, error="Description does not have enough information. Please add more."))

    # Phone number validation
    phone = fields.String(validate=And(
        Length(min=6, error="Phone number must have at least 6 numbers."),
        Regexp("^[0-9]+$", error="Phone number can contain only numbers.")
    ))

    # Identity Document Type validation 
    identity_doc_type = fields.String(validate=OneOf(VALID_IDENTITY_DOC_TYPE, error="Invalid input for document identity type! Please try again."))

    # Identity Document ID validation
    identity_doc_ID = fields.String(validate=And(
        Length(min=5, error="Identity Document ID must have at least 5 characters."),
        Regexp("^[a-zA-Z0-9]+$", error="Identity Document ID can contain only letters and numbers.")
    ))

    # Active account validation
    is_active = fields.Boolean(validate=OneOf([1,0], error="Invalid input! Please try again."))


    class Meta:
        fields = ('id', 'username', 'password', 'email', 'f_name', 'l_name', 'date_created', 'dob', 'gender', 'spoken_language', 'description', 'phone', 'identity_doc_type', 'identity_doc_ID', 'is_active', 'role', 'role_id', 'tours', 'tour_bookings')
        ordered = True

user_schema = UserSchema(unknown=EXCLUDE)
users_schema = UserSchema(many=True, unknown=EXCLUDE)


# User Schema for returning objects to authorized users with limited info access
# Sensitive data fields are excluded 
class otherUserSchema(ma.Schema):
    role = fields.Nested('UserRoleSchema', only=['name'])
    tours = fields.List(fields.Nested('TourSchema', exclude=['user', 'tour_bookings']))
    tour_bookings = fields.List(fields.Nested('TourBookingSchema', exclude=['user']))

    class Meta:
        fields = ('username', 'email', 'f_name', 'l_name', 'date_created', 'dob', 'gender', 'spoken_language', 'description', 'phone', 'is_active', 'role', 'tours', 'tour_bookings')
        ordered = True

other_user_schema = otherUserSchema()
other_users_schema = otherUserSchema(many=True)


