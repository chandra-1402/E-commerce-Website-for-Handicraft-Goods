from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from models import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        
        user = User.query.filter(db.func.lower(User.email) == email).first()
        if user and check_password_hash(user.password_hash, password):
            # Log the user in
            session['user_id'] = user.id
            session['role'] = user.role
            
            # Redirect based on role
            if user.role == 'SELLER':
                return redirect(url_for('seller.dashboard'))
            elif user.role == 'BUYER':
                return redirect(url_for('buyer.dashboard'))
            elif user.role == 'ADMIN':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('storefront.index'))
                
        flash('Invalid email or password')
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = (request.form.get('first_name') or '').strip()
        last_name = (request.form.get('last_name') or '').strip()
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        age = request.form.get('age')
        gender = (request.form.get('gender') or '').strip()
        phone = (request.form.get('phone') or '').strip()
        address_line_1 = (request.form.get('address_line_1') or '').strip()
        address_line_2 = (request.form.get('address_line_2') or '').strip()
        city = (request.form.get('city') or '').strip()
        state = (request.form.get('state') or '').strip()
        pincode = (request.form.get('pincode') or '').strip()
        
        if not first_name or not email or not password:
            flash('First name, email and password are required.')
            return redirect(url_for('auth.register'))
            
        if User.query.filter(db.func.lower(User.email) == email).first():
            flash('Email already registered. Please sign in or use a different email.')
            return redirect(url_for('auth.register'))
            
        parsed_age = None
        if age:
            try:
                parsed_age = int(age)
            except (ValueError, TypeError):
                parsed_age = None

        try:
            new_user = User(
                name=f"{first_name} {last_name}".strip(),
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=generate_password_hash(password),
                role='BUYER',
                age=parsed_age,
                gender=gender,
                phone=phone,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                state=state,
                pincode=pincode
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please login.')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error registering buyer: {e}")
            flash('An error occurred while creating your account. Please try again.')
            return redirect(url_for('auth.register'))
        
    return render_template('auth/register_buyer.html')

@bp.route('/register-seller', methods=['GET', 'POST'])
def register_seller():
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        
        if not name or not email or not password:
            flash('Please fill out all required fields.')
            return redirect(url_for('auth.register_seller'))
            
        if User.query.filter(db.func.lower(User.email) == email).first():
            flash('Email already registered. Please sign in or use a different email.')
            return redirect(url_for('auth.register_seller'))
            
        try:
            new_user = User(
                name=name,
                email=email,
                password_hash=generate_password_hash(password),
                role='SELLER'
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Seller account created successfully! Please login.')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error registering seller: {e}")
            flash('An error occurred while creating your account. Please try again.')
            return redirect(url_for('auth.register_seller'))
        
    return render_template('auth/register_seller.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('storefront.index'))
