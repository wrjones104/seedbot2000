import random
from random import randrange
from struct import pack

from .common import constants
from .common.ff6_rom import FF6_ROM

bad_mobs = {282: [0xFF, 0xFF, 0xFF, 0xFF], 298: [0xFF, 0xEF, 0xFF, 0xFF], 366: [0xB1, 0xF0, 0xF5, 0xFF],
            367: [0xFF, 0xFF, 0xFF, 0xFF], 370: [0xFF, 0xFF, 0xFF, 0xFF], 371: [0xFF, 0xFF, 0xFF, 0xFF],
            372: [0xFF, 0xFF, 0xFF, 0xFF], 375: [0xFF, 0xFF, 0xFF, 0xFF], 376: [0xFF, 0xFF, 0xFF, 0xFF],
            378: [0xFF, 0xFF, 0xFF, 0xFF], 379: [0xFF, 0xFF, 0xFF, 0xFF], 380: [0xFF, 0xFF, 0xFF, 0xFF],
            382: [0xFF, 0xFF, 0xFF, 0xFF], 383: [0xFF, 0xFF, 0xFF, 0xFF]}
dragons = {36: [0x21, 0xEA, 0x21, 0x21], 329: [0xFF, 0xFF, 0x68, 0x68], 331: [0xFF, 0xFF, 0x94, 0x94],
           332: [0xEA, 0xFF, 0x3C, 0x3C], 336: [0xFF, 0xFF, 0xCC, 0xCC], 337: [0xFF, 0xFF, 0xC8, 0xC8],
           338: [0xFF, 0xFF, 0x19, 0x19], 339: [0xFF, 0xFF, 0x31, 0x31]}
miabs = {25: [0xE8, 0xE8, 0xE8, 0xFF], 68: [0xEA, 0xFF, 0x72, 0x72], 174: [0xEE, 0xEA, 0x28, 0x28],
         187: [0xE9, 0xE8, 0x59, 0x59], 192: [0xEA, 0xFF, 0xFF, 0xFF], 255: [0x9C, 0xFF, 0x9C, 0xFF],
         257: [0xFF, 0xFF, 0x58, 0x58], 292: [0x31, 0x2F, 0xD3, 0xD3], 309: [0xFF, 0xFF, 0x58, 0x58],
         312: [0xEF, 0xEE, 0x08, 0x08], 342: [0xFF, 0xFF, 0xD2, 0xD2]}
statues = {295: [0xDC, 0xFF, 0x32, 0x32], 296: [0x9C, 0xFF, 0x18, 0x18], 297: [0x93, 0xFF, 0x23, 0x23]}
toptiers = (0x09, 0x1A, 0x1B, 0x1C, 0x23, 0x52, 0x67, 0x60, 0x61, 0x62, 0x78, 0x80, 0x9C, 0xA1, 0xA2, 0xD3, 0xE4)


def poverty():
    new_drops = b''
    for j in range(constants.MONSTER_COUNT):
        for i in range(constants.MONSTER_DROP_SIZE):
            item = 0xFF
            new_drops += pack('B', item)
    return new_drops


def true_loot():
    new_drops = b''
    for j in range(constants.MONSTER_COUNT):
        if j in bad_mobs:
            for i in range(constants.MONSTER_DROP_SIZE):
                item = bad_mobs[j][i]
                new_drops += pack('B', item)
        else:
            for i in range(constants.MONSTER_DROP_SIZE):
                item = randrange(len(constants.ITEMS.keys()))
                new_drops += pack('B', item)
    return new_drops


def loot():
    new_drops = b''
    for j in range(constants.MONSTER_COUNT):
        if j in bad_mobs:
            for i in range(constants.MONSTER_DROP_SIZE):
                item = bad_mobs[j][i]
                new_drops += pack('B', item)
        elif j in miabs:
            for i in range(constants.MONSTER_DROP_SIZE):
                item = miabs[j][i]
                new_drops += pack('B', item)
        elif j in dragons:
            for i in range(constants.MONSTER_DROP_SIZE):
                item = dragons[j][i]
                new_drops += pack('B', item)
        elif j in statues:
            for i in range(constants.MONSTER_DROP_SIZE):
                item = statues[j][i]
                new_drops += pack('B', item)
        else:
            for i in range(constants.MONSTER_DROP_SIZE):
                item = randrange(len(constants.ITEMS.keys()))
                new_drops += pack('B', item)
    return new_drops


def all_pally():
    new_drops = b''
    for j in range(constants.MONSTER_COUNT):
        if j in bad_mobs:
            for i in range(constants.MONSTER_DROP_SIZE):
                item = bad_mobs[j][i]
                new_drops += pack('B', item)
        elif j in miabs:
            for i in range(constants.MONSTER_DROP_SIZE):
                item = miabs[j][i]
                new_drops += pack('B', item)
        elif j in dragons:
            for i in range(constants.MONSTER_DROP_SIZE):
                item = dragons[j][i]
                new_drops += pack('B', item)
        elif j in statues:
            for i in range(constants.MONSTER_DROP_SIZE):
                item = statues[j][i]
                new_drops += pack('B', item)
        else:
            for i in range(constants.MONSTER_DROP_SIZE):
                item = 0x67
                new_drops += pack('B', item)
    return new_drops


def top_tiers():
    new_drops = b''
    for j in range(constants.MONSTER_COUNT):
        if j in bad_mobs:
            for i in range(constants.MONSTER_DROP_SIZE):
                item = bad_mobs[j][i]
                new_drops += pack('B', item)
        elif j in miabs:
            for i in range(constants.MONSTER_DROP_SIZE):
                item = miabs[j][i]
                new_drops += pack('B', item)
        elif j in dragons:
            for i in range(constants.MONSTER_DROP_SIZE):
                item = dragons[j][i]
                new_drops += pack('B', item)
        elif j in statues:
            for i in range(constants.MONSTER_DROP_SIZE):
                item = statues[j][i]
                new_drops += pack('B', item)
        else:
            for i in range(constants.MONSTER_DROP_SIZE):
                item = random.choice(toptiers)
                new_drops += pack('B', item)
    return new_drops


def run_item_rando(arg):
    input_file_path = '../worldscollide/seedbot.smc'
    output_file_path = '../worldscollide/seedbot.smc'
    wcrom = FF6_ROM(input_file_path)
    modified_data = bytearray(wcrom.data)
    offset = (wcrom.has_header * constants.HEADER_SIZE)
    drop_loc = constants.MONSTER_DROP_LOC + offset
    modified_data[drop_loc: drop_loc + constants.MONSTER_COUNT * constants.MONSTER_DROP_SIZE] = arg
    wcrom.data = modified_data
    wcrom.write(output_file_path, overwrite=True)
