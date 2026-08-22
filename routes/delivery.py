from flask import Blueprint

bp = Blueprint('delivery', __name__)

@bp.route('/dashboard')
def dashboard():
    return "Delivery Dashboard Stub"
