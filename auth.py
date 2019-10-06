import functools
from constants import AccessLevels

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash

from DatabaseController import DatabaseController
import DatabaseTables
from constants import InviteCodes

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def __get_assinged_role(invite_code):
    for access_level_hash, access_level in InviteCodes.invite_codes_roles.items():
        if check_password_hash(access_level_hash, invite_code):
            return access_level
    return None


@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        invite_code = request.form['invite_code']
        sekcija = request.form['section']

        db = DatabaseController()
        error = None

        assigned_role = __get_assinged_role(invite_code)

        # print([check_password_hash(x, invite_code) for x in InviteCodes.INVITE_CODES_LIST])
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif assigned_role is None:
            error = 'Invite code is invalid'
        elif not sekcija:
            error = 'Sekcija value is required.'
        elif db.account_exists(username):
            error = 'User {} is already registered.'.format(username)

        if error is None:
            entry_values = (username, generate_password_hash(password), assigned_role, sekcija)
            db.add_user_account(entry_values)
            flash("Racun %s sa ovlasti %s uspješno napravljen!" % (username, AccessLevels.access_levels_string[assigned_role]), 'success')
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
            flash("Nedozvoljen pristup linku. Morate se ulogirati!", "danger")
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapped_view


def savjetnik_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session['access_level'] > AccessLevels.SAVJETNIK:
            flash("Nemate ovlasti za pristup linku!", "danger")
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapped_view


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session['access_level'] > AccessLevels.ADMIN:
            flash("Nemate ovlasti za pristup linku!", "danger")
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapped_view
