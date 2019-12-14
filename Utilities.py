from constants import *

DATE_FORMAT = "%Y-%m-%d"
sections = {
    'svi': Sekcije.SVI,
    'bike': Sekcije.BIKE,
    'disco': Sekcije.DISCO,
    'dramska': Sekcije.DRAMSKA,
    'foto': Sekcije.FOTO,
    'glazbena': Sekcije.GLAZBENA,
    'pijandure': Sekcije.PLANINARSKA,
    'comp': Sekcije.RACUNARSKA,
    'tech': Sekcije.TEHNICKA,
    'video': Sekcije.VIDEO
}

shirt_sizes = {
    'mxxl': ShirtSizes.MXXL,
    'mxl': ShirtSizes.MXL,
    'ml': ShirtSizes.ML,
    'mm': ShirtSizes.MM,
    'ms': ShirtSizes.MS,
    'zxl': ShirtSizes.ZXL,
    'zl': ShirtSizes.ZL,
    'zm': ShirtSizes.ZM,
    'zs': ShirtSizes.ZS,
    'zxs': ShirtSizes.ZXS
}

teams = {
    'pr': Timovi.PR,
    'dizajn': Timovi.DIZAJN
}

sections_and_teams = {**sections, **teams}

card_colors = {
    Iskaznice.CRVENA: "Crvena",
    Iskaznice.NARANCASTA: "Narančasta",
    Iskaznice.PLAVA: "Plava"
}
