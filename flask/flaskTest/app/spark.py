from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


class initSpark(FlaskForm):

    # Generate a Spark and populate it.
    upperLimRDD = IntegerField(
        "Upper limit", default=10, validators=[DataRequired()])

    # Generate RDD
    genRDD = SubmitField('Generate!')

    # Select number more than 'TARGET' and show all result values..
    moreTarget = IntegerField(
        "More than: ", default=5,  validators=[DataRequired()])
    moreThanTargetRDD = SubmitField('Get all numbers more than the target')

    # Get all even results
    evenResultRDD = SubmitField('Get all EVEN numbers')

    # Get all odd results
    oddResultRDD = SubmitField('Get all ODD numbers')


# class getRDDResults(FlaskForm):
#     # Select number more than.
#     moreTarget = IntegerField(
#         "More than: ", validators=[DataRequired()])
#     moreThanTargetRDD = SubmitField('Get all numbers more than the target')
#     evenResultRDD = SubmitField('Get all EVEN numbers')
#     oddResultRDD = SubmitField('Get all ODD numbers')
