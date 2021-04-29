from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Optional, ValidationError, EqualTo, Regexp
from flask_wtf.file import FileField, FileAllowed
from .models import *


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=4, max=20, message='Ім\'я має бути довжиною від 4 до 20 символів'),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Ім\'я користувача повинно складатися лише із літер, цифр,'
                                              ' символів крапки або підкреслення')
                                       ]
                           )
    email = StringField('Email',
                        validators=[DataRequired(), Email(message="Невірно введений email")])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=5, max=20,
                                                message='Пароль має бути довжиною від 5 до 20 символів')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Паролі не співпадають')]
                                     )
    submit = SubmitField('Sign Up')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Користувач із даним ім\'ям вже існує! Будь ласка, оберіть інше ім\'я.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Користувач із даним емейлом уже зареєстрований! Будь ласка, оберіть інший емейл.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=4, max=20, message='The username length must be between 6 and 20 '
                                                                     'characters'),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'The username should only include letters, numbers, semicolons, '
                                              'or underscores')
                                       ]
                           )
    email = StringField('Email',
                        validators=[DataRequired(), Email(message="Incorrectly email")])

    about_me = TextAreaField('About Me', validators=[Optional()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update info')

    def validate_username(self, field):
        if field.data != current_user.username:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, field):
        if field.data != current_user.email:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('That email is taken. Please choose a different one.')


class ChangePasswordForm(FlaskForm):

    old_password = PasswordField('Old Password', validators=[DataRequired()])

    new_password = PasswordField('New Password',
                                 validators=[DataRequired(),
                                             Length(min=5, max=20,
                                                    message='The password length must be between 5 and 20 characters')])
    confirm_new_password = PasswordField('Confirm New Password',
                                         validators=[EqualTo('new_password', message='Паролі не співпадають')]
                                         )
    submit = SubmitField('Change password')

    def validate_old_password(self, field):
        if not bcrypt.check_password_hash(current_user.password, field.data):
            raise ValidationError('Incorrectly entered old password. Please, try again.')

    def validate_new_password(self, field):
        if bcrypt.check_password_hash(current_user.password, field.data):
            raise ValidationError('You entered the same password as if was before.')


class ImageForm(FlaskForm):

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')