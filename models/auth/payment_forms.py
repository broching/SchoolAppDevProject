from wtforms import StringField, SubmitField, IntegerField, SelectField, RadioField
from wtforms.validators import Length, DataRequired
from flask_wtf import FlaskForm


class ProfileCreditCardForm(FlaskForm):
    card_number = IntegerField('Card Number', validators=[DataRequired()])
    card_holder = StringField('Card Holder', validators=[Length(min=5, max=30), DataRequired()])
    expiration_month = SelectField(
        choices=[('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'),
                 ('08', '08'),
                 ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12')], validators=[DataRequired()])
    expiration_year = SelectField(
        choices=[('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'),
                 ('29', '29'),
                 ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33')], validators=[DataRequired()])
    cvv = IntegerField('cvv', validators=[DataRequired()])

    street_address = StringField(validators=[DataRequired()])
    state = StringField(validators=[DataRequired()])
    postal = IntegerField(validators=[DataRequired()])

    submit = SubmitField('ADD CARD')


class DeleteCreditCardForm(FlaskForm):
    submit = SubmitField('Confirm Delete')


class MakeCardDefaultForm(FlaskForm):
    submit = SubmitField('Make Default')
