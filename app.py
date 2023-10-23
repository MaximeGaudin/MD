import os.path
import urllib.request
from urllib.error import HTTPError

import pandas as pd
from flask import Flask, request

app = Flask(__name__)

dataframes = {}


def getDataframe(year, month):
    key = "{}{}".format(year, month)
    try:
        return dataframes[key]
    except KeyError:
        dataframes[key] = pd.read_csv(fetchFile(year, month), parse_dates=["timestamp"], index_col=["id"])
        return dataframes[key]


def fetchFile(year, month):
    outputFile = "./static/{}-{}.csv".format(year, f'{month:02}')

    if os.path.isfile(outputFile):
        return outputFile

    url = "https://work-sample-mk.s3.amazonaws.com/{}/{}/events.csv".format(year, f'{month:02}')

    urllib.request.urlretrieve(url, outputFile)
    return outputFile


@app.route('/query', methods=["POST"])
def runQuery():
    year = request.json['year']
    month = request.json['month']
    query = request.json['query']

    try:
        df = getDataframe(year, month)
        return pd.eval(query).to_json()
    except HTTPError:
        return "Requested Year/Month does not exist", 404
    except Exception as error:
        return str(error), 400


if __name__ == '__main__':
    app.run()
