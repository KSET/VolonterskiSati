class Sekcije:
    BIKE = 'Bike'
    DISCO = 'Disco'
    DRAMSKA = 'Dramska'
    FOTO = 'Foto'
    GLAZBENA = 'Glazbena'
    PLANINARSKA = 'Pijandure'
    RACUNARSKA = 'Računarska'
    TEHNICKA = 'Tech'
    VIDEO = 'Video'
    SVI = 'Svi'


class Timovi:
    PR = 'Pr'
    DIZAJN = 'Dizajn'


class Iskaznice:
    CRVENA = 0
    NARANCASTA = 1
    PLAVA = 2


class AccessLevels:
    ADMIN = 0
    SAVJETNIK = 1
    NARANCASTI_CLAN = 2
    PLAVI_CLAN = 3

    access_levels_string = {
        ADMIN: 'Administrator',
        SAVJETNIK: 'Savjetnik',
        NARANCASTI_CLAN: 'Narančasti član',
        PLAVI_CLAN: 'Plavi član'
    }


