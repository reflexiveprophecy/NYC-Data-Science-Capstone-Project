import sys
try:
    from pyspark import SparkContext
    print("PySpark loaded")
except ImportError as e:
    print("Fail to import PySpark {0}".format(e))

import sys
# sys.path.insert(0, '/Users/roger/anaconda3/lib/python3.6/site-packages/python')
# sys.path.insert(1, '/Users/roger/anaconda3/lib/python3.6/site-packages/python/lib/py4j-0.10.6-src.zip')
# print(sys.path)


# ###
# _sc = SparkContext('local[*]', 'nameOfYourSparkContext')
# _data = range(0, 100)
# _rdd = _sc.parallelize(_data)
###

"""Perform your operations on _rdd such as .map(), .collect()
"""
#_sc.close()
sc = SparkContext('local')

from flask import Flask, request
app = Flask(__name__)


@app.route('/', methods=['POST'])  # can set first param to '/'

def hello():
    return "Hello World!"

def toyFunction():
    posted_data = sc.parallelize([request.get_data()])
    return str(posted_data.collect()[0])

if __name__ == '__main_':
    app.run(port=8080)