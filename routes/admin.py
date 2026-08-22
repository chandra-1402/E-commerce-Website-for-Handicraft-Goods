from flask import Blueprint

bp = Blueprint('admin', __name__)

@bp.route('/dashboard')
def dashboard():
    return "Admin Dashboard Stub"
