from flask import Flask, jsonify, render_template
import db
import sys
import pytz


app = Flask(__name__)

@app.route('/last.json')
def last():
    last_snapshot = db.get_last_snapshot()
    return jsonify(last_snapshot["members"])

@app.route('/')
def home():
    last_snapshot = db.get_last_snapshot()
    return render_template('home.html', snapshot = last_snapshot)

def format_datetime(value):
    timezoneLocal = pytz.timezone('Europe/Prague')
    return pytz.utc.localize(value).astimezone(timezoneLocal).strftime('%-d.%-m.%Y %-H:%M')

app.jinja_env.filters['datetime'] = format_datetime

if __name__ == '__main__':
    if((len(sys.argv) > 1) and (sys.argv[1] == "dump")):
        print("* dumping index.html")
        open("build/index.html", "w+").write(app.test_client().get('/').get_data().decode("utf-8"))
        print("* dumping last.json")
        open("build/last.json", "w+").write(app.test_client().get('/last.json').get_data().decode("utf-8"))
    else:
        app.run()
