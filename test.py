from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    # return 'Sherry bae, thank you for taking care of me today!'
    return 'Hello World!'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)



<!-- {% block content %}
    <h1>Spark Test</h1>
    <form action="" method="post">
        {{ form.hidden_tag() }}
        <p>
            {{ form.upperLimRDD.label }}<br>
            {{ form.upperLimRDD(size=32) }}
        </p>

        <p>{{ form.genRDD() }}</p>

        <hr>
        <p>
            {{ form.moreTarget.label }}<br>
            {{ form.moreTarget(size=32) }}
        </p>

        <p>{{ form.moreThanTargetRDD() }}</p>

        <p>{{ form.evenResultRDD() }}</p>
        <p>{{ form.oddResultRDD() }}</p>

    </form1>
{% endblock %} -->