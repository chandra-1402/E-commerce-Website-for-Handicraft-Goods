from flask import Blueprint, render_template
from models.user import User
from models.product import Product

bp = Blueprint('storefront', __name__)

@bp.route('/')
def index():
    # Fetch latest products to display on homepage
    products = Product.query.order_by(Product.created_at.desc()).limit(8).all()
    return render_template('index.html', products=products)

@bp.route('/products')
def all_products():
    # Fetch all products
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('products.html', products=products)

@bp.route('/store/<int:seller_id>')
def seller_store(seller_id):
    seller = User.query.get_or_404(seller_id)
    if seller.role != 'SELLER':
        return "Not a valid store", 404
        
    products = Product.query.filter_by(seller_id=seller_id).all()
    return render_template('seller_store.html', seller=seller, products=products)

@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    seller = User.query.get(product.seller_id)
    
    # Fetch some suggested products (excluding current product)
    suggested = Product.query.filter(Product.id != product_id).limit(4).all()
    
    return render_template('product_detail.html', product=product, seller=seller, suggested=suggested)
