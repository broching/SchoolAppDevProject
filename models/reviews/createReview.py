from wtforms import Form, StringField, TextAreaField, validators, SelectField, IntegerField, FloatField, FileField

from models.reviews.Review import Review


class CreateNewReview(Form):
    rating = IntegerField('Product/Service Rating', [validators.DataRequired()])

    comment = TextAreaField('Write your review here', [validators.Optional()])

    image = FileField('Upload your image', [validators.Optional()])

    video = FileField('Upload your video', [validators.Optional()])
