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


class InviteCodes:
    INVITE_CODE_ADMIN = "pbkdf2:sha256:50000$CV4TAYsJ$f05d7ba9164169993524047ef2dbf38f1cb4deb2e7a34251e0d8f212442c182a"
    INVITE_CODE_SAVJETNIK = "pbkdf2:sha256:50000$zZCHObnJ$1463be39bb7a35b05e4ae4102ea717f0f8cdeef7fe2ef2f2ea2958674b44eb43"
    INVITE_CODE_NARANCASTI = "pbkdf2:sha256:50000$bV8W4EQ1$625159b3c3715a7563e5f39daadb19daad54e8ef419e0d83d84043862797236f"
    INVITE_CODE_PLAVI = "pbkdf2:sha256:50000$orUxUE5t$d6ff52038d9b9329cce5fed953ca9cb4cde226adc5c8bac1e2d3f48cd0f20b2b"

    INVITE_CODES_LIST = [INVITE_CODE_ADMIN, INVITE_CODE_SAVJETNIK, INVITE_CODE_NARANCASTI, INVITE_CODE_PLAVI]

    invite_codes_roles = {
        INVITE_CODE_ADMIN: AccessLevels.ADMIN,
        INVITE_CODE_SAVJETNIK: AccessLevels.SAVJETNIK,
        INVITE_CODE_NARANCASTI: AccessLevels.NARANCASTI_CLAN,
        INVITE_CODE_PLAVI: AccessLevels.PLAVI_CLAN
    }


