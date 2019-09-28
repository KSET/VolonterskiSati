from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from DatabaseController import DatabaseController, get_date_object
import DatabaseTables

from constants import AccessLevels
import Utilities

from auth import login_required, savjetnik_required, admin_required

from werkzeug.exceptions import HTTPException

activities_bp = Blueprint('activities', __name__, url_prefix='/activities')


@activities_bp.route('/add', methods=('GET', 'POST'))
@login_required
@savjetnik_required
def add_activity():
    db = DatabaseController()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        activity_start_date = request.form['date']
        type = request.form['type']
        try:
            section = request.form['section']
        except HTTPException:
            section = session["section"]

        error = None

        if not name:
            error = 'Username is required.'
        if not description:
            description = '-'
        if not activity_start_date:
            error = 'Date is required'
        if not type:
            error = 'Activity type value is required.'

        if error is None:
            activity_start_date = get_date_object(activity_start_date)
            entry_values = (name, description, activity_start_date, section, type)

            if db.activity_exists(name, activity_start_date, section):
                flash("Aktivnost sa istim imenom i datumom za ovu sekciju već postoji u bazi", "info")
                return redirect(url_for('activities.add_activity'))

            db.add_activity_entry(entry_values)
            activity_id = db.get_last_row_id()

            flash("Aktivnost %s je uspješno dodana!" % name, 'success')
            if request.form['action'] == "member_to_activity":
                flash("Preusmjeren si na formu za dodavanje članova koji su došli na aktivnost.", 'info')
                return redirect(url_for('activities.add_members_to_activity', activity_id=activity_id))
            return redirect(url_for('index'))

        flash(error, 'danger')

    activity_types = {}
    for row in db.get_all_rows_from_table(DatabaseTables.TIP_AKTIVNOSTI):
        activity_types[row[0]] = (row[1], row[3])

    return render_template('/activities/add.html', activity_types=activity_types)


@activities_bp.route('/list', methods=['GET'])
@login_required
def list_activities():
    db = DatabaseController()
    activities = db.get_full_activity_info()
    activities_list = {}
    for activity in sorted(activities, reverse=True, key=lambda x: x[3]):
        activities_list[activity[0]] = activity[1:]

    return render_template("/activities/list.html", list_records=activities_list)


@activities_bp.route('/edit/<activity_id>', methods=['GET', 'POST'])
@login_required
@savjetnik_required
def edit_activity(activity_id):
    db = DatabaseController()
    activity = db.get_full_activity_info(activity_id)[0]  # First index to remove the list type
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        activity_start_date = request.form['date']
        activity_type = request.form['type']
        try:
            section = request.form['section']
        except HTTPException:
            section = session["section"]

        error = None

        if not name:
            error = 'Activity name is required.'
        if not description:
            description = '-'
        if not activity_start_date:
            error = 'Date is required'
        if not activity_type:
            error = 'Activity type value is required.'

        if error is None:
            activity_start_date = get_date_object(activity_start_date)
            entry_values = (name, description, activity_start_date, section, int(activity_type))
            db.edit_activity(activity_id, entry_values)
            flash("Aktivnost %s je uspješno izmjenjena!" % name, 'success')
            return redirect(url_for('index'))

        flash(error, 'danger')

    activity_types = {}
    for row in db.get_all_rows_from_table(DatabaseTables.TIP_AKTIVNOSTI):
        activity_types[row[0]] = row[1]

    return render_template('/activities/edit.html', activity_types=activity_types, activity=activity[1:],
                           activity_id=activity[0], sections=Utilities.sections)


@activities_bp.route('/remove/<activity_id>', methods=['POST'])
@login_required
@savjetnik_required
def remove_activity(activity_id):

    if request.method == 'POST':

        db = DatabaseController()
        if not db.entry_exists(DatabaseTables.AKTIVNOST, activity_id):
            error = 'Neuspješno brisanje. Zapis ne postoji u bazi.'
            flash(error, 'danger')
        else:
            db.remove_entry(DatabaseTables.AKTIVNOST, activity_id)
            db.remove_member_activity_entry(activity_id=activity_id)
            flash('Aktivnost uspješno izbrisana', 'success')

    return "1"


@activities_bp.route('/add_type', methods=['GET', 'POST'])
@login_required
@savjetnik_required
def add_activity_type():
    db = DatabaseController()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        try:
            section = request.form['section']
        except HTTPException:
            section = session["section"]

        error = None

        if not name:
            error = 'Username is required.'
        if not description:
            description = '-'

        if error is None:
            entry_values = (name, description, section)
            db.add_activity_type_entry(entry_values)
            flash("Tip aktivnosti %s je uspješno dodan!" % name, 'success')
            return redirect(url_for('index'))

        flash(error, 'danger')

    return render_template('/activities/add_type.html')


@activities_bp.route('/list_types', methods=['GET'])
@login_required
def list_activity_types():
    db = DatabaseController()
    activities = db.get_all_rows_from_table(DatabaseTables.TIP_AKTIVNOSTI)
    activities_list = {}
    for activity in sorted(activities, key=lambda x: x[1]):
        if session['access_level'] == AccessLevels.ADMIN:
            activities_list[activity[0]] = activity[1:]
        elif activity[-1] == session['section'] or activity[-1] == 'svi':
            activities_list[activity[0]] = activity[1:-1]

    return render_template("/activities/list_types.html", list_records=activities_list)


