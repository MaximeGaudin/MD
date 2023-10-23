import os.path
import urllib.request
from urllib.error import HTTPError

import pandas as pd
import psycopg2
from flask import Flask, request

app = Flask(__name__)

# Quick & dirty dataframe cache to ensure you don't have to download & parse the file each time
dataframes = {}


def getDbConnection():
    conn = psycopg2.connect(host='localhost',
                            database='madkudu',
                            user="mgaudin",
                            password=os.environ['DB_PASSWORD'])
    return conn


def getDataframeFromCacheOrDownload(year, month):
    key = "{}{}".format(year, month)
    try:
        return dataframes[key]
    except KeyError:
        dataframes[key] = pd.read_csv(fetchFileIfNotAlreadyDownloaded(year, month), parse_dates=["timestamp"], index_col=["id"])
        return dataframes[key]


def fetchFileIfNotAlreadyDownloaded(year, month):
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
        df = getDataframeFromCacheOrDownload(year, month)
        # I did not had time to explore it further but this method is limited to one-liner
        # Handling more complex pandas script would required an "eval" call
        return pd.eval(query).to_json()
    except HTTPError:
        return "Requested Year/Month does not exist", 404
    except Exception as error:
        print(error)
        return str(error), 400


@app.route('/queries', methods=["GET"])
def getAllQueries():
    conn = getDbConnection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, query FROM analyses;')
    analyses = cur.fetchall()
    cur.close()
    conn.close()

    return list(map(lambda a: {
        "id": a[0],
        "name": a[1],
        "query": a[2]
    }, analyses))


@app.route('/queries', methods=["POST"])
def saveQuery():
    try:
        name = request.json['name']
        query = request.json['query']

        conn = getDbConnection()
        cur = conn.cursor()
        cur.execute('INSERT INTO analyses (name, query)'
                    'VALUES (%s, %s)',
                    (name, query))
        conn.commit()
        cur.close()
        conn.close()

        return "", 200
    except Exception as error:
        return str(error), 400


@app.route('/queries/<id>', methods=["DELETE"])
def deleteQuery(id):
    try:
        conn = getDbConnection()
        cur = conn.cursor()
        cur.execute('DELETE FROM analyses WHERE id = %s', (id,))
        conn.commit()
        cur.close()
        conn.close()

        return "", 200
    except Exception as error:
        return str(error), 400


if __name__ == '__main__':
    app.run()
