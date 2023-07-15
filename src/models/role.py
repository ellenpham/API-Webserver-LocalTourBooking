from init import db, ma
from marshmallow import fields

# Role model 
class UserRole(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)

    users = db.relationship('User', back_populates = 'role', cascade ='all, delete')

# Role schema
class UserRoleSchema(ma.Schema):
    users = fields.List(fields.Nested('UserSchema', exclude=['role']))

    class Meta:
        fields = ('id', 'name', 'users')
        ordered = True

role_schema = UserRoleSchema()
roles_schema = UserRoleSchema(many=True)
