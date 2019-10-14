import datetime

from dateutil.relativedelta import relativedelta
from flask import (
    Blueprint, flash, render_template, request, session, send_file
)

import DatabaseTables
from constants import AccessLevels
import Utilities
from DatabaseController import DatabaseController, get_date_object

import csv, io

from auth import login_required, savjetnik_required, admin_required


statistics_bp = Blueprint('statistics', __name__, url_prefix='/statistics')


def get_interval_member_activity(start_date=None, end_date=None, section=None):
    db = DatabaseController()

    if section is None:
        section = session['section']

    if start_date is None:
        start_date = datetime.date.today().replace(day=1)
    if end_date is None:
        end_date = start_date + relativedelta(months=+1, days=-1)
    members_activity = db.get_period_activity(start_date=start_date,
                                              end_date=end_date)

    total_activity = {}
    total_activity_weight = {}
    for member in members_activity:
        key = member[0]
        # Prikaži člana ako je član tvoje sekcije ili ako si admin
        test = db.get_all_members_sections(key)
        if section in test or session['access_level'] == AccessLevels.ADMIN:
            if key not in total_activity:
                total_activity[key] = 0
                total_activity_weight[key] = 0
            total_activity[key] += member[3]  # Beztežinski sati
            total_activity_weight[key] += (member[3] * member[4])  # Množi sate sa faktorom

    if session['access_level'] == AccessLevels.ADMIN:
        members = db.get_all_rows_from_table(DatabaseTables.CLAN)
    else:
        members = db.get_all_members()

    members_list = {}
    for member in members:
        if db.is_member_active(member[0]):
            key = member[0]
            if key not in total_activity:
                member_hours = 0
                member_hours_w = 0
            else:
                member_hours = total_activity[key]
                member_hours_w = total_activity_weight[key]

            members_list[member[0]] = member[1:4] + (member_hours, member_hours_w) + (db.get_member_primary_section(member[0]),)

    if session["access_level"] >= AccessLevels.SAVJETNIK:
        sorted_list = sorted(members_list.items(), reverse=True,
                             key=lambda x: (x[1][3], x[1][4]))  # Sati -> Težinski -> Prezime
    else:  # Sekcija -> Sati -> Težinski
        sorted_list = sorted(members_list.items(), reverse=True, key=lambda x: (x[1][-1], x[1][3], x[1][4]))

    sorted_members = {}
    for k, v in sorted_list:
        section_tmp = Utilities.sections[v[-1]]
        if section_tmp not in sorted_members:
            sorted_members[section_tmp] = {}
        sorted_members[section_tmp][k] = v[:-1]

    return sorted_members


@statistics_bp.route('/monthly', methods=['GET', 'POST'])
@login_required
def monthly_statistics():
    current_date = datetime.datetime.now().date()
    if request.method == 'POST':
        year, month = request.form['month'].split('-')
        month = int(month)
        year = int(year)
    else:
        month = current_date.month
        year = current_date.year

    start_of_month = current_date.replace(year=year).replace(month=month).replace(day=1)
    monthd = start_of_month.strftime("%m")

    member_list = get_interval_member_activity(start_of_month)

    all_possible_sections = [section for section in Utilities.sections.values() if section in member_list]

    section_hours = {}
    for section in all_possible_sections:
        section_hours[section] = _get_section_hours(member_list, section)

    return render_template('/statistics/monthly.html', month=month, monthd=monthd, year=year,
                           members_list=member_list, sections=all_possible_sections, section_hours=section_hours)


@statistics_bp.route('/interval', methods=['GET', 'POST'])
@login_required
def interval_statistics():

    if request.method == 'POST':
        if request.form['start_date'] == '':
            start = datetime.date.today() + relativedelta(months=-3)
            start_year, start_month, start_day = start.year, start.month, start.day
        else:
            start_year, start_month, start_day = [int(x) for x in request.form['start_date'].split('-')]

        if request.form['end_date'] == '':
            current_date = datetime.date.today()
            end_year = current_date.year
            end_month = current_date.month
            end_day = current_date.day
        else:
            end_year, end_month, end_day = [int(x) for x in request.form['end_date'].split('-')]
    else:
        current_date = datetime.date.today()
        end_year = current_date.year
        end_month = current_date.month
        end_day = current_date.day

        start = datetime.date(end_year, end_month, end_day) + relativedelta(months=-3)
        start_year, start_month, start_day = start.year, start.month, start.day

    start_date = datetime.date(start_year, start_month, start_day)
    end_date = datetime.date(end_year, end_month, end_day)

    start_monthd = start_date.strftime("%m")  # monthd - formatiran mjesec kao dvoznamenkasti broj (zbog defult inputa)
    end_monthd = end_date.strftime("%m")

    member_list = get_interval_member_activity(start_date, end_date)

    all_possible_sections = [section for section in Utilities.sections.values() if section in member_list]

    section_hours = {}
    for section in all_possible_sections:
        section_hours[section] = _get_section_hours(member_list, section)

    months = (start_month, end_month)
    monthds = (start_monthd, end_monthd)
    years = (start_year, end_year)
    days = (start_day, end_day)
    return render_template('/statistics/interval.html', days=days, months=months, monthds=monthds, years=years,
                           members_list=member_list, sections=all_possible_sections, section_hours=section_hours)


