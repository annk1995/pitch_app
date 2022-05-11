from . import auth
from .. import db
from flask import render_template, request, flash, redirect, url_for
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from ..email import mail_message
from flask_login import login_user, login_required, logout_user, current_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash('You entered wrong email or password', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("auth/login.html", user=current_user)


@auth.route('/logout')
@login_required  # user can only access this function when logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('A user with this email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(username) < 2:
            flash('Pick a username that is greater than 2 characters.', category='error')
        elif len(password1) < 7:
            flash('Use a stronger password that is more than 7 characters long.', category='error')
        elif password1 != password2:
            flash('Passwords did not match!!!', category='error')
        else:
            # create a new user if form is valid
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            # add the new user to our db
            db.session.add(new_user)
            db.session.commit()
            # send welcome email to new user
            # mail_message("Welcome to One Minute Pitch","email/welcome_user",new_user.email,user=user)
            flash('Account created successfully.', category='success')
            return redirect(url_for('auth.login'))

    return render_template("auth/sign-up.html", user=current_user)