import pygsheets

def get_users_n_roles():
    gc = pygsheets.authorize(service_file='db/seedbot-metrics-4134ac812cac.json')
    sh = gc.open('Ultros League Standings')
    wks = sh[6]

    cells = wks.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
    return cells
