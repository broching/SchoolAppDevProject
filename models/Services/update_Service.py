from wtforms import Form, StringField,TextAreaField, validators


class update_service(Form):
    service = StringField('Service', [validators.Length(min=1, max=150), validators.DataRequired()])

    hairstylist = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    appointment_date = StringField('Appointment Date', [validators.Length(min=8, max=8), validators.DataRequired()])
    appointment_time = StringField('Appointment Time', [validators.length(min=5, max=5), validators.DataRequired()])

    remarks = TextAreaField('Remarks', [validators.Optional()])
