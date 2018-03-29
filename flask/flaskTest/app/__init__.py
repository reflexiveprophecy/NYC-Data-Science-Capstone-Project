from flask import Flask
from config import Config
from NLPPipeLine import doc2vec
# from pyspark import SparkContext

# sc = SparkContext("local", "Simple App")
app = Flask(__name__)
app.config.from_object(Config)


from app import routes


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
