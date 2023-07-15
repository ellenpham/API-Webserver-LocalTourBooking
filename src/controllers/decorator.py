from init import db
from models.user import User
from flask_jwt_extended import get_jwt_identity
import functools

# Decorator for admin authorisation
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user.role_id == 1:
            return fn(*args, **kwargs)
        else: 
            return {'error' : 'User not authorised to perform this activity.'}, 401
    
    return wrapper

# Decorator for tourist authorisation 
def authorise_as_tourist(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user.role_id == 2:
            return fn(*args, **kwargs)
        else: 
            return {'error' : 'User not authorised to perform this activity.'}, 401
    return wrapper

# Decorator for tour guide authorisation 
def authorise_as_tourguide(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user.role_id == 3:
            return fn(*args, **kwargs)
        else: 
            return {'error' : 'User not authorised to perform this activity.'}, 401
    
    return wrapper

# Function to return the ID of an Admin User (admin's role ID is 1)
def admin_user_ID():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user.role_id == 1:
        return str(user.id)
    else:
        return {'error' : 'Not admin user.'}, 401
