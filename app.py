from flask import Flask
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("./static/events.csv", parse_dates=["timestamp"], index_col=["id"])

@app.route('/')
def hello_world():  # put application's code here
    return pd.eval('df.groupby(df.timestamp.dt.day).count()').to_html()


if __name__ == '__main__':
    app.run()
