from wtforms import Form, StringField, SelectField, TextAreaField, validators, DateField


class AddNewService(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])

    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')],
                         default='')
    appointment_date = DateField('Appointment Date', format='%Y-%m-%d')
    appointment_time = StringField('Appointment Time', [validators.length(min=5, max=5), validators.DataRequired()])

    remarks = TextAreaField('Remarks', [validators.Optional()])

    def validate_on_submit(self):
        pass