@statistics_bp.route('/member_statistics/<member_id>', methods=['GET', 'POST'])
@login_required
@savjetnik_required
def member_statistics(member_id):

    member_info, date_joined, section = get_member_info(member_id)
    member_sections = _get_member_sections(member_id)
    activity_types = {}
    for section in member_sections:
        activity_types.update(_get_activity_types(section))
    end_date = None
    if request.method == 'POST':
        if request.form['start_date'] == '':
            start_date = get_date_object(date_joined)
            start_year, start_month, start_day = start_date.year, start_date.month, start_date.day
        else:
            start_year, start_month, start_day = [int(x) for x in request.form['start_date'].split('-')]

        if request.form['end_date'] == '':
            end_date = datetime.date.today()
            end_year, end_month, end_day = end_date.year, end_date.month, end_date.day
        else:
            end_year, end_month, end_day = [int(x) for x in request.form['end_date'].split('-')]

        start_date = datetime.date(start_year, start_month, start_day)
        end_date = datetime.date(end_year, end_month, end_day)

        start_monthd = start_date.strftime("%m")
        end_monthd = end_date.strftime("%m")

    else:
        start_date = get_date_object(date_joined)
        start_year, start_month, start_day = start_date.year, start_date.month, start_date.day

        current_date = datetime.date.today()
        end_year, end_month, end_day = current_date.year, current_date.month, current_date.day

        start_monthd = start_date.strftime("%m")
        end_monthd = current_date.strftime("%m")

    member_hours, member_hours_weighted, member_attendance = get_member_activities(member_id, activity_types, start_date, end_date)
    activity_types_count = {}
    for section in member_sections + ['svi']:
        max_activities_for_section = get_max_possible_activities(activity_types, section, start_date, end_date)
        for _type, count in max_activities_for_section.items():
            if _type in activity_types_count:
                activity_types_count[_type] += count
            else:
                activity_types_count[_type] = count

    attendance_stats = {}
    for activity_type, count in activity_types_count.items():
        attendance_stats[activity_type] = {}
        attendance_stats[activity_type]["attendance_max"] = count
        attendance_stats[activity_type]["attendance_count"] = member_attendance[activity_type]
        try:
            attendance_stats[activity_type]["percentage"] = '{0:.2f}%'.format(member_attendance[activity_type] / count * 100)
        except ZeroDivisionError:
            attendance_stats[activity_type]["percentage"] = 'Ovaj tip aktivnosti nije održan za zadani raspon datuma.'

    months = (start_month, end_month)
    monthds = (start_monthd, end_monthd)
    years = (start_year, end_year)
    days = (start_day, end_day)

    if end_date is not None and end_date < start_date:
        flash("Početan datum je veći od prijašnjeg.", 'info')

    return render_template('/statistics/member_statistics.html', activity_types=activity_types,
                           percentage=attendance_stats, hours=member_hours,
                           hours_w=member_hours_weighted, member=member_info, days=days, months=months,
                           monthds=monthds, years=years)


def _get_section_hours(members, section):
    total_hours = 0
    total_hours_w = 0
    for _, v in members[section].items():
        total_hours += v[3]
        total_hours_w += v[4]

    return {'total_hours': total_hours, 'total_hours_w': total_hours_w}


def _get_activity_types(section):
    db = DatabaseController()
    all_types = db.get_all_rows_from_table(DatabaseTables.TIP_AKTIVNOSTI)
    activity_types = {}
    for _type in sorted(all_types, key=lambda x: x[1]):
        if _type[3] == 'svi' or _type[3] == section:
            activity_types[_type[0]] = _type[1]
    return activity_types


def get_member_activities(member_id, activity_types, start_date=None, end_date=None):
    db = DatabaseController()
    member_activities = db.get_all_activities_for_member(member_id, start_date, end_date)
    member_hours_by_activity_type = {}
    member_hours_by_activity_type_weighted = {}
    member_attendance = {}
    for activity in member_activities:
        if activity[0] not in member_hours_by_activity_type:
            member_hours_by_activity_type[activity[0]] = activity[2]
        else:
            member_hours_by_activity_type[activity[0]] += activity[2]

        if activity[0] not in member_hours_by_activity_type_weighted:
            member_hours_by_activity_type_weighted[activity[0]] = activity[2] * activity[3]
        else:
            member_hours_by_activity_type_weighted[activity[0]] += (activity[2] * activity[3])

        if activity[0] not in member_attendance:
            member_attendance[activity[0]] = 1
        else:
            member_attendance[activity[0]] += 1

    # Dodaj 0 sati na tipove na koje član nije došao
    for _type in activity_types:
        if _type not in member_hours_by_activity_type:
            member_hours_by_activity_type[_type] = 0

        if _type not in member_hours_by_activity_type_weighted:
            member_hours_by_activity_type_weighted[_type] = 0

        if _type not in member_attendance:
            member_attendance[_type] = 0

    return member_hours_by_activity_type, member_hours_by_activity_type_weighted, member_attendance


