import functools
import access_levels

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash

from DatabaseController import DatabaseController
import DatabaseTables

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sekcija = request.form['section']

        db = DatabaseController()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not sekcija:
            error = 'Sekcija value is required.'
        elif db.account_exists(username):
            error = 'User {} is already registered.'.format(username)

        if error is None:
            entry_values = (username, generate_password_hash(password), access_levels.SAVJETNIK, sekcija)
            db.add_user_account(entry_values)
            flash("Racun uspješno napravljen!", 'success')
            return redirect(url_for('index'))

        flash(error, 'error')

    return render_template('auth/register.html')


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = DatabaseController().get_row(DatabaseTables.KORISNICKI_RACUNI, 'id', user_id)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
