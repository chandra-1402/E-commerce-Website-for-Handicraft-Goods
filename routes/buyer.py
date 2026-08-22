from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.user import User
from models.order import Order

bp = Blueprint('buyer', __name__)

@bp.route('/dashboard')
def dashboard():
    # Ensure user is logged in and is a buyer
    user_id = session.get('user_id')
    if not user_id or session.get('role') != 'BUYER':
        flash('Please login as a buyer to access the dashboard.')
        return redirect(url_for('auth.login'))
        
    buyer = User.query.get_or_404(user_id)
    orders = Order.query.filter_by(buyer_id=user_id).order_by(Order.created_at.desc()).limit(3).all()
    
    return render_template('buyer/dashboard.html', buyer=buyer, orders=orders)

@bp.route('/orders')
def orders():
    # Ensure user is logged in and is a buyer
    user_id = session.get('user_id')
    if not user_id or session.get('role') != 'BUYER':
        flash('Please login as a buyer to view your orders.')
        return redirect(url_for('auth.login'))
        
    orders = Order.query.filter_by(buyer_id=user_id).order_by(Order.created_at.desc()).all()
    
    return render_template('buyer/orders.html', orders=orders)

@bp.route('/track/<int:order_id>')
def track_order(order_id):
    # Ensure user is logged in and is a buyer
    user_id = session.get('user_id')
    if not user_id or session.get('role') != 'BUYER':
        flash('Please login to track orders.')
        return redirect(url_for('auth.login'))
        
    order = Order.query.get_or_404(order_id)
    if order.buyer_id != user_id:
        return "Unauthorized", 401
        
    from datetime import timedelta
    expected_delivery = order.created_at + timedelta(days=10)
    
    return render_template('buyer/track.html', order=order, expected_delivery=expected_delivery)
