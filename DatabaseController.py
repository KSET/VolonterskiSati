import sqlite3
import os
import DatabaseCommands
import datetime


#Date format: YYYY-MM-DD
def get_date_object(date):
    try:
        return datetime.datetime.strptime(date, '%Y-%m-%d').date()
    except Exception as e:
        raise Exception("The format of input date is wrong. %s" % e)


class DatabaseController():

    def __init__(self):
        self.conn = sqlite3.connect("ksetBazaClanova.db")
        self.cursor = self.conn.cursor()

    def init_tables(self):
        self.cursor.execute(DatabaseCommands.CREATE_USER_TABLE)
        self.cursor.execute(DatabaseCommands.CREATE_ACTIVITY_TABLE)
        self.cursor.execute(DatabaseCommands.CREATE_ACTIVITY_USER_RELATIONSHIP_TABLE)
        self.cursor.execute(DatabaseCommands.CREATE_ACTIVITY_TYPE_TABLE)
        self.conn.commit()

    def _save_changes(self):
        self.conn.commit()

    """
    entry_values = tuple containing argument values corresponding to those defined before keyword values.
    """
    def add_member_entry(self, entry_values):
        self.cursor.execute("INSERT INTO CLAN(ime, prezime, nadimak, oib, mobitel, datum_rodenja, datum_uclanjenja, broj_iskaznice, email, sekcija) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);" , entry_values)
        self._save_changes()

    def edit_member(self, member_id, new_values):
        self.cursor.execute("UPDATE CLAN SET ime = ?, prezime = ?, nadimak = ?, oib = ?, mobitel = ?, datum_rodenja = ?, datum_uclanjenja = ?, broj_iskaznice = ?, email = ?, sekcija = ? WHERE id = ?", new_values + (member_id, ))
        self._save_changes()

    def deactivate_member(self, member_id):
        self.cursor.execute("UPDATE CLAN SET aktivan = 0 WHERE id = ?", (member_id, ))
        self._save_changes()

    def activate_member(self, member_id):
        self.cursor.execute("UPDATE CLAN SET aktivan = 1 WHERE id = ?", (member_id, ))
        self._save_changes()

    def add_activity_entry(self, entry_values):
        self.cursor.execute("INSERT INTO AKTIVNOST(naziv, opis, datum, id_vrsta_aktivnosti) VALUES (?, ?, ?, ?)", entry_values)
        self._save_changes()

    def edit_activity(self, activity_id, new_values):
        self.cursor.execute("UPDATE AKTIVNOST SET naziv = ?, opis = ?, datum= ? id_vrsta_aktivnosti = ? WHERE id = ?", new_values + (activity_id, ))
        self._save_changes()

    def add_activity_type_entry(self, entry_values):
        self.cursor.execute("INSERT INTO TIP_AKTIVNOSTI(naziv, opis) VALUES (?, ?)", entry_values)
        self._save_changes()

    def edit_activity_type(self, activity_type_id, new_values):
        self.cursor.execute("UPDATE TIP_AKTIVNOSTI SET naziv = ?, opis = ? WHERE id = ?", new_values + (activity_type_id, ))
        self._save_changes()

    def add_member_activity_entry(self, entry_values):
        self.cursor.execute("INSERT INTO CLAN_AKTIVNOST(id_clan, id_aktivnost, broj_sati, faktor) VALUES (?, ?, ?, ?)", entry_values)
        self._save_changes()

    def remove_entry(self, table_name, id):
        query = "DELETE FROM %s WHERE id = %d" % (table_name, id)
        self.cursor.execute(query)
        self._save_changes()

    """
    Generic method to fetch row with id from table table_name
    """
    def get_table_row(self, table_name, id):
        query = "SELECT * FROM %s WHERE id = %d" % (table_name, id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_member_id(self, name, last_name, nickname = None):
        query = "SELECT * FROM CLAN WHERE ime = \"%s\" AND prezime = \"%s\"" % (name, last_name)
        if nickname is not None:
            query = "%s AND nadimak = \"%s\"" % (query, nickname)
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    """
    Method that gets an id from table table_name which attribute field is equal to value
    """
    def get_row_id(self, table_name, field, value, return_all = False):
        query = "SELECT * FROM %s WHERE %s = \"%s\"" % (table_name, field, value)
        self.cursor.execute(query)
        if not return_all:
            return self.cursor.fetchone()[0] #Fetch first one and return an id
        else:
            return self.cursor.fetchall()

    def get_all_monthly_activities(self, month = None):
        if month is None:
            month = datetime.datetime.now().month

        query = 'SELECT * FROM aktivnost WHERE strftime("%m", datum) = \"{0}\"'.format(month)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_period_activity(self, start_date=None, end_date=None):
        if end_date is None:
            end_date = datetime.datetime.now()

        if start_date is None:
            start_date = end_date.replace(day=1)

        self.cursor.execute("select ime, broj_sati, faktor, datum "
                            "from CLAN inner join CLAN_AKTIVNOST on CLAN.id = CLAN_AKTIVNOST.id_clan "
                            "inner join AKTIVNOST on CLAN_AKTIVNOST.id_aktivnost = AKTIVNOST.id "
                            "where datum >= ? and datum <= ?", (start_date, end_date))

        return self.cursor.fetchall()

    def get_all_rows_from_table(self, table_name):
        query = "SELECT * FROM %s" % table_name
        self.cursor.execute(query)
        return self.cursor.fetchall()
