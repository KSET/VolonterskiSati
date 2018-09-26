from DatabaseController import DatabaseController

if __name__ == '__main__':
    db = DatabaseController()
    db._init_tables()
    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print(db.cursor.fetchall())
    db.cursor.execute("SELECT * from CLAN")
    print(db.cursor.fetchall())
    entry_values = ('Mladen','Petr','456','098-test','1994-02-26','2016-10-18','420','promjeni.me@kset.org','foto')
    db._add_user_entry(entry_values)
    db.cursor.execute("SELECT * from CLAN")
    print(db.cursor.fetchall())
    new_values = ('Mladen','Petir','123','091-test','1994-02-26','2016-10-18','420','promjenio.sam@kset.org','foto')
    db._edit_user_entry(1,new_values)
    db.cursor.execute("SELECT * from CLAN")
    print(db.cursor.fetchall())