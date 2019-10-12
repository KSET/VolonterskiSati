import sqlite3
import DatabaseTables
import DatabaseCommands
import datetime
from constants import AccessLevels
from flask import session
from constants import DATABASE_PATH


# Date format: YYYY-MM-DD
def get_date_object(date, current_format=None):
    try:
        if current_format is None:
            current_format = '%Y-%m-%d'
        return datetime.datetime.strptime(date, current_format).date()
    except Exception as e:
        raise Exception("The format of input date is wrong. %s" % e)


class DatabaseController:

    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()

    def init_tables(self):
        self.cursor.execute(DatabaseCommands.CREATE_ACCOUNTS_TABLE)
        self.cursor.execute(DatabaseCommands.CREATE_USER_TABLE)
        self.cursor.execute(DatabaseCommands.CREATE_ACTIVITY_TABLE)
        self.cursor.execute(DatabaseCommands.CREATE_ACTIVITY_USER_RELATIONSHIP_TABLE)
        self.cursor.execute(DatabaseCommands.CREATE_ACTIVITY_TYPE_TABLE)
        self.cursor.execute(DatabaseCommands.CREATE_MEMBERS_SECTION_RELATIONSHIP_TABLE)
        self.cursor.execute(DatabaseCommands.CREATE_MEMBERS_CARDS_RELATIONSHIP_TABLE)
        self.conn.commit()

    def _save_changes(self):
        self.conn.commit()

    def get_table_attribute_names(self, table_name):
        query = "PRAGMA table_info(%s)" % table_name
        self.cursor.execute(query)
        return [x[1] for x in self.cursor.fetchall()]
    """
    entry_values = tuple containing argument values corresponding to those defined before keyword values.
    """
    def add_member_entry(self, entry_values):
        self.cursor.execute("INSERT INTO CLAN(ime, prezime, nadimak, oib, mobitel, datum_rodenja, datum_uclanjenja, broj_iskaznice, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);" , entry_values)
        self._save_changes()

    def add_member_entry_full(self, entry_values):
        self.cursor.execute("INSERT INTO CLAN(ime, prezime, nadimak, oib, mobitel, datum_rodenja, datum_uclanjenja, broj_iskaznice, email, aktivan) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);" , entry_values)
        self._save_changes()

    def edit_member(self, member_id, new_values):
        self.cursor.execute("UPDATE CLAN SET ime = ?, prezime = ?, nadimak = ?, oib = ?, mobitel = ?, datum_rodenja = ?, datum_uclanjenja = ?, broj_iskaznice = ?, email = ? WHERE id = ?", new_values + (member_id, ))
        self._save_changes()

    def deactivate_member(self, member_id):
        deactivation_date = datetime.date.today()
        self.cursor.execute("UPDATE CLAN SET aktivan = 0, datum_deaktivacije = ? WHERE id = ?",
                            (deactivation_date, member_id,))
        self._save_changes()

    def activate_member(self, member_id):
        self.cursor.execute("UPDATE CLAN SET aktivan = 1, datum_deaktivacije = '-' WHERE id = ?", (member_id, ))
        self._save_changes()

    def add_member_to_section(self, entry_values):
        self.cursor.execute("INSERT INTO CLAN_SEKCIJE(id_clan, sekcija, datum_uclanjenja, maticna_sekcija) VALUES (?, ?, ?, ?);", entry_values)
        self._save_changes()

    def edit_member_section(self, entry_values):
        self.cursor.execute("UPDATE CLAN_SEKCIJE SET sekcija = ?, datum_uclanjenja = ? "
                            "WHERE id_clan = ? and maticna_sekcija = 1", entry_values)
        self._save_changes()

    def change_member_section_to_primary(self, member_id, section_name):
        self.cursor.execute("UPDATE CLAN_SEKCIJE SET maticna_sekcija = 1 WHERE id_clan = ? and sekcija = ?",
                            (member_id, section_name))
        self.cursor.execute("UPDATE CLAN_SEKCIJE SET maticna_sekcija = 0 WHERE id_clan = ? and sekcija != ?",
                            (member_id, section_name))
        self._save_changes()

    def add_member_card(self, entry_values):
        self.cursor.execute("INSERT INTO CLAN_ISKAZNICE (id_clan, iskaznica, datum_izdavanja) VALUES (?, ?, ?)", entry_values)
        self._save_changes()

    def edit_member_card(self, entry_values):
        self.cursor.execute("UPDATE CLAN_ISKAZNICE SET datum_izdavanja = ? WHERE id_clan = ? and iskaznica = ?", entry_values)
        self._save_changes()

    def get_member_card_ids(self):
        self.cursor.execute("SELECT broj_iskaznice FROM CLAN")
        return self.cursor.fetchall()

    def add_activity_entry(self, entry_values):
        self.cursor.execute("INSERT INTO AKTIVNOST(naziv, opis, datum, sekcija, id_vrsta_aktivnosti) "
                            "VALUES (?, ?, ?, ?, ?)", entry_values)
        self._save_changes()

    def edit_activity(self, activity_id, new_values):
        self.cursor.execute("UPDATE AKTIVNOST SET naziv = ?, opis = ?, datum= ?, sekcija = ?, id_vrsta_aktivnosti = ? "
                            "WHERE id = ?", new_values + (activity_id, ))
        self._save_changes()

    def add_activity_type_entry(self, entry_values):
        self.cursor.execute("INSERT INTO TIP_AKTIVNOSTI(naziv, opis, sekcija) VALUES (?, ?, ?)",
                            entry_values)
        self._save_changes()

    def edit_activity_type(self, activity_type_id, new_values):
        self.cursor.execute("UPDATE TIP_AKTIVNOSTI SET naziv = ?, opis = ?, sekcija = ? WHERE id = ?",
                            new_values + (activity_type_id, ))
        self._save_changes()

    def add_member_activity_entry(self, entry_values):
        self.cursor.execute("INSERT INTO CLAN_AKTIVNOST(id_clan, id_aktivnost, broj_sati, faktor) VALUES (?, ?, ?, ?)",
                            entry_values)
        self._save_changes()

    def edit_member_activity_entry(self, entry_values):
        self.cursor.execute("UPDATE CLAN_AKTIVNOST SET broj_sati = ?, faktor = ? "
                            "WHERE id_clan = ? and id_aktivnost = ?", entry_values)
        self._save_changes()

    def add_user_account(self, entry_values):
        self.cursor.execute("INSERT INTO ACCOUNTS (username, password, access_level, sekcija) VALUES (?, ?, ?, ?)",
                            entry_values)
        self._save_changes()

    def edit_user_account(self, user_id, new_values):
        self.cursor.execute("UPDATE ACCOUNTS SET username = ?, access_level = ?, sekcija = ? WHERE id = ?",
                            new_values + (user_id,))
        self._save_changes()

    def remove_entry(self, table_name, id):
        query = "DELETE FROM %s WHERE id = %s" % (table_name, id)
        self.cursor.execute(query)
        self._save_changes()

    def remove_member_activity_entry(self, activity_id=None, member_id=None):
        if activity_id is None and member_id is None:
            return
        base_query = "DELETE FROM CLAN_AKTIVNOST WHERE "
        if activity_id is not None:
            base_query += "id_aktivnost = %s " % activity_id
        if member_id is not None:
            if activity_id is not None:
                base_query += "AND "
            base_query += "id_clan = %s" % member_id
        self.cursor.execute(base_query)
        self._save_changes()

    def is_member_active(self, member_id):
        status = self.cursor.execute('SELECT aktivan FROM CLAN WHERE id = ?', (member_id,)).fetchone()[0]
        return status == 1

    """
    Methods that test existence of database entries.
    """
    def account_exists(self, username):
        self.cursor.execute('SELECT id FROM ACCOUNTS WHERE username = ?', (username, ))
        return self.cursor.fetchone() is not None

    def member_exists(self, card_id):
        query = 'SELECT id FROM CLAN WHERE broj_iskaznice = "%s"' % card_id
        self.cursor.execute(query)
        return self.cursor.fetchone() is not None

    def member_exists_by_name(self, name, last_name, nickname):
        query = 'SELECT id FROM CLAN WHERE ime = "%s" and prezime = "%s" and nadimak = "%s"' % (name, last_name, nickname)
        self.cursor.execute(query)
        return self.cursor.fetchone() is not None

    def activity_exists(self, name, date, section):
        self.cursor.execute('SELECT * FROM AKTIVNOST WHERE naziv = ? AND datum = ? AND sekcija = ?',
                            (name, date, section))
        return self.cursor.fetchone() is not None

    def activity_type_exists(self, name):
        self.cursor.execute('SELECT id FROM TIP_AKTIVNOSTI WHERE naziv = ?', (name, ))
        return self.cursor.fetchone() is not None

    def entry_exists(self, table_name, activity_id):
        query = 'SELECT id FROM %s WHERE id = %s' % (table_name, activity_id)
        self.cursor.execute(query)
        return self.cursor.fetchone() is not None

    def member_activity_exists(self, member_id, activity_id):
        return self.cursor.execute('SELECT id_clan, id_aktivnost FROM CLAN_AKTIVNOST WHERE id_clan = ? '
                                   'AND id_aktivnost = ?', (member_id, activity_id)).fetchone() is not None

    def member_has_card_color(self, member_id, card_color):
        return self.cursor.execute("SELECT iskaznica FROM CLAN_ISKAZNICE WHERE id_clan = ? and iskaznica = ?",
                                   (member_id, card_color)).fetchone() is not None

    """
    Generic method to fetch row with id from table table_name
    """
    def get_table_row(self, table_name, _id):
        query = "SELECT * FROM %s WHERE id = %d" % (table_name, _id)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_member_id(self, name, last_name, nickname=None):
        query = "SELECT * FROM CLAN WHERE ime = \"%s\" AND prezime = \"%s\"" % (name, last_name)
        if nickname is not None:
            query = "%s AND nadimak = \"%s\"" % (query, nickname)
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    """
    Method that gets an id from table table_name which attribute field is equal to value
    """
    def get_row(self, table_name, field, value, return_all=False):
        query = "SELECT * FROM %s WHERE %s = \"%s\"" % (table_name, field, value)
        self.cursor.execute(query)
        if not return_all:
            return self.cursor.fetchone()  # Fetch first one
        else:
            return self.cursor.fetchall()

    def get_all_monthly_activities(self, month=None):
        if month is None:
            month = datetime.datetime.now().month

        query = 'SELECT * FROM aktivnost WHERE strftime("%m", datum) = \"{0}\"'.format(month)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_full_activity_info(self, activity_id=None):
        query = "select AKTIVNOST.id, AKTIVNOST.naziv, AKTIVNOST.opis, datum, TIP_AKTIVNOSTI.naziv, " \
                "TIP_AKTIVNOSTI.opis, AKTIVNOST.sekcija from AKTIVNOST inner join TIP_AKTIVNOSTI " \
                "on AKTIVNOST.id_vrsta_aktivnosti = TIP_AKTIVNOSTI.id "

        if activity_id is not None:
            query = "%s WHERE AKTIVNOST.id = %s" % (query, activity_id)

        if session['access_level'] >= AccessLevels.SAVJETNIK:
            if activity_id is not None:
                query = "%s AND AKTIVNOST.sekcija = '%s'" % (query, session['section'])
            else:
                query = "%s WHERE AKTIVNOST.sekcija = '%s'" % (query, session['section'])
            query = "%s OR AKTIVNOST.sekcija = 'svi'" % query

        self.cursor.execute(query)

        return self.cursor.fetchall()

    def get_period_activity(self, start_date=None, end_date=None):
        if end_date is None:
            end_date = datetime.datetime.now()

        if start_date is None:
            start_date = end_date.replace(day=1)

        query = "select CLAN.id, ime, prezime, broj_sati, faktor, datum, AKTIVNOST.naziv, sekcija " \
                "from CLAN inner join CLAN_AKTIVNOST on CLAN.id = CLAN_AKTIVNOST.id_clan " \
                "inner join AKTIVNOST on CLAN_AKTIVNOST.id_aktivnost = AKTIVNOST.id " \
                "where datum >= '%s' and datum <= '%s'" % (start_date, end_date)


        # TODO: Ovdje se dohvaćaju svi aktivni članovi.
        # TODO: Potrebno je nekad promjeniti logiku i odmah filtrirati po sekcijama. Trenutno se filtrira u samim metodama.

        self.cursor.execute(query)

        return self.cursor.fetchall()

    def get_all_members_admin(self):
        return [x[:-1] for x in self.get_row(DatabaseTables.CLAN, "aktivan", 1, return_all=True)]

    def get_all_rows_from_table(self, table_name):
        query = "SELECT * FROM %s" % table_name
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_members(self):
        query = 'SELECT id, ime, prezime, nadimak, oib, mobitel, datum_rodenja, CLAN.datum_uclanjenja,' \
                'broj_iskaznice, email, sekcija, aktivan FROM CLAN inner join CLAN_SEKCIJE on ' \
                'CLAN.id = CLAN_SEKCIJE.id_clan WHERE sekcija = "%s" and aktivan = 1' \
                % session["section"]
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_member_by_card_id(self, card_id):
        query = 'SELECT id FROM CLAN WHERE broj_iskaznice = "%s"' % card_id
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_member_card_id(self, name, last_name, nickname):
        query = 'SELECT broj_iskaznice FROM CLAN WHERE ime = "%s" and prezime = "%s" and nadimak = "%s"' % (name, last_name, nickname)
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_member_card_color(self, member_id):
        self.cursor.execute("SELECT iskaznica FROM CLAN_ISKAZNICE WHERE id_clan = ? "
                            "ORDER BY date(datum_izdavanja) DESC", (member_id, ))
        return self.cursor.fetchone()[0]

    def get_member_primary_section(self, member_id):
        self.cursor.execute("SELECT sekcija FROM CLAN inner join CLAN_SEKCIJE on CLAN.id = CLAN_SEKCIJE.id_clan "
                            "WHERE id = ? and maticna_sekcija = 1", (member_id, ))
        return self.cursor.fetchone()[0]

    def get_all_members_sections(self, member_id):
        self.cursor.execute("SELECT sekcija FROM CLAN inner join CLAN_SEKCIJE on CLAN.id = CLAN_SEKCIJE.id_clan "
                            "WHERE id = ?", (member_id,))
        return [x[0] for x in self.cursor.fetchall()]

    def get_all_accounts(self):
        query = "SELECT id, username, access_level, sekcija FROM ACCOUNTS where access_level >= %d" % session['access_level']
        return self.cursor.execute(query).fetchall()

    def get_activity_members(self, activity_id, section_specific=False):
        query = "SELECT id, ime, prezime, CLAN_AKTIVNOST.broj_sati, CLAN_AKTIVNOST.faktor " \
                "FROM CLAN inner join CLAN_AKTIVNOST on CLAN.id = CLAN_AKTIVNOST.id_clan " \
                "inner join CLAN_SEKCIJE on CLAN.id = CLAN_SEKCIJE.id_clan " \
                "WHERE CLAN_AKTIVNOST.id_aktivnost = %d AND broj_sati > 0" % int(activity_id)

        if section_specific:
            query = "%s AND sekcija = '%s'" % (query, session['section'])

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_section_activitiy_types(self):
        query = 'SELECT * FROM %s where sekcija = "%s" or sekcija = "svi"' \
                % (DatabaseTables.TIP_AKTIVNOSTI, session['section'])
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_activities_for_member(self, member_id, start_date=None, end_date=None):
        query = "select AKTIVNOST.id_vrsta_aktivnosti, AKTIVNOST.naziv, broj_sati, faktor " \
                "from CLAN inner join CLAN_AKTIVNOST on CLAN.id = CLAN_AKTIVNOST.id_clan " \
                "inner join AKTIVNOST on CLAN_AKTIVNOST.id_aktivnost = AKTIVNOST.id " \
                "where CLAN.id = %d" % (int(member_id))

        if start_date is not None:
            query = "%s and AKTIVNOST.datum >= '%s'" % (query, start_date)

        if end_date is not None:
            query = "%s and AKTIVNOST.datum <= '%s'" % (query, end_date)

        return self.cursor.execute(query).fetchall()

    def get_all_activities_after_date(self, section, start_date, end_date=None):
        query = "select TIP_AKTIVNOSTI.id, datum, AKTIVNOST.naziv, TIP_AKTIVNOSTI.naziv, " \
                "AKTIVNOST.sekcija from AKTIVNOST inner join TIP_AKTIVNOSTI " \
                "on AKTIVNOST.id_vrsta_aktivnosti = TIP_AKTIVNOSTI.id where datum >= '%s' " \
                "and AKTIVNOST.sekcija = '%s'" % (start_date, section)

        if end_date is not None:
            query = "%s and datum <= '%s'" % (query, end_date)

        return self.cursor.execute(query).fetchall()

    def get_all_volunteering_events(self, section, start_date, end_date=None):
        query = "select TIP_AKTIVNOSTI.id, datum, AKTIVNOST.naziv, TIP_AKTIVNOSTI.naziv, " \
                "AKTIVNOST.sekcija from AKTIVNOST inner join TIP_AKTIVNOSTI " \
                "on AKTIVNOST.id_vrsta_aktivnosti = TIP_AKTIVNOSTI.id where datum >= '%s' " \
                "and AKTIVNOST.sekcija = '%s' and TIP_AKTIVNOSTI.naziv = 'Dežurstvo'" % (start_date, section)

        if end_date is not None:
            query = "%s and datum <= '%s'" % (query, end_date)

        return self.cursor.execute(query).fetchall()

    # Card_id format is <letter><letter>-<year><year>
    def generate_new_card_id(self):
        current_card_ids = self.get_member_card_ids()
        this_year = str(datetime.date.today().year)[-2:]
        if len(current_card_ids) == 0:
            return "aa-%s" % this_year
        last_id = None
        for card_id_tuple in current_card_ids:
            card_id = card_id_tuple[0]
            if '-' in card_id:
                letters, numbers = card_id.split("-")
                if numbers == this_year:
                    if last_id is None:
                        last_id = card_id
                    elif card_id > last_id:
                        last_id = card_id

        letters, numbers = last_id.split("-")
        if letters[1] == 'z':
            letters = "%sa" % chr(ord(letters[0]) + 1)
        else:
            letters = "%s%s" % (letters[0], chr(ord(letters[1]) + 1))

        return "-".join((letters, numbers))

    def get_last_row_id(self):
        return self.cursor.lastrowid

