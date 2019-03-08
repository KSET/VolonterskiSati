from DatabaseController import DatabaseController
import DatabaseTables
import csv
import datetime
import matplotlib.pyplot as plt
import Utilities

if __name__ == '__main__':
    db = DatabaseController()
    db.init_tables()


    print(db.get_all_rows_from_table(DatabaseTables.CLAN_AKTIVNOST))
    start_date = datetime.datetime(2019, 2, 1)
    end_date = datetime.datetime(2019, 3, 15)
    activity = db.get_period_activity(start_date, end_date)
    print(activity)
    total_activity = {}
    for item in activity:
        key = "%s %s" % (item[0], item[1])
        if key not in total_activity:
            total_activity[key] = 0
        total_activity[key] += item[2] * item[3]

    print(total_activity)


    """
    plt.title("Aktivnost od %s do %s" % (start_date.strftime(Utilities.DATE_FORMAT), end_date.strftime(Utilities.DATE_FORMAT)))
    plt.pie(list(total_activity.values()), labels=list(total_activity.keys()))
    plt.show()
    """