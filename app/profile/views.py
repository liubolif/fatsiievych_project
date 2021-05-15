# -*- coding: utf-8 -*-
from functools import wraps

import PIL.Image
from flask import render_template, url_for, request, redirect, flash, abort
from flask_login import login_user, logout_user, login_required
import os
import secrets
from app.profile import user_bp
from .forms import *
from .models import *
from app import db, bcrypt
from datetime import datetime

from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules

class CustomView(BaseView):
    @expose('/')
    # @login_required
    # @has_role('admin')
    def index(self):
        return self.render('admin/custom.html')

    @expose('/second_page')
    # @login_required
    # @has_role('admin')
    def second_page(self):
        return self.render('admin/second_page.html')


class UserModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    column_searchable_list = ('username',)
    column_sortable_list = ('username', 'admin')
    column_exclude_list = ('pwdhash',)
    form_excluded_columns = ('pwdhash',)
    form_edit_rules = (
        'username', 'email', 'admin',
        rules.Header('Reset Password'),
        'new_password', 'confirm'
    )
    form_create_rules = (
        'username', 'email', 'admin', 'password'
    )

    def scaffold_form(self):
        form_class = super(UserModelView, self).scaffold_form()
        form_class.password = PasswordField('Password')
        form_class.new_password = PasswordField('New Password')
        form_class.confirm = PasswordField('Confirm New Password')
        return form_class

    def create_model(self, form):
        model = self.model(form.username.data, form.email.data,
                           bcrypt.generate_password_hash(form.password.data).decode('utf-8'), form.admin.data)
        # form.populate_obj(model)
        self.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()

    def update_model(self, form, model):
        form.populate_obj(model)
        if form.new_password.data:
            if form.new_password.data != form.confirm.data:
                flash('Passwords must match')
                return
            model.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        self.session.add(model)
        self._on_model_change(form, model, False)
        self.session.commit()


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin


@user_bp.route("/register", methods=['GET', 'POST'])
def register():
    print('register')
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.username.data, form.email.data, form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, admin=False)
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


#############################################
###########    ADMIN   ######################
#############################################
def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin():
            return abort(403)
        return func(*args, **kwargs)

    return decorated_view


@user_bp.route('/administrator')
@login_required
@admin_login_required
def home_admin():
    return render_template('admin-home.html', title='Home Admin')


@user_bp.route('/administrator/users-list')
@login_required
@admin_login_required
def users_list_admin():
    print('users_list_admin')
    users = User.query.all()
    return render_template('user-list-admin.html', title='List of users', users=users)


@user_bp.route('/administrator/create-user', methods=['GET', 'POST'])
@login_required
@admin_login_required
def user_create_admin():
    print('user_create_admin')
    form = AdminUserCreateForm()
    if form.validate_on_submit():
        print(form.username.data, form.email.data, form.password.data, form.admin.data)
        user = User(username=form.username.data, email=form.email.data, password=form.password.data,
                    admin=form.admin.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f'Admin {form.username.data} successfully created!', 'success')
        except:
            db.session.rollback()
            flash(f'DB error!', 'danger')
        return redirect(url_for('user_bp_in.users_list_admin'))
    return render_template('user-create-admin.html', title='Create Admin', form=form)


@user_bp.route('/administrator/update-user/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_login_required
def user_update_admin(id):
    print('user_update_admin', id)
    form = AdminUserUpdateForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        inputed_username = form.username.data
        inputed_email = form.email.data

        if inputed_username != user.username and User.query.filter_by(username=inputed_username).first():
            flash('That username is taken. Please choose a different one.', 'warning')
            return render_template('user-update-admin.html', title='Admin update', form=form, user_id=user.id)

        elif inputed_email != user.email and User.query.filter_by(email=inputed_email).first():
            flash('That email is taken. Please choose a different one.', 'warning')
            return render_template('user-update-admin.html', title='Admin update', form=form, user_id=user.id)
        else:
            user.username = form.username.data
            user.email = form.email.data
            user.admin = form.admin.data

            try:
                db.session.commit()
                flash('Admin has been successfully updated!', 'success')
            except:
                db.session.rollback()
                flash('DB error!', 'danger')

            usersss = User.query.all()
            print(usersss)
            return redirect(url_for('user_bp_in.users_list_admin'))
    else:
        form.username.data = user.username
        form.email.data = user.email
        form.admin.data = user.admin
        return render_template('user-update-admin.html', title='Admin update', form=form, user_id=user.id)


@user_bp.route('/administrator/delete-user/<int:id>')
@login_required
@admin_login_required
def user_delete_admin(id):
    print('user_delete_admin', id)
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'Admin "{user.username}" successfully deleted', 'warning')
    except:
        flash(f'DB error occured during deleting "{user.username}" admin!', 'danger')
    return redirect(url_for('user_bp_in.users_list_admin'))
