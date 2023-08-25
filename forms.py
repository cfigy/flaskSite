from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length


class NamerForm(FlaskForm):
  name = StringField("First Name:", validators=[DataRequired()])
  submit = SubmitField("Submit")


class LoginForm(FlaskForm):
  username = StringField("Username:", validators=[DataRequired()])
  password_hash = PasswordField("Password:", validators=[DataRequired()])
  submit = SubmitField("Submit")


class PasswordForm(FlaskForm):
  email = StringField("Email:", validators=[DataRequired()])
  password_hash = PasswordField("Password:", validators=[DataRequired()])
  submit = SubmitField("Submit")


class UserForm(FlaskForm):
  name = StringField("Name:", validators=[DataRequired()])
  username = StringField("Username:", validators=[DataRequired()])
  email = StringField("Email:", validators=[DataRequired()])
  phone_number = StringField("Phone Number:")
  password_hash = PasswordField('Password:',
                                validators=[
                                  DataRequired(),
                                  EqualTo('password_hash2',
                                          message="Passwords must match.")
                                ])
  password_hash2 = PasswordField('Confirm Password:',
                                 validators=[DataRequired()])
  submit = SubmitField("Submit")
