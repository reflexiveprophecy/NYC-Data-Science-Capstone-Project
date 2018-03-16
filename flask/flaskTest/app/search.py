from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateField, validators
from wtforms.validators import DataRequired


class searchForm(FlaskForm):

    # From and To cities
    originCity = StringField('From:', validators=[DataRequired()])
    destiCity = StringField('To:', validators=[DataRequired()])

    # Select dates
    startDate = DateField('Start Date', format='%m/%d/%Y',
                          validators=(validators.Optional(),))
    endDate = DateField('End Date', format='%m/%d/%Y',
                        validators=(validators.Optional(),))

    # Flexible dates?
    felxibleDates = BooleanField('+/- 3 days?')
    search = SubmitField('Find me a room!')
