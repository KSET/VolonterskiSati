from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import HTTPException

from DatabaseController import DatabaseController, get_date_object
import DatabaseTables


members_bp = Blueprint('members', __name__, url_prefix='/members')


@members_bp.route('/add', methods=('GET', 'POST'))
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
        section = request.form['section']

        db = DatabaseController()
        error = None

        if not name:
            error = 'Username is required.'
        elif not last_name:
            error = 'Password is required.'
        elif not nickname:
            nickname = '-'
        elif not oib:
            error = 'Oib value is required.'
        elif not phone_number:
            error = 'Phone number is required.'
        elif not date_of_birth:
            error = 'Date of birth is required.'
        elif not membership_start:
            error = 'Membership start date is required.'
        elif not card_id:
            error = 'Card id is required.'
        elif not email:
            error = 'Email is required.'
        elif not section or section == 'Izaberi sekciju':
            error = 'Sekcija value is required.'
        elif db.account_exists(card_id):
            error = 'User card id {} is already registered.'.format("%s %s" % (name, last_name))

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
def list_members():
    db = DatabaseController()
    members = db.get_all_rows_from_table(DatabaseTables.CLAN)
    members_list = {}
    for member in members:
        members_list[member[0]] = member[1:-1]

    return render_template("/members/list.html", list_records=members_list)


@members_bp.route('/edit/<member_id>', methods=['GET', 'POST'])
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
            section = member[9]

        db = DatabaseController()
        error = None

        if not name:
            error = 'Username is required.'
        elif not last_name:
            error = 'Password is required.'
        elif not nickname:
            nickname = '-'
        elif not oib:
            error = 'Oib value is required.'
        elif not phone_number:
            error = 'Phone number is required.'
        elif not date_of_birth:
            error = 'Date of birth is required.'
        elif not membership_start:
            error = 'Membership start date is required.'
        elif not card_id:
            error = 'Card id is required.'
        elif not email:
            error = 'Email is required.'
        elif not section or section == 'Izaberi sekciju':
            error = 'Sekcija value is required.'
        elif card_id != member[8] and db.account_exists(card_id):
            error = 'User card id {} is already registered.'.format("%s %s" % (name, last_name))

        if error is None:
            date_of_birth = get_date_object(date_of_birth)
            membership_start = get_date_object(membership_start)
            entry_values = (name, last_name, nickname, oib, phone_number, date_of_birth, membership_start,
                            card_id, email, section)
            db.edit_member(member_id, entry_values)
            flash("Podaci člana %s %s je uspješno izmjenjen!" % (name, last_name), 'success')
            return redirect(url_for('index'))

        flash(error, 'danger')

    return render_template('/members/edit.html', member=member[1:], member_id=member[0])


@members_bp.route('/remove/<member_id>', methods=['POST'])
def remove_member(member_id):

    if request.method == 'POST':

        db = DatabaseController()
        if not db.entry_exists(DatabaseTables.CLAN, member_id):
            error = 'Neuspješno brisanje. Zapis ne postoji u bazi.'
            flash(error, 'danger')
        else:
            db.remove_entry(DatabaseTables.CLAN, member_id)
            flash('Član uspješno izbrisan', 'success')

    return "1"

