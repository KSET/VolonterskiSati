import sys, csv
from import_utility import import_data
import DatabaseTables
from DatabaseController import DatabaseController, get_date_object
from Utilities import Iskaznice, sections
import datetime

DATE_FORMAT = "%d.%m.%Y."
DELIMITER = ';'


def __get_member_entry_format(entry_data):
    return (
        entry_data['ime'],
        entry_data['prezime'],
        entry_data['nadimak'],
        entry_data['oib'],
        entry_data['mobitel'],
        entry_data['datum_rodenja'],
        entry_data['datum_uclanjenja'],
        entry_data['broj_iskaznice'],
        entry_data['email'],
        entry_data['aktivan']
    )


def __get_member_card_color(card_color_string):
    card_color_string = card_color_string.lower()
    if card_color_string == 'plava':
        return Iskaznice.PLAVA
    elif 'naran' in card_color_string:
        return Iskaznice.NARANCASTA
    elif card_color_string == 'crvena':
        return Iskaznice.CRVENA

    raise ValueError()


if __name__ == '__main__':
    input_file_path = sys.argv[1]
    db = DatabaseController()
    members_attributes = DatabaseController().get_table_attribute_names(DatabaseTables.CLAN)
    members_attributes.pop(0)  # Remove id
    print("Starting import_members script...")
    try:
        csv_file = open(input_file_path, "r")
        print("Successfully loaded file...")
    except Exception as e:
        print("ERROR while loading file: %s. Please check file path and read permissions." % input_file_path)
        sys.exit(1)

    input_data = csv.DictReader(csv_file, delimiter=DELIMITER)
    input_data_keys = [x.lower() for x in input_data.fieldnames]
    for row in input_data:
        entry_data = {}
        for attribute in members_attributes:
            if attribute not in input_data_keys:
                if attribute == 'broj_iskaznice':
                    entry_data[attribute] = db.generate_new_card_id()
                else:
                    entry_data[attribute] = '-'
            else:
                if attribute == 'broj_iskaznice' and not row[attribute]:
                    entry_data[attribute] = db.generate_new_card_id()
                elif 'datum' in attribute:
                    entry_data[attribute] = get_date_object(row[attribute], DATE_FORMAT)
                else:
                    entry_data[attribute] = row[attribute]

        name, last_name, nickname = entry_data['ime'], entry_data['prezime'], entry_data['nadimak']
        if db.member_exists_by_name(name, last_name, nickname):
            print("Member %s %s (%s) is already in the database. No action was done." % (name, last_name, nickname))
            continue

        card_color = None
        if "boja_iskaznice" in input_data_keys:
            try:
                entry_data['boja_iskaznice'] = __get_member_card_color(row['boja_iskaznice'])
            except ValueError as e:
                print("Card color value for member %s %s must be either plava, narancasta or crvena. Current value is %s"
                      % (name, last_name, row['boja_iskaznice']))
                sys.exit(1)

            card_color = entry_data['boja_iskaznice']

        try:
            section = row['section']
            if section not in sections.keys():
                print("Section name is defined wrong. Please use one of the following names: %s" % sections.keys())
                sys.exit(1)
        except Exception as e:
            print("Section column must be defined. Please create and define section for every member.")
            sys.exit(1)

        membership_start = entry_data['datum_uclanjenja']
        try:
            db.add_member_entry_full(__get_member_entry_format(entry_data))
        except Exception as e:
            print("Failed to add member %s %s to database. Error: %s" % (name, last_name, e))
            sys.exit(1)

        print("Member %s %s is successfully added to database!" % (name, last_name))
        try:
            if card_color is None:
                card_color = Iskaznice.PLAVA
            db.add_member_card((db.get_member_id(name, last_name, nickname), card_color, membership_start))
        except Exception as e:
            print("Failed to assign card color to member %s %s. Error: %s" % (name, last_name, e))
            sys.exit(1)

        print("Successfully assigned card color %s to member %s %s!" % (row['boja_iskaznice'], name, last_name))

        member_id = db.get_member_id(name, last_name, nickname)
        native_section = 1  # Sekcija novododanog člana je matična
        try:
            db.add_member_to_section((member_id, section, membership_start, native_section))
        except Exception as e:
            print("Failed to add member %s %s to section %s. Error: %s" % (name, last_name, section, e))

        print("Successfully added member %s %s to section %s!" % (name, last_name, section))
