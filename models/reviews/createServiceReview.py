from wtforms import Form, StringField, TextAreaField, validators, SelectField, RadioField, FloatField, FileField, \
    HiddenField


class CreateServiceReview(Form):
    user_id = HiddenField('')

    user_name = HiddenField('')

    service_selection = SelectField('Service', [validators.DataRequired()],
                                    choices=[('', 'Click to choose your service'), ('Hair Cut', 'Hair Cut'),
                                             ('Hair Styling', 'Hair Styling'),
                                             ('Hair Dye', 'Hair Dye')], default='')

    stylist_selection = SelectField('Stylist', [validators.DataRequired()],
                                    choices=[('', 'Click to choose your hairstylist'),
                                             ('Hairstylist 1', 'Hairstylist 1'),
                                             ('Hairstylist 2', 'Hairstylist 2'),
                                             ('Hairstylist 3', 'Hairstylist 3')], default='')

    service_rating = RadioField('Service Rating', [validators.DataRequired()],
                                choices=[('1', '1'), ('22', '2'),
                                         ('3', '3'), ('4', '4'), ('5', '5')], default='')

    service_comment = TextAreaField('Write your review here', [validators.Optional()])

    service_image = FileField('Upload your image', [validators.Optional()])

    service_video = FileField('Upload your video', [validators.Optional()])
