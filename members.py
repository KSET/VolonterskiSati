from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import HTTPException

from auth import login_required, savjetnik_required, admin_required

import access_levels
import Utilities

from DatabaseController import DatabaseController, get_date_object
import DatabaseTables


members_bp = Blueprint('members', __name__, url_prefix='/members')


@members_bp.route('/add', methods=('GET', 'POST'))
@login_required
@savjetnik_required
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['lastname']
        nickname = request.form['nickname']
        oib = request.form['oib']
        phone_number = request.form['phone']
        date_of_birth = request.form['dateofbirth']
        membership_start = request.form['membership']
        card_id = request.form['idcard']
        email = request.form['email']
        try:
            section = request.form['section']
        except HTTPException:
            section = session['section']

        db = DatabaseController()
        error = None

        if not name:
            error = 'Username is required.'
        if not last_name:
            error = 'Password is required.'
        if not nickname:
            nickname = '-'
        if not oib:
            error = 'Oib value is required.'
        if not phone_number:
            error = 'Phone number is required.'
        if not date_of_birth:
            error = 'Date of birth is required.'
        if not membership_start:
            error = 'Membership start date is required.'
        if not card_id:
            error = 'Card id is required.'
        if not email:
            error = 'Email is required.'
        if not section or section == 'Izaberi sekciju':
            error = 'Sekcija value is required.'
        if db.member_exists(card_id.strip()):
            registered_member = db.get_row(DatabaseTables.CLAN, 'broj_iskaznice', card_id.strip())
            name, last_name = registered_member[1], registered_member[2]
            error = 'Broj iskaznice već postoji i glasi na ime {0} {1}'.format(name, last_name)

        if error is None:
            date_of_birth = get_date_object(date_of_birth)
            membership_start = get_date_object(membership_start)
            entry_values = (name, last_name, nickname, oib, phone_number, date_of_birth, membership_start,
                            card_id, email, section)
            db.add_member_entry(entry_values)
            flash("Član %s %s je uspješno dodan!" % (name, last_name), 'success')
            return redirect(url_for('index'))

        flash(error, 'danger')

    return render_template('/members/add.html')


@members_bp.route('/list', methods=['GET'])
@login_required
def list_members():
    db = DatabaseController()
    if session["access_level"] >= access_levels.SAVJETNIK:
        members = db.get_all_members()
    else:
        members = db.get_all_rows_from_table(DatabaseTables.CLAN)

    members_list = {}
    for member in members:
        if db.is_member_active(member[0]):
            members_list[member[0]] = member[1:-2]

    if session["access_level"] >= access_levels.SAVJETNIK:
        sorted_list = sorted(members_list.items(), key=lambda x: x[1][1])  # Sort po prezimenu ako je unutar sekcije
    else:
        sorted_list = sorted(members_list.items(), key=lambda x: (x[1][-1], x[1][1]))  # Sort po sekciji prvo pa prezimenu

    sorted_members = {}
    for k, v in sorted_list:
        sorted_members[k] = v
    return render_template("/members/list.html", list_records=sorted_members)


@members_bp.route('/edit/<member_id>', methods=['GET', 'POST'])
@login_required
@savjetnik_required
def edit_member(member_id):
    db = DatabaseController()
    member = db.get_row(DatabaseTables.CLAN, 'id', member_id)
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['lastname']
        nickname = request.form['nickname']
        oib = request.form['oib']
        phone_number = request.form['phone']
        date_of_birth = request.form['dateofbirth']
        membership_start = request.form['membership']
        card_id = request.form['idcard']
        email = request.form['email']
        try:
            section = request.form['section']
        except HTTPException:
            section = member[-3]

        db = DatabaseController()
        error = None

        if not name:
            error = 'Username is required.'
        if not last_name:
            error = 'Password is required.'
        if not nickname:
            nickname = '-'
        if not oib:
            error = 'Oib value is required.'
        if not phone_number:
            error = 'Phone number is required.'
        if not date_of_birth:
            error = 'Date of birth is required.'
        if not membership_start:
            error = 'Membership start date is required.'
        if not card_id:
            error = 'Card id is required.'
        if not email:
            error = 'Email is required.'
        if not section or section == 'Izaberi sekciju':
            error = 'Sekcija value is required.'
        if card_id != member[8] and db.member_exists(card_id.strip()):
            registered_member = db.get_row(DatabaseTables.CLAN, 'broj_iskaznice', card_id.strip())
            name, last_name = registered_member[1], registered_member[2]
            error = 'Broj iskaznice već postoji i glasi na ime {0} {1}'.format(name, last_name)

        if error is None:
            date_of_birth = get_date_object(date_of_birth)
            membership_start = get_date_object(membership_start)
            entry_values = (name, last_name, nickname, oib, phone_number, date_of_birth, membership_start,
                            card_id, email, section)
            db.edit_member(member_id, entry_values)
            flash("Podaci člana %s %s je uspješno izmjenjen!" % (name, last_name), 'success')
            return redirect(url_for('index'))

        flash(error, 'danger')

    return render_template('/members/edit.html', member=member[1:-1], member_id=member[0], sections=Utilities.sections)


@members_bp.route('/remove/<member_id>', methods=['POST'])
@savjetnik_required
@login_required
def remove_member(member_id):

    if request.method == 'POST':

        db = DatabaseController()
        if not db.entry_exists(DatabaseTables.CLAN, member_id):
            error = 'Neuspješno brisanje. Zapis ne postoji u bazi.'
            flash(error, 'danger')
        else:
            db.deactivate_member(member_id)
            flash('Član uspješno arhiviran', 'success')

    return "1"


@members_bp.route('/erase/<member_id>', methods=['POST'])
@admin_required
@login_required
def erase_member(member_id):

    if request.method == 'POST':

        db = DatabaseController()
        if not db.entry_exists(DatabaseTables.CLAN, member_id):
            error = 'Neuspješno brisanje. Zapis ne postoji u bazi.'
            flash(error, 'danger')
        else:
            db.remove_entry(DatabaseTables.CLAN, member_id)
            flash('Član uspješno arhiviran', 'success')

    return "1"


@members_bp.route('/archive', methods=['GET'])
@login_required
def archive():
    db = DatabaseController()
    all_archived_members = db.get_row(DatabaseTables.CLAN, 'aktivan', 0, return_all=True)
    members_list = {}
    for member in sorted(all_archived_members, key=lambda x: x[10]):
        members_list[member[0]] = (member[1], member[2], member[3], member[7],
                                   member[8], member[9], member[10], member[-1])

    return render_template('/members/archive.html', members_list=members_list)


@members_bp.route('/<member_id>/activate', methods=['POST'])
@login_required
@savjetnik_required
def activate(member_id=None):
    if request.method == 'POST':
        db = DatabaseController()
        db.activate_member(member_id)
        flash('Član je uspješno aktiviran', 'success')

        all_archived_members = db.get_row(DatabaseTables.CLAN, 'aktivan', 0, return_all=True)
        members_list = {}
        for member in all_archived_members:
            members_list[member[0]] = (member[1], member[2], member[3], member[7],
                                       member[8], member[9], member[10], member[-1])

    return "1"

