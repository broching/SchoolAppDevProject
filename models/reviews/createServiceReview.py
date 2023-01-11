from wtforms import Form, StringField, TextAreaField, validators, SelectField, IntegerField, FloatField, FileField

from models.reviews.serviceReview import serviceReview


class CreateServiceReview(Form):
    service_id = IntegerField('Service ID', [validators.DataRequired()])

    service_rating = IntegerField('Service Rating', [validators.DataRequired()])

    service_comment = TextAreaField('Write your review here', [validators.Optional()])

    service_image = FileField('Upload your image', [validators.Optional()])

    service_video = FileField('Upload your video', [validators.Optional()])
