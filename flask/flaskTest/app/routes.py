from flask import render_template, flash, redirect, session, request
# from app.sparkQuery import sparkQuery
from app import app, doc2vec  # , sc
from app.search import searchForm
# from app.spark import initSpark
from app.questions import questionForm
# from app.NLPPipeLine import doc2vec


# Home page


@app.route('/')
@app.route('/index')
def index():
    # Uncomment the below to show Hello Word
    # return "Hello, World!"
    user = {'username': 'Team Panda'}
    posts = [
        {
            'author': {'username': 'Test#12'},
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
def sparkTest():
    return render_template('spark.html', title='Under Development')
# def spark():
#     # form = initSpark()
#     # form2 = getRDDResults()
#     # if form.validate_on_submit():
#     #     if form.genRDD.data:
#     #         tempRDD = sparkQuery(sc=sc, upperLimit=form.upperLimRDD.data)
#     #         flash('Populate Spark: There are {0} data points in the Spark!'.format(
#     #             tempRDD.dataSet.count()))
#     #     if form.moreThanTargetRDD:
#     #         result = tempRDD.moreThan(form.moreTarget.data)
#     #         flash('There are {0} numbers more than {1}'.format(
#     #             result, form.moreTarget.data))
#     #     if form.evenResultRDD:
#     #         result = tempRDD.getEven()
#     #         flash('The even numbers are{0}'.format(result))
#     #     if form.oddResultRDD:
#     #         result = tempRDD.getOdd()
#     #         flash('The odd numbers are{0}'.format(result))
#     #     else:
#     #         pass

#     #     return redirect('/spark')

#     # return render_template('spark.html', title='Spark', form=form)
#     return render_template('spark.html')


keyWords = {'Museums': ['museum', 'art', 'culture', 'history'],
            'Restaurants': ['restaurant', 'food', 'delicious'],
            'Shopping': ['shopping', 'clothing', 'mall'],
            'Parks': ['central park', 'forest', 'nature'],
            'Bars': ['bar', 'club', 'party', 'beer'],
            'Music': ['music' 'venue', 'artist'],
            'Location': ['location'],
            'Close to Subway': ['close subway'],
            'Bringing my Pet': ['pet friendly'],
            'King bed': ['king bed', 'queen bed'],
            'Queen bed': ['queen bed'],
            'Kitchen': ['kitchen'],
            'Parking': ['parking'],
            'Handicap': ['handicap'],
            'Classic': ['classic', 'historic', 'antique'],
            'Modern': ['modern', 'stylish', 'new', 'renovated']}


@app.route('/questions',  methods=['GET', 'POST'])
def questions():
    #form = questionForm()
    # # session['getInputString'] = 'museum art shopping venue close subway'
    # # return redirect(url_for('b'))
    # if form.validate_on_submit():
    #     tempList = []
    #     tempList.append(form.qSpecialNeeds.data)
    #     tempList.extend(keyWords[form.qStyle.data])
    #     tempList.extend(keyWords[form.qAttractions.data])

    #     tempString = form.qSpecialNeeds.data + form.qStyle.data + form.qAttractions.data
    #     print(form.qSpecialNeeds.data)
    #     print(form.qStyle.data)
    #     flash(' '.join(tempList))
    if request.method == "POST":
        if request.form['submit'] == 'submit':
            value1 = request.form.getlist('attraction')
            value2 = request.form.getlist('specialInput')
            final = []
            for item in value1:
                final.extend(keyWords[item])
            for item in value2:
                final.append(item)

            #flash(final) 

            finalString = ' '.join(final)
            session['getInputString'] = finalString
        
            return redirect('/results')

    return render_template('question.html', title='Question')


test1 = 'museum art shopping venue close subway'
list1 = ['id', 'name', 'summary', 'property_type', 'room_type',
    'neighbourhood_group_cleansed', 'price', 'price_good']


@app.route('/results',  methods=['GET', 'POST'])
def result():
    test = session.get('getInputString', None)
    flash('Based on your results, the Panda guesses:" {} "are important.'.format(test))
    tempResult = doc2vec(test1)
    tempResult = tempResult[list1]
    tempResult.sort_index(inplace=True)
    tempResult.set_index(['id'], inplace=True)
    tempResult.index.name = None

    return render_template('result.html', tables=[tempResult.to_html()], titles=['Result'])
    # return str(result)

@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if request.method == "POST":
        if request.form['submit'] == 'submit':
            value = request.form.getlist('att')
            session['budget'] = value
            flash(value) 
            print(value)
    # return redirect('/')
    return render_template('budget.html', title='Budget Example')


@app.route('/andrew', methods=['GET', 'POST'])
def andrew():
    # Uncomment the below to show Hello Word
    # return "Hello, World!"
    user = {'username': 'Team Panda'}
    posts = [
        {
            'author': {'username': 'Test#12'},
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
    return render_template('andrew.html', title='SpecialTreat', user=user, posts=posts)
