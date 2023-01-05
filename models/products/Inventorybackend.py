from wtforms import Form, StringField, TextAreaField, validators, SelectField

# import id value from Product class from Product.py
from models.products.Product import Product


class CreateNewProduct(Form):
    product_name = StringField('Product name', [validators.Length(min=1, max=100), validators.DataRequired()])

    product_type = SelectField('Product type', [validators.DataRequired()], choices=[('', 'Select'), ('Shampoo', 'Shampoo'), ('Conditioner', 'Conditioner'), ('Hair', 'Hair products'), ('Shaving', 'Shaving products'), ('Others', 'Others')], default='')

    product_price = StringField('Price', [validators.Length(min=1), validators.DataRequired()])

    product_price_range = StringField('Price range', [validators.Length(min=1), validators.DataRequired()])

    product_quantity = StringField('Quantity', [validators.DataRequired()])

    product_description = TextAreaField('Description', [validators.Length(max=200), validators.Optional()])
    # description data is not required. 'validators.Optional'

    product_id = StringField('ID', [validators.DataRequired()], default=str(Product.count_id))
    # ^^^^^^ product ID holds a default value of 'count_id' class variable

    product_image = StringField('Image', [validators.DataRequired()])
