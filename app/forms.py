from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, TextAreaField, SubmitField, DateTimeField, DateField, SelectField, BooleanField, \
    SelectMultipleField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Optional, ValidationError, EqualTo, Regexp
from flask_wtf.file import FileField, FileAllowed
from app.models import *
from app import db
from flask import flash


# метод для витягування списку категорій з БД
def getСategoryList():
    categ_list = []
    categories = Category.query.all()
    for categ in categories:
        categ_list.append((categ.id, categ.name))
    return categ_list


def getEmployeeList():
    empl_list = []
    employes = Employee.query.all()
    for emp in employes:
        empl_list.append((emp.id, emp.name))
    return empl_list


class ContactForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(message="Введіть своє ім'я!")]
                       )
    email = StringField('Email',
                        validators=[DataRequired(message="Введіть свій email"),
                                    Email(message="Невірно введений email!")]
                        )
    message = TextAreaField('Message',
                            validators=[
                                DataRequired(),
                                Length(min=2, max=100,
                                       message="Текстове повідомлення повинне містити від 2 до 200 символів!")]
                            )
    submit = SubmitField('Submit')


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])

    description = TextAreaField('Description', validators=[DataRequired()])

    # created = DateTimeField('Created', format='%d-%m-%Y %H:%M:%S', validators=[])
    # ValidationError(message="Введіть дату у форматі y-m-d")
    created = DateField('Created', format='%Y-%m-%d', validators=[Optional()])

    priority = SelectField('Priority', choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high')])

    category = SelectField('Category', coerce=int)

    employee = SelectMultipleField('Employee', coerce=int)

    is_done = BooleanField('Is done')

    submit = SubmitField('Submit')

    @classmethod
    def new(cls):
        form = cls()

        form.category.choices = getСategoryList()
        form.employee.choices = getEmployeeList()
        return form


class CategoryForm(FlaskForm):
    name = StringField('Category name', validators=[DataRequired()])

    submit = SubmitField('Submit')


class EmployeeForm(FlaskForm):
    name = StringField('Employee name', validators=[DataRequired()])

    submit = SubmitField('Submit')


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