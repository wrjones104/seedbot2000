import re
import flags

cr_flags = flags.cr_flags()
cr = 0

# SPOILER LOG
if '-sl' not in cr_flags:
    cr = cr + 8

# KEFKA'S TOWER CHARACTER REQUIREMENT
a = int(cr_flags.split('-ktcr ', 1)[1].split(' ', 1)[0])
b = int(cr_flags.split('-ktcr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
cr = cr + ((((a + b)/2)-3)/11)

# KEFKA'S TOWER ESPER REQUIREMENT
a = int(cr_flags.split('-kter ', 1)[1].split(' ', 1)[0])
b = int(cr_flags.split('-kter ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
cr = cr + (((a + b)/2)/27)

# KEFKA'S TOWER DRAGON REQUIREMENT
a = int(cr_flags.split('-ktdr ', 1)[1].split(' ', 1)[0])
b = int(cr_flags.split('-ktdr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
cr = cr + (((a + b)/2)/8)

# STATUE SKIP ---- ASK DOCTORDT ABOUT THIS ONE
if '-stno' in cr_flags:
    cr = cr + 3

# SKIP CHARACTER REQUIREMENT
if '-stno' not in cr_flags:
    a = int(cr_flags.split('-stcr ', 1)[1].split(' ', 1)[0])
    b = int(cr_flags.split('-stcr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
    cr = cr + ((((a + b)/2)-3)/11)

# SKIP ESPER REQUIREMENT
if '-stno' not in cr_flags:
    a = int(cr_flags.split('-ster ', 1)[1].split(' ', 1)[0])
    b = int(cr_flags.split('-ster ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
    cr = cr + (((a + b)/2)/27)

# SKIP DRAGON REQUIREMENT
if '-stno' not in cr_flags:
    a = int(cr_flags.split('-stdr ', 1)[1].split(' ', 1)[0])
    b = int(cr_flags.split('-stdr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
    cr = cr + (((a + b)/2)/8)

# STARTING CHARACTERS
if '-sc2' not in cr_flags:
    cr = cr + 1
if '-sc3' not in cr_flags:
    cr = cr + 1
if '-sc4' not in cr_flags:
    cr = cr + 1

# START AVERAGE LEVEL
if '-sal' not in cr_flags:
    cr = cr + 4

# START NAKED
if '-sn' in cr_flags:
    cr = cr + 2

# EQUIPPABLE UMARO
if '-eu' not in cr_flags:
    cr = cr + 1

# CHARACTER STATS
a = int(cr_flags.split('-csrp ', 1)[1].split(' ', 1)[0])
b = int(cr_flags.split('-csrp ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
cr = cr + ((1 - (a + b)/2)/200)

# SWORDTECH EVERYONE LEARNS
if '-sel' not in cr_flags:
    cr = cr + 1

# BUM RUSH LAST
if '-brl' not in cr_flags:
    cr = cr + 1

# BLITZ EVERYONE LEARNS
if '-bel' not in cr_flags:
    cr = cr + 1

# STARTING LORES
if 'slr' in cr_flags:
    a = int(cr_flags.split('-slr ', 1)[1].split(' ', 1)[0])
    b = int(cr_flags.split('-slr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
    cr = cr + ((1 - (a + b)/2)/24)
else:
    cr = cr + ((1 - (3 + 3)/2)/24)

# LORE MP
if '-lmps' in cr_flags:
    cr = cr + 0.175
elif 'lmprv' in cr_flags:
    a = int(cr_flags.split('-lmprv ', 1)[1].split(' ', 1)[0])
    b = int(cr_flags.split('-lmprv ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
    cr = cr + (((a + b)/2)/99)
elif 'lmprp' in cr_flags:
    a = int(cr_flags.split('-lmprp ', 1)[1].split(' ', 1)[0])
    b = int(cr_flags.split('-lmprp ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
    cr = cr + (((a + b)/2)/200)
else:
    cr = cr + 0.35

# LORE EVERYONE LEARNS
if '-lel' not in cr_flags:
    cr = cr + 1

# STARTING RAGES
if '-srr' in cr_flags:
    a = int(cr_flags.split('-srr ', 1)[1].split(' ', 1)[0])
    b = int(cr_flags.split('-srr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
    cr = cr + ((1 - (a + b)/2)/255)
else:
    cr = cr + (1 - (9/255))


cr_flags_r = ' '.join([cr_flags, "--Rating:", str(cr)])

print("Flags: ", cr_flags)
print("Rating: ", cr)
