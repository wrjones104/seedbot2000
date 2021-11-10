import flags
import math

def get_cr():
    cr_flags = flags.cr_flags()
    cr = 0
    # print("Flags: ", cr_flags)

    # GAME MODE
    if '-ow ' in cr_flags:
        cr_gm = 0
    if '-cg ' in cr_flags:
        cr_gm = 2
    cr = cr = cr_gm

    # SPOILER LOG
    if '-sl' not in cr_flags:
        cr_sl = 8
    else:
        cr_sl = 0
    cr = cr + cr_sl

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
    else:
        cr_stno = 0
    cr = cr + cr_stno

    # SKIP CHARACTER REQUIREMENT
    if '-stno' not in cr_flags:
        a = int(cr_flags.split('-stcr ', 1)[1].split(' ', 1)[0])
        b = int(cr_flags.split('-stcr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        cr_stc = ((((a + b)/2)-3)/11)
    else:
        cr_stc = 0
    cr = cr + cr_stc

    # SKIP ESPER REQUIREMENT
    if '-stno' not in cr_flags:
        a = int(cr_flags.split('-ster ', 1)[1].split(' ', 1)[0])
        b = int(cr_flags.split('-ster ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        cr_ste = (((a + b)/2)/27)
    else:
        cr_ste = 0
    cr = cr + cr_ste

    # SKIP DRAGON REQUIREMENT
    if '-stno' not in cr_flags:
        a = int(cr_flags.split('-stdr ', 1)[1].split(' ', 1)[0])
        b = int(cr_flags.split('-stdr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        cr_std =(((a + b)/2)/8)
    else:
        cr_std = 0
    cr = cr + cr_std

    # STARTING CHARACTERS
    if '-sc2' not in cr_flags:
        cr_sc2 = 1
    else:
        cr_sc2 = 0
    cr = cr + cr_sc2

    if '-sc3' not in cr_flags:
        cr_sc3 = 1
    else:
        cr_sc3 = 0
    cr = cr + cr_sc3

    if '-sc4' not in cr_flags:
        cr_sc4 = 1
    else:
        cr_sc4 = 0
    cr = cr + cr_sc4

    # START AVERAGE LEVEL
    if '-sal' not in cr_flags:
        cr_sal = 4
    else:
        cr_sal = 0
    cr = cr + cr_sal

    # START NAKED
    if '-sn' in cr_flags:
        cr_sn = 2
    else:
        cr_sn = 0
    cr = cr + cr_sn

    # EQUIPPABLE UMARO
    if '-eu' not in cr_flags:
        cr_eu = 1
    else:
        cr_eu = 0
    cr = cr + cr_eu

    # CHARACTER STATS
    if '-csrp ' in cr_flags:
        a = int(cr_flags.split('-csrp ', 1)[1].split(' ', 1)[0])
        b = int(cr_flags.split('-csrp ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        cr_csrp = 2 - (((a + b)/2)/200)*2
    else:
        cr_csrp = 2 - ((100/200)*2)
    cr = cr + cr_csrp

    # SWORDTECH EVERYONE LEARNS
    if '-sel' not in cr_flags:
        cr_sel = 1
    else:
        cr_sel = 0
    cr = cr + cr_sel

    # BUM RUSH LAST
    if '-brl' not in cr_flags:
        cr_brl = 0
    else:
        cr_brl = 2
    cr = cr + cr_brl

    # BLITZ EVERYONE LEARNS
    if '-bel' not in cr_flags:
        cr_bel = 1
    else:
        cr_bel = 0
    cr = cr + cr_bel

    # STARTING LORES
    if 'slr' in cr_flags:
        a = int(cr_flags.split('-slr ', 1)[1].split(' ', 1)[0])
        b = int(cr_flags.split('-slr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        cr_slr = 2 - (((a + b)/2)/24)*2
    else:
        cr_slr = 2 - (((3 + 3)/2)/24)*2
    cr = cr + cr_slr

    # LORE MP
    if '-lmps' in cr_flags:
        cr_loremp = 0.175 * 2
    elif 'lmprv' in cr_flags:
        a = int(cr_flags.split('-lmprv ', 1)[1].split(' ', 1)[0])
        b = int(cr_flags.split('-lmprv ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        cr_loremp = 2 - (((a + b)/2)/99)*2
    elif 'lmprp' in cr_flags:
        a = int(cr_flags.split('-lmprp ', 1)[1].split(' ', 1)[0])
        b = int(cr_flags.split('-lmprp ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        cr_loremp = 2 - (((a + b)/2)/200)*2
    else:
        cr_loremp = 0.35 * 2
    cr = cr + cr_loremp

    # LORE EVERYONE LEARNS
    if '-lel' not in cr_flags:
        cr_lel = 1
    else:
        cr_lel = 0
    cr = cr + cr_lel

    # STARTING RAGES
    if '-srr' in cr_flags:
        a = int(cr_flags.split('-srr ', 1)[1].split(' ', 1)[0])
        b = int(cr_flags.split('-srr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        cr_srr = 2 - ((1 - (a + b)/2)/255)*2
    else:
        cr_srr = (1 - (9/255))*2
    cr = cr + cr_srr

    # NO CHARM
    if '-rnc' in cr_flags:
        cr_rnc = 2
    else:
        cr_rnc = 0
    cr = cr + cr_rnc

    # STARTING DANCE
    if '-sdr' in cr_flags:
        a = int(cr_flags.split('-sdr ', 1)[1].split(' ', 1)[0])
        b = int(cr_flags.split('-sdr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        cr_sdr = 1 - (((a + b) / 2) / 8)
    else:
        cr_sdr = 0
    cr = cr + cr_sdr

    # DANCE ABILITY SHUFFLE
    if '-das' not in cr_flags:
        cr_das = 1
    else:
        cr_das = 0
    cr = cr + cr_das

    # DISPLAY DANCE ABILITY NAMES
    if '-dda' not in cr_flags:
        cr_dda = 2
    else:
        cr_dda = 0
    cr = cr + cr_dda

    # DANCE NO STUMBLE
    if '-dns' not in cr_flags:
        cr_dns = 2
    else:
        cr_dns = 0
    cr = cr + cr_dns

    # DANCE EVERYONE LEARNS
    if '-del' not in cr_flags:
        cr_del = 1
    else:
        cr_del = 0
    cr = cr + cr_del

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
    elif '-xpm' not in cr_flags:
        cr_xpm = 8
    else:
        cr_xpm = ((1 - math.sqrt(math.log(int(cr_flags.split('-xpm ', 1)[1].split(' ', 1)[0]))/math.log(255)))*4)
    cr = cr + cr_xpm

    # MP MODIFIER
    if '-mpm' not in cr_flags:
        cr_mpm = 4
    else:
        cr_mpm = ((1 - math.sqrt(math.log(int(cr_flags.split('-mpm ', 1)[1].split(' ', 1)[0]))/math.log(255)))*4)
    cr = cr + cr_mpm

    # GP MODIFIER
    if '-gpm' not in cr_flags:
        cr_gpm = 4
    else:
        cr_gpm = ((1 - math.sqrt(math.log(int(cr_flags.split('-gpm ', 1)[1].split(' ', 1)[0]))/math.log(255)))*4)
    cr = cr + cr_gpm

    # NO PARTY EXP SPLIT
    if '-nxppd' not in cr_flags:
        cr_nxppd = 4
    else:
        cr_nxppd = 0
    cr = cr + cr_nxppd

    # LEVEL SCALING
    if '-lsa' in cr_flags:
        cr_ls = (.9 * (float(cr_flags.split('-lsa ', 1)[1].split(' ', 1)[0]))/5)*8
    elif 'lsh' in cr_flags:
        cr_ls = (1 * (float(cr_flags.split('-lsh ', 1)[1].split(' ', 1)[0])) / 5)*8
    elif 'lsp' in cr_flags:
        cr_ls = (.8 * (float(cr_flags.split('-lsp ', 1)[1].split(' ', 1)[0])) / 5)*8
    elif 'lst' in cr_flags:
        cr_ls = (.7 * (1 - (float(cr_flags.split('-lst ', 1)[1].split(' ', 1)[0])) / 5))*8
    else:
        cr_ls = 0.2 * 8
    cr = cr + cr_ls

    # HP/MP SCALING
    if '-hma' in cr_flags:
        cr_hs = (.9 * (float(cr_flags.split('-hma ', 1)[1].split(' ', 1)[0]))/5)*4
    elif 'hmh' in cr_flags:
        cr_hs = (1 * (float(cr_flags.split('-hmh ', 1)[1].split(' ', 1)[0])) / 5)*4
    elif 'hmp' in cr_flags:
        cr_hs = (.8 * (float(cr_flags.split('-hmp ', 1)[1].split(' ', 1)[0])) / 5)*4
    elif 'hmt' in cr_flags:
        cr_hs = (.7 * (1 - (float(cr_flags.split('-hmt ', 1)[1].split(' ', 1)[0])) / 5))*4
    else:
        cr_hs = 0.2 * 4
    cr = cr + cr_hs

    # EXP/GP SCALING
    if '-xga' in cr_flags:
        cr_xgp = (.9 * (1 - (float(cr_flags.split('-xga ', 1)[1].split(' ', 1)[0]))/5))*4
    elif 'xgh' in cr_flags:
        cr_xgp = (.8 * (1 - (float(cr_flags.split('-xgh ', 1)[1].split(' ', 1)[0])) / 5))*4
    elif 'xgp' in cr_flags:
        cr_xgp = (1 - (.8 * (float(cr_flags.split('-xgp ', 1)[1].split(' ', 1)[0])) / 5))*4
    elif 'xgt' in cr_flags:
        cr_xgp = (.7 * (float(cr_flags.split('-xgt ', 1)[1].split(' ', 1)[0])) / 5)*4
    else:
        cr_xgp = 0.2 * 4
    cr = cr + cr_xgp

    # ABILITY SCALING
    if '-ase' in cr_flags:
        cr_as = (.6 * (1 - (float(cr_flags.split('-ase ', 1)[1].split(' ', 1)[0]))/5))*4
    elif '-asr' in cr_flags:
        cr_as = (1 * (1 - (float(cr_flags.split('-asr ', 1)[1].split(' ', 1)[0])) / 5))*4
    else:
        cr_as = 0.8 * 4
    cr = cr + cr_as

    # MAX SCALE LEVEL ----- Another one that's close but not close enough - must be the logs
    if '-msl' in cr_flags:
        cr_msl = (((math.log(float(cr_flags.split('-msl ', 1)[1].split(' ', 1)[0])))/math.log(99-2))**6)*4
    else:
        cr_msl = 0
    cr = cr + cr_msl

    # EXTRA ENEMY LEVELS ----- Another one that's close but not close enough - must be the logs
    if '-eel' in cr_flags and '-eel 0' not in cr_flags:
        cr_eel = (((math.log(float(cr_flags.split('-eel ', 1)[1].split(' ', 1)[0])))/math.log(99+1))**2)*4
    else:
        cr_eel = 0
    cr = cr + cr_eel

    # SCALE FINAL BOSS
    if '-sfb' in cr_flags:
        cr_sfb = (min([cr_msl/4, cr_eel/4]))*2
    else:
        cr_sfb = (min(.4 + cr_eel/4, 1))*2
    cr = cr + cr_sfb

    # SCALE EIGHT DRAGONS
    if '-sed' in cr_flags:
        cr_sed = (min([cr_msl/4, cr_eel/4]))*2
    else:
        cr_sed = (min(.4 + cr_eel/4, 1))*2
    cr = cr + cr_sed

    # BOSS BATTLES
    if '-bbs' in cr_flags:
        cr_bb = 0.5 * 2
    elif '-bbr' in cr_flags:
        cr_bb = 1 * 2
    else:
        cr_bb = 0
    cr = cr + cr_bb

    # MIX BOSSES AND DRAGONS
    if '-bmbd' in cr_flags:
        cr_bmbd = 1 * 2
    else:
        cr_bmbd = 0
    cr = cr + cr_bmbd

    # SHUFFLE PHUNBABA3
    if '-srp3' in cr_flags:
        cr_srp3 = 1 * 2
    else:
        cr_srp3 = 0
    cr = cr + cr_srp3

    # NORMALIZE & DISTORT
    if '-bnds' in cr_flags:
        cr_bnds = 1 * 4
    else:
        cr_bnds = 0
    cr = cr + cr_bnds

    # BOSS EXPERIENCE
    if '-be ' not in cr_flags:
        cr_be = 1 * 4
    else:
        cr_be = 0
    cr = cr + cr_be

    # NO UNDEAD BOSSES
    if '-bnu' in cr_flags:
        cr_bnu = 1
    else:
        cr_bnu = 0
    cr = cr + cr_bnu

    # RANDOM ENCOUNTERS
    if '-res ' in cr_flags:
        cr_renc = .2 * 2
    elif '-rer ' in cr_flags:
        cr_renc = 2 * (.2 + (1 - .2)*(float(cr_flags.split('-rer ', 1)[1].split(' ', 1)[0]))/100)
    else:
        cr_renc = 0
    cr = cr + cr_renc

    # FIXED ENCOUNTERS
    if '-fer ' in cr_flags:
        cr_fenc = (.25 + ((float(cr_flags.split('-fer ', 1)[1].split(' ', 1)[0]))/100)*(1 - .25)) * 2
    else:
        cr_fenc = 0
    cr = cr + cr_fenc

    # ESCAPABLE BATTLES
    if '-escr' in cr_flags and float(cr_flags.split('-escr ', 1)[1].split(' ', 1)[0]) > 0:
        cr_escr = (1-float(cr_flags.split('-escr ', 1)[1].split(' ', 1)[0])/100)*2
    else:
        cr_escr = 0
    cr = cr + cr_escr

    # DOOMGAZE NO ESCAPE
    if '-dgne' not in cr_flags:
        cr_dgne = 2
    else:
        cr_dgne = 0
    cr = cr + cr_dgne

    # WREXSOUL NO ZINGER
    if '-wnz' not in cr_flags:
        cr_wnz = 2
    else:
        cr_wnz = 0
    cr = cr + cr_wnz

    # MAGIMASTER NO ULTIMA
    if '-mmnu' not in cr_flags:
        cr_mmnu = 4
    else:
        cr_mmnu = 0
    cr = cr + cr_mmnu

    # CHADARNOOK MORE LIKE BADARNOOK
    if '-cmd' not in cr_flags:
        cr_cmd = 2
    else:
        cr_cmd = 0
    cr = cr + cr_cmd

    # ESPER SPELLS
    if '-esrr ' in cr_flags:
        cr_espells = .222 * 2
    elif '-ess ' in cr_flags:
        cr_espells = .326 * 2
    elif '-essrr ' in cr_flags:
        cr_espells = .222 * 2
    elif '-esr ' in cr_flags:
        cr_espells = (2 * (1 - (((float(cr_flags.split('-esr ', 1)[1].split(' ', 1)[0])) +
                                (float(cr_flags.split('-esr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])))/2)/5))
    elif '-esrt ' in cr_flags:
        cr_espells = .6 * 2
    else:
        cr_espells = 0.326 * 2
    cr = cr + cr_espells

    # ESPER BONUSES
    if '-ebs ' in cr_flags:
        cr_ebonus = .333 * 1
    elif '-ebr ' in cr_flags:
        cr_ebonus = (1 - ((float(cr_flags.split('-ebr ', 1)[1].split(' ', 1)[0]))/100))
    else:
        cr_ebonus = .333 * 1
    cr = cr + cr_ebonus

    # ESPER MP
    if '-emps ' in cr_flags:
        cr_emp = .4 * 1
    elif '-emprv ' in cr_flags:
        cr_emp = ((((float(cr_flags.split('-emprv ', 1)[1].split(' ', 1)[0])) +
                       (float(cr_flags.split('-emprv ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])))/2)/128)
    elif '-emprp ' in cr_flags:
        cr_emp = (.773 * ((((float(cr_flags.split('-emprp ', 1)[1].split(' ', 1)[0])) +
                       (float(cr_flags.split('-emprp ', 1)[1].split(' ', 1)[1].split(' ', 1)[0]))) / 2) / 200))
    else:
        cr_emp = .388 * 1
    cr = cr + cr_emp

    # EQUIPPABLE ESPERS
    if '-eer ' in cr_flags:
        a = float(cr_flags.split('-eer ', 1)[1].split(' ', 1)[0])
        b = float(cr_flags.split('-eer ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        cr_eqes = (1 - (((a+b)/2)/12))*4
    elif '-eebr ' in cr_flags:
        cr_eqes = ((.9 * (1 - (float(cr_flags.split('-eebr ', 1)[1].split(' ', 1)[0]))/12))*4)
    else:
        cr_eqes = 0
    cr = cr + cr_eqes

    # MULTI-SUMMON
    if '-ems ' in cr_flags:
        cr_ems = 0
    else:
        cr_ems = 2
    cr = cr + cr_ems

    # NATURAL MAGIC
    if '-nm1 ' in cr_flags:
        cr_nm1 = 0
    else:
        cr_nm1 = 2
    cr = cr + cr_nm1

    if '-nm2 ' in cr_flags:
        cr_nm2 = 0
    else:
        cr_nm2 = 2
    cr = cr + cr_nm2

    # STARTING GP ----- Talk with Doc about this. Any extra GP should actually LOWER the difficulty, not raise it.
    if '-gp ' in cr_flags:
        a = float(cr_flags.split('-gp ', 1)[1].split(' ', 1)[0])
        cr_gp = (1 - ((math.log(a+1)/math.log(999999))**3))*2
    else:
        cr_gp = 1
    cr = cr + cr_gp

    cr_flags_r = ' '.join([cr_flags, "--Rating:", str(cr)])

    # STARTING MOOGLE CHARMS
    if '-smc ' in cr_flags:
        a = float(cr_flags.split('-smc ', 1)[1].split(' ', 1)[0])
        if a == 0:
            cr_smc = 2
        else:
            cr_smc = (.1 * (3 - a))*2
    else:
        cr_smc = 2
    cr = cr + cr_smc

    # STARTING WARP STONES
    if '-sws ' in cr_flags:
        a = float(cr_flags.split('-sws ', 1)[1].split(' ', 1)[0])
        cr_sws = 1 - math.log(a+1)/math.log(11)
    else:
        cr_sws = 1
    cr = cr + cr_sws

    # STARTING FENIX DOWNS
    if '-sfd ' in cr_flags:
        a = float(cr_flags.split('-sfd ', 1)[1].split(' ', 1)[0])
        cr_sfd = 1 - a / 10
    else:
        cr_sfd = 1
    cr = cr + cr_sfd

    # STARTING TOOLS
    if '-sto ' in cr_flags:
        a = float(cr_flags.split('-sto ', 1)[1].split(' ', 1)[0])
        cr_sto = 1 - a / 8
    else:
        cr_sto = 1
    cr = cr + cr_sto

    # EQUIPPABLE ITEMS
    if '-ier ' in cr_flags:
        a = float(cr_flags.split('-ier ', 1)[1].split(' ', 1)[0])
        b = float(cr_flags.split('-ier ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        cr_eqitems = (1 - (((a + b)/2)/14)) * 8
    elif '-iebr ' in cr_flags:
        a = float(cr_flags.split('-iebr ', 1)[1].split(' ', 1)[0])
        cr_eqitems = (1 - (a/14)) * 8
    elif '-ieor ' in cr_flags:
        a = float(cr_flags.split('-ieor ', 1)[1].split(' ', 1)[0])
        cr_eqitems = ((100 - a)/200) * 8
    elif '-iesr ' in cr_flags:
        a = float(cr_flags.split('-iesr ', 1)[1].split(' ', 1)[0])
        cr_eqitems = ((100 - a)/200) * 8
    else:
        cr_eqitems = .149 * 8
    cr = cr + cr_eqitems

    # EQUIPPABLE RELICS
    if '-ierr ' in cr_flags:
        a = float(cr_flags.split('-ierr ', 1)[1].split(' ', 1)[0])
        b = float(cr_flags.split('-ierr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        cr_eqrelics = (1 - (((a + b)/2)/14)) * 8
    elif '-ierbr ' in cr_flags:
        a = float(cr_flags.split('-ierbr ', 1)[1].split(' ', 1)[0])
        cr_eqrelics = (1 - (a/14)) * 8
    elif '-ieror ' in cr_flags:
        a = float(cr_flags.split('-ieror ', 1)[1].split(' ', 1)[0])
        cr_eqrelics = ((100 - a)/200) * 8
    elif '-iersr ' in cr_flags:
        a = float(cr_flags.split('-iersr ', 1)[1].split(' ', 1)[0])
        cr_eqrelics = ((100 - a)/200) * 8
    else:
        cr_eqrelics = .149 * 8
    cr = cr + cr_eqrelics

    # CURSED SHIELD BATTLES
    if '-csb ' in cr_flags:
        a = float(cr_flags.split('-csb ', 1)[1].split(' ', 1)[0])
        b = float(cr_flags.split('-csb ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        cr_csb = (math.log((a + b)/2)/math.log(256)) * 2
    else:
        cr_csb = 2

    # MOOGLE CHARM ALL
    if '-mca ' in cr_flags:
        cr_mca = 0
    else:
        cr_mca = 4
    cr = cr + cr_mca

    # STRONGER ATMA WEAPON
    if '-saw ' in cr_flags:
        cr_saw = 0
    else:
        cr_saw = 2
    cr = cr + cr_saw

    # SHOP INVENTORY
    if '-sisr ' in cr_flags:
        a = float(cr_flags.split('-sisr ', 1)[1].split(' ', 1)[0])
        cr_shopinv = (.6 * (1 - (a/100)))*4
    elif '-sirt ' in cr_flags:
        cr_shopinv = .54 * 4
    elif '-sie ' in cr_flags:
        cr_shopinv = 4
    else:
        cr_shopinv = 2.4
    cr = cr + cr_shopinv

    # SHOP PRICES
    if '-sprv ' in cr_flags:
        a = float(cr_flags.split('-sprv ', 1)[1].split(' ', 1)[0])
        b = float(cr_flags.split('-sprv ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        cr_shopprice = (.25 * ((math.log(a + b / 2) + 1)/math.log(65536))) * 2
    elif '-sprp ' in cr_flags:
        a = float(cr_flags.split('-sprp ', 1)[1].split(' ', 1)[0])
        b = float(cr_flags.split('-sprp ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        cr_shopprice = (((a + b) / 2) / 200) * 2
    else:
        cr_shopprice = .5 * 2
    cr = cr + cr_shopprice

    # SELL PRICES
    if '-ssf4 ' in cr_flags:
        cr_sellp = .25 * 2
    elif '-ssf8 ' in cr_flags:
        cr_sellp = .5 * 2
    elif '-ssf0 ' in cr_flags:
        cr_sellp = 1 * 2
    else:
        cr_sellp = 0
    cr = cr + cr_sellp

    # DRIED MEAT
    if '-sdm 0' in cr_flags:
        cr_sdm = 16
    elif '-sdm ' in cr_flags:
        a = float(cr_flags.split('-sdm ', 1)[1].split(' ', 1)[0])
        cr_sdm = 1 - (a/5)
    else:
        cr_sdm = 0
    cr = cr + cr_sdm

    # NO PRICELESS ITEMS
    if '-npi ' in cr_flags:
        cr_npi = 8
    else:
        cr_npi = 0
    cr = cr + cr_npi

    # NO BREAKABLE RODS
    if '-snbr' in cr_flags:
        cr_snbr = 4
    else:
        cr_snbr = 0
    cr = cr + cr_snbr

    # NO ELEMENTAL SHIELDS
    if '-snes' in cr_flags:
        cr_snes = 2
    else:
        cr_snes = 0
    cr = cr + cr_snes

    # NO SUPER BALLS
    if '-snsb' in cr_flags:
        cr_snsb = 2
    else:
        cr_snsb = 0
    cr = cr + cr_snsb

    # CHEST CONTENTS
    if '-ccsr ' in cr_flags:
        a = float(cr_flags.split('-ccsr ', 1)[1].split(' ', 1)[0])
        cr_ccontents = (.6 * (1 - (a / 100))) * 2
    elif '-ccrt ' in cr_flags:
        cr_ccontents = .54 * 2
    elif '-cce ' in cr_flags:
        cr_ccontents = 1 * 2
    else:
        cr_ccontents = .2 * 2
    cr = cr + cr_ccontents

    # SHUFFLE MIAB
    if '-cms ' in cr_flags:
        cr_cms = 1
    else:
        cr_cms = 0
    cr = cr + cr_cms

    # COLISEUM OPPONENTS
    if '-cos ' in cr_flags:
        cr_col = .5 * 2
    elif '-cor ' in cr_flags:
        cr_col = 0
    else:
        cr_col = 1 * 2
    cr = cr + cr_col

    # COLISEUM REWARDS
    if '-crs ' in cr_flags:
        cr_crew = .5 * 2
    elif '-crr ' in cr_flags:
        cr_crew = 0
    else:
        cr_crew = 1 * 2

    # COLISEUM REWARDS VISIBLE
    if '-crvr ' in cr_flags:
        a = float(cr_flags.split('-crvr ', 1)[1].split(' ', 1)[0])
        b = float(cr_flags.split('-crvr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        cr_crv = (1 - (((a + b)/2)/255)) * 2
    else:
        cr_crv = 0

    # COLISEUM REWARDS MENU
    if '-crm ' in cr_flags:
        cr_crm = 0
    else:
        cr_crm = 1 * 2
    cr = cr + cr_crm

    # RANDOMIZE AUTION HOUSE ITEMS
    if '-ari ' in cr_flags:
        cr_ari = 0
    else:
        cr_ari = 1 * 2
    cr = cr + cr_ari

    # DOOR ESPER HINT
    if '-adeh ' in cr_flags:
        cr_adeh = 0
    else:
        cr_adeh = 1 * 4
    cr = cr + cr_adeh

    # NO MOOGLE CHARMS
    if '-nmc ' in cr_flags and cr_smc == 0:
        cr_nmc = 16
    elif '-nmc ' in cr_flags:
        cr_nmc = 1
    else:
        cr_nmc = 0
    cr = cr + cr_nmc

    # NO EXPERIENCE EGGS
    if '-nee ' in cr_flags:
        cr_nee = 1 * 2
    else:
        cr_nee = 0
    cr = cr + cr_nee

    # NO ILLUMINAS
    if '-nil ' in cr_flags:
        cr_nil = 1 * 2
    else:
        cr_nil = 0
    cr = cr + cr_nil

    # NO FREE PALADIN SHIELDS
    if '-nfps ' in cr_flags:
        cr_nfps = 1 * 2
    else:
        cr_nfps = 0
    cr = cr + cr_nfps

    # NO ULTIMA
    if '-nu ' in cr_flags:
        cr_nu = 1 * 2
    else:
        cr_nu = 0
    cr = cr + cr_nu

    # NO FREE PROGRESSION
    if '-nfp ' not in cr_flags:
        cr_nfp = 1 * 2
    else:
        cr_nfp = 0
    cr = cr + cr_nfp

    # HIDDEN REQUIREMENTS
    if '-kthr ' in cr_flags:
        cr_kthr = 1 * 4
    else:
        cr_kthr = 0
    cr = cr + cr_kthr

    # PERMADEATH
    if '-pd ' in cr_flags:
        cr_pd = 1 * 8
    else:
        cr_pd = 0
    cr = cr + cr_pd

    # ORIGINAL NAME DISPLAY
    if '-ond ' not in cr_flags:
        cr_ond = 1 * 1
    else:
        cr_ond = 0
    cr = cr + cr_ond

    # RANDOMIZE RNG
    if '-rr ' in cr_flags:
        cr_rr = 1 * 1
    else:
        cr_rr = 0
    cr = cr + cr_rr

    # SCAN ALL
    if '-scan ' not in cr_flags:
        cr_scan = 1
    else:
        cr_scan = 0
    cr = cr + cr_scan

    # EVENT TIMERS
    if '-etn ' in cr_flags:
        cr_et = 0
    else:
        cr_et = 1
    cr = cr + cr_et

    # FIX EVADE
    if '-fe ' in cr_flags:
        cr_fe = 1 * 2
    else:
        cr_fe = 0
    cr = cr + cr_fe

    # FIX VANISH DOOM
    if '-fvd ' in cr_flags:
        cr_fvd = 1 * 2
    else:
        cr_fvd = 0
    cr = cr + cr_fvd

    # FIX RETORT
    if '-fr ' in cr_flags:
        cr_fr = 1 * 2
    else:
        cr_fr = 0
    cr = cr + cr_fr

    # FIX BOSS SKIP
    if '-fbs ' in cr_flags:
        cr_fbs = 1 * 1
    else:
        cr_fbs = 0
    cr = cr + cr_fbs

    # FIX ENEMY DAMAGE COUNTER
    if '-fedc ' not in cr_flags:
        cr_fedc = 1 * 1
    else:
        cr_fedc = 0
    cr = cr + cr_fedc

    # print("Rating: ", cr)
    # print("sl:", cr_sl, "ktc:", cr_ktc, "kte:", cr_kte, "ktd:", cr_ktd, "stno:", cr_stno, "stc:", cr_stc)
    # print("ste:", cr_ste, "std:", cr_std, "sc2:", cr_sc2, "sc3:", cr_sc3, "sc4:", cr_sc4, "sal:", cr_sal)
    # print("sn:", cr_sn, "eu:", cr_eu, "csrp:", cr_csrp, "sel:", cr_sel, "brl:", cr_brl, "bel:", cr_bel, "slr:", cr_slr)
    # print("loremp:", cr_loremp, "lel:", cr_lel, "srr:", cr_srr, "rnc:", cr_rnc, "sdr:", cr_sdr, "das:", cr_das)
    # print("dda:", cr_dda, "dns:", cr_dns, "del:", cr_del, "com:", cr_com, "xpm:", cr_xpm, "mpm:", cr_mpm, "gpm:", cr_gpm)
    # print("nxppd:", cr_nxppd, "ls:", cr_ls, "hs:", cr_hs, "xgp:", cr_xgp, "as:", cr_as, "msl:", cr_msl, "eel:", cr_eel)
    # print("sfb:", cr_sfb, "sed:", cr_sed, "bb:", cr_bb, "bmbd:", cr_bmbd, "srp3:", cr_srp3, "bnds:", cr_bnds, "be:", cr_be)
    # print("bnu:", cr_bnu, "renc:", cr_renc, "fenc:", cr_fenc, "escr:", cr_escr, "dgne:", cr_dgne, "wnz:", cr_wnz)
    # print("mmnu:", cr_mmnu, "cmd:", cr_cmd, "espells:", cr_espells, "ebonus:", cr_ebonus, "emp:", cr_emp, "eqes:", cr_eqes)
    # print("ems:", cr_ems, "nm1:", cr_nm1, "nm2:", cr_nm2, "gp:", cr_gp, "smc:", cr_smc, "sws:", cr_sws, "sfd:", cr_sfd)
    # print("sto:", cr_sto, "eqitems:", cr_eqitems, "eqrelics:", cr_eqrelics, "csb:", cr_csb, "mca:", cr_mca, "saw:", cr_saw)
    # print("shopinv:", cr_shopinv, "shopprice:", cr_shopprice, "sellp:", cr_sellp, "sdm:", cr_sdm, "npi:", cr_npi)
    # print("snbr:", cr_snbr, "snes:", cr_snes, "snsb:", cr_snsb, "ccontents:", cr_ccontents, "cms:", cr_cms, "col:", cr_col)
    # print("crv:", cr_crv, "crm:", cr_crm, "ari:", cr_ari, "adeh:", cr_adeh, "nmc:", cr_nmc, "nee:", cr_nee, "nil:", cr_nil)
    # print("nfps:", cr_nfps, "nu:", cr_nu, "nfp:", cr_nfp, "kthr:", cr_kthr, "pd:", cr_pd, "ond:", cr_ond, "rr:", cr_rr)
    # print("scan:", cr_scan, "et:", cr_et, "fe:", cr_fe, "fvd:", cr_fvd, "fr:", cr_fr, "fbs:", cr_fbs, "fedc:", cr_fedc)
    return cr_flags, cr