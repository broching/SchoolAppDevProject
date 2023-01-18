import shelve

from wtforms import Form, StringField, TextAreaField, validators, SelectField, IntegerField, FloatField, FileField


class CreateNewProduct(Form):
    product_name = StringField('Product name', [validators.Length(min=1, max=100), validators.DataRequired()])

    product_type = SelectField('Product type', [validators.DataRequired()],
                               choices=[('', 'Select'), ('Shampoo', 'Shampoo'), ('Conditioner', 'Conditioner'),
                                        ('Hair', 'Hair products'), ('Shaving', 'Shaving products'),
                                        ('Others', 'Others')], default='')

    product_price = FloatField('Price', [validators.DataRequired()], default='0')

    product_price_range = SelectField('Price range', [validators.DataRequired()],
                                      choices=[('', 'Select'), ('0-9', '$0 to $9'), ('10-19', '$10-$19'),
                                               ('20-29', '$20-$29'), ('30-39', '$30-$39'), ('40-49', '$40-$49'),
                                               ('50-59', '$50-$59'), ('above60', '$60 and above')], default='')

    product_quantity = IntegerField('Quantity', [validators.DataRequired()])

    product_description = TextAreaField('Description', [validators.Length(max=200), validators.Optional()])
    # description data is not required. 'validators.Optional'

    product_cost = FloatField('Cost', [validators.DataRequired()], default=0)

    product_image = FileField('Image', [validators.DataRequired()])
