from flask import render_template, flash, redirect
from app.sparkQuery import sparkQuery
from app import app, sc
from app.search import searchForm
from app.spark import initSpark


# Home page


@app.route('/')
@app.route('/index')
def index():
    # Uncomment the below to show Hello Word
    # return "Hello, World!"
    user = {'username': 'Team Panda'}
    posts = [
        {
            'author': {'username': 'Test#1'},
            'body': 'Joker'
        },
        {
            'author': {'username': 'Test#2'},
            'body': 'Why so serious?'
        }
    ]

    # Below is the naive approach to render a webpage.
    #     return '''
    # <html>
    #     <head>
    #         <title>NYCDSA-Capstone-AirBnB</title>
    #     </head>
    #     <body>
    #         <h1>Hello, ''' + user['username'] + '''!</h1>
    #     </body>
    # </html>'''

    # Using template to render webpage
    # if True:
    # return render_template('index.html', title='Home', user=user)
    # else:
    # return render_template('index.html', user=user)

    # return loop
    return render_template('index.html', title='Home', user=user, posts=posts)


# Search page
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = searchForm()
    if form.validate_on_submit():
        flash('User choose to go from {0} to {1} \
            \n Start date is {2} and end date is {3} \
            \n Flexible with dates? {4}'
              .format(form.originCity.data, form.destiCity.data, form.startDate.data, form.endDate.data, form.felxibleDates.data))
        return redirect('/search')
    return render_template('search.html', title='Search', form=form)


# Spark page
@app.route('/spark', methods=['GET', 'POST'])
def spark():
    form = initSpark()
    # form2 = getRDDResults()
    if form.validate_on_submit():
        if form.genRDD.data:
            tempRDD = sparkQuery(sc=sc, upperLimit=form.upperLimRDD.data)
            flash('Populate Spark: There are {0} data points in the Spark!'.format(
                tempRDD.dataSet.count()))
        if form.moreThanTargetRDD:
            result = tempRDD.moreThan(form.moreTarget.data)
            flash('There are {0} numbers more than {1}'.format(
                result, form.moreTarget.data))
        if form.evenResultRDD:
            result = tempRDD.getEven()
            flash('The even numbers are{0}'.format(result))
        if form.oddResultRDD:
            result = tempRDD.getOdd()
            flash('The odd numbers are{0}'.format(result))
        else:
            pass

        return redirect('/spark')
    return render_template('spark.html', title='Spark', form=form)
