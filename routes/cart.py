from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.product import Product
from models.order import Order, OrderItem

bp = Blueprint('cart', __name__)

@bp.route('/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    
    if 'cart' not in session:
        session['cart'] = {}
        
    cart = session['cart']
    # If the user clicked "Buy Now", we can pass a special flag or just redirect them straight to checkout
    # but for simplicity, both buttons add to cart, and "Buy Now" just redirects to checkout immediately.
    is_buy_now = request.form.get('buy_now', 'false') == 'true'
    
    pid_str = str(product_id)
    if pid_str in cart:
        cart[pid_str] += 1
    else:
        cart[pid_str] = 1
        
    session.modified = True
    
    if is_buy_now:
        return redirect(url_for('cart.checkout'))
        
    flash(f'{product.name} added to your cart!')
    return redirect(request.referrer or url_for('storefront.index'))

@bp.route('/')
def view_cart():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            discounted_price = product.price * (1 - product.discount/100)
            item_total = discounted_price * qty
            total_price += item_total
            cart_items.append({
                'product': product,
                'quantity': qty,
                'price': discounted_price,
                'total': item_total
            })
            
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@bp.route('/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    pid_str = str(product_id)
    if pid_str in cart:
        del cart[pid_str]
        session.modified = True
        flash('Item removed from cart.')
    return redirect(url_for('cart.view_cart'))

@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session or session.get('role') != 'BUYER':
        flash("Please log in as a buyer to proceed to checkout.")
        return redirect(url_for('auth.login'))
        
    cart = session.get('cart', {})
    if not cart:
        flash("Your cart is empty!")
        return redirect(url_for('cart.view_cart'))
        
    if request.method == 'POST':
        address = request.form.get('shipping_address')
        payment = request.form.get('payment_method')
        
        # Calculate total
        total_price = 0
        order_items_data = []
        for pid, qty in cart.items():
            product = Product.query.get(int(pid))
            if product:
                discounted_price = product.price * (1 - product.discount/100)
                total_price += discounted_price * qty
                order_items_data.append((product, qty, discounted_price))
                
        # Create Order
        new_order = Order(
            buyer_id=session['user_id'],
            total_amount=total_price,
            shipping_address=address,
            payment_method=payment,
            status='Pending'
        )
        db.session.add(new_order)
        db.session.commit() # To get order ID
        
        # Create Order Items
        for product, qty, price in order_items_data:
            item = OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=qty,
                price_at_purchase=price
            )
            db.session.add(item)
            
        db.session.commit()
        
        # Clear Cart
        session['cart'] = {}
        session.modified = True
        
        return redirect(url_for('cart.order_success', order_id=new_order.id))
        
    # GET request - show checkout page
    total_price = sum(Product.query.get(int(pid)).price * (1 - Product.query.get(int(pid)).discount/100) * qty for pid, qty in cart.items() if Product.query.get(int(pid)))
    return render_template('checkout.html', total_price=total_price)

@bp.route('/success/<int:order_id>')
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    if order.buyer_id != session.get('user_id'):
        return "Unauthorized", 401
    return render_template('order_success.html', order=order)

@bp.route('/invoice/<int:order_id>')
def invoice(order_id):
    order = Order.query.get_or_404(order_id)
    if order.buyer_id != session.get('user_id'):
        return "Unauthorized", 401
    
    # Get user to display buyer info on invoice
    from models.user import User
    buyer = User.query.get(order.buyer_id)
    
    # Calculate expected delivery (10 days from order creation)
    from datetime import timedelta
    expected_delivery = order.created_at + timedelta(days=10)
    
    return render_template('invoice.html', order=order, buyer=buyer, expected_delivery=expected_delivery)
