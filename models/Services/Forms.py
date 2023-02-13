from wtforms import Form, StringField, SelectField, TextAreaField, validators, DateField, SubmitField


class AddNewService(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])

    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')],
                         default='')
    service = SelectField('Service', [validators.DataRequired()],
                         choices=[('', 'Select'), ('1-Men-Hair Cut + Hair Wash', '1-Men-Hair Cut + Hair Wash'),
                                  ('2-Men-Basic Hair Cut', '2-Men-Basic Hair Cut'),
                                  ('3-Men-Hair Cut + Hair Wash + Hair Styling', '3-Men-Hair Cut + Hair Wash + Hair Styling'),
                                  ('4-Women-Hair Cut + Hair Wash','4-Women-Hair Cut + Hair Wash'),
                                  ('5-Women-Basic Hair Cut','5-Women-Basic Hair Cut'),
                                  ('6-Women-Hair Cut + Hair Wash + Hair Styling','6-Women-Hair Cut + Hair Wash + Hair Styling'),
                                  ('7-Hair Wash + Head Massage','7-Hair Wash + Head Massage'),
                                  ('8-Basic Hair Wash','8-Basic Hair Wash'),
                                  ('9-Hair Wash + Hair Styling','9-Hair Wash + Hair Styling'),
                                  ('10-Men-Hair Cut + Hairstyling','10-Men-Hair Cut + Hairstyling'),
                                  ('11-Men-Basic Hairstyling','11-Men-Basic Hairstyling'),
                                  ('12-Men-Hair Cut + Hair Wash + Hair Styling','12-Men-Hair Cut + Hair Wash + Hair Styling'),
                                  ('13-Women-Hair Wash+ HairStyling','13-Women-Hair Wash+ HairStyling'),
                                  ('14-Women-Basic Hairstyling','14-Women-Basic Hairstyling'),
                                  ('15-Women-Hair Cut + Hair Wash + Hair Styling','15-Women-Hair Cut + Hair Wash + Hair Styling'),
                                  ('16-Men-Hair Cut + Hair color','16-Men-Hair Cut + Hair color'),
                                  ('17-Men-All in one Package','17-Men-All in one Package'),
                                  ('18-Women-Hair Cut+ Hair Color','18-Women-Hair Cut+ Hair Color'),
                                  ('19-Women-All In one Package','19-Women-All In one Package') ],
                         default='')
    appointment_date = DateField('Appointment Date', format='%Y-%m-%d')
    appointment_time = SelectField('Appointment Time', [validators.DataRequired()],
                         choices=[('', 'Select'),('10','10am') ,('10.30','10.30am'),('11','11am'),('11.30','11.30am'),('12', '12.30Pm'), ('1', '1PM'),('1.30','1.30pm'),('2pm','2pm'),('2.30','2.30pm'),('3.30','3.30pm'),('4','4pm')],
                         default='')
    remarks = TextAreaField('Remarks', [validators.Optional()])
    submit = SubmitField('Book Appointment')

    def __init__(
            self,
            formdata=None,
            obj=None,
            prefix="",
            data=None,
            meta=None,
            **kwargs,
    ):
        super().__init__(formdata, obj, prefix, data, meta)


    def validate_on_submit(self):
        pass




