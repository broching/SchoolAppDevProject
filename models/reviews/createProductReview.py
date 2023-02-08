from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, validators, SelectField, IntegerField, FloatField, FileField, \
    RadioField, SubmitField


class CreateProductReview(Form):
    product_rating = RadioField('Product Rating', [validators.DataRequired()],
                                choices=[('1', '1'), ('2', '2'),
                                         ('3', '3'), ('4', '4'), ('5', '5')], default='')

    product_comment = TextAreaField('Write your review here', [validators.Length(max=10), validators.DataRequired()])

    product_image = FileField('Upload your image', [validators.Optional()])

    product_video = FileField('Upload your video', [validators.Optional()])
