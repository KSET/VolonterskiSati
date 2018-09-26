import sqlite3
import os
import DatabaseCommands

class DatabaseController():

    def __init__(self):
        self.conn = sqlite3.connect("ksetBazaClanova.db")
        self.cursor = self.conn.cursor()

    def _init_tables(self):
        self.cursor.execute(DatabaseCommands.CREATE_USER_TABLE)
        self.cursor.execute(DatabaseCommands.CREATE_ACTIVITY_TABLE)
        self.cursor.execute(DatabaseCommands.CREATE_ACTIVITY_USER_RELATIONSHIP_TABLE)
        self.conn.commit()

    """
    entry_values = tuple containing argument values corresponding to those defined before keyword values.
    """
    def _add_user_entry(self, entry_values):
        self.cursor.execute("INSERT INTO CLAN(ime, prezime, oib, mobitel, datum_rodenja, datum_uclanjenja, broj_iskaznice, email, sekcija) VALUES (?,?,?,?,?,?,?,?,?);" , entry_values)
        self.conn.commit()

    def _edit_user_entry(self, user_id, new_values):
        self.cursor.execute("UPDATE CLAN SET ime = ?, prezime = ?, oib = ?, mobitel = ?, datum_rodenja = ?, datum_uclanjenja = ?, broj_iskaznice = ?, email = ?, sekcija = ? WHERE id = ?", new_values+(user_id,))
        self.conn.commit()


