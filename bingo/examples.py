from common import constants
from common.ff6_rom import FF6_ROM

# Read in a vanilla FF3 US ROM and print out its attributes
ff3rom = FF6_ROM('./roms/FinalFantasy3e.smc')
print(ff3rom)

# Read in a WC ROM and print out its attributes
wcrom = FF6_ROM('./roms/wc.smc')
print(wcrom)

# Read in a vanilla FF6J ROM and print out its attributes
ff6jrom = FF6_ROM('./roms/FinalFantasy6j.smc')
print(ff6jrom)

# Modify the vanilla FF3 ROM and save it out to new file. Note that you can't directly
# insert/overwrite bytes into ff3rom.data, you need to copy it out to a bytearray first.

## This will edit the ROM title internally. It's normally FINAL FANTASY 3
output_file_path = "./output/output.smc"
modified_data = bytearray(ff3rom.data)
offset = (ff3rom.has_header * constants.HEADER_SIZE)
title_loc = constants.HiROM_HEADER_TITLE_OFFSET + offset

## The actual title length limit is 21 characters. We'll bring things if the title isn't
## exactly 21 characters long
new_title = b'Presenter is awesome!'
if len(new_title) > constants.HiROM_HEADER_TITLE_SIZE:
    print("Title can't be longer than %s bytes" % constants.HiROM_HEADER_TITLE_SIZE)
    exit()
while len(new_title) < constants.HiROM_HEADER_TITLE_SIZE:
    new_title += b' '

modified_data[title_loc: title_loc + constants.HiROM_HEADER_TITLE_SIZE] = new_title

## We are saving the data back in to ff3rom. Note that this does not overwrite the data in the
## original FF3 file, just in the object in memory. Only the .write command will write data to disk
ff3rom.data = modified_data

## Now we write our ROM, including the modified data, out to output_file_path
ff3rom.write(output_file_path, overwrite=True)

# Read in the modified rom and print out its attributes. Notice that the program doesn't think this
# is FF6 anymore because of the name change
modified_rom = FF6_ROM(output_file_path)
print(modified_rom)
