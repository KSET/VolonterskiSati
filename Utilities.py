import sekcije
import iskaznice

DATE_FORMAT = "%Y-%m-%d"
sections = {
    'svi': sekcije.SVI,
    'bike': sekcije.BIKE,
    'disco': sekcije.DISCO,
    'dramska': sekcije.DRAMSKA,
    'foto': sekcije.FOTO,
    'glazbena': sekcije.GLAZBENA,
    'pijandure': sekcije.PLANINARSKA,
    'comp': sekcije.RACUNARSKA,
    'tech': sekcije.TEHNICKA,
    'video': sekcije.VIDEO
}

card_colors = {
    iskaznice.CRVENA: "Crvena",
    iskaznice.NARANCASTA: "Narančasta",
    iskaznice.PLAVA: "Plava"
}
