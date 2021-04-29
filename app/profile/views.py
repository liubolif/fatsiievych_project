# -*- coding: utf-8 -*-
import PIL.Image
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, login_required
import os
import secrets
# from app import app
from app.profile import user_bp
from .forms import *
from .models import *
from app import db, bcrypt
from datetime import datetime


#@app.route("/register", methods=['GET', 'POST'])
@user_bp.route("/register", methods=['GET', 'POST'])
def register():
    print('register')
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.username.data, form.email.data, form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f'Користувач {form.username.data} успішно зареєстрований!', 'success')
        except:
            db.session.rollback()
            flash(f'Помилка під час запису користувача до БД', 'danger')
        return redirect(url_for('user_bp_in.login'))
    return render_template('register.html', title='Register', form=form)


@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    print('login')
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = LoginForm()
    if form.validate_on_submit():
        print(form.email.data, form.password.data)
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash(f'Користувач успішно увійшов у свій аккаунт!', 'success')
                next = request.args.get('next')
                print('next post', next)
                # from werkzeug.urls import url_parse
                # next_page = request.args.get('next')
                # if not next_page or url_parse(next_page).netloc != '':
                #     next_page = url_for('index')

                # if not is_safe_url(next, {'127.0.0.1:5000'}):
                #     return abort(400)

                if next:
                    return redirect(next)
                return redirect(url_for('user_bp_in.account'))
            else:
                flash('Введено невірний пароль.', 'danger')
                return redirect(url_for('user_bp_in.login'))
        else:
            flash('Користувача із вказаним емейлом не існує в базі даних.', 'danger')
    return render_template('login.html', title='Login', form=form)


@user_bp.after_request
def after_request_func(response):
    if current_user:
        current_user.last_time_seen = datetime.utcnow()
        try:
            db.session.commit()
        except:
            db.session.rollback()
    return response


@user_bp.route("/logout")
def logout():
    logout_user()
    flash(f'User exit from account!', 'info')
    return redirect(url_for('about'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(user_bp.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = PIL.Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@user_bp.route("/account", methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data

        try:
            db.session.commit()
            flash('Your account has been updated!', 'success')
        except:
            db.session.rollback()
            flash('Error occurs during data recording to DB', 'danger')

        usersss = User.query.all()
        print(usersss)
        return redirect(url_for('user_bp_in.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    image_file = url_for('user_bp_in.static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@user_bp.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        try:
            db.session.commit()
            flash('Your password was successfully changed!', 'success')
        except:
            db.session.rollback()
            flash('Error occurs during data recording to DB', 'danger')
        return redirect(url_for('user_bp_in.account'))
    return render_template('change_password.html', title='Password Changer', form=form)

