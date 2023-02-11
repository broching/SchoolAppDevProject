from wtforms import Form, StringField, TextAreaField, validators, SelectField, FloatField, FileField, \
    RadioField, SubmitField, HiddenField


class CreateProductReview(Form):
    user_name = HiddenField('')

    user_id = HiddenField('')

    product_selection = SelectField('Product', [validators.DataRequired()],
                                    choices=[('', 'Click to select your product'), ('Product 1', 'Product 1'),
                                             ('Product 2', 'Product 2'),
                                             ('Product 3', 'Product 3')], default='')

    product_rating = RadioField('Product Rating', [validators.DataRequired()],
                                choices=[('1', '1'), ('22', '2'),
                                         ('3', '3'), ('4', '4'), ('5', '5')], default='')

    product_comment = TextAreaField('Write your review here', [validators.Length(max=200), validators.DataRequired()])

    product_image = FileField('Upload your image', [validators.Optional()])

    product_video = FileField('Upload your video', [validators.Optional()])
