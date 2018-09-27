import sqlite3
import os
import DatabaseCommands
import datetime

class DatabaseController():

    def __init__(self):
        self.conn = sqlite3.connect("ksetBazaClanova.db")
        self.cursor = self.conn.cursor()

    def _init_tables(self):
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
    def _add_user_entry(self, entry_values):
        self.cursor.execute("INSERT INTO CLAN(ime, prezime, oib, mobitel, datum_rodenja, datum_uclanjenja, broj_iskaznice, email, sekcija) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);" , entry_values)
        self._save_changes()

    def _edit_user(self, user_id, new_values):
        self.cursor.execute("UPDATE CLAN SET ime = ?, prezime = ?, oib = ?, mobitel = ?, datum_rodenja = ?, datum_uclanjenja = ?, broj_iskaznice = ?, email = ?, sekcija = ? WHERE id = ?", new_values + (user_id, ))
        self._save_changes()

    def _deactivate_user(self, user_id):
        self.cursor.execute("UPDATE CLAN SET aktivan = 0 WHERE id = ?", (user_id, ))
        self._save_changes()

    def _activate_user(self, user_id):
        self.cursor.execute("UPDATE CLAN SET aktivan = 1 WHERE id = ?", (user_id, ))
        self._save_changes()

    def _add_activity_entry(self, entry_values):
        self.cursor.execute("INSERT INTO AKTIVNOST(naziv, opis, datum, id_vrsta_aktivnosti) VALUES (?, ?, ?, ?)", entry_values)
        self._save_changes()

    def _edit_activity(self, activity_id, new_values):
        self.cursor.execute("UPDATE AKTIVNOST SET naziv = ?, opis = ?, datum= ? id_vrsta_aktivnosti = ? WHERE id = ?", new_values + (activity_id, ))
        self._save_changes()

    def _add_activity_type_entry(self, entry_values):
        self.cursor.execute("INSERT INTO TIP_AKTIVNOSTI(naziv, opis) VALUES (?, ?)", entry_values)
        self._save_changes()

    def _edit_activity_type(self, activity_type_id, new_values):
        self.cursor.execute("UPDATE TIP_AKTIVNOSTI SET naziv = ?, opis = ? WHERE id = ?", new_values + (activity_type_id, ))
        self._save_changes()

    """
    Generic method to fetch row with id from table table_name
    """
    def _get_table_row(self, table_name, id):
        self.cursor.execute("SELECT * FROM ? WHERE id = ?", (table_name, id))
        return self.cursor.fetchall()

    def _get_monthly_activity(self, month = None):
        if month is None:
            month = datetime.datetime.now().month

        ##TODO: Command which gets all hours in month defined by variable month.

