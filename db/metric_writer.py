import pygsheets


def write_gsheets(m):
    gc = pygsheets.authorize(service_file='db/seedbot-metrics-4134ac812cac.json')
    sh = gc.open('SeedBot Metrics')
    wks = sh[0]

    cells = wks.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
    lastrow = len(cells)

    wks.insert_rows(lastrow, number=1, values=[m['creator_id'], m['creator_name'], m['seed_type'], m['random_sprites'],
                                                 m['share_url'], m['timestamp'], m['server_name'], m['server_id'],
                                                 m['channel_name'], m['channel_id']])
