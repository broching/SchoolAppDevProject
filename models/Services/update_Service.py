from wtforms import Form, StringField, TextAreaField, validators, DateField, SelectField


class update_service_form(Form):
    service = SelectField('Service', [validators.DataRequired()],
                         choices=[('', 'Select'), ('1', 'Men-Hair Cut + Hair Wash'),
                                  ('2', 'Men-Basic Hair Cut'),
                                  ('3', 'Men-Hair Cut + Hair Wash + Hair Styling'),
                                  ('4','Women-Hair Cut + Hair Wash'),
                                  ('5','Women-Basic Hair Cut'),
                                  ('6','Women-Hair Cut + Hair Wash + Hair Styling'),
                                  ('7','Hair Wash + Head Massage'),
                                  ('8','Basic Hair Wash'),
                                  ('9','Hair Wash + Hair Styling'),
                                  ('10','Men-Hair Cut + Hairstyling'),
                                  ('11','Men-Basic Hairstyling'),
                                  ('12','Men-Hair Cut + Hair Wash + Hair Styling'),
                                  ('13','Women-Hair Wash+ HairStyling'),
                                  ('14','Women-Basic Hairstyling'),
                                  ('15','Women-Hair Cut + Hair Wash + Hair Styling'),
                                  ('16','Men-Hair Cut + Hair color'),
                                  ('17','Men-All in one Package'),
                                  ('18','Women-Hair Cut+ Hair Color'),
                                  ('19','Women-All In one Package') ],
                         default='')
    service_id = StringField('Service ID', [validators.Length(min=1, max=150), validators.DataRequired()])
    hairstylist = SelectField('hairstylist/barber', [validators.DataRequired()],
                         choices=[('', 'Select'), ('A', 'Alison'), ('J', 'Jennifer')],
                         default='')
    appointment_date = DateField('Appointment Date', format='%Y-%m-%d')
    appointment_time = StringField('Appointment Time', [validators.length(min=5, max=5), validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.Optional()])




