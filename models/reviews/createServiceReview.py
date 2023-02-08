from wtforms import Form, StringField, TextAreaField, validators, SelectField, IntegerField, FloatField, FileField

from models.reviews.serviceReview import serviceReview


class CreateServiceReview(Form):
    service_selection = SelectField('Service', [validators.DataRequired()],
                                    choices=[('', 'Click to choose your service'), ('Hair Wash', 'Hair Wash'),
                                             ('Hair Styling', 'Hair Styling'),
                                             ('Hair Dye', 'Hair Dye')], default='')

    service_rating = IntegerField('Service Rating', [validators.DataRequired()])

    service_comment = TextAreaField('Write your review here', [validators.Optional()])

    service_image = FileField('Upload your image', [validators.DataRequired()])

    service_video = FileField('Upload your video', [validators.Optional()])
