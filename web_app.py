from flask import Flask, render_template, redirect, flash, request, session, url_for
from DatabaseController import DatabaseController
import DatabaseTables

from werkzeug.security import check_password_hash

import datetime
from auth import auth_bp
from members import members_bp

app = Flask(__name__)
app.config.from_mapping(
        SECRET_KEY='dev',
    )

app.register_blueprint(auth_bp)
app.register_blueprint(members_bp)

DatabaseController().init_tables()


@app.route('/', methods = ['GET'])
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

    return render_template("index.html", list_records=total_activity)


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
            session["access_level"] = user[3]  # user[3] - access level
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


if __name__ == '__main__':
   app.run(debug=True)
