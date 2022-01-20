from random import randrange
from struct import pack

from .common import constants
from .common.ff6_rom import FF6_ROM


def randomize_items():
    new_drops = b''

    for j in range(constants.MONSTER_COUNT):
        if j == (282, 298, 366, 367, 368, 370, 371, 372, 375, 376, 378, 379, 380, 382, 383):
            continue
        for i in range(constants.MONSTER_DROP_SIZE):
            item = randrange(len(constants.ITEMS.keys()))
            new_drops += pack('B', item)
    return new_drops


# def all_pally():
#     new_drops = b''
#
#     for j in range(constants.MONSTER_COUNT):
#         if j == (282, 298, 366, 367, 368, 370, 371, 372, 375, 376, 378, 379, 380, 382, 383):
#             continue
#         for i in range(constants.MONSTER_DROP_SIZE):
#             item = 0x67
#             new_drops += pack('B', item)
#     return new_drops
#
#
# def all_top_tier():
#     new_drops = b''
#     toptiers = (0x09, 0x1A, 0x1B, 0x1C, 0x23, 0x52, 0x67, 0x60, 0x61, 0x62, 0x78, 0x80, 0x9C, 0xA1, 0xA2, 0xD3, 0xE4)
#
#     for j in range(constants.MONSTER_COUNT):
#         if j == (282, 298, 366, 367, 368, 370, 371, 372, 375, 376, 378, 379, 380, 382, 383):
#             continue
#         for i in range(constants.MONSTER_DROP_SIZE):
#             item = random.choice(toptiers)
#             new_drops += pack('B', item)
#     return new_drops

def run_item_rando():
    # Read in a WC ROM
    # input_file_name = input('File name? ')
    # file_no_ext = input_file_name.replace(".smc","")
    input_file_path = '../worldscollide/seedbot.smc'
    output_file_path = '../worldscollide/seedbot.smc'
    wcrom = FF6_ROM(input_file_path)
    new_drops = randomize_items()

    # Paladin shields
    # output_file_path = './roms/' + file_no_ext + "oops_all_pally_shields.smc"
    # new_drops = all_pally()

    # Top Tier Items
    # output_file_path = './roms/' + file_no_ext + "top_tier_items.smc"
    # new_drops = all_top_tier()

    modified_data = bytearray(wcrom.data)
    offset = (wcrom.has_header * constants.HEADER_SIZE)
    drop_loc = constants.MONSTER_DROP_LOC + offset
    modified_data[drop_loc: drop_loc + constants.MONSTER_COUNT * constants.MONSTER_DROP_SIZE] = randomize_items()
    wcrom.data = modified_data
    wcrom.write(output_file_path, overwrite=True)

    wcrom = FF6_ROM(input_file_path)
    rando_rom = FF6_ROM(output_file_path)
    if rando_rom.data != wcrom.data:
        print("Randomized steal and item data. Output file is %s" % output_file_path)
    else:
        print("Item data wasn't randomized")
