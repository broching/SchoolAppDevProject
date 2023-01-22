from wtforms import Form, StringField, TextAreaField, validators, SelectField, IntegerField, FloatField, FileField, \
    DateField, MultipleFileField
from datetime import datetime


def validate():
    if not validators.DataRequired():
        raise "Please enter required data."


def validate_expiry(form, field):
    if field.data < datetime.now():
        raise validators.ValidationError("Your card has expired")


class CreateNewProduct(Form):
    product_name = StringField('Product name', [validators.Length(min=1, max=100), validators.DataRequired()])

    product_type = SelectField('Product type', [validators.DataRequired()],
                               choices=[('', 'Select'), ('Shampoo', 'Shampoo'), ('Conditioner', 'Conditioner'),
                                        ('Hair', 'Hair products'), ('Shaving', 'Shaving products'),
                                        ('Others', 'Others')], default='')

    product_price = FloatField('Price ($)', [validators.DataRequired()], default='0')

    product_quantity = IntegerField('Quantity', [validators.DataRequired()])

    product_description = TextAreaField('Description', [validators.Length(max=200), validators.Optional()])
    # description data is not required. 'validators.Optional'

    product_cost = FloatField('Cost ($)', [validators.DataRequired()], default=0)

    product_image = StringField('Image', [validators.DataRequired()])

    images = MultipleFileField("Product image", [
        # validators.DataRequired(message="Image is required")
    ])


class PaymentForm(Form):
    card_no = IntegerField('Card details',
                           [validators.DataRequired()])

    expiry = DateField('Expiry Date', [validators.DataRequired()])

    cvv = IntegerField('CVV', [validators.DataRequired()])

    name = StringField('Name on Card', [validators.DataRequired()])

    address = StringField('Billing Address', [validators.DataRequired()])

    postal_code = IntegerField('Postal code', [validators.DataRequired()])

