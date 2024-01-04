from struct import pack

from .common import constants
from .common.ff6_rom import FF6_ROM


# steve = pack('B', constants.CHAR_TO_CODE["S"]) + \
#        pack('B', constants.CHAR_TO_CODE["t"]) + \
#        pack('B', constants.CHAR_TO_CODE["e"]) + \
#        pack('B', constants.CHAR_TO_CODE["v"]) + \
#        pack('B', constants.CHAR_TO_CODE["e"]) + \
#        pack('B', constants.CHAR_TO_CODE[''])

def steveify(s, f):
    # Parse incoming STEVE name
    if not s:
        steve = pack('B', constants.CHAR_TO_CODE["S"]) + \
                pack('B', constants.CHAR_TO_CODE["t"]) + \
                pack('B', constants.CHAR_TO_CODE["e"]) + \
                pack('B', constants.CHAR_TO_CODE["v"]) + \
                pack('B', constants.CHAR_TO_CODE["e"]) + \
                pack('B', constants.CHAR_TO_CODE[''])
    else:
        if len(s) < 6:
            extras = 6 - len(s)
            while extras > 0:
                s += " "
                extras -= 1
        steve = pack('B', constants.CHAR_TO_CODE[s[0]]) + \
                pack('B', constants.CHAR_TO_CODE[s[1]]) + \
                pack('B', constants.CHAR_TO_CODE[s[2]]) + \
                pack('B', constants.CHAR_TO_CODE[s[3]]) + \
                pack('B', constants.CHAR_TO_CODE[s[4]]) + \
                pack('B', constants.CHAR_TO_CODE[s[5]])

    # Read in a WC ROM
    input_file_path = 'WorldsCollide/seeds/'+f+'.smc'
    output_file_path = 'WorldsCollide/seeds/'+f+'.smc'
    wcrom = FF6_ROM(input_file_path)
    modified_data = bytearray(wcrom.data)
    offset = (wcrom.has_header * constants.HEADER_SIZE)

    # What shall we Steve?
    STEVEIFY_CHARACTERS = True
    STEVEIFY_SWDTECH = True
    STEVEIFY_MONSTER_NAMES = True
    STEVEIFY_MONSTER_ATTACK_NAMES = True
    STEVEIFY_ITEM_NAMES = True
    STEVEIFY_MAGIC_NAMES = True
    STEVEIFY_ESPER_NAMES = True
    STEVEIFY_ATTACK_NAMES = True
    STEVEIFY_ESPER_ATTACK_NAMES = True
    STEVEIFY_DANCE_NAMES = True
    STEVEIFY_TRACK = False

    if STEVEIFY_CHARACTERS:
        steve_this = steveify_characters(steve)
        loc = offset + constants.CHAR_NAME_LOC
        count = constants.CHARACTER_COUNT
        size = constants.CHAR_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_SWDTECH:
        steve_this = steveify_swdtech(steve)
        loc = offset + constants.SWDTECH_NAME_LOC
        count = constants.SWDTECH_NAME_COUNT
        size = constants.SWDTECH_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_MONSTER_NAMES:
        steve_this = steveify_monster_names(steve)
        loc = offset + constants.MONSTER_NAME_LOC
        count = constants.MONSTER_COUNT
        size = constants.MONSTER_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_MONSTER_ATTACK_NAMES:
        steve_this = steveify_monster_attack_names(steve)
        loc = offset + constants.MONSTER_ATTACK_NAME_LOC
        count = constants.MONSTER_COUNT
        size = constants.MONSTER_ATTACK_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_ITEM_NAMES:
        steve_this = steveify_item_names(steve)
        loc = offset + constants.ITEM_NAME_LOC
        count = constants.ITEM_COUNT
        size = constants.ITEM_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_MAGIC_NAMES:
        steve_this = steveify_magic_names(steve)
        loc = offset + constants.MAGIC_NAME_LOC
        count = constants.MAGIC_COUNT
        size = constants.MAGIC_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_ESPER_NAMES:
        steve_this = steveify_esper_names(steve)
        loc = offset + constants.ESPER_NAME_LOC
        count = constants.ESPER_COUNT
        size = constants.ESPER_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_ATTACK_NAMES:
        steve_this = steveify_attack_names(steve)
        loc = offset + constants.ATTACK_NAME_LOC
        count = constants.ATTACK_COUNT
        size = constants.ATTACK_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_ESPER_ATTACK_NAMES:
        steve_this = steveify_esper_attack_names(steve)
        loc = offset + constants.ESPER_ATTACK_NAME_LOC
        count = constants.ESPER_COUNT
        size = constants.ESPER_ATTACK_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_DANCE_NAMES:
        steve_this = steveify_dance_names(steve)
        loc = offset + constants.DANCE_NAME_LOC
        count = constants.DANCE_COUNT
        size = constants.DANCE_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_TRACK:
        steve_this = steve[:5]
        loc = offset + 0x3F481
        count = 1
        size = 5
        modified_data[loc: loc + count * size] = steve_this

    wcrom.data = modified_data
    wcrom.write(output_file_path, overwrite=True)


