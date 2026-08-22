from models import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0.0)
    # Relationships
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seller = db.relationship('User', foreign_keys=[seller_id])
    
    # Images (up to 5)
    image_1 = db.Column(db.String(255), nullable=True)
    image_2 = db.Column(db.String(255), nullable=True)
    image_3 = db.Column(db.String(255), nullable=True)
    image_4 = db.Column(db.String(255), nullable=True)
    image_5 = db.Column(db.String(255), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