def _get_member_sections(member_id):
    db = DatabaseController()
    return db.get_all_members_sections(member_id)


def get_max_possible_activities(activity_types, section, start_date, end_date=None):
    db = DatabaseController()
    activities_after_member_joined = db.get_all_activities_after_date(section, start_date, end_date)
    activity_types_count = {}
    for activity in activities_after_member_joined:
        if activity[0] not in activity_types_count:
            activity_types_count[activity[0]] = 1
        else:
            activity_types_count[activity[0]] += 1

    for _type in activity_types:
        if _type not in activity_types_count:
            activity_types_count[_type] = 0

    return activity_types_count


def get_member_info(member_id):
    db = DatabaseController()
    member = db.get_table_row(DatabaseTables.CLAN, int(member_id))
    member_info = (member[1], member[2], member[3])
    date_joined = member[7]
    section = member[10]
    return member_info, date_joined, section


@statistics_bp.route("/section_stats", methods=['GET', 'POST'])
@login_required
@admin_required
def section_stats():
    db = DatabaseController()
    if request.method == 'POST':
        if request.form['start_date'] == '':
            start = datetime.date.today() + relativedelta(months=-1)
            start_year, start_month, start_day = start.year, start.month, start.day
        else:
            start_year, start_month, start_day = [int(x) for x in request.form['start_date'].split('-')]

        if request.form['end_date'] == '':
            current_date = datetime.date.today()
            end_year = current_date.year
            end_month = current_date.month
            end_day = current_date.day
        else:
            end_year, end_month, end_day = [int(x) for x in request.form['end_date'].split('-')]
    else:
        current_date = datetime.date.today()
        end_year = current_date.year
        end_month = current_date.month
        end_day = current_date.day

        start = datetime.date(end_year, end_month, end_day) + relativedelta(months=-1)
        start_year, start_month, start_day = start.year, start.month, start.day

    start_date = datetime.date(start_year, start_month, start_day)
    end_date = datetime.date(end_year, end_month, end_day)

    start_monthd = start_date.strftime("%m")  # monthd - formatiran mjesec kao dvoznamenkasti broj (zbog defult inputa)
    end_monthd = end_date.strftime("%m")

    section_event_count = {}
    for section in Utilities.sections:
        section_events = db.get_all_volunteering_events(section, start_date, end_date)
        section_event_count[section] = len(section_events)

    months = (start_month, end_month)
    monthds = (start_monthd, end_monthd)
    years = (start_year, end_year)
    days = (start_day, end_day)
    return render_template('/statistics/section_stats.html', days=days, months=months, monthds=monthds,
                           sections=Utilities.sections, years=years, section_count=section_event_count)


@statistics_bp.route("/export", methods=['GET'])
@login_required
@savjetnik_required
def export():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    all_sections = False if request.args.get('all_sections') == 'false' else True

    if all_sections and session['access_level'] == Utilities.AccessLevels.ADMIN:
        section = 'svi'
    else:
        section = session['section']

    start_year, start_month, start_day = [int(x) for x in start_date.split('-')]
    end_year, end_month, end_day = [int(x) for x in end_date.split('-')]

    start_date = datetime.date(start_year, start_month, start_day)
    end_date = datetime.date(end_year, end_month, end_day)

    activity_data = get_interval_member_activity(start_date, end_date, section)

    with open('export.csv', 'w', newline='') as csvfile:
        fieldnames = ['Ime', 'Prezime', 'Nadimak', 'Sati', 'Težinski sati']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for section in activity_data:
            writer.writerow({'Ime': section.upper(), 'Prezime': 'Sekcija'})
            for entry in activity_data[section]:
                name = activity_data[section][entry][0]
                last_name = activity_data[section][entry][1]
                nickname = activity_data[section][entry][2]
                hours = activity_data[section][entry][3]
                hours_w = activity_data[section][entry][4]
                writer.writerow({'Ime': name, 'Prezime': last_name, 'Nadimak': nickname,
                                 'Sati': hours, 'Težinski sati': hours_w})

    return send_file('export.csv',
                     mimetype='text/csv',
                     attachment_filename='export.csv',
                     as_attachment=True)
