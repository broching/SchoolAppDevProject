from wtforms import Form, StringField, SelectField, TextAreaField, validators


class AddNewService(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])

    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')],
                         default='')

    membership_ID = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    Appointment_Date = StringField('Appointment Date', [validators.Length(min=8, max=8), validators.DataRequired()])
    Appointment_Time = StringField('Appointment Time', [validators.length(min=4, max=4), validators.DataRequired()])


remarks = TextAreaField('Remarks', [validators.Optional()])