@activities_bp.route('/edit_type/<type_id>', methods=['GET', 'POST'])
@login_required
@savjetnik_required
def edit_activity_type(type_id):
    db = DatabaseController()
    activity_type = db.get_row(DatabaseTables.TIP_AKTIVNOSTI, 'id', type_id)
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        try:
            section = request.form['section']
        except HTTPException:
            section = session["section"]

        error = None

        if not name:
            error = 'Name is required.'
        if not description:
            description = '-'
        if activity_type[1] != name and db.activity_type_exists(name):
            error = 'Tip aktivnosti %s već postoji u bazi podataka' % name

        if error is None:
            entry_values = (name, description, section)
            db.edit_activity_type(type_id, entry_values)
            flash("Tip aktivnosti %s je uspješno izmjenjen!" % name, 'success')
            return redirect(url_for('index'))

        flash(error, 'danger')

    return render_template('/activities/edit_type.html', activity_type=activity_type[1:],
                           activity_type_id=activity_type[0], sections=Utilities.sections)


@activities_bp.route('/remove_type/<activity_type_id>', methods=['POST'])
@login_required
@savjetnik_required
def remove_activity_type(activity_type_id):

    if request.method == 'POST':

        db = DatabaseController()
        if not db.entry_exists(DatabaseTables.TIP_AKTIVNOSTI, activity_type_id):
            error = 'Neuspješno brisanje. Zapis ne postoji u bazi.'
            flash(error, 'danger')
        else:
            db.remove_entry(DatabaseTables.TIP_AKTIVNOSTI, activity_type_id)
            flash('Tip aktivnosti uspješno izbrisana', 'success')

    return "1"


@activities_bp.route('/<activity_id>/add_members', methods=['GET', 'POST'])
@login_required
@savjetnik_required
def add_members_to_activity(activity_id):
    db = DatabaseController()
    if session["access_level"] >= AccessLevels.SAVJETNIK:  # Ako je razina ovlasti savjetnik ili manja, dohvati matičnu sekciju samo
        all_members = db.get_all_members()
    else:
        all_members = db.get_all_members_admin()  # Za admina dohvati sve članove
    members_list = {}
    for member in all_members:
        member_id = member[0]
        if db.is_member_active(member_id) and not db.member_activity_exists(member_id, activity_id):
            members_list[member[0]] = member[1:]

    if session["access_level"] >= AccessLevels.SAVJETNIK:
        sorted_list = sorted(members_list.items(), key=lambda x: x[1][1])  # Sort po prezimenu ako je unutar sekcije
    else:
        sorted_list = sorted(members_list.items(), key=lambda x: (x[1][-1], x[1][1]))  # Sort po sekciji prvo pa prezimenu

    sorted_members = {}
    for k, v in sorted_list:
        sorted_members[k] = v

    if request.method == 'POST':
        for member_id, _ in sorted_members.items():
            if request.form.get('checkbox%s' % member_id):
                hours_worked = request.form["hoursworked%s" % member_id]
                factor = request.form["factor%s" % member_id]
                if float(hours_worked) != 0:
                    if not db.member_activity_exists(member_id, activity_id):
                        db.add_member_activity_entry((member_id, activity_id, hours_worked, factor))

        flash("Volonterski sati su uspješno izmjenjeni!", "success")
        return redirect("/activities/list")

    return render_template("/activities/add_members_to_activity.html", activity_id=activity_id, members_list=sorted_members)


@activities_bp.route('/<activity_id>/list_members', methods=['GET'])
@login_required
def list_activity_members(activity_id):
    db = DatabaseController()
    activity_members = db.get_activity_members(activity_id)
    activity_name = db.get_table_row(DatabaseTables.AKTIVNOST, int(activity_id))[1]
    activity_date = get_croatian_date_format(db.get_table_row(DatabaseTables.AKTIVNOST, int(activity_id))[3])
    members_list = {}
    for member in sorted(activity_members, reverse=True, key=lambda x: x[3]):
        members_list[member[0]] = member[1:]
    return render_template("/activities/list_activity_members.html", members_list=members_list,
                           activity_name=activity_name, activity_date=activity_date, activity_id=activity_id)


@activities_bp.route('/<activity_id>/edit_member_hours/', methods=['GET', 'POST'])
@login_required
@savjetnik_required
def edit_activity_member_hours(activity_id):
    db = DatabaseController()
    if session['access_level'] == AccessLevels.ADMIN:
        all_members = db.get_activity_members(activity_id)
    else:
        all_members = db.get_activity_members(activity_id, section_specific=True)
    members_list = {}
    for member in all_members:
        members_list[member[0]] = member[1:]

    activity_name = db.get_table_row(DatabaseTables.AKTIVNOST, int(activity_id))[1]
    activity_date = get_croatian_date_format(db.get_table_row(DatabaseTables.AKTIVNOST, int(activity_id))[3])

    if request.method == 'POST':
        changed = False
        for member_id, member_data in members_list.items():
            member_name, member_last_name, member_hours, member_factor = member_data
            hours_worked = request.form["hoursworked%s" % member_id]
            factor = request.form["factor%s" % member_id]
            if not hours_worked or float(hours_worked) == 0:
                db.remove_member_activity_entry(activity_id, member_id)
                changed = True
            elif float(hours_worked) != member_hours or float(factor) != member_factor:
                entry_values = (float(hours_worked), float(factor), member_id, activity_id)
                db.edit_member_activity_entry(entry_values)
                changed = True
            else:
                pass

        if changed:
            flash("Sati volontiranja uspješno izmjenjeni", 'success')
        else:
            flash("Sati volontiranja su ostali isti", "info")

        return redirect(url_for('index'))

    return render_template('/activities/edit_member_hours.html', members_list=members_list, activity_name=activity_name,
                           activity_date=activity_date, activity_id=activity_id)


def get_croatian_date_format(date):
    date_year, date_month, date_day = date.split('-')
    return "%s.%s %s" % (date_day, date_month, date_year)
