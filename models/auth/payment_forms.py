from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import Length, DataRequired
from flask_wtf import FlaskForm


class ProfileCreditCardForm(FlaskForm):
    card_number = IntegerField('Card Number', validators=[DataRequired()])
    card_holder = StringField('Card Holder', validators=[Length(min=5, max=30), DataRequired()])
    expiration_month = SelectField(
        choices=[(1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08'),
                 (9, '09'), (10, '10'), (11, '11'), (12, '12')], validators=[DataRequired()])
    expiration_year = SelectField(
        choices=[(1, '22'), (2, '23'), (3, '24'), (4, '25'), (5, '26'), (6, '27'), (7, '28'), (8, '29'),
                 (9, '30'), (10, '31'), (11, '32'), (12, '33')], validators=[DataRequired()])
    cvv = IntegerField('cvv', validators=[DataRequired()])
    submit = SubmitField('ADD CARD')
