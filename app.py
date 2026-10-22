from flask import Flask, render_template, url_for
from config import Config
from models import db
from datetime import datetime

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Configure Cloudinary if credentials provided
    import cloudinary
    if app.config.get('CLOUDINARY_URL'):
        cloudinary.config(cloudinary_url=app.config.get('CLOUDINARY_URL'))
    elif app.config.get('CLOUDINARY_CLOUD_NAME'):
        cloudinary.config(
            cloud_name=app.config.get('CLOUDINARY_CLOUD_NAME'),
            api_key=app.config.get('CLOUDINARY_API_KEY'),
            api_secret=app.config.get('CLOUDINARY_API_SECRET'),
            secure=True
        )

    # Register blueprints
    from routes import auth, seller, storefront, cart
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(seller.bp, url_prefix='/seller')
    app.register_blueprint(storefront.bp)
    app.register_blueprint(cart.bp, url_prefix='/cart')

    from routes.buyer import bp as buyer_bp
    app.register_blueprint(buyer_bp, url_prefix='/buyer')


    from routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from routes.delivery import bp as delivery_bp
    app.register_blueprint(delivery_bp, url_prefix='/delivery')
    
    # Custom template filters
    @app.template_filter('datetime')
    def format_datetime(value, format="%d %b, %Y"):
        if value is None:
            return ""
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except:
                return value
        return value.strftime(format)
        
    @app.template_filter('image_url')
    def image_url_filter(img):
        if not img:
            return url_for('static', filename='images/logo.jpg')
        if img.startswith('http://') or img.startswith('https://'):
            return img
        return url_for('static', filename='images/' + img)

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('base.html'), 500

    with app.app_context():
        # Import models so they are registered with SQLAlchemy
        import models.user
        import models.product
        import models.category
        import models.order
        # Create all tables
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, port=port)
