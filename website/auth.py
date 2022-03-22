from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
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

@auth.route('/results')
@login_required
def results():
    return render_template("result.html", user=current_user)


@auth.route('/service')
def service():
    return render_template("service.html", user=current_user)

@auth.route('/serve')
def serve():
    return render_template("serve.html", user=current_user)

@auth.route('/', methods=['GET', 'POST'])
def sign_up():
    # logout_user()
    if request.method == 'POST':
        full_name = request.form.get('fullName')
        faility_name = request.form.get('facilityName')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        contact = request.form.get('contact')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(full_name) < 4:
            flash('Full Name must be greater than 3 character.', category='error')
        elif len(faility_name) < 4:
            flash('Facility Name must be greater than 3 characters.', category='error')
        elif len(email) < 5:
            flash('Email must be greater than 4 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif len(contact) < 10 or len(contact) > 12:
            flash('Contact must be 10 to 12 characters.', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'),
                        full_name=full_name, facility_name = faility_name, contact = contact )
            db.session.add(new_user)
            db.session.commit()
            # login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("index.html", user=current_user)