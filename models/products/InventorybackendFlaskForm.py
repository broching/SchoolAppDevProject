from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, FloatField, FileField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from datetime import datetime


class CreateNewProduct(FlaskForm):
    product_name = StringField('Product name', [Length(min=1, max=100), DataRequired()])
    product_type = SelectField('Product type', [DataRequired()],
                               choices=[('', 'Select'), ('Shampoo', 'Shampoo'), ('Conditioner', 'Conditioner'),
                                        ('Hair', 'Hair products'), ('Shaving', 'Shaving products'),
                                        ('Others', 'Others')], default='')
    product_price = FloatField('Price ($)', [DataRequired()], default='0')
    product_quantity = IntegerField('Quantity', [DataRequired()])
    product_description = TextAreaField('Description', [Length(max=200), Optional()])
    product_cost = FloatField('Cost ($)', [DataRequired()], default=0)
    product_image = FileField("Product image", validators=[DataRequired()])
    submit1 = SubmitField('Submit')


class UpdateNewProduct(FlaskForm):
    product_name = StringField('Product name', [Length(min=1, max=100), DataRequired()])
    product_type = SelectField('Product type', [DataRequired()],
                               choices=[('', 'Select'), ('Shampoo', 'Shampoo'), ('Conditioner', 'Conditioner'),
                                        ('Hair', 'Hair products'), ('Shaving', 'Shaving products'),
                                        ('Others', 'Others')], default='')
    product_price = FloatField('Price ($)', [DataRequired()], default='0')
    product_quantity = IntegerField('Quantity', [DataRequired()])
    product_description = TextAreaField('Description', [Length(max=200), Optional()])
    product_cost = FloatField('Cost ($)', [DataRequired()], default=0)
    product_image = FileField("Product image", validators=[Optional()])
    submit1 = SubmitField('Submit')

class PaymentForm(FlaskForm):
    card_no = IntegerField('Card details', [DataRequired()])
    expiry = DateField('Expiry Date', [DataRequired()])
    cvv = IntegerField('CVV', [DataRequired()])
    name = StringField('Name on Card', [DataRequired()])
    address = StringField('Billing Address', [DataRequired()])
    postal_code = IntegerField('Postal code', [DataRequired()])
