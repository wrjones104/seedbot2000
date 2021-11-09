import flags
import math

cr_flags = flags.cr_flags()
cr = 0

# SPOILER LOG
if '-sl' not in cr_flags:
    cr_sl = 8
    cr = cr + cr_sl
else:
    cr_sl = 0

# KEFKA'S TOWER CHARACTER REQUIREMENT
a = int(cr_flags.split('-ktcr ', 1)[1].split(' ', 1)[0])
b = int(cr_flags.split('-ktcr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
cr_ktc = ((((a + b)/2)-3)/11)
cr = cr + cr_ktc

# KEFKA'S TOWER ESPER REQUIREMENT
a = int(cr_flags.split('-kter ', 1)[1].split(' ', 1)[0])
b = int(cr_flags.split('-kter ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
cr_kte = (((a + b)/2)/27)
cr = cr + cr_kte

# KEFKA'S TOWER DRAGON REQUIREMENT
a = int(cr_flags.split('-ktdr ', 1)[1].split(' ', 1)[0])
b = int(cr_flags.split('-ktdr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
cr_ktd = (((a + b)/2)/8)
cr = cr + cr_ktd

# STATUE SKIP ---- ASK DOCTORDT ABOUT THIS ONE
if '-stno' in cr_flags:
    cr_stno = 3
    cr = cr + cr_stno
else:
    cr_stno = 0

# SKIP CHARACTER REQUIREMENT
if '-stno' not in cr_flags:
    a = int(cr_flags.split('-stcr ', 1)[1].split(' ', 1)[0])
    b = int(cr_flags.split('-stcr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
    cr_stc = ((((a + b)/2)-3)/11)
    cr = cr + cr_stc
else:
    cr_stc = 0

# SKIP ESPER REQUIREMENT
if '-stno' not in cr_flags:
    a = int(cr_flags.split('-ster ', 1)[1].split(' ', 1)[0])
    b = int(cr_flags.split('-ster ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
    cr_ste = (((a + b)/2)/27)
    cr = cr + cr_ste
else:
    cr_ste = 0

# SKIP DRAGON REQUIREMENT
if '-stno' not in cr_flags:
    a = int(cr_flags.split('-stdr ', 1)[1].split(' ', 1)[0])
    b = int(cr_flags.split('-stdr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
    cr_std =(((a + b)/2)/8)
    cr = cr + cr_std
else:
    cr_std = 0

# STARTING CHARACTERS
if '-sc2' not in cr_flags:
    cr_sc2 = 1
    cr = cr + cr_sc2
else:
    cr_sc2 = 0

if '-sc3' not in cr_flags:
    cr_sc3 = 1
    cr = cr + cr_sc3
else:
    cr_sc3 = 0

if '-sc4' not in cr_flags:
    cr_sc4 = 1
    cr = cr + cr_sc4
else:
    cr_sc4 = 0

# START AVERAGE LEVEL
if '-sal' not in cr_flags:
    cr_sal = 4
    cr = cr + cr_sal
else:
    cr_sal = 0

# START NAKED
if '-sn' in cr_flags:
    cr_sn = 2
    cr = cr + cr_sn
else:
    cr_sn = 0

# EQUIPPABLE UMARO
if '-eu' not in cr_flags:
    cr_eu = 1
    cr = cr + cr_eu
else:
    cr_eu = 0

# CHARACTER STATS
a = int(cr_flags.split('-csrp ', 1)[1].split(' ', 1)[0])
b = int(cr_flags.split('-csrp ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
cr_csrp = 2 - (((a + b)/2)/200)*2
cr = cr + cr_csrp

# SWORDTECH EVERYONE LEARNS
if '-sel' not in cr_flags:
    cr_sel = 1
    cr = cr + cr_sel
else:
    cr_sel = 0

# BUM RUSH LAST
if '-brl' not in cr_flags:
    cr_brl = 0
    cr = cr + cr_brl
else:
    cr_brl = 2

# BLITZ EVERYONE LEARNS
if '-bel' not in cr_flags:
    cr_bel = 1
    cr = cr + cr_bel
else:
    cr_bel = 0

# STARTING LORES
if 'slr' in cr_flags:
    a = int(cr_flags.split('-slr ', 1)[1].split(' ', 1)[0])
    b = int(cr_flags.split('-slr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
    cr_slr = 2 - (((a + b)/2)/24)*2
    cr = cr + cr_slr
else:
    cr_slr = 2 - (((3 + 3)/2)/24)*2
    cr = cr + cr_slr

# LORE MP
if '-lmps' in cr_flags:
    cr_loremp = 0.175 * 2
    cr = cr + cr_loremp
elif 'lmprv' in cr_flags:
    a = int(cr_flags.split('-lmprv ', 1)[1].split(' ', 1)[0])
    b = int(cr_flags.split('-lmprv ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
    cr_loremp = 2 - (((a + b)/2)/99)*2
    cr = cr + cr_loremp
elif 'lmprp' in cr_flags:
    a = int(cr_flags.split('-lmprp ', 1)[1].split(' ', 1)[0])
    b = int(cr_flags.split('-lmprp ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
    cr_loremp = 2 - (((a + b)/2)/200)*2
    cr = cr + cr_loremp
else:
    cr_loremp = 0.35 * 2
    cr = cr + cr_loremp

# LORE EVERYONE LEARNS
if '-lel' not in cr_flags:
    cr_lel = 1
    cr = cr + cr_lel
else:
    cr_lel = 0

# STARTING RAGES
if '-srr' in cr_flags:
    a = int(cr_flags.split('-srr ', 1)[1].split(' ', 1)[0])
    b = int(cr_flags.split('-srr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
    cr_srr = 2 - ((1 - (a + b)/2)/255)*2
    cr = cr + cr_srr
else:
    cr_srr = (1 - (9/255))*2
    cr = cr + cr_srr

# NO CHARM
if '-rnc' in cr_flags:
    cr_rnc = 2
    cr = cr + cr_rnc
else:
    cr_rnc = 0

# STARTING DANCE
if '-sdr' in cr_flags:
    a = int(cr_flags.split('-sdr ', 1)[1].split(' ', 1)[0])
    b = int(cr_flags.split('-sdr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
    cr_sdr = 1 - (((a + b) / 2) / 8)
    cr = cr + cr_sdr
else:
    cr_sdr = 0

# DANCE ABILITY SHUFFLE
if '-das' not in cr_flags:
    cr_das = 1
    cr = cr + cr_das
else:
    cr_das = 0

# DISPLAY DANCE ABILITY NAMES
if '-dda' not in cr_flags:
    cr_dda = 2
    cr = cr + cr_dda
else:
    cr_dda = 0

# DANCE NO STUMBLE
if '-dns' not in cr_flags:
    cr_dns = 2
    cr = cr + cr_dns
else:
    cr_dns = 0

# DANCE EVERYONE LEARNS
if '-del' not in cr_flags:
    cr_del = 1
    cr = cr + cr_del
else:
    cr_del = 0

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
    cr_com = ((skills[com1] + skills[com2] + skills[com3] + skills[com4] + skills[com5] + skills[com6] + skills[com7] \
         + skills[com8] + skills[com9] + skills[com10] + skills[com11] + skills[com12] + skills[com13]) * 4)
    cr = cr + cr_com
else:
    cr_com = (13.22 * 4)
    cr = cr + cr_com

# SHUFFLE COMMANDS
# Not relevant for current flag generation

# RANDOM EXCLUDED SKILLS ----- I have to figure out how to work in Doc's calculation for excluded skills above
# if '-rec1' in cr_flags:
#     recvar1 = 2 - (skills[cr_flags.split('-rec1 ', 1)[1].split(' ', 1)[0]])
# else:
#     recvar1 = 0
#
# if '-rec2' in cr_flags:
#     recvar2 = 2 - (skills[cr_flags.split('-rec2 ', 1)[1].split(' ', 1)[0]])
# else:
#     recvar2 = 0
#
# if '-rec3' in cr_flags:
#     recvar3 = 2 - (skills[cr_flags.split('-rec3 ', 1)[1].split(' ', 1)[0]])
# else:
#     recvar3 = 0
#
# if '-rec4' in cr_flags:
#     recvar4 = 2 - (skills[cr_flags.split('-rec4 ', 1)[1].split(' ', 1)[0]])
# else:
#     recvar4 = 0
#
# if '-rec5' in cr_flags:
#     recvar5 = 2 - (skills[cr_flags.split('-rec5 ', 1)[1].split(' ', 1)[0]])
# else:
#     recvar5 = 0
#
# cr_rec = (recvar1 + recvar2 + recvar3 + recvar4 + recvar5) * 2
# cr = cr + cr_rec

# EXP MODIFIER ----- Not sure how to translate this calculation exactly - it's close but not 100%
if '-xpm 0' in cr_flags:
    cr_xpm = 80
    cr = cr + cr_xpm
elif '-xpm' not in cr_flags:
    cr_xpm = 8
    cr = cr + cr_xpm
else:
    cr_xpm = ((1 - math.sqrt(math.log(int(cr_flags.split('-xpm ', 1)[1].split(' ', 1)[0]))/math.log(255)))*4)
    cr = cr + cr_xpm

# MP MODIFIER
if '-mpm' not in cr_flags:
    cr_mpm = 4
    cr = cr + cr_mpm
else:
    cr_mpm = ((1 - math.sqrt(math.log(int(cr_flags.split('-mpm ', 1)[1].split(' ', 1)[0]))/math.log(255)))*4)
    cr = cr + cr_mpm

# GP MODIFIER
if '-gpm' not in cr_flags:
    cr_gpm = 4
    cr = cr + cr_gpm
else:
    cr_gpm = ((1 - math.sqrt(math.log(int(cr_flags.split('-gpm ', 1)[1].split(' ', 1)[0]))/math.log(255)))*4)
    cr = cr + cr_gpm

# NO PARTY EXP SPLIT
if '-nxppd' not in cr_flags:
    cr_nxppd = 4
    cr = cr + cr_nxppd
else:
    cr_nxppd = 0

# LEVEL SCALING
if '-lsa' in cr_flags:
    cr_ls = (.9 * (float(cr_flags.split('-lsa ', 1)[1].split(' ', 1)[0]))/5)*8
    cr = cr + cr_ls
elif 'lsh' in cr_flags:
    cr_ls = (1 * (float(cr_flags.split('-lsh ', 1)[1].split(' ', 1)[0])) / 5)*8
    cr = cr + cr_ls
elif 'lsp' in cr_flags:
    cr_ls = (.8 * (float(cr_flags.split('-lsp ', 1)[1].split(' ', 1)[0])) / 5)*8
    cr = cr + cr_ls
elif 'lst' in cr_flags:
    cr_ls = (.7 * (1 - (float(cr_flags.split('-lst ', 1)[1].split(' ', 1)[0])) / 5))*8
    cr = cr + cr_ls
else:
    cr_ls = 0.2 * 8
    cr = cr + cr_ls

# HP/MP SCALING
if '-hma' in cr_flags:
    cr_hs = (.9 * (float(cr_flags.split('-hma ', 1)[1].split(' ', 1)[0]))/5)*4
    cr = cr + cr_hs
elif 'hmh' in cr_flags:
    cr_hs = (1 * (float(cr_flags.split('-hmh ', 1)[1].split(' ', 1)[0])) / 5)*4
    cr = cr + cr_hs
elif 'hmp' in cr_flags:
    cr_hs = (.8 * (float(cr_flags.split('-hmp ', 1)[1].split(' ', 1)[0])) / 5)*4
    cr = cr + cr_hs
elif 'hmt' in cr_flags:
    cr_hs = (.7 * (1 - (float(cr_flags.split('-hmt ', 1)[1].split(' ', 1)[0])) / 5))*4
    cr = cr + cr_hs
else:
    cr_hs = 0.2 * 4
    cr = cr + cr_hs

# EXP/GP SCALING
if '-xga' in cr_flags:
    cr_xgp = (.9 * (1 - (float(cr_flags.split('-xga ', 1)[1].split(' ', 1)[0]))/5))*4
    cr = cr + cr_xgp
elif 'xgh' in cr_flags:
    cr_xgp = (.8 * (1 - (float(cr_flags.split('-xgh ', 1)[1].split(' ', 1)[0])) / 5))*4
    cr = cr + cr_xgp
elif 'xgp' in cr_flags:
    cr_xgp = (1 - (.8 * (float(cr_flags.split('-xgp ', 1)[1].split(' ', 1)[0])) / 5))*4
    cr = cr + cr_xgp
elif 'xgt' in cr_flags:
    cr_xgp = (.7 * (float(cr_flags.split('-xgt ', 1)[1].split(' ', 1)[0])) / 5)*4
    cr = cr + cr_xgp
else:
    cr_xgp = 0.2 * 4
    cr = cr + cr_xgp
    
# ABILITY SCALING
if '-ase' in cr_flags:
    cr_as = (.6 * (1 - (float(cr_flags.split('-ase ', 1)[1].split(' ', 1)[0]))/5))*4
    cr = cr + cr_as
elif '-asr' in cr_flags:
    cr_as = (1 * (1 - (float(cr_flags.split('-asr ', 1)[1].split(' ', 1)[0])) / 5))*4
    cr = cr + cr_as
else:
    cr_as = 0.8 * 4
    cr = cr + cr_as

# MAX SCALE LEVEL ----- Another one that's close but not close enough - must be the logs
if '-msl' in cr_flags:
    cr_msl = (((math.log(float(cr_flags.split('-msl ', 1)[1].split(' ', 1)[0])))/math.log(99-2))**6)*4
    cr = cr + cr_msl
else:
    cr_msl = 0
    cr = cr + cr_msl

# EXTRA ENEMY LEVELS ----- Another one that's close but not close enough - must be the logs
if '-eel' in cr_flags:
    cr_eel = (((math.log(float(cr_flags.split('-eel ', 1)[1].split(' ', 1)[0])))/math.log(99+1))**2)*4
    cr = cr + cr_eel
else:
    cr_eel = 0
    cr = cr + cr_eel

# SCALE FINAL BOSS
if '-sfb' in cr_flags:
    cr_sfb = (min([cr_msl/4, cr_eel/4]))*2
    cr = cr + cr_sfb
else:
    cr_sfb = (min(.4 + cr_eel/4, 1))*2
    cr = cr + cr_sfb

# SCALE EIGHT DRAGONS
if '-sed' in cr_flags:
    cr_sed = (min([cr_msl/4, cr_eel/4]))*2
    cr = cr + cr_sed
else:
    cr_sed = (min(.4 + cr_eel/4, 1))*2
    cr = cr + cr_sed

# BOSS BATTLES
if '-bbs' in cr_flags:
    cr_bb = 0.5 * 2
    cr = cr + cr_bb
elif '-bbr' in cr_flags:
    cr_bb = 1 * 2
    cr = cr + cr_bb
else:
    cr_bb = 0
    cr = cr + cr_bb

# MIX BOSSES AND DRAGONS
if '-bmbd' in cr_flags:
    cr_bmbd = 1 * 2
    cr = cr + cr_bmbd
else:
    cr_bmbd = 0
    cr = cr + cr_bmbd
    
# SHUFFLE PHUNBABA3
if '-srp3' in cr_flags:
    cr_srp3 = 1 * 2
    cr = cr + cr_srp3
else:
    cr_srp3 = 0
    cr = cr + cr_srp3

# NORMALIZE & DISTORT
if '-bnds' in cr_flags:
    cr_bnds = 1 * 4
    cr = cr + cr_bnds
else:
    cr_bnds = 0
    cr = cr + cr_bnds
    
# BOSS EXPERIENCE
if '-be ' not in cr_flags:
    cr_be = 1 * 4
    cr = cr + cr_be
else:
    cr_be = 0
    cr = cr + cr_be

# NO UNDEAD BOSSES
if '-bnu' in cr_flags:
    cr_bnu = 1
    cr = cr + cr_bnu
else:
    cr_bnu = 0
    cr = cr + cr_bnu

# RANDOM ENCOUNTERS
if '-res ' in cr_flags:
    cr_renc = .2 * 2
    cr = cr + cr_renc
elif '-rer ' in cr_flags:
    cr_renc = 2 * (.2 + (1 - .2)*(float(cr_flags.split('-rer ', 1)[1].split(' ', 1)[0]))/100)
    cr = cr + cr_renc
else:
    cr_renc = 0
    cr = cr + cr_renc

# FIXED ENCOUNTERS
if '-fer ' in cr_flags:
    cr_fenc = (.25 + ((float(cr_flags.split('-fer ', 1)[1].split(' ', 1)[0]))/100)*(1 - .25)) * 2
    cr = cr + cr_fenc
else:
    cr_fenc = 0
    cr = cr + cr_fenc

# ESCAPABLE BATTLES
if '-escr' in cr_flags and float(cr_flags.split('-escr ', 1)[1].split(' ', 1)[0]) > 0:
    cr_escr = (1-float(cr_flags.split('-escr ', 1)[1].split(' ', 1)[0])/100)*2
    cr = cr + cr_escr
else:
    cr_escr = 0
    cr = cr + cr_escr
    
# DOOMGAZE NO ESCAPE
if '-dgne' not in cr_flags:
    cr_dgne = 2
    cr = cr + cr_dgne
else:
    cr_dgne = 0
    cr = cr + cr_dgne
    
# WREXSOUL NO ZINGER
if '-wnz' not in cr_flags:
    cr_wnz = 2
    cr = cr + cr_wnz
else:
    cr_wnz = 0
    cr = cr + cr_wnz

# MAGIMASTER NO ULTIMA
if '-mmnu' not in cr_flags:
    cr_mmnu = 4
    cr = cr + cr_mmnu
else:
    cr_mmnu = 0
    cr = cr + cr_mmnu
    
# CHADARNOOK MORE LIKE BADARNOOK
if '-cmd' not in cr_flags:
    cr_cmd = 2
    cr = cr + cr_cmd
else:
    cr_cmd = 0
    cr = cr + cr_cmd

cr_flags_r = ' '.join([cr_flags, "--Rating:", str(cr)])

print("Flags: ", cr_flags)
print("Rating: ", cr)
print("sl:", cr_sl, "ktc:", cr_ktc, "kte:", cr_kte, "ktd:", cr_ktd, "stno:", cr_stno, "stc:", cr_stc)
print("ste:", cr_ste, "std:", cr_std, "sc2:", cr_sc2, "sc3:", cr_sc3, "sc4:", cr_sc4, "sal:", cr_sal)
print("sn:", cr_sn, "eu:", cr_eu, "csrp:", cr_csrp, "sel:", cr_sel, "brl:", cr_brl, "bel:", cr_bel, "slr:", cr_slr)
print("loremp:", cr_loremp, "lel:", cr_lel, "srr:", cr_srr, "rnc:", cr_rnc, "sdr:", cr_sdr, "das:", cr_das)
print("dda:", cr_dda, "dns:", cr_dns, "del:", cr_del, "com:", cr_com, "xpm:", cr_xpm, "mpm:", cr_mpm, "gpm:", cr_gpm)
print("nxppd:", cr_nxppd, "ls:", cr_ls, "hs:", cr_hs, "xgp:", cr_xgp, "as:", cr_as, "msl:", cr_msl, "eel:", cr_eel)
print("sfb:", cr_sfb, "sed:", cr_sed, "bb:", cr_bb, "bmbd:", cr_bmbd, "srp3:", cr_srp3, "bnds:", cr_bnds, "be:", cr_be)
print("bnu:", cr_bnu, "renc:", cr_renc, "fenc:", cr_fenc, "escr:", cr_escr, "dgne:", cr_dgne, "wnz:", cr_wnz)
print("mmnu:", cr_mmnu, "cmd:", cr_cmd)


# print(cr_flags.split('-xpm ', 1)[1].split(' ', 1)[0])
# print(1 - (math.sqrt(math.log(int(cr_flags.split('-xpm ', 1)[1].split(' ', 1)[0])))/math.log(255)))
