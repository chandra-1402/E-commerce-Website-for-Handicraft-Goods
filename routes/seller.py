from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.product import Product
from models.user import User
import os
from werkzeug.utils import secure_filename
from flask import current_app

bp = Blueprint('seller', __name__)

def check_seller():
    if not session.get('user_id') or session.get('role') != 'SELLER':
        flash('Please login as a seller to access this page.')
        return False
    return True

@bp.route('/dashboard')
def dashboard():
    if not check_seller(): return redirect(url_for('auth.login'))
    
    # Fetch seller's products
    products = Product.query.filter_by(seller_id=session['user_id']).all()
    return render_template('seller/dashboard.html', products=products)

@bp.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if not check_seller(): return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        discount = request.form.get('discount', 0)
        
        new_product = Product(
            name=name,
            description=description,
            price=float(price),
            discount=float(discount),
            seller_id=session['user_id']
        )
        
        # Handle images
        for i in range(1, 6):
            image = request.files.get(f'image_{i}')
            if image and image.filename:
                filename = secure_filename(image.filename)
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                setattr(new_product, f'image_{i}', filename)
                
        db.session.add(new_product)
        db.session.commit()
        
        flash('Product added successfully!')
        return redirect(url_for('seller.dashboard'))
        
    return render_template('seller/add_product.html')

@bp.route('/edit-product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if not check_seller(): return redirect(url_for('auth.login'))
    
    product = Product.query.get_or_404(product_id)
    if product.seller_id != session['user_id']:
        return "Unauthorized", 401
        
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.discount = float(request.form.get('discount', 0))
        
        # Handle image updates
        for i in range(1, 6):
            image = request.files.get(f'image_{i}')
            if image and image.filename:
                filename = secure_filename(image.filename)
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                setattr(product, f'image_{i}', filename)
                
        db.session.commit()
        flash('Product updated successfully!')
        return redirect(url_for('seller.dashboard'))
        
    return render_template('seller/edit_product.html', product=product)

@bp.route('/delete-product/<int:product_id>')
def delete_product(product_id):
    if not check_seller(): return redirect(url_for('auth.login'))
    
    product = Product.query.get_or_404(product_id)
    if product.seller_id != session['user_id']:
        return "Unauthorized", 401
        
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!')
    return redirect(url_for('seller.dashboard'))

@bp.route('/products')
def my_products():
    if not check_seller(): return redirect(url_for('auth.login'))
    products = Product.query.filter_by(seller_id=session['user_id']).all()
    return render_template('seller/my_products.html', products=products)

@bp.route('/orders')
def orders():
    if not check_seller(): return redirect(url_for('auth.login'))
    
    from models.order import Order, OrderItem
    
    # Find all orders that contain products from this seller
    seller_order_ids = db.session.query(OrderItem.order_id)\
        .join(Product, OrderItem.product_id == Product.id)\
        .filter(Product.seller_id == session['user_id'])\
        .distinct()
        
    orders = Order.query.filter(Order.id.in_(seller_order_ids)).order_by(Order.created_at.desc()).all()
    
    return render_template('seller/orders.html', orders=orders)

@bp.route('/update_order_status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    if not check_seller(): return redirect(url_for('auth.login'))
    
    from models.order import Order, OrderItem
    
    # Verify this seller has items in this order
    has_items = db.session.query(OrderItem)\
        .join(Product, OrderItem.product_id == Product.id)\
        .filter(OrderItem.order_id == order_id, Product.seller_id == session['user_id'])\
        .first()
        
    if not has_items:
        return "Unauthorized", 401
        
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    valid_statuses = ['Pending', 'Confirmed', 'Shipped', 'Out for Delivery', 'Delivered']
    if new_status in valid_statuses:
        order.status = new_status
        db.session.commit()
        flash(f'Order #{10000 + order.id} status updated to {new_status}!')
        
    return redirect(url_for('seller.orders'))

@bp.route('/earnings')
def earnings():
    if not check_seller(): return redirect(url_for('auth.login'))
    # Dummy data for now
    return render_template('seller/earnings.html')

@bp.route('/settings', methods=['GET', 'POST'])
def store_settings():
    if not check_seller(): return redirect(url_for('auth.login'))
    
    seller = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        seller.name = request.form.get('name')
        seller.store_description = request.form.get('store_description')
        
        logo = request.files.get('store_logo')
        if logo and logo.filename:
            filename = secure_filename(logo.filename)
            logo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            logo.save(logo_path)
            seller.store_logo = filename
            
        db.session.commit()
        flash('Store settings updated successfully!')
        return redirect(url_for('seller.store_settings'))
        
    return render_template('seller/settings.html', seller=seller)
