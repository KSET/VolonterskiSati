from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from DatabaseController import DatabaseController, get_date_object
import DatabaseTables

import datetime

import access_levels

from werkzeug.exceptions import HTTPException

statistics_bp = Blueprint('statistics', __name__, url_prefix='/statistics')


@statistics_bp.route('/monthly', methods=['GET', 'POST'])
def monthly_statistics(month=None, year=None):
    db = DatabaseController()
    current_date = datetime.datetime.now().date()
    if request.method == 'POST':
        year, month = request.form['month'].split('-')
        month = int(month)
        year = int(year)
    else:
        if month is None:
            month = current_date.month
        if year is None:
            year = current_date.year
    start_of_month = current_date.replace(year=year).replace(month=month).replace(day=1)
    monthd = start_of_month.strftime("%m")
    members_activity = db.get_period_activity(start_date=start_of_month, end_date=start_of_month.replace(month=month+1))
    total_activity = {}
    total_activity_weight = {}
    for member in members_activity:
        key = member[0]
        if key not in total_activity:
            total_activity[key] = 0
            total_activity_weight[key] = 0
        total_activity[key] += member[3]  # Beztežinski sati
        total_activity_weight[key] += (member[3] * member[4])  # Množi sate sa faktorom

    if session['access_level'] == access_levels.ADMIN:
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

            members_list[member[0]] = member[1:4] + (member_hours, member_hours_w)
            if session['access_level'] == access_levels.ADMIN:
                members_list[member[0]] += (member[-2],)

    if session["access_level"] >= access_levels.SAVJETNIK:
        sorted_list = sorted(members_list.items(), reverse=True,
                             key=lambda x: (x[1][3], x[1][4])) # Sati -> Težinski -> Prezime
    else:
        #
        sorted_list = sorted(members_list.items(), reverse=True, key=lambda x: (x[1][3], x[1][4], x[1][-1]))

    sorted_members = {}
    for k, v in sorted_list:
        sorted_members[k] = v

    return render_template('/statistics/monthly.html', month=month, monthd=monthd, year=year, members_list=sorted_members)

@statistics_bp.route('/interval', methods=('GET', 'POST'))
def interval_statistics():
    return NotImplemented


@statistics_bp.route('/orange', methods=['GET'])
def above_average_activity():
    return NotImplemented


@statistics_bp.route('/member_statistics/<member_id>', methods=['GET'])
def member_statistics(member_id):
    db = DatabaseController()
    # TODO DOVRŠITI
    return
