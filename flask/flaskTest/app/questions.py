from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateField, RadioField, SelectField, validators
from wtforms.validators import DataRequired





class questionForm(FlaskForm):
    attrList = [('Museums', 'Museums'), ('Restaurants', 'Restaurants'),
                ('Shopping', 'Shopping'), ('Parks', 'Parks'),
                ('Bars', 'Bars'), ('Music', 'Music')]
    imporList = []
    # Attracts you
    Museums = BooleanField('Museums')
    qAttractions = SelectField('What attracts you?', choices=attrList,
                render_kw={"multiple": "multiple", "data-tags": "1"}, validators=[DataRequired()])

    # Options important to you

    # Anything special
    qSpecialNeeds = StringField('Special Needs:', validators=[DataRequired()])

    # Choose sytle
    qStyle = RadioField('Choose a style', choices=[
                        ('Classic', 'Classic'), ('Modern', 'Modern')], validators=(validators.Optional(),))
   # example = RadioField('Label', choices=[('value','description'),('value_two','whatever')])
    # Panda GOGOGO
    qSearch = SubmitField('PandaGO!')
    # # Select dates
    # startDate = DateField('Start Date', format='%m/%d/%Y',
    #                       validators=(validators.Optional(),))
    # endDate = DateField('End Date', format='%m/%d/%Y',
    #                     validators=(validators.Optional(),))

    # Flexible dates?
    # felxibleDates = BooleanField('+/- 3 days?')
