from wtforms import StringField, SubmitField, EmailField, DateField, TelField, PasswordField, IntegerField, SelectField, TextAreaField
from wtforms.validators import Email, Length, EqualTo, DataRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
import pycountry


class CountrySelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)
        self.choices = [(country.alpha_2, country.name) for country in pycountry.countries]


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=5, max=15), DataRequired()])
    email = EmailField('Email Address', validators=[Email(), DataRequired()])
    phone_number = TelField('Phone number', validators=[Length(min=8, max=8)])
    first_name = StringField('First Name', validators=[Length(min=3, max=15)])
    last_name = StringField('Last Name', validators=[Length(min=3, max=15)])
    birthday = DateField('Birth Date')
    image = FileField('Upload account image')
    submit1 = SubmitField('Save Changes')


class UpdateSecurityForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[Length(min=5, max=15), DataRequired()])
    password1 = PasswordField("New Password", validators=[Length(min=5, max=15), DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[EqualTo(password1), DataRequired()])
    submit2 = SubmitField('Save Changes')


class ShippingAddressForm(FlaskForm):
    street_address = StringField(validators=[DataRequired()])
    country = CountrySelectField()
    postal = IntegerField(validators=[DataRequired()])
    submit4 = SubmitField('Save Changes')


class DeleteAccountForm(FlaskForm):
    submit3 = SubmitField('Confirm Delete')


class AddNewAccountForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=5, max=15), DataRequired()])
    email = EmailField('Email Address', validators=[Email(), DataRequired()])
    phone_number = TelField('Phone number', validators=[Length(min=8, max=8)])
    first_name = StringField('First Name', validators=[Length(min=3, max=15)])
    last_name = StringField('Last Name', validators=[Length(min=3, max=15)])
    password1 = PasswordField("New Password", validators=[Length(min=5, max=15), DataRequired()])
    account_type = SelectField(
        choices=[('customer', 'customer'), ('staff', 'staff')], validators=[DataRequired()])
    status = SelectField(
        choices=[('active', 'active'), ('deactivated', 'deactivated')], validators=[DataRequired()])

    submit1 = SubmitField('Save Changes')


class ContactUsForm(FlaskForm):
    email = EmailField(validators=[DataRequired(), Email()])
    subject = StringField(validators=[DataRequired()])
    message = TextAreaField(validators=[DataRequired()])
    submit = SubmitField()
