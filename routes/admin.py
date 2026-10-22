from flask import Blueprint, jsonify
from models import db
from models.product import Product
from models.order import Order, OrderItem

bp = Blueprint('admin', __name__)

@bp.route('/dashboard')
def dashboard():
    return "Admin Dashboard Stub"

@bp.route('/clear-all-products', methods=['GET', 'POST'])
def clear_all_products():
    try:
        OrderItem.query.delete()
        Order.query.delete()
        deleted_count = Product.query.delete()
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": f"Successfully cleared {deleted_count} products and associated orders from database."
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
