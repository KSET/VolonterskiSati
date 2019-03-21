CREATE_USER_TABLE = "CREATE TABLE IF NOT EXISTS CLAN (id integer primary key, ime text, prezime text, nadimak text," \
                    " oib text default '-', mobitel text default '-', datum_rodenja date default '-'," \
                    " datum_uclanjenja date default '-', broj_iskaznice text default '-', email text default '-'," \
                    " sekcija text default '-', aktivan int default 1);"

CREATE_ACTIVITY_TABLE = "CREATE TABLE IF NOT EXISTS AKTIVNOST (id integer primary key, naziv text," \
                        " opis text default '-', datum date default '-', id_vrsta_aktivnosti integer default none," \
                        " foreign key(id_vrsta_aktivnosti) references TIP_AKTIVNOSTI(id));"

CREATE_ACTIVITY_TYPE_TABLE = "CREATE TABLE IF NOT EXISTS TIP_AKTIVNOSTI (id integer primary key, naziv text," \
                             " opis text default '-');"

CREATE_ACTIVITY_USER_RELATIONSHIP_TABLE = "CREATE TABLE IF NOT EXISTS CLAN_AKTIVNOST (id_clan integer," \
                                          " id_aktivnost integer, broj_sati real, faktor real," \
                                          " foreign key(id_clan) references CLAN(id)," \
                                          " foreign key(id_aktivnost) references AKTIVNOST(id));"

CREATE_ACCOUNTS_TABLE = "CREATE TABLE IF NOT EXISTS ACCOUNTS (id integer primary key, username text," \
                        " password text, access_level text, sekcija text);"
