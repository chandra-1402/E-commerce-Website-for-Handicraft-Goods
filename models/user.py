from models import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='BUYER') # BUYER, SELLER, ADMIN, SUPER_ADMIN, DELIVERY
    status = db.Column(db.String(20), nullable=False, default='Active')
    profile_image = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Detailed Buyer Info
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address_line_1 = db.Column(db.String(255), nullable=True)
    address_line_2 = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    pincode = db.Column(db.String(20), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Store specific details for Sellers
    store_description = db.Column(db.Text, nullable=True)
    store_logo = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Float, default=0.0)
