import json
import sqlite3

with open('db/SeedBot Metrics.json', encoding="utf-8") as infile:
    inflow = json.load(infile)
with open('db/user_presets.json', encoding="utf-8") as infile:
    pinflow = json.load(infile)
    
conn = sqlite3.connect('db/seeDBot.sqlite')

cur2 = conn.cursor()
cur2.execute("CREATE TABLE IF NOT EXISTS seedlist (creator_id INTEGER, creator_name TEXT, seed_type TEXT, share_url TEXT, timestamp TEXT, server_name TEXT, server_id INTEGER, channel_name TEXT, channel_id INTEGER)")
for item in inflow:
    cur2.execute("INSERT INTO seedlist VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (item['creator_id'],item['creator_name'],item['seed_type'],item['share_url'],item['timestamp'],item['server_name'],item['server_id'],item['channel_name'],item['channel_id']))

# curcount = conn.cursor()
# curcount.execute("SELECT seed_type FROM seedlist WHERE seed_type LIKE '%' || 'preset_' || '%' ")
# thisquery = curcount.fetchall()
# curpluscount = conn.cursor()
# pgens = {}
# for x in thisquery:
#     pcheck = x[0].split("preset_")[1:][0].split("_")[:1]
#     print(f'pcheck = {pcheck[0]}')
#     pgens = pcheck[0]
#     try:
#         pgens['c'] += 1
#     except KeyError:
#         pgens['c'] = 1
# print(f'pgens = {pgens}')

cur1 = conn.cursor()
cur1.execute("CREATE TABLE IF NOT EXISTS presets (preset_name TEXT PRIMARY KEY, creator_id INTEGER, creator_name TEXT, created_at TEXT, flags TEXT, description TEXT, arguments TEXT, official INTEGER, hidden INTEGER, gen_count INTEGER)")
for item in pinflow.values():
    try:
        if item['official']:
            o = True
        else:
            o = False
    except KeyError:
        o = False
    try:
        if item['hidden']:
            if item['hidden'] == "true":
                h = True
            else:
                h = False
    except KeyError:
        h = False
    cur1.execute("INSERT INTO presets (preset_name, creator_id, creator_name, flags, description, arguments, official, hidden, gen_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (item['name'], item['creator_id'], item['creator'],item['flags'],item['description'],item['arguments'], o, h, 0))

conn.commit()
conn.close()