from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import HTTPException

from auth import login_required, savjetnik_required, admin_required

import Utilities

from constants import AccessLevels

from DatabaseController import DatabaseController, get_date_object
import DatabaseTables


accounts_bp = Blueprint('accounts', __name__, url_prefix='/accounts')


@accounts_bp.route('/list', methods=['GET'])
@login_required
@savjetnik_required
def list_accounts():
    db = DatabaseController()
    all_accounts = db.get_all_accounts()
    accounts_list = {}
    for account in sorted(all_accounts, key=lambda x: x[2]):
        access_level = AccessLevels.access_levels_string[int(account[2])]
        accounts_list[account[0]] = (account[1], access_level, account[3])

    return render_template('/accounts/list.html', accounts_list=accounts_list)


@accounts_bp.route('/edit_account/<account_id>', methods=['GET', 'POST'])
@login_required
@savjetnik_required
def edit_account(account_id):
    db = DatabaseController()
    account = db.get_row(DatabaseTables.KORISNICKI_RACUNI, 'id', account_id)
    if request.method == 'POST':
        username = request.form['username']
        access_level = request.form['level']
        section = request.form['section']

        error = None
        if username.strip() != account[1] and db.account_exists(username):
            error = "Korisnički račun %s je već registriran"

        if error is None:
            db.edit_user_account(account_id, (username, access_level, section))
            flash('Podaci o korisničkom računu su uspješno spremljeni!', 'success')
            return redirect(url_for('accounts.list_accounts'))

        flash(error, 'danger')

    all_access_levels = AccessLevels.access_levels_string
    sections = Utilities.sections_and_teams
    account_info = (account[1],) + account[3:]
    return render_template('/accounts/edit.html', account=account_info,
                           account_id=account_id, levels=all_access_levels, sections=sections)

