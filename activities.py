from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from DatabaseController import DatabaseController, get_date_object
import DatabaseTables

activities_bp = Blueprint('activities', __name__, url_prefix='/activities')

@activities_bp.route('/add', methods=('GET', 'POST'))
def add_activity():
    db = DatabaseController()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        activity_start_date = request.form['date']
        type = request.form['type']

        error = None

        if not name:
            error = 'Username is required.'
        elif not description:
            description = '-'
        elif not activity_start_date:
            error = 'Date is required'
        elif not type:
            error = 'Activity type value is required.'

        if error is None:
            activity_start_date = get_date_object(activity_start_date)
            entry_values = (name, description, activity_start_date, type)
            db.add_activity_entry(entry_values)
            flash("Aktivnost %s je uspješno dodana!" % name, 'success')
            return redirect(url_for('index'))

        flash(error, 'danger')

    activity_types = {}
    for row in db.get_all_rows_from_table(DatabaseTables.TIP_AKTIVNOSTI):
        activity_types[row[0]] = row[1]

    return render_template('/activities/add.html', activity_types=activity_types)

@activities_bp.route('/list', methods=['GET'])
def list_activities():
    db = DatabaseController()
    activities = db.get_full_activity_info()
    activities_list = {}
    for activity in activities:
        activities_list[activity[0]] = activity[1:]

    return render_template("/activities/list.html", list_records=activities_list)


@activities_bp.route('/edit/<activity_id>', methods=['GET', 'POST'])
def edit_activity(activity_id):
    db = DatabaseController()
    activity = db.get_full_activity_info(activity_id)[0]  # First index to remove the list type
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        activity_start_date = request.form['date']
        activity_type = request.form['type']

        error = None

        if not name:
            error = 'Username is required.'
        elif not description:
            description = '-'
        elif not activity_start_date:
            error = 'Date is required'
        elif not activity_type:
            error = 'Activity type value is required.'

        if error is None:
            activity_start_date = get_date_object(activity_start_date)
            entry_values = (name, description, activity_start_date, int(activity_type))
            print(activity_id)
            print(entry_values)
            db.edit_activity(activity_id, entry_values)
            flash("Aktivnost %s je uspješno izmjenjena!" % name, 'success')
            return redirect(url_for('index'))

        flash(error, 'danger')

    activity_types = {}
    for row in db.get_all_rows_from_table(DatabaseTables.TIP_AKTIVNOSTI):
        activity_types[row[0]] = row[1]

    return render_template('/activities/edit.html', activity_types=activity_types, activity=activity[1:])


@activities_bp.route('/add_type', methods=['GET', 'POST'])
def add_activity_type():
    db = DatabaseController()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        error = None

        if not name:
            error = 'Username is required.'
        elif not description:
            description = '-'

        if error is None:
            entry_values = (name, description)
            db.add_activity_type_entry(entry_values)
            flash("Tip aktivnosti %s je uspješno dodan!" % name, 'success')
            return redirect(url_for('index'))

        flash(error, 'danger')

    return render_template('/activities/add_type.html')


@activities_bp.route('/list_types', methods=['GET'])
def list_activity_types():
    db = DatabaseController()
    activities = db.get_all_rows_from_table(DatabaseTables.TIP_AKTIVNOSTI)
    activities_list = {}
    for activity in activities:
        activities_list[activity[0]] = activity[1:]

    return render_template("/activities/list_types.html", list_records=activities_list)



@activities_bp.route('/edit_type/<type_id>', methods=['GET', 'POST'])
def edit_activity_type(type_id):
    db = DatabaseController()
    activity_type = db.get_row(DatabaseTables.TIP_AKTIVNOSTI, 'id', type_id)
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        error = None

        if not name:
            error = 'Name is required.'
        elif not description:
            description = '-'
        elif activity_type[1] != name and db.activity_type_exists(name):
            error = 'Tip aktivnosti %s već postoji u bazi podataka' % name

        if error is None:
            entry_values = (name, description)
            db.edit_activity_type(type_id, entry_values)
            flash("Tip aktivnosti %s je uspješno izmjenjen!" % name, 'success')
            return redirect(url_for('index'))

        flash(error, 'danger')

    return render_template('/activities/edit_type.html', activity_type=activity_type[1:])
