from wtforms import Form, StringField, TextAreaField, validators, SelectField, IntegerField, FloatField, FileField

from models.reviews.productReview import productReview


class CreateProductReview(Form):
    product_rating = IntegerField('Product Rating', [validators.DataRequired()])

    product_comment = TextAreaField('Write your review here', [validators.Optional()])

    product_image = FileField('Upload your image', [validators.Optional()])

    product_video = FileField('Upload your video', [validators.Optional()])
