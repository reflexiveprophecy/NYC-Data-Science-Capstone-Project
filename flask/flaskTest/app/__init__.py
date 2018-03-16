from flask import Flask
from config import Config
from pyspark import SparkContext

sc = SparkContext("local", "Simple App")
app = Flask(__name__)
app.config.from_object(Config)


from app import routes

