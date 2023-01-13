from wtforms import Form, StringField, TextAreaField, validators


class update_service_form(Form):
    service = StringField('Service', [validators.Length(min=1, max=150), validators.DataRequired()])
    service_id = StringField('Service ID', [validators.Length(min=1, max=150), validators.DataRequired()])
    hairstylist = StringField('Hairstylist/barber', [validators.Length(min=1, max=150), validators.DataRequired()])
    appointment_date = StringField('Appointment Date', [validators.Length(min=8, max=8), validators.DataRequired()])
    appointment_time = StringField('Appointment Time', [validators.length(min=5, max=5), validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.Optional()])
