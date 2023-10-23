import pandas as pd
from flask import Flask, request

app = Flask(__name__)

df = pd.read_csv("./static/events.csv", parse_dates=["timestamp"], index_col=["id"])


@app.route('/query', methods=["POST"])
def runQuery():
    year = request.json['year']
    month = request.json['month']
    query = request.json['query']

    return pd.eval(query).to_json()


if __name__ == '__main__':
    app.run()
