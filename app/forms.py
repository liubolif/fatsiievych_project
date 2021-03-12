from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateTimeField, DateField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Optional, ValidationError


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

    is_done = BooleanField('Is done')

    submit = SubmitField('Submit')
