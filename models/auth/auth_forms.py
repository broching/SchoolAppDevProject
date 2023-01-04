from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import Email, EqualTo, DataRequired, Length
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=5, max=15), DataRequired()])
    email = EmailField('Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password', validators=[Length(min=5, max=15),
                                                      DataRequired(message="Please do not leave this field empty")])
    password2 = PasswordField('Confirm Password',
                              validators=[DataRequired(message="Please do not leave this field empty"),
                                          EqualTo("password1", message="Passwords do not match")])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username/Email Address', validators=[Length(min=5, max=15), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=5, max=15), DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateCustomerForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=5, max=15), DataRequired()])
    email = EmailField('Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password', validators=[Length(min=5, max=15),
                                                      DataRequired(message="Please do not leave this field empty")])
    password2 = PasswordField('Confirm Password',
                              validators=[DataRequired(message="Please do not leave this field empty"),
                                          EqualTo("password1", message="Passwords do not match")])
