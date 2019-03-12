from flask import Flask, render_template, redirect
from DatabaseController import DatabaseController
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    db = DatabaseController()
    start_date = datetime.datetime(2019, 2, 1)
    end_date = datetime.datetime(2019, 3, 15)
    activity = db.get_period_activity(start_date, end_date)
    total_activity = {}
    for item in activity:
        key = "%s %s" % (item[0], item[1])
        if key not in total_activity:
            total_activity[key] = 0
        total_activity[key] += item[2] * item[3]
    return render_template("index.html", list_records = {})

if __name__ == '__main__':
   app.run(debug = True)