def steveify_characters(steve):
    new_data = b''
    for j in range(constants.CHARACTER_COUNT):
        new_data += steve
    return new_data


def steveify_swdtech(steve):
    new_data = b''
    for j in range(constants.SWDTECH_NAME_COUNT):
        name = steve
        while len(name) < constants.SWDTECH_NAME_SIZE:
            name += pack('B', constants.CHAR_TO_CODE[''])
        new_data += name
    return new_data


def steveify_monster_names(steve):
    new_data = b''
    for j in range(constants.MONSTER_COUNT):
        name = steve
        while len(name) < constants.MONSTER_NAME_SIZE:
            name += pack('B', constants.CHAR_TO_CODE[''])
        new_data += name
    return new_data


def steveify_monster_attack_names(steve):
    new_data = b''
    for j in range(constants.MONSTER_COUNT):
        name = steve
        while len(name) < constants.MONSTER_ATTACK_NAME_SIZE:
            name += pack('B', constants.CHAR_TO_CODE[''])
        new_data += name
    return new_data


def steveify_item_names(steve):
    new_data = b''
    counter = 0
    for j in range(constants.ITEM_COUNT):
        item_type = constants.ITEMS[counter][0]
        name = pack('B', constants.CHAR_TO_CODE[item_type]) + steve
        while len(name) < constants.ITEM_NAME_SIZE:
            name += pack('B', constants.CHAR_TO_CODE[''])
        new_data += name
        counter += 1
    return new_data


def steveify_magic_names(steve):
    new_data = b''
    for j in range(constants.MAGIC_COUNT):
        magic_type = constants.SPELLS[j][0]
        name = pack('B', constants.CHAR_TO_CODE[magic_type]) + steve
        if '2' in constants.SPELLS[j] or '3' in constants.SPELLS[j]:
            spell_level = constants.SPELLS[j]
            while spell_level[-1] == '_':
                spell_level = spell_level[:-1]
            spell_level = spell_level[-1]

            spell_level = constants.CHAR_TO_CODE[spell_level]
            name = pack('B', constants.CHAR_TO_CODE[magic_type]) + steve[:-1]
            name += pack('B', spell_level)
        while len(name) < constants.MAGIC_NAME_SIZE:
            name += pack('B', constants.CHAR_TO_CODE[''])
        new_data += name

    return new_data


def steveify_esper_names(steve):
    new_data = b''
    for j in range(constants.ESPER_COUNT):
        name = steve
        while len(name) < constants.ESPER_NAME_SIZE:
            name += pack('B', constants.CHAR_TO_CODE[''])
        new_data += name
    return new_data


def steveify_attack_names(steve):
    new_data = b''
    for j in range(constants.ATTACK_COUNT):
        name = steve
        while len(name) < constants.ATTACK_NAME_SIZE:
            name += pack('B', constants.CHAR_TO_CODE[''])
        new_data += name
    return new_data


def steveify_esper_attack_names(steve):
    new_data = b''
    for j in range(constants.ESPER_COUNT):
        name = steve
        while len(name) < constants.ESPER_ATTACK_NAME_SIZE:
            name += pack('B', constants.CHAR_TO_CODE[''])
        new_data += name
    return new_data


def steveify_dance_names(steve):
    new_data = b''
    for j in range(constants.DANCE_COUNT):
        name = steve
        while len(name) < constants.DANCE_NAME_SIZE:
            name += pack('B', constants.CHAR_TO_CODE[''])
        new_data += name
    return new_data
