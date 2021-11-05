import flags
import math

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

# NO CHARM
if '-rnc' in cr_flags:
    cr = cr + 2

# STARTING DANCE
if '-sdr' in cr_flags:
    a = int(cr_flags.split('-sdr ', 1)[1].split(' ', 1)[0])
    b = int(cr_flags.split('-sdr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
    cr = cr + ((1 - (a + b) / 2) / 8)

# DANCE ABILITY SHUFFLE
if '-das' not in cr_flags:
    cr = cr + 1

# DISPLAY DANCE ABILITY NAMES
if '-dda' not in cr_flags:
    cr = cr + 2

# DANCE NO STUMBLE
if '-dns' not in cr_flags:
    cr = cr + 2

# COMMANDS ----- Talk to Doc about these the CR mod for these
skills = {
    '00': .9,  # FIGHT
    '99': .485,  # RANDOM
    '98': .485,  # RANDOM UNIQUE
    '97': 1,  # NONE
    '10': .4,  # BLITZ
    '06': .7,  # CAPTURE
    '14': .8,  # CONTROL
    '19': .6,  # DANCE
    '24': .5,  # GP RAIN
    '26': .5,  # HEALTH
    '22': .4,  # JUMP
    '12': .5,  # LORE
    '03': .4,  # MORPH
    '28': .1,  # POSSESS
    '16': .4,  # RAGE
    '11': .6,  # RUNIC
    '27': .1,  # SHOCK
    '13': .9,  # SKETCH
    '15': .5,  # SLOT
    '05': .9,  # STEAL
    '07': .4,  # SWDTECH
    '08': .2,  # THROW
    '09': .3,  # TOOLS
    '23': .5  # X-MAGIC
}

if '-com' in cr_flags:
    com1 = cr_flags.split('-com ', 1)[1].split(' ', 1)[0][:2]
    com2 = cr_flags.split('-com ', 1)[1].split(' ', 1)[0][2:4]
    com3 = cr_flags.split('-com ', 1)[1].split(' ', 1)[0][4:6]
    com4 = cr_flags.split('-com ', 1)[1].split(' ', 1)[0][6:8]
    com5 = cr_flags.split('-com ', 1)[1].split(' ', 1)[0][8:10]
    com6 = cr_flags.split('-com ', 1)[1].split(' ', 1)[0][10:12]
    com7 = cr_flags.split('-com ', 1)[1].split(' ', 1)[0][12:14]
    com8 = cr_flags.split('-com ', 1)[1].split(' ', 1)[0][14:16]
    com9 = cr_flags.split('-com ', 1)[1].split(' ', 1)[0][16:18]
    com10 = cr_flags.split('-com ', 1)[1].split(' ', 1)[0][18:20]
    com11 = cr_flags.split('-com ', 1)[1].split(' ', 1)[0][20:22]
    com12 = cr_flags.split('-com ', 1)[1].split(' ', 1)[0][22:24]
    com13 = cr_flags.split('-com ', 1)[1].split(' ', 1)[0][24:26]
    cr = cr + ((skills[com1] + skills[com2] + skills[com3] + skills[com4] + skills[com5] + skills[com6] + skills[com7] \
         + skills[com8] + skills[com9] + skills[com10] + skills[com11] + skills[com12] + skills[com13]) * 4)
else:
    cr = cr + (13.22 * 4)

# SHUFFLE COMMANDS
# Not relevant for current flag generation

# RANDOM EXCLUDED SKILLS ----- I think I need to fix these (excluding crappy skills should make it easier, not harder)
recvar = 0
if '-rec1' in cr_flags:
    recvar = recvar + 1 - (skills[cr_flags.split('-rec1 ', 1)[1].split(' ', 1)[0]])

if '-rec2' in cr_flags:
    recvar = recvar + 1 - (skills[cr_flags.split('-rec2 ', 1)[1].split(' ', 1)[0]])

if '-rec3' in cr_flags:
    recvar = recvar + 1 - (skills[cr_flags.split('-rec3 ', 1)[1].split(' ', 1)[0]])

if '-rec4' in cr_flags:
    recvar = recvar + 1 - (skills[cr_flags.split('-rec4 ', 1)[1].split(' ', 1)[0]])

if '-rec5' in cr_flags:
    recvar = recvar + 1 - (skills[cr_flags.split('-rec5 ', 1)[1].split(' ', 1)[0]])

cr = cr + (recvar * 2)

# EXP MODIFIER ----- This is freakin' dumpster fire right now
if '-xpm 0' in cr_flags:
    cr = cr + 80
elif '-xpm' not in cr_flags:
    cr = cr + 8
else:
    cr = cr + (1 - (math.log(int(cr_flags.split('-xpm ', 1)[1].split(' ', 1)[0]))/math.log(255)))




cr_flags_r = ' '.join([cr_flags, "--Rating:", str(cr)])

print("Flags: ", cr_flags)
print("Rating: ", cr)
print(cr_flags.split('-xpm ', 1)[1].split(' ', 1)[0])
print(1 - (math.sqrt(math.log(int(cr_flags.split('-xpm ', 1)[1].split(' ', 1)[0])))/math.log(255)))
