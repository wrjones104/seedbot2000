from struct import pack
from bot.common import constants
from bot.common.ff6_rom import FF6_ROM

def steveify(s, smc_path):
    # Parse incoming STEVE name
    if not s or s.isspace():
        steve_name_str = "Steve"
    else:
        steve_name_str = s

    # Ensure the name is 6 characters for character names
    char_name_str = steve_name_str[:6]
    if len(char_name_str) < 6:
        char_name_str = char_name_str.ljust(6)

    steve = bytearray()
    for char in char_name_str:
        steve.append(constants.CHAR_TO_CODE.get(char, constants.CHAR_TO_CODE[' ']))
    steve = bytes(steve)

    # Read in a WC ROM from the provided path
    wcrom = FF6_ROM(smc_path)
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

    # For other fields, use the original (potentially longer) steve name
    steve_long_bytes = bytearray()
    for char in steve_name_str:
        steve_long_bytes.append(constants.CHAR_TO_CODE.get(char, constants.CHAR_TO_CODE[' ']))
    steve_long = bytes(steve_long_bytes)


    if STEVEIFY_SWDTECH:
        steve_this = steveify_generic(steve_long, constants.SWDTECH_NAME_COUNT, constants.SWDTECH_NAME_SIZE)
        loc = offset + constants.SWDTECH_NAME_LOC
        count = constants.SWDTECH_NAME_COUNT
        size = constants.SWDTECH_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_MONSTER_NAMES:
        steve_this = steveify_generic(steve_long, constants.MONSTER_COUNT, constants.MONSTER_NAME_SIZE)
        loc = offset + constants.MONSTER_NAME_LOC
        count = constants.MONSTER_COUNT
        size = constants.MONSTER_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_MONSTER_ATTACK_NAMES:
        steve_this = steveify_generic(steve_long, constants.MONSTER_COUNT, constants.MONSTER_ATTACK_NAME_SIZE)
        loc = offset + constants.MONSTER_ATTACK_NAME_LOC
        count = constants.MONSTER_COUNT
        size = constants.MONSTER_ATTACK_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_ITEM_NAMES:
        steve_this = steveify_item_names(steve_long)
        loc = offset + constants.ITEM_NAME_LOC
        count = constants.ITEM_COUNT
        size = constants.ITEM_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_MAGIC_NAMES:
        steve_this = steveify_magic_names(steve_long)
        loc = offset + constants.MAGIC_NAME_LOC
        count = constants.MAGIC_COUNT
        size = constants.MAGIC_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_ESPER_NAMES:
        steve_this = steveify_generic(steve_long, constants.ESPER_COUNT, constants.ESPER_NAME_SIZE)
        loc = offset + constants.ESPER_NAME_LOC
        count = constants.ESPER_COUNT
        size = constants.ESPER_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_ATTACK_NAMES:
        steve_this = steveify_generic(steve_long, constants.ATTACK_COUNT, constants.ATTACK_NAME_SIZE)
        loc = offset + constants.ATTACK_NAME_LOC
        count = constants.ATTACK_COUNT
        size = constants.ATTACK_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_ESPER_ATTACK_NAMES:
        steve_this = steveify_generic(steve_long, constants.ESPER_COUNT, constants.ESPER_ATTACK_NAME_SIZE)
        loc = offset + constants.ESPER_ATTACK_NAME_LOC
        count = constants.ESPER_COUNT
        size = constants.ESPER_ATTACK_NAME_SIZE
        modified_data[loc: loc + count * size] = steve_this

    if STEVEIFY_DANCE_NAMES:
        steve_this = steveify_generic(steve_long, constants.DANCE_COUNT, constants.DANCE_NAME_SIZE)
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
    wcrom.write(smc_path, overwrite=True)

def steveify_characters(steve):
    new_data = b''
    for _ in range(constants.CHARACTER_COUNT):
        new_data += steve
    return new_data

def steveify_generic(steve_bytes, count, size):
    new_data = bytearray()
    for _ in range(count):
        name = bytearray(steve_bytes)
        if len(name) > size:
            name = name[:size]
        while len(name) < size:
            name.append(constants.CHAR_TO_CODE[''])
        new_data.extend(name)
    return bytes(new_data)

def steveify_item_names(steve_bytes):
    new_data = bytearray()
    for i in range(constants.ITEM_COUNT):
        item_type = constants.ITEMS[i][0]
        
        name = bytearray()
        name.append(constants.CHAR_TO_CODE.get(item_type, constants.CHAR_TO_CODE[' ']))
        name.extend(steve_bytes)

        if len(name) > constants.ITEM_NAME_SIZE:
            name = name[:constants.ITEM_NAME_SIZE]
        
        while len(name) < constants.ITEM_NAME_SIZE:
            name.append(constants.CHAR_TO_CODE[''])
            
        new_data.extend(name)
    return bytes(new_data)


def steveify_magic_names(steve_bytes):
    new_data = bytearray()
    for i in range(constants.MAGIC_COUNT):
        original_spell = constants.SPELLS[i]
        magic_type = original_spell[0]

        name = bytearray()
        name.append(constants.CHAR_TO_CODE.get(magic_type, constants.CHAR_TO_CODE[' ']))
        
        # Handle spells with levels like "Fire 2"
        spell_level_char = None
        if ' 2' in original_spell or ' 3' in original_spell:
            clean_spell = original_spell.replace('_', '')
            spell_level_char = clean_spell[-1]

        if spell_level_char:
            name.extend(steve_bytes[:constants.MAGIC_NAME_SIZE - 2])
            name.append(constants.CHAR_TO_CODE.get(spell_level_char, constants.CHAR_TO_CODE[' ']))
        else:
            name.extend(steve_bytes)

        if len(name) > constants.MAGIC_NAME_SIZE:
            name = name[:constants.MAGIC_NAME_SIZE]
            
        while len(name) < constants.MAGIC_NAME_SIZE:
            name.append(constants.CHAR_TO_CODE[''])
        
        new_data.extend(name)
    return bytes(new_data)