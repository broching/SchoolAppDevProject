from flask_wtf import FlaskForm
from wtforms import TextAreaField, FileField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class CreateProductReviewTest(FlaskForm):
    product_rating = RadioField('Product Rating', [DataRequired()],
                                choices=[('1', '1'), ('2', '2'),
                                         ('3', '3'), ('4', '4'), ('5', '5')], default='')

    product_comment = TextAreaField('Write your review here', [Length(max=200), DataRequired()])

    product_image = FileField('Upload your image', [Optional()])

    product_video = FileField('Upload your video', [Optional()])

    submit_p = SubmitField('Submit')
