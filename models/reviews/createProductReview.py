from wtforms import Form, StringField, TextAreaField, validators, SelectField, IntegerField, FloatField, FileField

from models.reviews.productReview import productReview


class CreateProductReview(Form):
    product_rating = SelectField('Product Rating', [validators.DataRequired()],
                                 choices=[('', 'Rate Product from 1 (Lowest) to 5 (Highest)'), ('1', '1'), ('2', '2'),
                                          ('3', '3'), ('4', '4'), ('5', '5')], default='')

    product_comment = TextAreaField('Write your review here', [validators.Optional()])

    product_image = FileField('Upload your image', [validators.Optional()])

    product_video = FileField('Upload your video', [validators.Optional()])
