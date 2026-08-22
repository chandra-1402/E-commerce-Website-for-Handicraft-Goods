from flask import Flask
from config import Config
from models import db
from datetime import datetime

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

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

    with app.app_context():
        # Import models so they are registered with SQLAlchemy
        import models.user
        import models.product
        import models.category
        import models.order
        # Create all tables
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
