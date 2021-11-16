from flags import chaos, true_chaos, standard, rated
import math
import challenge_ratings as r


def get_cr():
    cr_flags = rated()

    def sf1(f):
        f1 = float(cr_flags.split(f, 1)[1].split(' ', 1)[0])
        return f1

    def sf2(f):
        f2 = float(cr_flags.split(f, 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        return f2

    cr = 0

    # GAME MODE
    flag = '-ow '
    if flag in cr_flags:
        cr_gm = 0 * r.cr_gm
    else:
        cr_gm = 1 * r.cr_gm
    cr += cr_gm

    # SPOILER LOG
    flag = '-sl '
    if flag not in cr_flags:
        cr_sl = 1 * r.cr_sl
    else:
        cr_sl = 0 * r.cr_sl
    cr += cr_sl

    # KEFKA'S TOWER CHARACTER REQUIREMENT
    flag = 'ktcr '
    a = sf1(flag)
    b = sf2(flag)
    cr_ktc = ((((a + b) / 2) - 3) / 11) * r.cr_ktcr
    cr += cr_ktc

    # KEFKA'S TOWER ESPER REQUIREMENT
    flag = 'kter '
    a = sf1(flag)
    b = sf2(flag)
    cr_kte = (((a + b) / 2) / 27) * r.cr_kter
    cr += cr_kte

    # KEFKA'S TOWER DRAGON REQUIREMENT
    flag = 'ktdr '
    a = sf1(flag)
    b = sf2(flag)
    cr_ktd = (((a + b) / 2) / 8) * r.cr_ktdr
    cr += cr_ktd

    # STATUE SKIP ---- ASK DOCTORDT ABOUT THIS ONE
    flag = 'stno '
    if flag in cr_flags:
        cr_stno = 1 * r.cr_stno
    else:
        cr_stno = 0 * r.cr_stno
    cr += cr_stno

    # SKIP CHARACTER REQUIREMENT
    flag = '-stcr '
    if '-stno ' not in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_stc = ((((a + b) / 2) - 3) / 11) * r.cr_stcr
    else:
        cr_stc = 0 * r.cr_stcr
    cr += cr_stc

    # SKIP ESPER REQUIREMENT
    flag = '-ster '
    if '-stno ' not in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_ste = (((a + b) / 2) / 27) * r.cr_ster
    else:
        cr_ste = 0
    cr += cr_ste

    # SKIP DRAGON REQUIREMENT
    flag = '-stdr '
    if '-stno ' not in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_std = (((a + b) / 2) / 8) * r.cr_stdr
    else:
        cr_std = 0
    cr += cr_std

    # STARTING CHARACTERS
    flag = '-sc2 '
    if flag not in cr_flags:
        cr_sc2 = 1 * r.cr_sc2
    else:
        cr_sc2 = 0 * r.cr_sc2
    cr += cr_sc2

    flag = '-sc3 '
    if flag not in cr_flags:
        cr_sc3 = 1 * r.cr_sc3
    else:
        cr_sc3 = 0 * r.cr_sc3
    cr += cr_sc3

    flag = '-sc4 '
    if flag not in cr_flags:
        cr_sc4 = 1 * r.cr_sc4
    else:
        cr_sc4 = 0 * r.cr_sc4
    cr += cr_sc4

    # START AVERAGE LEVEL
    flag = '-sal '
    if flag not in cr_flags:
        cr_sal = 1 * r.cr_sal
    else:
        cr_sal = 0 * r.cr_sal
    cr += cr_sal

    # START NAKED
    flag = '-sn '
    if flag in cr_flags:
        cr_sn = 1 * r.cr_sn
    else:
        cr_sn = 0 * r.cr_sn
    cr += cr_sn

    # EQUIPPABLE UMARO
    flag = '-eu '
    if flag not in cr_flags:
        cr_eu = 1 * r.cr_eu
    else:
        cr_eu = 0 * r.cr_eu
    cr += cr_eu

    # CHARACTER STATS
    flag = '-csrp '
    if flag in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_csrp = (2 - (((a + b) / 2) / 200)) * r.cr_csrp
    else:
        cr_csrp = (2 - ((100 / 200) * 2)) * r.cr_csrp
    cr += cr_csrp

    # SWORDTECH EVERYONE LEARNS
    flag = '-sel '
    if flag not in cr_flags:
        cr_sel = 1 * r.cr_sel
    else:
        cr_sel = 0 * r.cr_sel
    cr += cr_sel

    # BUM RUSH LAST
    flag = '-brl '
    if flag not in cr_flags:
        cr_brl = 0 * r.cr_brl
    else:
        cr_brl = 1 * r.cr_brl
    cr += cr_brl

    # BLITZ EVERYONE LEARNS
    flag = '-bel '
    if flag not in cr_flags:
        cr_bel = 1 * r.cr_bel
    else:
        cr_bel = 0 * r.cr_bel
    cr += cr_bel

    # STARTING LORES
    flag = '-slr '
    if flag in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_slr = (2 - (((a + b) / 2) / 24)) * r.cr_slr
    else:
        cr_slr = (2 - (((3 + 3) / 2) / 24)) * r.cr_slr
    cr = cr + cr_slr

    # LORE MP
    if '-lmps ' in cr_flags:
        cr_loremp = 0.175 * r.cr_loremp
    elif '-lmprv ' in cr_flags:
        a = sf1('-lmprv ')
        b = sf2('-lmprv ')
        cr_loremp = (2 - (((a + b) / 2) / 99)) * r.cr_loremp
    elif '-lmprp ' in cr_flags:
        a = sf1('-lmprp ')
        b = sf2('-lmprp ')
        cr_loremp = (2 - (((a + b) / 2) / 200)) * r.cr_loremp
    else:
        cr_loremp = 0.35 * r.cr_loremp
    cr += cr_loremp

    # LORE EVERYONE LEARNS
    flag = '-lel '
    if flag not in cr_flags:
        cr_lel = 1 * r.cr_lel
    else:
        cr_lel = 0 * r.cr_lel
    cr += cr_lel

    # STARTING RAGES
    flag = '-srr '
    if flag in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_srr = (2 - ((1 - (a + b) / 2) / 255)) * r.cr_srr
    else:
        cr_srr = (1 - (9 / 255)) * r.cr_srr
    cr += cr_srr

    # NO CHARM
    flag = '-rnc '
    if flag in cr_flags:
        cr_rnc = 1 * r.cr_rnc
    else:
        cr_rnc = 0 * r.cr_rnc
    cr += cr_rnc

    # STARTING DANCES
    flag = '-sdr '
    if flag in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_sdr = (1 - (((a + b) / 2) / 8)) * r.cr_sdr
    else:
        cr_sdr = 0 * r.cr_sdr
    cr += cr_sdr

    # DANCE ABILITY SHUFFLE
    flag = '-das '
    if flag not in cr_flags:
        cr_das = 1 * r.cr_das
    else:
        cr_das = 0 * r.cr_das
    cr += cr_das

    # DISPLAY DANCE ABILITY NAMES
    flag = '-dda '
    if flag not in cr_flags:
        cr_dda = 1 * r.cr_dda
    else:
        cr_dda = 0 * r.cr_dda
    cr += cr_dda

    # DANCE NO STUMBLE
    flag = '-dns '
    if flag not in cr_flags:
        cr_dns = 1 * r.cr_dns
    else:
        cr_dns = 0 * r.cr_dns
    cr += cr_dns

    # DANCE EVERYONE LEARNS
    flag = '-del '
    if flag not in cr_flags:
        cr_del = 1 * r.cr_del
    else:
        cr_del = 0 * r.cr_del
    cr += cr_del

    # COMMANDS ----- Talk to Doc about the CR mod for these
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
        cr_com = (skills[com1] + skills[com2] + skills[com3] + skills[com4] + skills[com5] + skills[com6] + skills[com7]
             + skills[com8] + skills[com9] + skills[com10] + skills[com11] + skills[com12] + skills[com13]) * r.cr_com
    else:
        cr_com = 6.6 * r.cr_com
    cr += cr_com

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
    flag = '-xpm '
    if '-xpm 0' in cr_flags:
        cr_xpm = 80
    elif flag not in cr_flags:
        cr_xpm = 1 * r.cr_xpm
    else:
        cr_xpm = ((1 - math.sqrt(math.log(int(cr_flags.split('-xpm ', 1)[1].split(' ', 1)[0]))/math.log(255))) *
                  (r.cr_xpm / 2))
    cr += cr_xpm

    # MP MODIFIER
    flag = '-mpm '
    if flag not in cr_flags:
        cr_mpm = 1 * r.cr_mpm
    else:
        cr_mpm = ((1 - math.sqrt(math.log(int(cr_flags.split('-mpm ', 1)[1].split(' ', 1)[0]))/math.log(255)))*r.cr_mpm)
    cr += cr_mpm

    # GP MODIFIER
    flag = '-gpm '
    if flag not in cr_flags:
        cr_gpm = 1 * r.cr_mpm
    else:
        cr_gpm = ((1 - math.sqrt(math.log(int(cr_flags.split('-gpm ', 1)[1].split(' ', 1)[0]))/math.log(255)))*r.cr_gpm)
    cr += cr_gpm

    # NO PARTY EXP SPLIT
    flag = '-nxppd '
    if flag not in cr_flags:
        cr_nxppd = 1 * r.cr_nxppd
    else:
        cr_nxppd = 0 * r.cr_nxppd
    cr += cr_nxppd

    # LEVEL SCALING
    if '-lsa' in cr_flags:
        cr_ls = (.9 * (float(cr_flags.split('-lsa ', 1)[1].split(' ', 1)[0]))/5) * r.cr_ls
    elif 'lsh' in cr_flags:
        cr_ls = (1 * (float(cr_flags.split('-lsh ', 1)[1].split(' ', 1)[0])) / 5) * r.cr_ls
    elif 'lsp' in cr_flags:
        cr_ls = (.8 * (float(cr_flags.split('-lsp ', 1)[1].split(' ', 1)[0])) / 5) * r.cr_ls
    elif 'lst' in cr_flags:
        cr_ls = (.7 * (1 - (float(cr_flags.split('-lst ', 1)[1].split(' ', 1)[0])) / 5)) * r.cr_ls
    else:
        cr_ls = 0.2 * r.cr_ls
    cr += cr_ls

    # HP/MP SCALING
    if '-hma' in cr_flags:
        cr_hs = (.9 * (float(cr_flags.split('-hma ', 1)[1].split(' ', 1)[0]))/5) * r.cr_hs
    elif 'hmh' in cr_flags:
        cr_hs = (1 * (float(cr_flags.split('-hmh ', 1)[1].split(' ', 1)[0])) / 5) * r.cr_hs
    elif 'hmp' in cr_flags:
        cr_hs = (.8 * (float(cr_flags.split('-hmp ', 1)[1].split(' ', 1)[0])) / 5) * r.cr_hs
    elif 'hmt' in cr_flags:
        cr_hs = (.7 * (1 - (float(cr_flags.split('-hmt ', 1)[1].split(' ', 1)[0])) / 5)) * r.cr_hs
    else:
        cr_hs = 0.2 * r.cr_hs
    cr += cr_hs

    # EXP/GP SCALING
    if '-xga' in cr_flags:
        cr_xgp = (.9 * (1 - (float(cr_flags.split('-xga ', 1)[1].split(' ', 1)[0]))/5)) * r.cr_xgp
    elif 'xgh' in cr_flags:
        cr_xgp = (.8 * (1 - (float(cr_flags.split('-xgh ', 1)[1].split(' ', 1)[0])) / 5)) * r.cr_xgp
    elif 'xgp' in cr_flags:
        cr_xgp = (1 - (.8 * (float(cr_flags.split('-xgp ', 1)[1].split(' ', 1)[0])) / 5)) * r.cr_xgp
    elif 'xgt' in cr_flags:
        cr_xgp = (.7 * (float(cr_flags.split('-xgt ', 1)[1].split(' ', 1)[0])) / 5) * r.cr_xgp
    else:
        cr_xgp = 0.2 * r.cr_xgp
    cr += cr_xgp

    # ABILITY SCALING
    if '-ase' in cr_flags:
        cr_as = (.6 * (1 - (float(cr_flags.split('-ase ', 1)[1].split(' ', 1)[0]))/5)) * r.cr_as
    elif '-asr' in cr_flags:
        cr_as = (1 * (1 - (float(cr_flags.split('-asr ', 1)[1].split(' ', 1)[0])) / 5)) * r.cr_as
    else:
        cr_as = 0.8 * r.cr_as
    cr += cr_as

    # MAX SCALE LEVEL ----- Another one that's close but not close enough - must be the logs
    flag = '-msl '
    if flag in cr_flags:
        cr_msl = (((math.log(float(cr_flags.split('-msl ', 1)[1].split(' ', 1)[0])))/math.log(99-2))**6) * r.cr_msl
    else:
        cr_msl = 0 * r.cr_msl
    cr += cr_msl

    # EXTRA ENEMY LEVELS ----- Another one that's close but not close enough - must be the logs
    flag = '-eel '
    if flag in cr_flags and '-eel 0' not in cr_flags:
        cr_eel = (((math.log(float(cr_flags.split('-eel ', 1)[1].split(' ', 1)[0])))/math.log(99+1))**2) * r.cr_eel
    else:
        cr_eel = 0 * r.cr_eel
    cr += cr_eel

    # SCALE FINAL BOSS
    flag = '-sfb '
    if flag in cr_flags:
        cr_sfb = (min([cr_msl/4, cr_eel/4])) * r.cr_sfb
    else:
        cr_sfb = (min(.4 + cr_eel/4, 1)) * r.cr_sfb
    cr += cr_sfb

    # SCALE EIGHT DRAGONS
    flag = '-sed '
    if flag in cr_flags:
        cr_sed = (min([cr_msl/4, cr_eel/4])) * r.cr_sed
    else:
        cr_sed = (min(.4 + cr_eel/4, 1)) * r.cr_sed
    cr += cr_sed

    # BOSS BATTLES
    if '-bbs' in cr_flags:
        cr_bb = 0.5 * r.cr_bb
    elif '-bbr' in cr_flags:
        cr_bb = 1 * r.cr_bb
    else:
        cr_bb = 0 * r.cr_bb
    cr += cr_bb

    # MIX BOSSES AND DRAGONS
    flag = '-bmbd '
    if flag in cr_flags:
        cr_bmbd = 1 * r.cr_bmbd
    else:
        cr_bmbd = 0 * r.cr_bmbd
    cr += cr_bmbd

    # SHUFFLE PHUNBABA3
    flag = 'srp3 '
    if flag in cr_flags:
        cr_srp3 = 1 * r.cr_srp3
    else:
        cr_srp3 = 0 * r.cr_srp3
    cr += cr_srp3

    # NORMALIZE & DISTORT
    flag = '-bnds '
    if flag in cr_flags:
        cr_bnds = 1 * r.cr_bnds
    else:
        cr_bnds = 0 * r.cr_bnds
    cr += cr_bnds

    # BOSS EXPERIENCE
    flag = '-be '
    if flag not in cr_flags:
        cr_be = 1 * r.cr_be
    else:
        cr_be = 0 * r.cr_be
    cr += cr_be

    # NO UNDEAD BOSSES
    flag = '-bnu '
    if flag in cr_flags:
        cr_bnu = 1 * r.cr_bnu
    else:
        cr_bnu = 0 * r.cr_bnu
    cr += cr_bnu

    # RANDOM ENCOUNTERS
    if '-res ' in cr_flags:
        cr_renc = .2 * r.cr_renc
    elif '-rer ' in cr_flags:
        cr_renc = (.2 + (1 - .2)*(float(cr_flags.split('-rer ', 1)[1].split(' ', 1)[0]))/100) * r.cr_renc
    else:
        cr_renc = 0 * r.cr_renc
    cr += cr_renc

    # FIXED ENCOUNTERS
    flag = '-fer '
    if flag in cr_flags:
        cr_fenc = (.25 + ((float(cr_flags.split('-fer ', 1)[1].split(' ', 1)[0]))/100)*(1 - .25)) * r.cr_fenc
    else:
        cr_fenc = 0 * r.cr_fenc
    cr += cr_fenc

    # ESCAPABLE BATTLES
    flag = '-escr '
    if flag in cr_flags and float(cr_flags.split('-escr ', 1)[1].split(' ', 1)[0]) > 0:
        cr_escr = (1-float(cr_flags.split('-escr ', 1)[1].split(' ', 1)[0])/100) * r.cr_escr
    else:
        cr_escr = 0 * r.cr_escr
    cr += cr_escr

    # DOOMGAZE NO ESCAPE
    flag = '-dgne '
    if flag not in cr_flags:
        cr_dgne = 1 * r.cr_dgne
    else:
        cr_dgne = 0 * r.cr_dgne
    cr += cr_dgne

    # WREXSOUL NO ZINGER
    flag = '-wnz '
    if flag not in cr_flags:
        cr_wnz = 1 * r.cr_wnz
    else:
        cr_wnz = 0 * r.cr_wnz
    cr += cr_wnz

    # MAGIMASTER NO ULTIMA
    flag = '-mmnu '
    if flag not in cr_flags:
        cr_mmnu = 1 * r.cr_mmnu
    else:
        cr_mmnu = 0 * r.cr_mmnu
    cr += cr_mmnu

    # CHADARNOOK MORE LIKE BADARNOOK
    flag = '-cmd '
    if flag not in cr_flags:
        cr_cmd = 1 * r.cr_cmd
    else:
        cr_cmd = 0 * r.cr_cmd
    cr += cr_cmd

    # ESPER SPELLS
    if '-esrr ' in cr_flags:
        cr_espells = .222 * r.cr_espells
    elif '-ess ' in cr_flags:
        cr_espells = .326 * r.cr_espells
    elif '-essrr ' in cr_flags:
        cr_espells = .222 * r.cr_espells
    elif '-esr ' in cr_flags:
        cr_espells = (1 - (((float(cr_flags.split('-esr ', 1)[1].split(' ', 1)[0])) +
                        (float(cr_flags.split('-esr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])))/2)/5) * r.cr_espells
    elif '-esrt ' in cr_flags:
        cr_espells = .6 * r.cr_espells
    else:
        cr_espells = 0.326 * r.cr_espells
    cr += cr_espells

    # ESPER BONUSES
    if '-ebs ' in cr_flags:
        cr_ebonus = .333 * r.cr_ebonus
    elif '-ebr ' in cr_flags:
        cr_ebonus = (1 - ((float(cr_flags.split('-ebr ', 1)[1].split(' ', 1)[0]))/100)) * r.cr_ebonus
    else:
        cr_ebonus = .333 * r.cr_ebonus
    cr += cr_ebonus

    # ESPER MP
    if '-emps ' in cr_flags:
        cr_emp = .4 * r.cr_emp
    elif '-emprv ' in cr_flags:
        cr_emp = ((((float(cr_flags.split('-emprv ', 1)[1].split(' ', 1)[0])) +
                       (float(cr_flags.split('-emprv ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])))/2)/128) * r.cr_emp
    elif '-emprp ' in cr_flags:
        cr_emp = (.773 * ((((float(cr_flags.split('-emprp ', 1)[1].split(' ', 1)[0])) +
                       (float(cr_flags.split('-emprp ', 1)[1].split(' ', 1)[1].split(' ', 1)[0]))) / 2) / 200)) * r.cr_emp
    else:
        cr_emp = .388 * r.cr_emp
    cr += cr_emp

    # EQUIPPABLE ESPERS
    if '-eer ' in cr_flags:
        a = sf1('-eer ')
        b = sf2('-eer ')
        cr_eqes = (1 - (((a+b)/2)/12)) * r.cr_eqes
    elif '-eebr ' in cr_flags:
        cr_eqes = (.9 * (1 - (float(cr_flags.split('-eebr ', 1)[1].split(' ', 1)[0]))/12)) * r.cr_eqes
    else:
        cr_eqes = 0 * r.cr_eqes
    cr += cr_eqes

    # MULTI-SUMMON
    flag = '-ems '
    if flag in cr_flags:
        cr_ems = 0 * r.cr_ems
    else:
        cr_ems = 1 * r.cr_ems
    cr += cr_ems

    # NATURAL MAGIC
    flag = '-nm1 '
    if flag in cr_flags:
        cr_nm1 = 0 * r.cr_nm1
    else:
        cr_nm1 = 1 * r.cr_nm1
    cr += cr_nm1

    flag = '-nm2 '
    if flag in cr_flags:
        cr_nm2 = 0 * r.cr_nm2
    else:
        cr_nm2 = 1 * r.cr_nm2
    cr += cr_nm2

    # STARTING GP ----- Talk with Doc about this. Any extra GP should actually LOWER the difficulty, not raise it.
    flag = '-gp '
    if flag in cr_flags:
        a = sf1(flag)
        cr_gp = (1 - ((math.log(a+1)/math.log(999999))**3)) * r.cr_gp
    else:
        cr_gp = 1 * r.cr_gp
    cr += cr_gp

    # STARTING MOOGLE CHARMS
    flag = '-smc '
    if flag in cr_flags:
        a = sf1(flag)
        if a == 0:
            cr_smc = 1 * r.cr_smc
        else:
            cr_smc = (.1 * (3 - a)) * r.cr_smc
    else:
        cr_smc = 1 * r.cr_smc
    cr += cr_smc

    # STARTING WARP STONES
    flag = '-sws '
    if flag in cr_flags:
        a = sf1(flag)
        cr_sws = (1 - math.log(a+1)/math.log(11)) * r.cr_sws
    else:
        cr_sws = 1 * r.cr_sws
    cr += cr_sws

    # STARTING FENIX DOWNS
    flag = '-sfd '
    if flag in cr_flags:
        a = sf1(flag)
        cr_sfd = (1 - a / 10) * r.cr_sfd
    else:
        cr_sfd = 1 * r.cr_sfd
    cr += cr_sfd

    # STARTING TOOLS
    flag = '-sto '
    if flag in cr_flags:
        a = sf1(flag)
        cr_sto = (1 - a / 8) * r.cr_sto
    else:
        cr_sto = 1 * r.cr_sto
    cr += cr_sto

    # EQUIPPABLE ITEMS
    if '-ier ' in cr_flags:
        a = sf1('-ier ')
        b = sf2('-ier ')
        cr_eqitems = (1 - (((a + b)/2)/14)) * r.cr_eqitems
    elif '-iebr ' in cr_flags:
        a = sf1('-iebr ')
        cr_eqitems = (1 - (a/14)) * r.cr_eqitems
    elif '-ieor ' in cr_flags:
        a = sf1('-ieor ')
        cr_eqitems = ((100 - a)/200) * r.cr_eqitems
    elif '-iesr ' in cr_flags:
        a = sf1('-iesr ')
        cr_eqitems = ((100 - a)/200) * r.cr_eqitems
    else:
        cr_eqitems = .149 * r.cr_eqitems
    cr += cr_eqitems

    # EQUIPPABLE RELICS
    if '-ierr ' in cr_flags:
        a = sf1('-ierr ')
        b = sf2('-ierr ')
        cr_eqrelics = (1 - (((a + b)/2)/14)) * r.cr_eqrelics
    elif '-ierbr ' in cr_flags:
        a = sf1('-ierbr ')
        cr_eqrelics = (1 - (a/14)) * r.cr_eqrelics
    elif '-ieror ' in cr_flags:
        a = sf1('-ieror ')
        cr_eqrelics = ((100 - a)/200) * r.cr_eqrelics
    elif '-iersr ' in cr_flags:
        a = sf1('-iersr ')
        cr_eqrelics = ((100 - a)/200) * r.cr_eqrelics
    else:
        cr_eqrelics = .149 * r.cr_eqrelics
    cr += cr_eqrelics

    # CURSED SHIELD BATTLES
    flag = '-csb '
    if flag in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_csb = (math.log((a + b)/2)/math.log(256)) * r.cr_csb
    else:
        cr_csb = 1 * r.cr_csb
    cr += cr_csb

    # MOOGLE CHARM ALL
    flag = '-mca '
    if flag in cr_flags:
        cr_mca = 0 * r.cr_mca
    else:
        cr_mca = 1 * r.cr_mca
    cr += cr_mca

    # STRONGER ATMA WEAPON
    flag = '-saw '
    if flag in cr_flags:
        cr_saw = 0 * r.cr_saw
    else:
        cr_saw = 1 * r.cr_saw
    cr += cr_saw

    # SHOP INVENTORY
    if '-sisr ' in cr_flags:
        a = sf1('-sisr ')
        cr_shopinv = (.6 * (1 - (a/100))) * r.cr_shopinv
    elif '-sirt ' in cr_flags:
        cr_shopinv = .54 * r.cr_shopinv
    elif '-sie ' in cr_flags:
        cr_shopinv = r.cr_shopinv
    else:
        cr_shopinv = .6 * r.cr_shopinv
    cr += cr_shopinv

    # SHOP PRICES
    if '-sprv ' in cr_flags:
        a = sf1('-sprv ')
        b = sf2('-sprv ')
        cr_shopprice = (.25 * ((math.log(a + b / 2) + 1)/math.log(65536))) * r.cr_shopprice
    elif '-sprp ' in cr_flags:
        a = sf1('-sprp ')
        b = sf2('-sprp ')
        cr_shopprice = (((a + b) / 2) / 200) * r.cr_shopprice
    else:
        cr_shopprice = .5 * r.cr_shopprice
    cr += cr_shopprice

    # SELL PRICES
    if '-ssf4 ' in cr_flags:
        cr_sellp = .25 * r.cr_sellp
    elif '-ssf8 ' in cr_flags:
        cr_sellp = .5 * r.cr_sellp
    elif '-ssf0 ' in cr_flags:
        cr_sellp = 1 * r.cr_sellp
    else:
        cr_sellp = 0 * r.cr_sellp
    cr += cr_sellp

    # DRIED MEAT
    flag = '-sdm '
    if '-sdm 0' in cr_flags:
        cr_sdm = 16
    elif flag in cr_flags:
        a = sf1(flag)
        cr_sdm = (1 - (a/5)) * r.cr_sdm
    else:
        cr_sdm = 0 * r.cr_sdm
    cr += cr_sdm

    # NO PRICELESS ITEMS
    flag = '-npi '
    if flag in cr_flags:
        cr_npi = 1 * r.cr_npi
    else:
        cr_npi = 0 * r.cr_npi
    cr += cr_npi

    # NO BREAKABLE RODS
    flag = '-snbr '
    if flag in cr_flags:
        cr_snbr = 1 * r.cr_snbr
    else:
        cr_snbr = 0 * r.cr_snbr
    cr += cr_snbr

    # NO ELEMENTAL SHIELDS
    flag = '-snes '
    if flag in cr_flags:
        cr_snes = 1 * r.cr_snes
    else:
        cr_snes = 0 * r.cr_snes
    cr += cr_snes

    # NO SUPER BALLS
    flag = '-snsb '
    if flag in cr_flags:
        cr_snsb = 1 * r.cr_snsb
    else:
        cr_snsb = 0 * r.cr_snsb
    cr += cr_snsb

    # CHEST CONTENTS
    if '-ccsr ' in cr_flags:
        a = sf1('-ccsr ')
        cr_ccontents = (.6 * (1 - (a / 100))) * r.cr_ccontents
    elif '-ccrt ' in cr_flags:
        cr_ccontents = .54 * r.cr_ccontents
    elif '-cce ' in cr_flags:
        cr_ccontents = 1 * r.cr_ccontents
    else:
        cr_ccontents = .2 * r.cr_ccontents
    cr += cr_ccontents

    # SHUFFLE MIAB
    flag = '-cms '
    if flag in cr_flags:
        cr_cms = 1 * r.cr_cms
    else:
        cr_cms = 0 * r.cr_cms
    cr += cr_cms

    # COLISEUM OPPONENTS
    if '-cos ' in cr_flags:
        cr_col = .5 * r.cr_col
    elif '-cor ' in cr_flags:
        cr_col = 0 * r.cr_col
    else:
        cr_col = 1 * r.cr_col
    cr += cr_col

    # COLISEUM REWARDS
    if '-crs ' in cr_flags:
        cr_crew = .5 * r.cr_crew
    elif '-crr ' in cr_flags:
        cr_crew = 0 * r.cr_crew
    else:
        cr_crew = 1 * r.cr_crew
    cr += cr_crew

    # COLISEUM REWARDS VISIBLE
    flag = '-crvr '
    if flag in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_crv = (1 - (((a + b)/2)/255)) * r.cr_crvr
    else:
        cr_crv = 0 * r.cr_crvr
    cr += cr_crv

    # COLISEUM REWARDS MENU
    flag = '-crm '
    if flag in cr_flags:
        cr_crm = 0 * r.cr_crm
    else:
        cr_crm = 1 * r.cr_crm
    cr += cr_crm

    # RANDOMIZE AUTION HOUSE ITEMS
    flag = '-ari '
    if flag in cr_flags:
        cr_ari = 0 * r.cr_ari
    else:
        cr_ari = 1 * r.cr_ari
    cr += cr_ari

    # DOOR ESPER HINT
    flag = '-adeh '
    if flag in cr_flags:
        cr_adeh = 0 * r.cr_adeh
    else:
        cr_adeh = 1 * r.cr_adeh
    cr += cr_adeh

    # NO MOOGLE CHARMS
    flag = '-nmc '
    if flag in cr_flags and cr_smc == 0:
        cr_nmc = 16
    elif flag in cr_flags:
        cr_nmc = 1 * r.cr_nmc
    else:
        cr_nmc = 0 * r.cr_nmc
    cr += cr_nmc

    # NO EXPERIENCE EGGS
    flag = '-nee '
    if flag in cr_flags:
        cr_nee = 1 * r.cr_nee
    else:
        cr_nee = 0 * r.cr_nee
    cr += cr_nee

    # NO ILLUMINAS
    flag = '-nil '
    if flag in cr_flags:
        cr_nil = 1 * r.cr_nil
    else:
        cr_nil = 0 * r.cr_nil
    cr += cr_nil

    # NO FREE PALADIN SHIELDS
    flag = '-nfps '
    if flag in cr_flags:
        cr_nfps = 1 * r.cr_nfps
    else:
        cr_nfps = 0 * r.cr_nfps
    cr += cr_nfps

    # NO ULTIMA
    flag = '-nu '
    if flag in cr_flags:
        cr_nu = 1 * r.cr_nu
    else:
        cr_nu = 0 * r.cr_nu
    cr += cr_nu

    # NO FREE PROGRESSION
    flag = '-nfp '
    if flag not in cr_flags:
        cr_nfp = 1 * r.cr_nfp
    else:
        cr_nfp = 0 * r.cr_nfp
    cr += cr_nfp

    # HIDDEN REQUIREMENTS
    flag = '-kthr '
    if flag in cr_flags:
        cr_kthr = 1 * r.cr_kthr
    else:
        cr_kthr = 0 * r.cr_kthr
    cr += cr_kthr

    # PERMADEATH
    flag = '-pd '
    if flag in cr_flags:
        cr_pd = 1 * r.cr_pd
    else:
        cr_pd = 0 * r.cr_pd
    cr += cr_pd

    # ORIGINAL NAME DISPLAY
    flag = '-ond '
    if flag not in cr_flags:
        cr_ond = 1 * r.cr_ond
    else:
        cr_ond = 0 * r.cr_ond
    cr += cr_ond

    # RANDOMIZE RNG
    flag = '-rr '
    if flag in cr_flags:
        cr_rr = 1 * r.cr_rr
    else:
        cr_rr = 0 * r.cr_rr
    cr += cr_rr

    # SCAN ALL
    flag = '-scan '
    if flag not in cr_flags:
        cr_scan = 1 * r.cr_scan
    else:
        cr_scan = 0 * r.cr_scan
    cr += cr_scan

    # EVENT TIMERS
    flag = '-etn '
    if flag in cr_flags:
        cr_et = 0 * r.cr_et
    else:
        cr_et = 1 * r.cr_et
    cr += cr_et

    # FIX EVADE
    flag = '-fe '
    if flag in cr_flags:
        cr_fe = 1 * r.cr_fe
    else:
        cr_fe = 0 * r.cr_fe
    cr += cr_fe

    # FIX VANISH DOOM
    flag = '-fvd '
    if flag in cr_flags:
        cr_fvd = 1 * r.cr_fvd
    else:
        cr_fvd = 0 * r.cr_fvd
    cr += cr_fvd

    # FIX RETORT
    flag = '-fr '
    if flag in cr_flags:
        cr_fr = 1 * r.cr_fr
    else:
        cr_fr = 0 * r.cr_fr
    cr += cr_fr

    # FIX BOSS SKIP
    flag = '-fbs '
    if flag in cr_flags:
        cr_fbs = 1 * r.cr_fbs
    else:
        cr_fbs = 0 * r.cr_fbs
    cr += cr_fbs

    # FIX ENEMY DAMAGE COUNTER
    flag = '-fedc '
    if flag not in cr_flags:
        cr_fedc = 1 * r.cr_fedc
    else:
        cr_fedc = 0 * r.cr_fedc
    cr += cr_fedc

    # print("Rating: ", cr)
    # print("eel:", cr_eel)
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


def get_chaos_cr():
    cr_flags = chaos()

    def sf1(f):
        f1 = float(cr_flags.split(f, 1)[1].split(' ', 1)[0])
        return f1

    def sf2(f):
        f2 = float(cr_flags.split(f, 1)[1].split(' ', 1)[1].split(' ', 1)[0])
        return f2

    cr = 0

    # GAME MODE
    flag = '-ow '
    if flag in cr_flags:
        cr_gm = 0 * r.cr_gm
    else:
        cr_gm = 1 * r.cr_gm
    cr += cr_gm

    # SPOILER LOG
    flag = '-sl '
    if flag not in cr_flags:
        cr_sl = 1 * r.cr_sl
    else:
        cr_sl = 0 * r.cr_sl
    cr += cr_sl

    # KEFKA'S TOWER CHARACTER REQUIREMENT
    flag = 'ktcr '
    a = sf1(flag)
    b = sf2(flag)
    cr_ktc = ((((a + b) / 2) - 3) / 11) * r.cr_ktcr
    cr += cr_ktc

    # KEFKA'S TOWER ESPER REQUIREMENT
    flag = 'kter '
    a = sf1(flag)
    b = sf2(flag)
    cr_kte = (((a + b) / 2) / 27) * r.cr_kter
    cr += cr_kte

    # KEFKA'S TOWER DRAGON REQUIREMENT
    flag = 'ktdr '
    a = sf1(flag)
    b = sf2(flag)
    cr_ktd = (((a + b) / 2) / 8) * r.cr_ktdr
    cr += cr_ktd

    # STATUE SKIP ---- ASK DOCTORDT ABOUT THIS ONE
    flag = 'stno '
    if flag in cr_flags:
        cr_stno = 1 * r.cr_stno
    else:
        cr_stno = 0 * r.cr_stno
    cr += cr_stno

    # SKIP CHARACTER REQUIREMENT
    flag = '-stcr '
    if '-stno ' not in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_stc = ((((a + b) / 2) - 3) / 11) * r.cr_stcr
    else:
        cr_stc = 0 * r.cr_stcr
    cr += cr_stc

    # SKIP ESPER REQUIREMENT
    flag = '-ster '
    if '-stno ' not in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_ste = (((a + b) / 2) / 27) * r.cr_ster
    else:
        cr_ste = 0
    cr += cr_ste

    # SKIP DRAGON REQUIREMENT
    flag = '-stdr '
    if '-stno ' not in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_std = (((a + b) / 2) / 8) * r.cr_stdr
    else:
        cr_std = 0
    cr += cr_std

    # STARTING CHARACTERS
    flag = '-sc2 '
    if flag not in cr_flags:
        cr_sc2 = 1 * r.cr_sc2
    else:
        cr_sc2 = 0 * r.cr_sc2
    cr += cr_sc2

    flag = '-sc3 '
    if flag not in cr_flags:
        cr_sc3 = 1 * r.cr_sc3
    else:
        cr_sc3 = 0 * r.cr_sc3
    cr += cr_sc3

    flag = '-sc4 '
    if flag not in cr_flags:
        cr_sc4 = 1 * r.cr_sc4
    else:
        cr_sc4 = 0 * r.cr_sc4
    cr += cr_sc4

    # START AVERAGE LEVEL
    flag = '-sal '
    if flag not in cr_flags:
        cr_sal = 1 * r.cr_sal
    else:
        cr_sal = 0 * r.cr_sal
    cr += cr_sal

    # START NAKED
    flag = '-sn '
    if flag in cr_flags:
        cr_sn = 1 * r.cr_sn
    else:
        cr_sn = 0 * r.cr_sn
    cr += cr_sn

    # EQUIPPABLE UMARO
    flag = '-eu '
    if flag not in cr_flags:
        cr_eu = 1 * r.cr_eu
    else:
        cr_eu = 0 * r.cr_eu
    cr += cr_eu

    # CHARACTER STATS
    flag = '-csrp '
    if flag in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_csrp = (2 - (((a + b) / 2) / 200)) * r.cr_csrp
    else:
        cr_csrp = (2 - ((100 / 200) * 2)) * r.cr_csrp
    cr += cr_csrp

    # SWORDTECH EVERYONE LEARNS
    flag = '-sel '
    if flag not in cr_flags:
        cr_sel = 1 * r.cr_sel
    else:
        cr_sel = 0 * r.cr_sel
    cr += cr_sel

    # BUM RUSH LAST
    flag = '-brl '
    if flag not in cr_flags:
        cr_brl = 0 * r.cr_brl
    else:
        cr_brl = 1 * r.cr_brl
    cr += cr_brl

    # BLITZ EVERYONE LEARNS
    flag = '-bel '
    if flag not in cr_flags:
        cr_bel = 1 * r.cr_bel
    else:
        cr_bel = 0 * r.cr_bel
    cr += cr_bel

    # STARTING LORES
    flag = '-slr '
    if flag in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_slr = (2 - (((a + b) / 2) / 24)) * r.cr_slr
    else:
        cr_slr = (2 - (((3 + 3) / 2) / 24)) * r.cr_slr
    cr = cr + cr_slr

    # LORE MP
    if '-lmps ' in cr_flags:
        cr_loremp = 0.175 * r.cr_loremp
    elif '-lmprv ' in cr_flags:
        a = sf1('-lmprv ')
        b = sf2('-lmprv ')
        cr_loremp = (2 - (((a + b) / 2) / 99)) * r.cr_loremp
    elif '-lmprp ' in cr_flags:
        a = sf1('-lmprp ')
        b = sf2('-lmprp ')
        cr_loremp = (2 - (((a + b) / 2) / 200)) * r.cr_loremp
    else:
        cr_loremp = 0.35 * r.cr_loremp
    cr += cr_loremp

    # LORE EVERYONE LEARNS
    flag = '-lel '
    if flag not in cr_flags:
        cr_lel = 1 * r.cr_lel
    else:
        cr_lel = 0 * r.cr_lel
    cr += cr_lel

    # STARTING RAGES
    flag = '-srr '
    if flag in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_srr = (2 - ((1 - (a + b) / 2) / 255)) * r.cr_srr
    else:
        cr_srr = (1 - (9 / 255)) * r.cr_srr
    cr += cr_srr

    # NO CHARM
    flag = '-rnc '
    if flag in cr_flags:
        cr_rnc = 1 * r.cr_rnc
    else:
        cr_rnc = 0 * r.cr_rnc
    cr += cr_rnc

    # STARTING DANCES
    flag = '-sdr '
    if flag in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_sdr = (1 - (((a + b) / 2) / 8)) * r.cr_sdr
    else:
        cr_sdr = 0 * r.cr_sdr
    cr += cr_sdr

    # DANCE ABILITY SHUFFLE
    flag = '-das '
    if flag not in cr_flags:
        cr_das = 1 * r.cr_das
    else:
        cr_das = 0 * r.cr_das
    cr += cr_das

    # DISPLAY DANCE ABILITY NAMES
    flag = '-dda '
    if flag not in cr_flags:
        cr_dda = 1 * r.cr_dda
    else:
        cr_dda = 0 * r.cr_dda
    cr += cr_dda

    # DANCE NO STUMBLE
    flag = '-dns '
    if flag not in cr_flags:
        cr_dns = 1 * r.cr_dns
    else:
        cr_dns = 0 * r.cr_dns
    cr += cr_dns

    # DANCE EVERYONE LEARNS
    flag = '-del '
    if flag not in cr_flags:
        cr_del = 1 * r.cr_del
    else:
        cr_del = 0 * r.cr_del
    cr += cr_del

    # COMMANDS ----- Talk to Doc about the CR mod for these
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
        cr_com = (skills[com1] + skills[com2] + skills[com3] + skills[com4] + skills[com5] + skills[com6] + skills[com7] \
             + skills[com8] + skills[com9] + skills[com10] + skills[com11] + skills[com12] + skills[com13]) * r.cr_com
    else:
        cr_com = 6.6 * r.cr_com
    cr += cr_com

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
    flag = '-xpm '
    if '-xpm 0' in cr_flags:
        cr_xpm = 80
    elif flag not in cr_flags:
        cr_xpm = 1 * r.cr_xpm
    else:
        cr_xpm = ((1 - math.sqrt(math.log(int(cr_flags.split('-xpm ', 1)[1].split(' ', 1)[0]))/math.log(255))) *
                  (r.cr_xpm / 2))
    cr += cr_xpm

    # MP MODIFIER
    flag = '-mpm '
    if flag not in cr_flags:
        cr_mpm = 1 * r.cr_mpm
    else:
        cr_mpm = ((1 - math.sqrt(math.log(int(cr_flags.split('-mpm ', 1)[1].split(' ', 1)[0]))/math.log(255)))*r.cr_mpm)
    cr += cr_mpm

    # GP MODIFIER
    flag = '-gpm '
    if flag not in cr_flags:
        cr_gpm = 1 * r.cr_mpm
    else:
        cr_gpm = ((1 - math.sqrt(math.log(int(cr_flags.split('-gpm ', 1)[1].split(' ', 1)[0]))/math.log(255)))*r.cr_gpm)
    cr += cr_gpm

    # NO PARTY EXP SPLIT
    flag = '-nxppd '
    if flag not in cr_flags:
        cr_nxppd = 1 * r.cr_nxppd
    else:
        cr_nxppd = 0 * r.cr_nxppd
    cr += cr_nxppd

    # LEVEL SCALING
    if '-lsa' in cr_flags:
        cr_ls = (.9 * (float(cr_flags.split('-lsa ', 1)[1].split(' ', 1)[0]))/5) * r.cr_ls
    elif 'lsh' in cr_flags:
        cr_ls = (1 * (float(cr_flags.split('-lsh ', 1)[1].split(' ', 1)[0])) / 5) * r.cr_ls
    elif 'lsp' in cr_flags:
        cr_ls = (.8 * (float(cr_flags.split('-lsp ', 1)[1].split(' ', 1)[0])) / 5) * r.cr_ls
    elif 'lst' in cr_flags:
        cr_ls = (.7 * (1 - (float(cr_flags.split('-lst ', 1)[1].split(' ', 1)[0])) / 5)) * r.cr_ls
    else:
        cr_ls = 0.2 * r.cr_ls
    cr += cr_ls

    # HP/MP SCALING
    if '-hma' in cr_flags:
        cr_hs = (.9 * (float(cr_flags.split('-hma ', 1)[1].split(' ', 1)[0]))/5) * r.cr_hs
    elif 'hmh' in cr_flags:
        cr_hs = (1 * (float(cr_flags.split('-hmh ', 1)[1].split(' ', 1)[0])) / 5) * r.cr_hs
    elif 'hmp' in cr_flags:
        cr_hs = (.8 * (float(cr_flags.split('-hmp ', 1)[1].split(' ', 1)[0])) / 5) * r.cr_hs
    elif 'hmt' in cr_flags:
        cr_hs = (.7 * (1 - (float(cr_flags.split('-hmt ', 1)[1].split(' ', 1)[0])) / 5)) * r.cr_hs
    else:
        cr_hs = 0.2 * r.cr_hs
    cr += cr_hs

    # EXP/GP SCALING
    if '-xga' in cr_flags:
        cr_xgp = (.9 * (1 - (float(cr_flags.split('-xga ', 1)[1].split(' ', 1)[0]))/5)) * r.cr_xgp
    elif 'xgh' in cr_flags:
        cr_xgp = (.8 * (1 - (float(cr_flags.split('-xgh ', 1)[1].split(' ', 1)[0])) / 5)) * r.cr_xgp
    elif 'xgp' in cr_flags:
        cr_xgp = (1 - (.8 * (float(cr_flags.split('-xgp ', 1)[1].split(' ', 1)[0])) / 5)) * r.cr_xgp
    elif 'xgt' in cr_flags:
        cr_xgp = (.7 * (float(cr_flags.split('-xgt ', 1)[1].split(' ', 1)[0])) / 5) * r.cr_xgp
    else:
        cr_xgp = 0.2 * r.cr_xgp
    cr += cr_xgp

    # ABILITY SCALING
    if '-ase' in cr_flags:
        cr_as = (.6 * (1 - (float(cr_flags.split('-ase ', 1)[1].split(' ', 1)[0]))/5)) * r.cr_as
    elif '-asr' in cr_flags:
        cr_as = (1 * (1 - (float(cr_flags.split('-asr ', 1)[1].split(' ', 1)[0])) / 5)) * r.cr_as
    else:
        cr_as = 0.8 * r.cr_as
    cr += cr_as

    # MAX SCALE LEVEL ----- Another one that's close but not close enough - must be the logs
    flag = '-msl '
    if flag in cr_flags:
        cr_msl = (((math.log(float(cr_flags.split('-msl ', 1)[1].split(' ', 1)[0])))/math.log(99-2))**6) * r.cr_msl
    else:
        cr_msl = 0 * r.cr_msl
    cr += cr_msl

    # EXTRA ENEMY LEVELS ----- Another one that's close but not close enough - must be the logs
    flag = '-eel '
    if flag in cr_flags and '-eel 0' not in cr_flags:
        cr_eel = (((math.log(float(cr_flags.split('-eel ', 1)[1].split(' ', 1)[0])))/math.log(99+1))**2) * r.cr_eel
    else:
        cr_eel = 0 * r.cr_eel
    cr += cr_eel

    # SCALE FINAL BOSS
    flag = '-sfb '
    if flag in cr_flags:
        cr_sfb = (min([cr_msl/4, cr_eel/4])) * r.cr_sfb
    else:
        cr_sfb = (min(.4 + cr_eel/4, 1)) * r.cr_sfb
    cr += cr_sfb

    # SCALE EIGHT DRAGONS
    flag = '-sed '
    if flag in cr_flags:
        cr_sed = (min([cr_msl/4, cr_eel/4])) * r.cr_sed
    else:
        cr_sed = (min(.4 + cr_eel/4, 1)) * r.cr_sed
    cr += cr_sed

    # BOSS BATTLES
    if '-bbs' in cr_flags:
        cr_bb = 0.5 * r.cr_bb
    elif '-bbr' in cr_flags:
        cr_bb = 1 * r.cr_bb
    else:
        cr_bb = 0 * r.cr_bb
    cr += cr_bb

    # MIX BOSSES AND DRAGONS
    flag = '-bmbd '
    if flag in cr_flags:
        cr_bmbd = 1 * r.cr_bmbd
    else:
        cr_bmbd = 0 * r.cr_bmbd
    cr += cr_bmbd

    # SHUFFLE PHUNBABA3
    flag = 'srp3 '
    if flag in cr_flags:
        cr_srp3 = 1 * r.cr_srp3
    else:
        cr_srp3 = 0 * r.cr_srp3
    cr += cr_srp3

    # NORMALIZE & DISTORT
    flag = '-bnds '
    if flag in cr_flags:
        cr_bnds = 1 * r.cr_bnds
    else:
        cr_bnds = 0 * r.cr_bnds
    cr += cr_bnds

    # BOSS EXPERIENCE
    flag = '-be '
    if flag not in cr_flags:
        cr_be = 1 * r.cr_be
    else:
        cr_be = 0 * r.cr_be
    cr += cr_be

    # NO UNDEAD BOSSES
    flag = '-bnu '
    if flag in cr_flags:
        cr_bnu = 1 * r.cr_bnu
    else:
        cr_bnu = 0 * r.cr_bnu
    cr += cr_bnu

    # RANDOM ENCOUNTERS
    if '-res ' in cr_flags:
        cr_renc = .2 * r.cr_renc
    elif '-rer ' in cr_flags:
        cr_renc = (.2 + (1 - .2)*(float(cr_flags.split('-rer ', 1)[1].split(' ', 1)[0]))/100) * r.cr_renc
    else:
        cr_renc = 0 * r.cr_renc
    cr += cr_renc

    # FIXED ENCOUNTERS
    flag = '-fer '
    if flag in cr_flags:
        cr_fenc = (.25 + ((float(cr_flags.split('-fer ', 1)[1].split(' ', 1)[0]))/100)*(1 - .25)) * r.cr_fenc
    else:
        cr_fenc = 0 * r.cr_fenc
    cr += cr_fenc

    # ESCAPABLE BATTLES
    flag = '-escr '
    if flag in cr_flags and float(cr_flags.split('-escr ', 1)[1].split(' ', 1)[0]) > 0:
        cr_escr = (1-float(cr_flags.split('-escr ', 1)[1].split(' ', 1)[0])/100) * r.cr_escr
    else:
        cr_escr = 0 * r.cr_escr
    cr += cr_escr

    # DOOMGAZE NO ESCAPE
    flag = '-dgne '
    if flag not in cr_flags:
        cr_dgne = 1 * r.cr_dgne
    else:
        cr_dgne = 0 * r.cr_dgne
    cr += cr_dgne

    # WREXSOUL NO ZINGER
    flag = '-wnz '
    if flag not in cr_flags:
        cr_wnz = 1 * r.cr_wnz
    else:
        cr_wnz = 0 * r.cr_wnz
    cr += cr_wnz

    # MAGIMASTER NO ULTIMA
    flag = '-mmnu '
    if flag not in cr_flags:
        cr_mmnu = 1 * r.cr_mmnu
    else:
        cr_mmnu = 0 * r.cr_mmnu
    cr += cr_mmnu

    # CHADARNOOK MORE LIKE BADARNOOK
    flag = '-cmd '
    if flag not in cr_flags:
        cr_cmd = 1 * r.cr_cmd
    else:
        cr_cmd = 0 * r.cr_cmd
    cr += cr_cmd

    # ESPER SPELLS
    if '-esrr ' in cr_flags:
        cr_espells = .222 * r.cr_espells
    elif '-ess ' in cr_flags:
        cr_espells = .326 * r.cr_espells
    elif '-essrr ' in cr_flags:
        cr_espells = .222 * r.cr_espells
    elif '-esr ' in cr_flags:
        cr_espells = (1 - (((float(cr_flags.split('-esr ', 1)[1].split(' ', 1)[0])) +
                        (float(cr_flags.split('-esr ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])))/2)/5) * r.cr_espells
    elif '-esrt ' in cr_flags:
        cr_espells = .6 * r.cr_espells
    else:
        cr_espells = 0.326 * r.cr_espells
    cr += cr_espells

    # ESPER BONUSES
    if '-ebs ' in cr_flags:
        cr_ebonus = .333 * r.cr_ebonus
    elif '-ebr ' in cr_flags:
        cr_ebonus = (1 - ((float(cr_flags.split('-ebr ', 1)[1].split(' ', 1)[0]))/100)) * r.cr_ebonus
    else:
        cr_ebonus = .333 * r.cr_ebonus
    cr += cr_ebonus

    # ESPER MP
    if '-emps ' in cr_flags:
        cr_emp = .4 * r.cr_emp
    elif '-emprv ' in cr_flags:
        cr_emp = ((((float(cr_flags.split('-emprv ', 1)[1].split(' ', 1)[0])) +
                       (float(cr_flags.split('-emprv ', 1)[1].split(' ', 1)[1].split(' ', 1)[0])))/2)/128) * r.cr_emp
    elif '-emprp ' in cr_flags:
        cr_emp = (.773 * ((((float(cr_flags.split('-emprp ', 1)[1].split(' ', 1)[0])) +
                       (float(cr_flags.split('-emprp ', 1)[1].split(' ', 1)[1].split(' ', 1)[0]))) / 2) / 200)) * r.cr_emp
    else:
        cr_emp = .388 * r.cr_emp
    cr += cr_emp

    # EQUIPPABLE ESPERS
    if '-eer ' in cr_flags:
        a = sf1('-eer ')
        b = sf2('-eer ')
        cr_eqes = (1 - (((a+b)/2)/12)) * r.cr_eqes
    elif '-eebr ' in cr_flags:
        cr_eqes = (.9 * (1 - (float(cr_flags.split('-eebr ', 1)[1].split(' ', 1)[0]))/12)) * r.cr_eqes
    else:
        cr_eqes = 0 * r.cr_eqes
    cr += cr_eqes

    # MULTI-SUMMON
    flag = '-ems '
    if flag in cr_flags:
        cr_ems = 0 * r.cr_ems
    else:
        cr_ems = 1 * r.cr_ems
    cr += cr_ems

    # NATURAL MAGIC
    flag = '-nm1 '
    if flag in cr_flags:
        cr_nm1 = 0 * r.cr_nm1
    else:
        cr_nm1 = 1 * r.cr_nm1
    cr += cr_nm1

    flag = '-nm2 '
    if flag in cr_flags:
        cr_nm2 = 0 * r.cr_nm2
    else:
        cr_nm2 = 1 * r.cr_nm2
    cr += cr_nm2

    # STARTING GP ----- Talk with Doc about this. Any extra GP should actually LOWER the difficulty, not raise it.
    flag = '-gp '
    if flag in cr_flags:
        a = sf1(flag)
        cr_gp = (1 - ((math.log(a+1)/math.log(999999))**3)) * r.cr_gp
    else:
        cr_gp = 1 * r.cr_gp
    cr += cr_gp

    # STARTING MOOGLE CHARMS
    flag = '-smc '
    if flag in cr_flags:
        a = sf1(flag)
        if a == 0:
            cr_smc = 1 * r.cr_smc
        else:
            cr_smc = (.1 * (3 - a)) * r.cr_smc
    else:
        cr_smc = 1 * r.cr_smc
    cr += cr_smc

    # STARTING WARP STONES
    flag = '-sws '
    if flag in cr_flags:
        a = sf1(flag)
        cr_sws = (1 - math.log(a+1)/math.log(11)) * r.cr_sws
    else:
        cr_sws = 1 * r.cr_sws
    cr += cr_sws

    # STARTING FENIX DOWNS
    flag = '-sfd '
    if flag in cr_flags:
        a = sf1(flag)
        cr_sfd = (1 - a / 10) * r.cr_sfd
    else:
        cr_sfd = 1 * r.cr_sfd
    cr += cr_sfd

    # STARTING TOOLS
    flag = '-sto '
    if flag in cr_flags:
        a = sf1(flag)
        cr_sto = (1 - a / 8) * r.cr_sto
    else:
        cr_sto = 1 * r.cr_sto
    cr += cr_sto

    # EQUIPPABLE ITEMS
    if '-ier ' in cr_flags:
        a = sf1('-ier ')
        b = sf2('-ier ')
        cr_eqitems = (1 - (((a + b)/2)/14)) * r.cr_eqitems
    elif '-iebr ' in cr_flags:
        a = sf1('-iebr ')
        cr_eqitems = (1 - (a/14)) * r.cr_eqitems
    elif '-ieor ' in cr_flags:
        a = sf1('-ieor ')
        cr_eqitems = ((100 - a)/200) * r.cr_eqitems
    elif '-iesr ' in cr_flags:
        a = sf1('-iesr ')
        cr_eqitems = ((100 - a)/200) * r.cr_eqitems
    else:
        cr_eqitems = .149 * r.cr_eqitems
    cr += cr_eqitems

    # EQUIPPABLE RELICS
    if '-ierr ' in cr_flags:
        a = sf1('-ierr ')
        b = sf2('-ierr ')
        cr_eqrelics = (1 - (((a + b)/2)/14)) * r.cr_eqrelics
    elif '-ierbr ' in cr_flags:
        a = sf1('-ierbr ')
        cr_eqrelics = (1 - (a/14)) * r.cr_eqrelics
    elif '-ieror ' in cr_flags:
        a = sf1('-ieror ')
        cr_eqrelics = ((100 - a)/200) * r.cr_eqrelics
    elif '-iersr ' in cr_flags:
        a = sf1('-iersr ')
        cr_eqrelics = ((100 - a)/200) * r.cr_eqrelics
    else:
        cr_eqrelics = .149 * r.cr_eqrelics
    cr += cr_eqrelics

    # CURSED SHIELD BATTLES
    flag = '-csb '
    if flag in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_csb = (math.log((a + b)/2)/math.log(256)) * r.cr_csb
    else:
        cr_csb = 1 * r.cr_csb
    cr += cr_csb

    # MOOGLE CHARM ALL
    flag = '-mca '
    if flag in cr_flags:
        cr_mca = 0 * r.cr_mca
    else:
        cr_mca = 1 * r.cr_mca
    cr += cr_mca

    # STRONGER ATMA WEAPON
    flag = '-saw '
    if flag in cr_flags:
        cr_saw = 0 * r.cr_saw
    else:
        cr_saw = 1 * r.cr_saw
    cr += cr_saw

    # SHOP INVENTORY
    if '-sisr ' in cr_flags:
        a = sf1('-sisr ')
        cr_shopinv = (.6 * (1 - (a/100))) * r.cr_shopinv
    elif '-sirt ' in cr_flags:
        cr_shopinv = .54 * r.cr_shopinv
    elif '-sie ' in cr_flags:
        cr_shopinv = r.cr_shopinv
    else:
        cr_shopinv = .6 * r.cr_shopinv
    cr += cr_shopinv

    # SHOP PRICES
    if '-sprv ' in cr_flags:
        a = sf1('-sprv ')
        b = sf2('-sprv ')
        cr_shopprice = (.25 * ((math.log(a + b / 2) + 1)/math.log(65536))) * r.cr_shopprice
    elif '-sprp ' in cr_flags:
        a = sf1('-sprp ')
        b = sf2('-sprp ')
        cr_shopprice = (((a + b) / 2) / 200) * r.cr_shopprice
    else:
        cr_shopprice = .5 * r.cr_shopprice
    cr += cr_shopprice

    # SELL PRICES
    if '-ssf4 ' in cr_flags:
        cr_sellp = .25 * r.cr_sellp
    elif '-ssf8 ' in cr_flags:
        cr_sellp = .5 * r.cr_sellp
    elif '-ssf0 ' in cr_flags:
        cr_sellp = 1 * r.cr_sellp
    else:
        cr_sellp = 0 * r.cr_sellp
    cr += cr_sellp

    # DRIED MEAT
    flag = '-sdm '
    if '-sdm 0' in cr_flags:
        cr_sdm = 16
    elif flag in cr_flags:
        a = sf1(flag)
        cr_sdm = (1 - (a/5)) * r.cr_sdm
    else:
        cr_sdm = 0 * r.cr_sdm
    cr += cr_sdm

    # NO PRICELESS ITEMS
    flag = '-npi '
    if flag in cr_flags:
        cr_npi = 1 * r.cr_npi
    else:
        cr_npi = 0 * r.cr_npi
    cr += cr_npi

    # NO BREAKABLE RODS
    flag = '-snbr '
    if flag in cr_flags:
        cr_snbr = 1 * r.cr_snbr
    else:
        cr_snbr = 0 * r.cr_snbr
    cr += cr_snbr

    # NO ELEMENTAL SHIELDS
    flag = '-snes '
    if flag in cr_flags:
        cr_snes = 1 * r.cr_snes
    else:
        cr_snes = 0 * r.cr_snes
    cr += cr_snes

    # NO SUPER BALLS
    flag = '-snsb '
    if flag in cr_flags:
        cr_snsb = 1 * r.cr_snsb
    else:
        cr_snsb = 0 * r.cr_snsb
    cr += cr_snsb

    # CHEST CONTENTS
    if '-ccsr ' in cr_flags:
        a = sf1('-ccsr ')
        cr_ccontents = (.6 * (1 - (a / 100))) * r.cr_ccontents
    elif '-ccrt ' in cr_flags:
        cr_ccontents = .54 * r.cr_ccontents
    elif '-cce ' in cr_flags:
        cr_ccontents = 1 * r.cr_ccontents
    else:
        cr_ccontents = .2 * r.cr_ccontents
    cr += cr_ccontents

    # SHUFFLE MIAB
    flag = '-cms '
    if flag in cr_flags:
        cr_cms = 1 * r.cr_cms
    else:
        cr_cms = 0 * r.cr_cms
    cr += cr_cms

    # COLISEUM OPPONENTS
    if '-cos ' in cr_flags:
        cr_col = .5 * r.cr_col
    elif '-cor ' in cr_flags:
        cr_col = 0 * r.cr_col
    else:
        cr_col = 1 * r.cr_col
    cr += cr_col

    # COLISEUM REWARDS
    if '-crs ' in cr_flags:
        cr_crew = .5 * r.cr_crew
    elif '-crr ' in cr_flags:
        cr_crew = 0 * r.cr_crew
    else:
        cr_crew = 1 * r.cr_crew
    cr += cr_crew

    # COLISEUM REWARDS VISIBLE
    flag = '-crvr '
    if flag in cr_flags:
        a = sf1(flag)
        b = sf2(flag)
        cr_crv = (1 - (((a + b)/2)/255)) * r.cr_crvr
    else:
        cr_crv = 0 * r.cr_crvr
    cr += cr_crv

    # COLISEUM REWARDS MENU
    flag = '-crm '
    if flag in cr_flags:
        cr_crm = 0 * r.cr_crm
    else:
        cr_crm = 1 * r.cr_crm
    cr += cr_crm

    # RANDOMIZE AUTION HOUSE ITEMS
    flag = '-ari '
    if flag in cr_flags:
        cr_ari = 0 * r.cr_ari
    else:
        cr_ari = 1 * r.cr_ari
    cr += cr_ari

    # DOOR ESPER HINT
    flag = '-adeh '
    if flag in cr_flags:
        cr_adeh = 0 * r.cr_adeh
    else:
        cr_adeh = 1 * r.cr_adeh
    cr += cr_adeh

    # NO MOOGLE CHARMS
    flag = '-nmc '
    if flag in cr_flags and cr_smc == 0:
        cr_nmc = 16
    elif flag in cr_flags:
        cr_nmc = 1 * r.cr_nmc
    else:
        cr_nmc = 0 * r.cr_nmc
    cr += cr_nmc

    # NO EXPERIENCE EGGS
    flag = '-nee '
    if flag in cr_flags:
        cr_nee = 1 * r.cr_nee
    else:
        cr_nee = 0 * r.cr_nee
    cr += cr_nee

    # NO ILLUMINAS
    flag = '-nil '
    if flag in cr_flags:
        cr_nil = 1 * r.cr_nil
    else:
        cr_nil = 0 * r.cr_nil
    cr += cr_nil

    # NO FREE PALADIN SHIELDS
    flag = '-nfps '
    if flag in cr_flags:
        cr_nfps = 1 * r.cr_nfps
    else:
        cr_nfps = 0 * r.cr_nfps
    cr += cr_nfps

    # NO ULTIMA
    flag = '-nu '
    if flag in cr_flags:
        cr_nu = 1 * r.cr_nu
    else:
        cr_nu = 0 * r.cr_nu
    cr += cr_nu

    # NO FREE PROGRESSION
    flag = '-nfp '
    if flag not in cr_flags:
        cr_nfp = 1 * r.cr_nfp
    else:
        cr_nfp = 0 * r.cr_nfp
    cr += cr_nfp

    # HIDDEN REQUIREMENTS
    flag = '-kthr '
    if flag in cr_flags:
        cr_kthr = 1 * r.cr_kthr
    else:
        cr_kthr = 0 * r.cr_kthr
    cr += cr_kthr

    # PERMADEATH
    flag = '-pd '
    if flag in cr_flags:
        cr_pd = 1 * r.cr_pd
    else:
        cr_pd = 0 * r.cr_pd
    cr += cr_pd

    # ORIGINAL NAME DISPLAY
    flag = '-ond '
    if flag not in cr_flags:
        cr_ond = 1 * r.cr_ond
    else:
        cr_ond = 0 * r.cr_ond
    cr += cr_ond

    # RANDOMIZE RNG
    flag = '-rr '
    if flag in cr_flags:
        cr_rr = 1 * r.cr_rr
    else:
        cr_rr = 0 * r.cr_rr
    cr += cr_rr

    # SCAN ALL
    flag = '-scan '
    if flag not in cr_flags:
        cr_scan = 1 * r.cr_scan
    else:
        cr_scan = 0 * r.cr_scan
    cr += cr_scan

    # EVENT TIMERS
    flag = '-etn '
    if flag in cr_flags:
        cr_et = 0 * r.cr_et
    else:
        cr_et = 1 * r.cr_et
    cr += cr_et

    # FIX EVADE
    flag = '-fe '
    if flag in cr_flags:
        cr_fe = 1 * r.cr_fe
    else:
        cr_fe = 0 * r.cr_fe
    cr += cr_fe

    # FIX VANISH DOOM
    flag = '-fvd '
    if flag in cr_flags:
        cr_fvd = 1 * r.cr_fvd
    else:
        cr_fvd = 0 * r.cr_fvd
    cr += cr_fvd

    # FIX RETORT
    flag = '-fr '
    if flag in cr_flags:
        cr_fr = 1 * r.cr_fr
    else:
        cr_fr = 0 * r.cr_fr
    cr += cr_fr

    # FIX BOSS SKIP
    flag = '-fbs '
    if flag in cr_flags:
        cr_fbs = 1 * r.cr_fbs
    else:
        cr_fbs = 0 * r.cr_fbs
    cr += cr_fbs

    # FIX ENEMY DAMAGE COUNTER
    flag = '-fedc '
    if flag not in cr_flags:
        cr_fedc = 1 * r.cr_fedc
    else:
        cr_fedc = 0 * r.cr_fedc
    cr += cr_fedc

    # print("Rating: ", cr)
    # print("eel:", cr_eel)
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
