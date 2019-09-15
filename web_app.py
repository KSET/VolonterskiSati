from flask import Flask, render_template, redirect, flash, request, session, url_for
from DatabaseController import DatabaseController
import DatabaseTables

from werkzeug.security import check_password_hash

import datetime
from auth import auth_bp
from members import members_bp
from activities import activities_bp
from statistics import statistics_bp
from accounts import accounts_bp

app = Flask(__name__)
app.config.from_mapping(
        SECRET_KEY='dev',
    )

app.register_blueprint(auth_bp)
app.register_blueprint(members_bp)
app.register_blueprint(activities_bp)
app.register_blueprint(statistics_bp)
app.register_blueprint(accounts_bp)

DatabaseController().init_tables()


@app.route('/', methods=['GET'])
def index():
    db = DatabaseController()
    start_date = datetime.datetime.today().replace(day=1).date()
    end_date = datetime.datetime.today().replace(month=datetime.datetime.today().month + 1, day=1).date()
    members_activity = db.get_period_activity(start_date, end_date)
    total_activity = {}
    member_names = {}
    for member in members_activity:
        key = member[0]
        if key not in total_activity:
            total_activity[key] = 0
        total_activity[key] += member[3]  # Beztežinski sati
        member_names[key] = "%s %s" % (member[1], member[2])

    sorted_list = sorted(total_activity.items(), reverse=True, key=lambda x: x[1])

    sorted_activity = {}
    for k, v in sorted_list:
        sorted_activity[k] = v

    return render_template("index.html", list_records=sorted_activity, names=member_names)


@app.route('/', methods=['POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        db = DatabaseController()

        error = None
        user = db.get_row(DatabaseTables.KORISNICKI_RACUNI, 'username', username)

        if user is None:
            error = 'Incorrect username or password.'
        elif not check_password_hash(user[2], password):  # user[2] - password
            error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session["user_id"] = user[0]  # user[0] - id
            session["username"] = user[1]  # user[1] - username
            session["access_level"] = int(user[3])  # user[3] - access level
            session["section"] = user[4]  # user[4] - sekcija
            return redirect(url_for('index'))

        flash(error)

    return render_template('index.html')


if __name__ == '__main__':
   app.run(debug=True)
