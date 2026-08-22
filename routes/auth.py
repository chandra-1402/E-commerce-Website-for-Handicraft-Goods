from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
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
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        age = request.form.get('age')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        address_line_1 = request.form.get('address_line_1')
        address_line_2 = request.form.get('address_line_2')
        city = request.form.get('city')
        state = request.form.get('state')
        pincode = request.form.get('pincode')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.register'))
            
        new_user = User(
            name=f"{first_name} {last_name}",
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=generate_password_hash(password),
            role='BUYER',
            age=int(age) if age else None,
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
        
    return render_template('auth/register_buyer.html')

@bp.route('/register-seller', methods=['GET', 'POST'])
def register_seller():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.register_seller'))
            
        new_user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            role='SELLER'
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Seller account created! Please login.')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register_seller.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('storefront.index'))
