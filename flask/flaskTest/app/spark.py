from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


class initSpark(FlaskForm):

    # Generate a Spark and populate it.
    upperLimRDD = IntegerField("Upper limit", validators=[DataRequired()])

    # Generate RDD
    genRDD = SubmitField('Generate!')


class getRDDResults(FlaskForm):
    # Select number more than.
    moreTarget = IntegerField(
        "More than: ", validators=[DataRequired()])
    moreThanTargetRDD = SubmitField('Get all numbers more than the target')
    evenResultRDD = SubmitField('Get all EVEN numbers')
    oddResultRDD = SubmitField('Get all ODD numbers')
