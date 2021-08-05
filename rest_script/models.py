from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime 
import uuid 


# Security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

# creation of tokens for API
import secrets 

from flask_login import LoginManager, UserMixin

from flask_marshmallow import Marshmallow

db = SQLAlchemy()

login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True, default = '')
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    build = db.relationship('Gunpla', backref = 'owner', lazy = True)

    def __init__(self, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)


class Gunpla(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    customize_price = db.Column(db.Numeric(precision=10, scale=2))
    creation_time = db.Column(db.String(100), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, customize_price, creation_time, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.customize_price = customize_price
        self.creation_time = creation_time
        self.user_token = user_token

    def set_id(self):
        return (secrets.token_urlsafe())


# Creating our Marshaller to pull k,v pairs out of Gunpla instance attributes
class GunplaSchema(ma.Schema):
    class Meta:
        # detailing which fields to pull out of our drone and send to API call and vice versa
        fields = ['id', 'name', 'description', 'customize_price', 'creation_time']

gunpla_schema = GunplaSchema()
gunplas_schema = GunplaSchema(many=True)