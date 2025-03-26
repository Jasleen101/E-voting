"""
Defines routes: sign up, log in and log out
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                
                # Determine redirect URL based on the user's role
                if user.user_role == 'voter':
                    return redirect(url_for('views.voter_home'))
                elif user.user_role == 'candidate':
                    return redirect(url_for('views.candidate_home'))
                elif user.user_role == 'admin' or user.user_role == 'User' or user.user_role == 'Admin':
                    return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # once the user sign ups we are getting the data and storing in relavant variables
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user_role = request.form.get('user_role')

        # validation
        user = User.query.filter_by(email=email).first()
        if user:
            # flash allows to print message and you can categorise them
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Check if a user with the provided email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already exists.', category='error')
            else:
                # Create a new user object and add it to the database
                new_user = User(email=email, first_name=first_name, 
                                password=generate_password_hash(password1, method='pbkdf2:sha256'),
                                user_role=user_role)
                db.session.add(new_user)
                db.session.commit()
                flash('Account created!', category='success')
                
                # Log in the newly created user and redirect to the appropriate page
                login_user(new_user, remember=True)
                if user_role == 'voter':
                    return redirect(url_for('views.voter_home'))
                elif user_role == 'candidate':
                    return redirect(url_for('views.candidate_home'))
                else:
                    return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)