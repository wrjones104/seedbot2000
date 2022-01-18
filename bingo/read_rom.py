from common import constants
from common.ff6_rom import FF6_ROM
from common.functions import text_to_bytes, format_hex

# Read in a WC ROM
input_file_path = './roms/wc.smc'
# input_file_path = './roms/FinalFantasy3e.smc'
# input_file_path = './output/steve.smc'
output_file_path = "./output/randomized_items.smc"

wcrom = FF6_ROM(input_file_path)
data = wcrom.data
loc = constants.ITEM_NAME_LOC
sz = constants.ITEM_NAME_SIZE
count = constants.ITEM_COUNT

i = wcrom.has_header * constants.HEADER_SIZE + loc

if False:
    counter = 0
    while i < wcrom.has_header * constants.HEADER_SIZE + loc + count * sz:
        n = data[i:i + sz]
        name = ''
        # print(n)
        for j in n:
            name += constants.CODE_TO_CHAR[j]

        print("%s: \"%s\", " % (hex(counter), name))
        i += sz
        counter += 1

if False:
    m = 0xff1e4
    loc = 0xFE1E0
    counter = loc
    output = ""
    while counter < 0xFF44F:
        try:
            txt = constants.CODE_TO_CHAR[data[counter]]
        except:
            txt = ('&')
        output += txt
        if output[-2:] == "&&":
            print(output)
            output = ""

        counter += 1

txt = "crazy"
bt = text_to_bytes(txt)
loc = data.find(bt)
trimmed = 0
while loc != -1:
    print(hex(loc + trimmed))
    data = data[loc + 1:]
    trimmed += loc + 1
    loc = data.find(bt)

counter = 0

data = wcrom.data
m = 0xff1e4
loc = 0xD0200
# loc = 0xD166D
counter = loc
output = ""
while counter < 0xEF2FF:
    # while counter < 0xD16A3:
    txt = data[counter]
    if txt in constants.DTE_TO_TEXT:

        output += constants.DTE_TO_TEXT[txt]
    else:
        output += "(" + format_hex(txt, 1) + ")"
    counter += 1
print(output.replace("\n", "\\n").replace("<EOC>", "<EOC>\n"))
