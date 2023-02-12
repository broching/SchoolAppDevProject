from wtforms import Form, StringField, TextAreaField, validators, DateField, SelectField


class update_service_form(Form):
    service = SelectField('Service', [validators.DataRequired()],
                         choices=[('', 'Select'), ('1', 'Haircut'), ('2', 'Hairwash')],
                         default='')
    service_id = StringField('Service ID', [validators.Length(min=1, max=150), validators.DataRequired()])
    hairstylist = SelectField('hairstylist/barber', [validators.DataRequired()],
                         choices=[('', 'Select'), ('AB', 'Alison'), ('J', 'Jennifer')],
                         default='')
    appointment_date = DateField('Appointment Date', format='%Y-%m-%d')
    appointment_time = StringField('Appointment Time', [validators.length(min=5, max=5), validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.Optional()])




