import random


def standard():
    # -----GAME-----
    # SETTINGS
    mode = random.choices(["-ow", "-cg"], weights=([1, 15]), k=1)[0]
    slog = ''
    settings = ''.join([mode, slog])

    # KEFKA'S TOWER & STATUE SKIP
    ktcr1 = random.randint(3, 7)
    ktcr2 = random.randint(ktcr1, 10)
    kter1 = random.randint(0, 9)
    kter2 = random.randint(kter1, 13)
    ktdr1 = random.randint(0, 1)
    ktdr2 = random.randint(ktdr1, 1)
    stcr1 = random.randint(3, 8)
    stcr2 = random.randint(stcr1, 11)
    ster1 = random.randint(0, 10)
    ster2 = random.randint(ster1, 14)
    stdr1 = random.randint(0, 2)
    stdr2 = random.randint(stdr1, 2)
    stno = random.choices([True, False], weights=([6, 1]), k=1)[0]

    if stno:
        kt = ' '.join([' -ktcr', str(ktcr1), str(ktcr2), '-kter', str(kter1), str(kter2), '-ktdr', str(ktdr1),
                       str(ktdr2), '-stno'])
    else:
        kt = ' '.join([' -ktcr', str(ktcr1), str(ktcr2), '-kter', str(kter1), str(kter2), '-ktdr', str(ktdr1),
                       str(ktdr2), '-stcr', str(stcr1), str(stcr2), '-ster', str(ster1), str(ster2), '-stdr',
                       str(stdr1), str(stdr2)])

    game = ''.join([settings, kt])

    # -----PARTY-----
    # STARTING PARTY
    sc1 = random.choice([' -sc1 random', ' -sc1 randomngu'])
    sc2 = random.choice([' -sc2 random', ' -sc2 randomngu'])
    sc3 = random.choices([' -sc3 random', ' -sc3 randomngu', ''], weights=([1, 1, 5]), k=1)[0]
    sc4 = ""
    sparty = ''.join([sc1, sc2, sc3, sc4])

    # SWORDTECHS
    fst = ' -fst'
    sel = random.choices([' -sel', ''], weights=([1, 5]), k=1)[0]
    swdtech = ''.join([fst, sel])

    # BLITZES
    brl = random.choices([' -brl', ''], weights=([10, 1]), k=1)[0]
    bel = random.choices([' -bel', ''], weights=([1, 10]), k=1)[0]
    blitz = ''.join([brl, bel])

    # LORES
    slr1 = random.randint(0, 7)
    slr2 = random.randint(slr1, 10)
    slrr = ' '.join([' -slr', str(slr1), str(slr2)])
    slr = random.choices([slrr, ''], weights=([10, 1]), k=1)[0]
    lmprp1 = random.randint(0, 100)
    lmprp2 = random.randint(lmprp1, 150)
    lmprv1 = random.randint(0, 40)
    lmprv2 = random.randint(lmprv1, 75)
    lmprp = ' '.join([' -lmprp', str(lmprp1), str(lmprp2)])
    lmprv = ' '.join([' -lmpr', str(lmprv1), str(lmprv2)])
    loremp = random.choices(['', ' -lmps', lmprp, lmprv], weights=([1, 3, 10, 3]), k=1)[0]
    lel = ' -lel'
    lores = ''.join([slr, loremp, lel])

    # RAGES
    srr1 = random.randint(0, 10)
    srr2 = random.randint(srr1, 25)
    srr = ' '.join([' -srr', str(srr1), str(srr2)])
    srages = random.choices(['', srr], weights=([1, 13]), k=1)[0]
    rnl = ' -rnl'
    rnc = random.choices([' -rnc', ''], weights=([15, 1]), k=1)[0]
    rage = ''.join([srages, rnl, rnc])

    # DANCES
    sdr1 = random.randint(0, 2)
    sdr2 = random.randint(sdr1, 4)
    sdr = ' '.join([' -sdr', str(sdr1), str(sdr2)])
    das = ' -das'
    dda = ' -dda'
    dns = ' -dns'
    d_el = ' -del'
    dance = ''.join([sdr, das, dda, dns, d_el])

    # CHARACTERS
    sal = random.choices([' -sal', ''], weights=([13, 1]), k=1)[0]
    sn = random.choices([' -sn', ''], weights=([1, 13]), k=1)[0]
    eu = random.choices([' -eu', ''], weights=([13, 1]), k=1)[0]
    csrp1 = random.randint(90, 120)
    csrp2 = random.randint(csrp1, 130)
    csrp = ' '.join([' -csrp', str(csrp1), str(csrp2)])
    cstats = ''.join([sal, sn, eu, csrp])

    # COMMANDS
    scc = random.choices([' -scc', ''], weights=([1, 10]), k=1)[0]
    com = random.choices([' -com 99999999999999999999999999', '', ' -com 98989898989898989898989898'],
                         weights= ([2, 1, 13]), k=1)[0]
    recskills = ['10', '6', '14', '19', '24', '26', '22', '12', '3', '28', '16', '11', '27', '13', '15', '5',
                 '7', '8', '9', '23']
    rec1 = ' -rec1 28'
    rec2 = ' -rec2 23'
    rec3 = ''
    rec4 = ''
    commands = ''.join([scc, com, rec1, rec2, rec3, rec4])

    party = ''.join([sparty, swdtech, blitz, lores, rage, dance, cstats, commands])

    # -----BATTLE-----
    xpm = ' '.join([' -xpm', str(random.choices([2, 3, 4], weights=([1, 10, 1]), k=1)[0])])
    gpm = ' '.join([' -gpm', str(random.choices([4, 5, 6], weights=([1, 10, 1]), k=1)[0])])
    mpm = ' '.join([' -mpm', str(random.choices([4, 5, 6], weights=([1, 10, 1]), k=1)[0])])
    nxppd = random.choices([' -nxppd', ''], weights=([13, 1]), k=1)[0]
    xpmpgp = ''.join([xpm, gpm, mpm, nxppd])

    # BOSSES
    bb = random.choices([' -bbr', ' -bbs', ''], weights=([1, 13, 1]), k=1)[0]
    bmbd = random.choices([' -bmbd', ''], weights=([0, 1]), k=1)[0]
    srp3 = random.choices([' -srp3', ''], weights=([0, 1]), k=1)[0]
    bnds = random.choices([' -bnds', ''], weights=([1, 13]), k=1)[0]
    be = random.choices([' -be', ''], weights=([1, 0]), k=1)[0]
    bnu = random.choices([' -bnu', ''], weights=([1, 10]), k=1)[0]
    bosses = ''.join([bb, bmbd, srp3, bnds, be, bnu])

    # BOSS AI
    dgne = random.choices([' -dgne', ''], weights=([1, 0]), k=1)[0]
    wnz = random.choices([' -wnz', ''], weights=([1, 0]), k=1)[0]
    mmnu = random.choices([' -mmnu', ''], weights=([1, 0]), k=1)[0]
    cmd = random.choices([' -cmd', ''], weights=([1, 0]), k=1)[0]
    b_ai = ''.join([dgne, wnz, mmnu, cmd])

    # SCALING
    scale_opt = ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5']
    lspf = ' '.join([' -lsp', random.choices(scale_opt, weights=([0, 1, 1, 10, 2, 1, 0, 0, 0, 0]), k=1)[0]])
    lsaf = ' '.join([' -lsa', random.choices(scale_opt, weights=([0, 13, 1, 0, 0, 0, 0, 0, 0, 0]), k=1)[0]])
    lshf = ' '.join([' -lsh', random.choices(scale_opt, weights=([0, 13, 1, 0, 0, 0, 0, 0, 0, 0]), k=1)[0]])
    lstf = ' '.join([' -lst', random.choices(scale_opt, weights=([0, 1, 5, 10, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    hmpf = ' '.join([' -hmp', random.choices(scale_opt, weights=([0, 1, 1, 10, 2, 1, 0, 0, 0, 0]), k=1)[0]])
    hmaf = ' '.join([' -hma', random.choices(scale_opt, weights=([0, 13, 1, 0, 0, 0, 0, 0, 0, 0]), k=1)[0]])
    hmhf = ' '.join([' -hmh', random.choices(scale_opt, weights=([0, 13, 1, 0, 0, 0, 0, 0, 0, 0]), k=1)[0]])
    hmtf = ' '.join([' -hmt', random.choices(scale_opt, weights=([0, 1, 5, 10, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    xgpf = ' '.join([' -xgp', random.choices(scale_opt, weights=([0, 1, 1, 10, 2, 1, 0, 0, 0, 0]), k=1)[0]])
    xgaf = ' '.join([' -xga', random.choices(scale_opt, weights=([0, 13, 1, 0, 0, 0, 0, 0, 0, 0]), k=1)[0]])
    xghf = ' '.join([' -xgh', random.choices(scale_opt, weights=([0, 13, 1, 0, 0, 0, 0, 0, 0, 0]), k=1)[0]])
    xgtf = ' '.join([' -xgt', random.choices(scale_opt, weights=([0, 1, 5, 10, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    asrf = ' '.join([' -asr', random.choices(scale_opt, weights=([0, 0, 1, 10, 2, 1, 0, 0, 0, 0]), k=1)[0]])
    asef = ' '.join([' -ase', random.choices(scale_opt, weights=([0, 0, 1, 10, 2, 1, 0, 0, 0, 0]), k=1)[0]])
    lscale = random.choices([lspf, lsaf, lshf, lstf, ''], weights=([15, 2, 2, 1, 0]), k=1)[0]
    hmscale = random.choices([hmpf, hmaf, hmhf, hmtf, ''], weights=([15, 2, 2, 1, 0]), k=1)[0]
    xgscale = random.choices([xgpf, xgaf, xghf, xgtf, ''], weights=([15, 2, 2, 1, 0]), k=1)[0]
    ascale = random.choices([asrf, asef, ''], weights=([1, 13, 0]), k=1)[0]
    msl = ' '.join([' -msl', str(random.randint(40, 60))])
    eel = ' '.join([' -eel', str(random.randint(0, 5))])
    sfb = random.choices([' -sfb', ''], weights=([0, 1]), k=1)[0]
    sed = random.choices([' -sed', ''], weights=([13, 1]), k=1)[0]
    scaling = ''.join([lscale, hmscale, xgscale, ascale, msl, eel, sfb, sed])

    # ENCOUNTERS
    renc = random.choices(['', ' -res', ' '.join([' -rer', str(random.randint(0, 10))])], weights=([1, 10, 10]), k=1)[0]
    fenc = random.choices(['', ' '.join([' -fer', str(random.randint(0, 10))])], weights=([1, 13]), k=1)[0]
    escr = ' -escr 100'
    encounters = ''.join([renc, fenc, escr])

    battle = ''.join([bosses, b_ai, scaling, encounters, xpmpgp])

    # -----MAGIC-----
    # ESPERS
    esr1 = random.randint(1, 3)
    esr2 = random.randint(esr1, 5)
    esr = ' '.join([' -esr', str(esr1), str(esr2)])
    ess = random.choices(['', esr, ' -esrr', ' -ess', ' -essrr', ' -esrt'], weights=([1, 13, 2, 2, 2, 3]), k=1)[0]
    ebonus = random.choices(['', ' '.join([' -ebr', str(random.randint(67, 100))]), ' -ebs'], weights=([1, 10, 2]),
                            k=1)[0]
    emprp1 = random.randint(75, 100)
    emprp2 = random.randint(emprp1, 125)
    emprv1 = random.randint(25, 75)
    emprv2 = random.randint(emprv1, 99)
    eer1 = random.randint(6, 12)
    eer2 = random.randint(eer1, 12)
    emprp = ' '.join([' -emprp', str(emprp1), str(emprp2)])
    emprv = ' '.join([' -emprv', str(emprv1), str(emprv2)])
    emp = random.choices(['', emprp, emprv, ' -emps'], weights=([1, 10, 1, 3]), k=1)[0]
    eer = ' '.join([' -eer', str(eer1), str(eer2)])
    eebr = ' '.join([' -eebr', str(random.randint(6, 12))])
    eeq = random.choices([eer, eebr, ''], weights=([1, 1, 15]), k=1)[0]
    ems = random.choices(['', ' -ems'], weights=([13, 1]), k=1)[0]
    espers = ''.join([ess, ebonus, emp, eeq, ems])

    # NATURAL MAGIC
    nm1 = random.choices(['', ' -nm1 random'], weights=([0, 1]), k=1)[0]
    nm2 = random.choices(['', ' -nm2 random'], weights=([0, 1]), k=1)[0]
    rnl1 = random.choices(['', ' -rnl1'], weights=([0, 1]), k=1)[0]
    rnl2 = random.choices(['', ' -rnl2'], weights=([0, 1]), k=1)[0]
    rns1 = random.choices(['', ' -rns1'], weights=([0, 1]), k=1)[0]
    rns2 = random.choices(['', ' -rns2'], weights=([0, 1]), k=1)[0]
    m_indicator = random.choices(['', ' -nmmi'], weights=([0, 1]), k=1)[0]
    nmagic = ''.join([nm1, nm2, rnl1, rnl2, rns1, rns2, m_indicator])

    magic = ''.join([espers, nmagic])

    # -----ITEMS-----
    # STARTING GOLD/ITEMS
    gp = ' '.join([' -gp', str(random.randint(0, 20000))])
    smc = ' -smc 3'
    sws = ' '.join([' -sws', str(random.randint(0, 7))])
    sfd = ' '.join([' -sfd', str(random.randint(0, 7))])
    sto = ' '.join([' -sto', str(random.randint(0, 4))])
    s_inv = ''.join([gp, smc, sfd, sto, sws])

    # ITEMS
    ier1 = random.randint(0, 14)
    ier2 = random.randint(ier1, 14)
    ier = ' -ier ' + str(ier1) + " " + str(ier2)
    iebr = ' -iebr ' + str(random.randint(0, 14))
    ieor = ' -ieor ' + str(random.randint(0, 100))
    iesr = ' -iesr ' + str(random.randint(0, 100))
    iequip = random.choice(['', ier, iebr, ieor, iesr])
    ierr1 = random.randint(0, 14)
    ierr2 = random.randint(ierr1, 14)
    ierr = ' -ierr ' + str(ierr1) + " " + str(ierr2)
    ierbr = ' -ierbr ' + str(random.randint(0, 14))
    ieror = ' -ieror ' + str(random.randint(0, 100))
    iersr = ' -iersr ' + str(random.randint(0, 100))
    requip = random.choice(['', ierr, ierbr, ieror, iersr])
    csb1 = random.randint(1, 256)
    csb2 = random.randint(csb1, 256)
    csb = ' -csb ' + str(csb1) + " " + str(csb2)
    mca = random.choice([' -mca', ''])
    stra = random.choice([' -stra', ''])
    saw = random.choice([' -saw', ''])
    equips = iequip + requip + csb + mca + stra + saw

    # SHOPS
    sisr = ' -sisr ' + str(random.randint(0, 100))
    shopinv = random.choice(['', sisr, ' -sirt', ' -sie'])
    sprv1 = random.randint(0, 65535)
    sprv2 = random.randint(sprv1, 65535)
    sprp1 = random.randint(0, 200)
    sprp2 = random.randint(sprp1, 200)
    sprv = ' -sprv ' + str(sprv1) + " " + str(sprv2)
    sprp = ' -sprp ' + str(sprp1) + " " + str(sprp2)
    shopprices = random.choice(['', sprv, sprp])
    ssf = random.choice(['', ' -ssf4', ' -ssf8', ' -ssf0'])
    sdm = ' -sdm ' + str(random.randint(0, 5))
    npi = random.choice(['', ' -npi'])
    snbr = random.choice(['', ' -snbr'])
    snes = random.choice(['', ' -snes'])
    snsb = random.choice(['', ' -snsb'])
    shops = shopinv + shopprices + ssf + sdm + npi + snbr + snes + snsb

    # CHESTS
    ccontents = random.choice(['', ' -ccrt', ' -cce', ' -ccsr ' + str(random.randint(0, 100))])
    cms = random.choice(['', ' -cms'])
    chests = ccontents + cms

    items = s_inv + equips + shops + chests

    # -----CUSTOM-----
    # SEE CUSTOM_SPRITES_PORTRAITS.PY

    # -----OTHER-----
    # COLISEUM
    co = random.choice(['', ' -cor', ' -cos'])
    cr = random.choice(['', ' -crs', ' -crr'])
    crvr1 = random.randint(0, 255)
    crvr2 = random.randint(crvr1, 255)
    visible = random.choice(['', ' -crvr ' + str(crvr1) + " " + str(crvr2)])
    rmenu = random.choice(['', ' -crm'])
    colo = ''.join([co, cr, visible, rmenu])

    # AUCTION HOUSE
    ari = random.choice(['', ' -ari'])
    anca = random.choice(['', ' -anca'])
    adeh = random.choice(['', ' -adeh'])
    ah = ''.join([ari, anca, adeh])

    # MISC
    asprint = random.choice(['', ' -as'])
    ond = random.choice(['', ' -ond'])
    rr = random.choice(['', ' -rr'])
    scan = random.choice(['', ' -scan'])
    etimers = random.choice(['', ' -etr', ' -etn'])
    ychoices = [' -ymascot', ' -ycreature', ' -yimperial', ' -ymain', ' -yreflect', ' -ystone', ' -ysketch',
                ' -yrandom', ' -yremove', '']
    ychoice = random.choice(ychoices)
    misc = ''.join([asprint, ond, rr, scan, etimers, ychoice])

    # CHALLENGES
    nmc = random.choice(['', ' -nmc'])
    nee = random.choice(['', ' -nee'])
    nil = random.choice(['', ' -nil'])
    nfps = random.choice(['', ' -nfps'])
    nu = random.choice(['', ' -nu'])
    nfp = random.choice(['', ' -nfp'])
    kthr = random.choice(['', ' -kthr'])
    pd = random.choice(['', ' -pd'])
    challenges = ''.join([nmc, nee, nil, nfps, nu, nfp, kthr, pd])

    # BUG FIXES
    fs = random.choice(['', ' -fs'])
    fe = random.choice(['', ' -fe'])
    fvd = random.choice(['', ' -fvd'])
    fr = random.choice(['', ' -fr'])
    fj = random.choice(['', ' -fj'])
    fbs = random.choice(['', ' -fbs'])
    fedc = random.choice(['', ' -fedc'])
    bugfixes = ''.join([fs, fe, fvd, fr, fj, fbs, fedc])

    other = ''.join([colo, ah, challenges, misc, bugfixes])

    flagset = game + party + battle + magic + items + other
    return flagset

def chaos():
    # -----GAME-----
    # SETTINGS
    mode = random.choice(["-ow", "-cg"])
    slog = random.choice([" -sl", ""])
    settings = mode + slog

    # KEFKA'S TOWER & STATUE SKIP
    ktcr1 = random.randint(3, 14)
    ktcr2 = random.randint(ktcr1, 14)
    kter1 = random.randint(0, 24)
    kter2 = random.randint(kter1, 24)
    ktdr1 = random.randint(0, 8)
    ktdr2 = random.randint(ktdr1, 8)
    stcr1 = random.randint(3, 14)
    stcr2 = random.randint(stcr1, 14)
    ster1 = random.randint(0, 24)
    ster2 = random.randint(ster1, 24)
    stdr1 = random.randint(0, 8)
    stdr2 = random.randint(stdr1, 8)
    stno = random.choice([True, False])

    if stno:
        kt = ' -ktcr ' + str(ktcr1) + " " + str(ktcr2) + ' -kter ' + str(kter1) + " " + str(kter2) + ' -ktdr ' + str(
            ktdr1) + " " + \
             str(ktdr2) + ' -stno'
    else:
        kt = ' -ktcr ' + str(ktcr1) + " " + str(ktcr2) + ' -kter ' + str(kter1) + " " + str(kter2) + ' -ktdr ' + str(
            ktdr1) + " " + \
             str(ktdr2) + ' -stcr ' + str(stcr1) + " " + str(stcr2) + ' -ster ' + str(ster1) + " " + str(ster2) + \
             ' -stdr ' + str(stdr1) + " " + str(stdr2)

    game = settings + kt

    # -----PARTY-----
    # STARTING PARTY
    sc1 = random.choice([' -sc1 random', ' -sc1 randomngu'])
    sc2 = random.choice([' -sc2 random', ' -sc2 randomngu', ''])
    sc3 = random.choice([' -sc3 random', ' -sc3 randomngu', ''])
    sc4 = random.choice([' -sc4 random', ' -sc4 randomngu', ''])
    sparty = sc1 + sc2 + sc3 + sc4

    # SWORDTECHS
    fst = random.choice([' -fst', ''])
    sel = random.choice([' -sel', ''])
    swdtech = fst + sel

    # BLITZES
    brl = random.choice([' -brl', ''])
    bel = random.choice([' -bel', ''])
    blitz = brl + bel

    # LORES
    slr1 = random.randint(0, 24)
    slr2 = random.randint(slr1, 24)
    slrr = ' -slr ' + str(slr1) + " " + str(slr2)
    slr = random.choice([slrr, ''])
    lmprp1 = random.randint(0, 200)
    lmprp2 = random.randint(lmprp1, 200)
    lmprv1 = random.randint(0, 99)
    lmprv2 = random.randint(lmprv1, 99)
    lmprp = ' -lmprp ' + str(lmprp1) + " " + str(lmprp2)
    lmprv = ' -lmprv ' + str(lmprv1) + " " + str(lmprv2)
    loremp = random.choice(['', ' -lmps', lmprp, lmprv])
    lel = random.choice([' -lel', ''])
    lores = slr + loremp + lel

    # RAGES
    srr1 = random.randint(0, 255)
    srr2 = random.randint(srr1, 255)
    srr = ' -srr ' + str(srr1) + " " + str(srr2)
    srages = random.choice(['', srr])
    rnl = random.choice([' -rnl', ''])
    rnc = random.choice([' -rnc', ''])
    rage = srages + rnl + rnc

    # DANCES
    sdr1 = random.randint(0, 8)
    sdr2 = random.randint(sdr1, 8)
    sdr = ' -sdr ' + str(sdr1) + " " + str(sdr2)
    das = random.choice([' -das', ''])
    dda = random.choice([' -dda', ''])
    dns = random.choice([' -dns', ''])
    d_el = random.choice([' -del', ''])
    dance = sdr + das + dda + dns + d_el

    # CHARACTERS
    sal = random.choice([' -sal', ''])
    sn = random.choice([' -sn', ''])
    eu = random.choice([' -eu', ''])
    csrp1 = random.randint(0, 200)
    csrp2 = random.randint(csrp1, 200)
    csrp = ' -csrp ' + str(csrp1) + " " + str(csrp2)
    cstats = sal + sn + eu + csrp

    # COMMANDS
    scc = random.choice([' -scc', ''])
    com = random.choice([' -com 99999999999999999999999999', '', ' -com 98989898989898989898989898'])
    recskills = ['10', '6', '14', '19', '24', '26', '22', '12', '3', '28', '16', '11', '27', '13', '15', '5',
                 '7', '8', '9', '23']
    rec1 = random.choice(['', ' -rec1 ' + random.choice(recskills)])
    rec2 = random.choice(['', ' -rec2 ' + random.choice(recskills)])
    rec3 = random.choice(['', ' -rec3 ' + random.choice(recskills)])
    rec4 = random.choice(['', ' -rec4 ' + random.choice(recskills)])
    commands = scc + com + rec1 + rec2 + rec3 + rec4

    party = sparty + swdtech + blitz + lores + rage + dance + cstats + commands

    # -----BATTLE-----
    # EXPERIENCE, MAGIC POINTS, GOLD !!![max on these values is 255, but that seems excessive]!!!
    xpm = ' -xpm ' + str(random.randint(1, 15))
    gpm = ' -gpm ' + str(random.randint(1, 15))
    mpm = ' -mpm ' + str(random.randint(1, 15))
    nxppd = random.choice([' -nxppd', ''])
    xpmpgp = xpm + gpm + mpm + nxppd

    # BOSSES
    bb = random.choice([' -bbr', ' -bbs', ''])
    bmbd = random.choice([' -bmbd', ''])
    srp3 = random.choice([' -srp3', ''])
    bnds = random.choice([' -bnds', ''])
    be = random.choice([' -be', ''])
    bnu = random.choice([' -bnu', ''])
    bosses = bb + bmbd + srp3 + bnds + be + bnu

    # BOSS AI
    dgne = random.choice([' -dgne', ''])
    wnz = random.choice([' -wnz', ''])
    mmnu = random.choice([' -mmnu', ''])
    cmd = random.choice([' -cmd', ''])
    b_ai = dgne + wnz + mmnu + cmd

    # SCALING
    scale_opt = ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5']
    lspf = ' -lsp ' + random.choice(scale_opt)
    lsaf = ' -lsa ' + random.choice(scale_opt)
    lshf = ' -lsh ' + random.choice(scale_opt)
    lstf = ' -lst ' + random.choice(scale_opt)
    hmpf = ' -hmp ' + random.choice(scale_opt)
    hmaf = ' -hma ' + random.choice(scale_opt)
    hmhf = ' -hmh ' + random.choice(scale_opt)
    hmtf = ' -hmt ' + random.choice(scale_opt)
    xgpf = ' -xgp ' + random.choice(scale_opt)
    xgaf = ' -xga ' + random.choice(scale_opt)
    xghf = ' -xgh ' + random.choice(scale_opt)
    xgtf = ' -xgt ' + random.choice(scale_opt)
    asrf = ' -asr ' + random.choice(scale_opt)
    asef = ' -ase ' + random.choice(scale_opt)
    lscale = random.choice([lspf, lsaf, lshf, lstf, ''])
    hmscale = random.choice([hmpf, hmaf, hmhf, hmtf, ''])
    xgscale = random.choice([xgpf, xgaf, xghf, xgtf, ''])
    ascale = random.choice([asrf, asef, ''])
    # !!![These two settings below can both go from 0-99 but I set limits to prevent super-easy/unbeatable seeds]!!!
    msl = ' -msl ' + str(random.randint(35, 99))
    eel = ' -eel ' + str(random.randint(0, 50))
    sfb = random.choice([' -sfb', ''])
    sed = random.choice([' -sed', ''])
    scaling = lscale + hmscale + xgscale + ascale + msl + eel + sfb + sed

    # ENCOUNTERS
    renc = random.choice(['', ' -res', ' -rer ' + str(random.randint(0, 100))])
    fenc = random.choice(['', ' -fer ' + str(random.randint(0, 100))])
    escr = ' -escr ' + str(random.randint(0, 100))
    encounters = renc + fenc + escr

    battle = bosses + b_ai + scaling + encounters + xpmpgp

    # -----MAGIC-----
    # ESPERS
    esr1 = random.randint(1, 5)
    esr2 = random.randint(esr1, 5)
    esr = ' -esr ' + str(esr1) + " " + str(esr2)
    ess = random.choice(['', esr, ' -esrr', ' -ess', ' -essrr', ' -esrt'])
    ebonus = random.choice(['', ' -ebr ' + str(random.randint(0, 100)), ' -ebs'])
    emprp1 = random.randint(0, 200)
    emprp2 = random.randint(emprp1, 200)
    emprv1 = random.randint(1, 128)
    emprv2 = random.randint(emprv1, 128)
    eer1 = random.randint(0, 12)
    eer2 = random.randint(eer1, 12)
    emprp = ' -emprp ' + str(emprp1) + " " + str(emprp2)
    emprv = ' -emprv ' + str(emprv1) + " " + str(emprv2)
    emp = random.choice(['', emprp, emprv, ' -emps'])
    eer = ' -eer ' + str(eer1) + " " + str(eer2)
    eebr = ' -eebr ' + str(random.randint(0, 12))
    eeq = random.choice([eer, eebr, ''])
    ems = random.choice(['', ' -ems'])
    espers = ess + ebonus + emp + eeq + ems

    # NATURAL MAGIC
    nm1 = random.choice(['', ' -nm1 random'])
    nm2 = random.choice(['', ' -nm2 random'])
    rnl1 = random.choice(['', ' -rnl1'])
    rnl2 = random.choice(['', ' -rnl2'])
    rns1 = random.choice(['', ' -rns1'])
    rns2 = random.choice(['', ' -rns2'])
    m_indicator = random.choice(['', ' -nmmi'])
    nmagic = nm1 + nm2 + rnl1 + rnl2 + rns1 + rns2 + m_indicator

    magic = espers + nmagic

    # -----ITEMS-----
    # STARTING GOLD/ITEMS
    gp = ' -gp ' + str(random.randint(0, 999999))
    smc = ' -smc ' + str(random.randint(0, 3))
    sws = ' -sws ' + str(random.randint(0, 10))
    sfd = ' -sfd ' + str(random.randint(0, 10))
    sto = ' -sto ' + str(random.randint(0, 8))
    s_inv = gp + smc + sfd + sto + sws

    # ITEMS
    ier1 = random.randint(0, 14)
    ier2 = random.randint(ier1, 14)
    ier = ' -ier ' + str(ier1) + " " + str(ier2)
    iebr = ' -iebr ' + str(random.randint(0, 14))
    ieor = ' -ieor ' + str(random.randint(0, 100))
    iesr = ' -iesr ' + str(random.randint(0, 100))
    iequip = random.choice(['', ier, iebr, ieor, iesr])
    ierr1 = random.randint(0, 14)
    ierr2 = random.randint(ierr1, 14)
    ierr = ' -ierr ' + str(ierr1) + " " + str(ierr2)
    ierbr = ' -ierbr ' + str(random.randint(0, 14))
    ieror = ' -ieror ' + str(random.randint(0, 100))
    iersr = ' -iersr ' + str(random.randint(0, 100))
    requip = random.choice(['', ierr, ierbr, ieror, iersr])
    csb1 = random.randint(1, 256)
    csb2 = random.randint(csb1, 256)
    csb = ' -csb ' + str(csb1) + " " + str(csb2)
    mca = random.choice([' -mca', ''])
    stra = random.choice([' -stra', ''])
    saw = random.choice([' -saw', ''])
    equips = iequip + requip + csb + mca + stra + saw

    # SHOPS
    sisr = ' -sisr ' + str(random.randint(0, 100))
    shopinv = random.choice(['', sisr, ' -sirt', ' -sie'])
    sprv1 = random.randint(0, 65535)
    sprv2 = random.randint(sprv1, 65535)
    sprp1 = random.randint(0, 200)
    sprp2 = random.randint(sprp1, 200)
    sprv = ' -sprv ' + str(sprv1) + " " + str(sprv2)
    sprp = ' -sprp ' + str(sprp1) + " " + str(sprp2)
    shopprices = random.choice(['', sprv, sprp])
    ssf = random.choice(['', ' -ssf4', ' -ssf8', ' -ssf0'])
    sdm = ' -sdm ' + str(random.randint(0, 5))
    npi = random.choice(['', ' -npi'])
    snbr = random.choice(['', ' -snbr'])
    snes = random.choice(['', ' -snes'])
    snsb = random.choice(['', ' -snsb'])
    shops = shopinv + shopprices + ssf + sdm + npi + snbr + snes + snsb

    # CHESTS
    ccontents = random.choice(['', ' -ccrt', ' -cce', ' -ccsr ' + str(random.randint(0, 100))])
    cms = random.choice(['', ' -cms'])
    chests = ccontents + cms

    items = s_inv + equips + shops + chests

    # -----CUSTOM-----
    # SEE CUSTOM_SPRITES_PORTRAITS.PY

    # -----OTHER-----
    # COLISEUM
    co = random.choice(['', ' -cor', ' -cos'])
    cr = random.choice(['', ' -crs', ' -crr'])
    crvr1 = random.randint(0, 255)
    crvr2 = random.randint(crvr1, 255)
    visible = random.choice(['', ' -crvr ' + str(crvr1) + " " + str(crvr2)])
    rmenu = random.choice(['', ' -crm'])
    colo = ''.join([co, cr, visible, rmenu])

    # AUCTION HOUSE
    ari = random.choice(['', ' -ari'])
    anca = random.choice(['', ' -anca'])
    adeh = random.choice(['', ' -adeh'])
    ah = ''.join([ari, anca, adeh])

    # MISC
    asprint = random.choice(['', ' -as'])
    ond = random.choice(['', ' -ond'])
    rr = random.choice(['', ' -rr'])
    scan = random.choice(['', ' -scan'])
    etimers = random.choice(['', ' -etr', ' -etn'])
    ychoices = [' -ymascot', ' -ycreature', ' -yimperial', ' -ymain', ' -yreflect', ' -ystone', ' -ysketch',
                ' -yrandom', ' -yremove', '']
    ychoice = random.choice(ychoices)
    misc = ''.join([asprint, ond, rr, scan, etimers, ychoice])

    # CHALLENGES
    nmc = random.choice(['', ' -nmc'])
    nee = random.choice(['', ' -nee'])
    nil = random.choice(['', ' -nil'])
    nfps = random.choice(['', ' -nfps'])
    nu = random.choice(['', ' -nu'])
    nfp = random.choice(['', ' -nfp'])
    kthr = random.choice(['', ' -kthr'])
    pd = random.choice(['', ' -pd'])
    challenges = ''.join([nmc, nee, nil, nfps, nu, nfp, kthr, pd])

    # BUG FIXES
    fs = random.choice(['', ' -fs'])
    fe = random.choice(['', ' -fe'])
    fvd = random.choice(['', ' -fvd'])
    fr = random.choice(['', ' -fr'])
    fj = random.choice(['', ' -fj'])
    fbs = random.choice(['', ' -fbs'])
    fedc = random.choice(['', ' -fedc'])
    bugfixes = ''.join([fs, fe, fvd, fr, fj, fbs, fedc])

    other = ''.join([colo, ah, challenges, misc, bugfixes])

    flagset = game + party + battle + magic + items + other
    return flagset

def true_chaos():
    # -----GAME-----
    # SETTINGS
    mode = random.choice(["-ow", "-cg"])
    slog = random.choice([" -sl", ""])
    settings = mode + slog

    # KEFKA'S TOWER & STATUE SKIP
    ktcr1 = random.randint(3, 14)
    ktcr2 = random.randint(ktcr1, 14)
    kter1 = random.randint(0, 24)
    kter2 = random.randint(kter1, 24)
    ktdr1 = random.randint(0, 8)
    ktdr2 = random.randint(ktdr1, 8)
    stcr1 = random.randint(3, 14)
    stcr2 = random.randint(stcr1, 14)
    ster1 = random.randint(0, 24)
    ster2 = random.randint(ster1, 24)
    stdr1 = random.randint(0, 8)
    stdr2 = random.randint(stdr1, 8)
    stno = random.choice([True, False])

    if stno:
        kt = ' -ktcr ' + str(ktcr1) + " " + str(ktcr2) + ' -kter ' + str(kter1) + " " + str(kter2) + ' -ktdr ' + str(
        ktdr1) + " " + \
         str(ktdr2) + ' -stno'
    else:
        kt = ' -ktcr ' + str(ktcr1) + " " + str(ktcr2) + ' -kter ' + str(kter1) + " " + str(kter2) + ' -ktdr ' + str(
        ktdr1) + " " + \
         str(ktdr2) + ' -stcr ' + str(stcr1) + " " + str(stcr2) + ' -ster ' + str(ster1) + " " + str(ster2) + \
         ' -stdr ' + str(stdr1) + " " + str(stdr2)

    game = settings + kt

    # -----PARTY-----
    # STARTING PARTY
    sc1 = random.choice([' -sc1 random', ' -sc1 randomngu'])
    sc2 = random.choice([' -sc2 random', ' -sc2 randomngu', ''])
    sc3 = random.choice([' -sc3 random', ' -sc3 randomngu', ''])
    sc4 = random.choice([' -sc4 random', ' -sc4 randomngu', ''])
    sparty = sc1 + sc2 + sc3 + sc4

    # SWORDTECHS
    fst = random.choice([' -fst', ''])
    sel = random.choice([' -sel', ''])
    swdtech = fst + sel

    # BLITZES
    brl = random.choice([' -brl', ''])
    bel = random.choice([' -bel', ''])
    blitz = brl + bel

    # LORES
    slr1 = random.randint(0, 24)
    slr2 = random.randint(slr1, 24)
    slrr = ' -slr ' + str(slr1) + " " + str(slr2)
    slr = random.choice([slrr, ''])
    lmprp1 = random.randint(0, 200)
    lmprp2 = random.randint(lmprp1, 200)
    lmprv1 = random.randint(0, 99)
    lmprv2 = random.randint(lmprv1, 99)
    lmprp = ' -lmprp ' + str(lmprp1) + " " + str(lmprp2)
    lmprv = ' -lmprv ' + str(lmprv1) + " " + str(lmprv2)
    loremp = random.choice(['', ' -lmps', lmprp, lmprv])
    lel = random.choice([' -lel', ''])
    lores = slr + loremp + lel

    # RAGES
    srr1 = random.randint(0, 255)
    srr2 = random.randint(srr1, 255)
    srr = ' -srr ' + str(srr1) + " " + str(srr2)
    srages = random.choice(['', srr])
    rnl = random.choice([' -rnl', ''])
    rnc = random.choice([' -rnc', ''])
    rage = srages + rnl + rnc

    # DANCES
    sdr1 = random.randint(0, 8)
    sdr2 = random.randint(sdr1, 8)
    sdr = ' -sdr ' + str(sdr1) + " " + str(sdr2)
    das = random.choice([' -das', ''])
    dda = random.choice([' -dda', ''])
    dns = random.choice([' -dns', ''])
    d_el = random.choice([' -del', ''])
    dance = sdr + das + dda + dns + d_el

    # CHARACTERS
    sal = random.choice([' -sal', ''])
    sn = random.choice([' -sn', ''])
    eu = random.choice([' -eu', ''])
    csrp1 = random.randint(0, 200)
    csrp2 = random.randint(csrp1, 200)
    csrp = ' -csrp ' + str(csrp1) + " " + str(csrp2)
    cstats = sal + sn + eu + csrp

    # COMMANDS
    scc = random.choice([' -scc', ''])
    com = random.choice([' -com 99999999999999999999999999', '', ' -com 98989898989898989898989898'])
    recskills = ['10', '6', '14', '19', '24', '26', '22', '12', '3', '28', '16', '11', '27', '13', '15', '5',
         '7', '8', '9', '23']
    rec1 = random.choice(['', ' -rec1 ' + random.choice(recskills)])
    rec2 = random.choice(['', ' -rec2 ' + random.choice(recskills)])
    rec3 = random.choice(['', ' -rec3 ' + random.choice(recskills)])
    rec4 = random.choice(['', ' -rec4 ' + random.choice(recskills)])
    commands = scc + com + rec1 + rec2 + rec3 + rec4

    party = sparty + swdtech + blitz + lores + rage + dance + cstats + commands

    # -----BATTLE-----
    xpm = ' -xpm ' + str(random.randint(1, 255))
    gpm = ' -gpm ' + str(random.randint(1, 255))
    mpm = ' -mpm ' + str(random.randint(1, 255))
    nxppd = random.choice([' -nxppd', ''])
    xpmpgp = xpm + gpm + mpm + nxppd

    # BOSSES
    bb = random.choice([' -bbr', ' -bbs', ''])
    bmbd = random.choice([' -bmbd', ''])
    srp3 = random.choice([' -srp3', ''])
    bnds = random.choice([' -bnds', ''])
    be = random.choice([' -be', ''])
    bnu = random.choice([' -bnu', ''])
    bosses = bb + bmbd + srp3 + bnds + be + bnu

    # BOSS AI
    dgne = random.choice([' -dgne', ''])
    wnz = random.choice([' -wnz', ''])
    mmnu = random.choice([' -mmnu', ''])
    cmd = random.choice([' -cmd', ''])
    b_ai = dgne + wnz + mmnu + cmd

    # SCALING
    scale_opt = ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5']
    lspf = ' -lsp ' + random.choice(scale_opt)
    lsaf = ' -lsa ' + random.choice(scale_opt)
    lshf = ' -lsh ' + random.choice(scale_opt)
    lstf = ' -lst ' + random.choice(scale_opt)
    hmpf = ' -hmp ' + random.choice(scale_opt)
    hmaf = ' -hma ' + random.choice(scale_opt)
    hmhf = ' -hmh ' + random.choice(scale_opt)
    hmtf = ' -hmt ' + random.choice(scale_opt)
    xgpf = ' -xgp ' + random.choice(scale_opt)
    xgaf = ' -xga ' + random.choice(scale_opt)
    xghf = ' -xgh ' + random.choice(scale_opt)
    xgtf = ' -xgt ' + random.choice(scale_opt)
    asrf = ' -asr ' + random.choice(scale_opt)
    asef = ' -ase ' + random.choice(scale_opt)
    lscale = random.choice([lspf, lsaf, lshf, lstf, ''])
    hmscale = random.choice([hmpf, hmaf, hmhf, hmtf, ''])
    xgscale = random.choice([xgpf, xgaf, xghf, xgtf, ''])
    ascale = random.choice([asrf, asef, ''])
    msl = ' -msl ' + str(random.randint(0, 99))
    eel = ' -eel ' + str(random.randint(0, 99))
    sfb = random.choice([' -sfb', ''])
    sed = random.choice([' -sed', ''])
    scaling = lscale + hmscale + xgscale + ascale + msl + eel + sfb + sed

    # ENCOUNTERS
    renc = random.choice(['', ' -res', ' -rer ' + str(random.randint(0, 100))])
    fenc = random.choice(['', ' -fer ' + str(random.randint(0, 100))])
    escr = ' -escr ' + str(random.randint(0, 100))
    encounters = renc + fenc + escr

    battle = bosses + b_ai + scaling + encounters + xpmpgp

    # -----MAGIC-----
    # ESPERS
    esr1 = random.randint(1, 5)
    esr2 = random.randint(esr1, 5)
    esr = ' -esr ' + str(esr1) + " " + str(esr2)
    ess = random.choice(['', esr, ' -esrr', ' -ess', ' -essrr', ' -esrt'])
    ebonus = random.choice(['', ' -ebr ' + str(random.randint(0, 100)), ' -ebs'])
    emprp1 = random.randint(0, 200)
    emprp2 = random.randint(emprp1, 200)
    emprv1 = random.randint(1, 128)
    emprv2 = random.randint(emprv1, 128)
    eer1 = random.randint(0, 12)
    eer2 = random.randint(eer1, 12)
    emprp = ' -emprp ' + str(emprp1) + " " + str(emprp2)
    emprv = ' -emprv ' + str(emprv1) + " " + str(emprv2)
    emp = random.choice(['', emprp, emprv, ' -emps'])
    eer = ' -eer ' + str(eer1) + " " + str(eer2)
    eebr = ' -eebr ' + str(random.randint(0, 12))
    eeq = random.choice([eer, eebr, ''])
    ems = random.choice(['', ' -ems'])
    espers = ess + ebonus + emp + eeq + ems

    # NATURAL MAGIC
    nm1 = random.choice(['', ' -nm1 random'])
    nm2 = random.choice(['', ' -nm2 random'])
    rnl1 = random.choice(['', ' -rnl1'])
    rnl2 = random.choice(['', ' -rnl2'])
    rns1 = random.choice(['', ' -rns1'])
    rns2 = random.choice(['', ' -rns2'])
    m_indicator = random.choice(['', ' -nmmi'])
    nmagic = nm1 + nm2 + rnl1 + rnl2 + rns1 + rns2 + m_indicator

    magic = espers + nmagic

    # -----ITEMS-----
    # STARTING GOLD/ITEMS
    gp = ' -gp ' + str(random.randint(0, 999999))
    smc = ' -smc ' + str(random.randint(0, 3))
    sws = ' -sws ' + str(random.randint(0, 10))
    sfd = ' -sfd ' + str(random.randint(0, 10))
    sto = ' -sto ' + str(random.randint(0, 8))
    s_inv = gp + smc + sfd + sto + sws

    # ITEMS
    ier1 = random.randint(0, 14)
    ier2 = random.randint(ier1, 14)
    ier = ' -ier ' + str(ier1) + " " + str(ier2)
    iebr = ' -iebr ' + str(random.randint(0, 14))
    ieor = ' -ieor ' + str(random.randint(0, 100))
    iesr = ' -iesr ' + str(random.randint(0, 100))
    iequip = random.choice(['', ier, iebr, ieor, iesr])
    ierr1 = random.randint(0, 14)
    ierr2 = random.randint(ierr1, 14)
    ierr = ' -ierr ' + str(ierr1) + " " + str(ierr2)
    ierbr = ' -ierbr ' + str(random.randint(0, 14))
    ieror = ' -ieror ' + str(random.randint(0, 100))
    iersr = ' -iersr ' + str(random.randint(0, 100))
    requip = random.choice(['', ierr, ierbr, ieror, iersr])
    csb1 = random.randint(1, 256)
    csb2 = random.randint(csb1, 256)
    csb = ' -csb ' + str(csb1) + " " + str(csb2)
    mca = random.choice([' -mca', ''])
    stra = random.choice([' -stra', ''])
    saw = random.choice([' -saw', ''])
    equips = iequip + requip + csb + mca + stra + saw

    # SHOPS
    sisr = ' -sisr ' + str(random.randint(0, 100))
    shopinv = random.choice(['', sisr, ' -sirt', ' -sie'])
    sprv1 = random.randint(0, 65535)
    sprv2 = random.randint(sprv1, 65535)
    sprp1 = random.randint(0, 200)
    sprp2 = random.randint(sprp1, 200)
    sprv = ' -sprv ' + str(sprv1) + " " + str(sprv2)
    sprp = ' -sprp ' + str(sprp1) + " " + str(sprp2)
    shopprices = random.choice(['', sprv, sprp])
    ssf = random.choice(['', ' -ssf4', ' -ssf8', ' -ssf0'])
    sdm = ' -sdm ' + str(random.randint(0, 5))
    npi = random.choice(['', ' -npi'])
    snbr = random.choice(['', ' -snbr'])
    snes = random.choice(['', ' -snes'])
    snsb = random.choice(['', ' -snsb'])
    shops = shopinv + shopprices + ssf + sdm + npi + snbr + snes + snsb

    # CHESTS
    ccontents = random.choice(['', ' -ccrt', ' -cce', ' -ccsr ' + str(random.randint(0, 100))])
    cms = random.choice(['', ' -cms'])
    chests = ccontents + cms

    items = s_inv + equips + shops + chests

    # -----CUSTOM-----
    # SEE CUSTOM_SPRITES_PORTRAITS.PY

    # -----OTHER-----
    # COLISEUM
    co = random.choice(['', ' -cor', ' -cos'])
    cr = random.choice(['', ' -crs', ' -crr'])
    crvr1 = random.randint(0, 255)
    crvr2 = random.randint(crvr1, 255)
    visible = random.choice(['', ' -crvr ' + str(crvr1) + " " + str(crvr2)])
    rmenu = random.choice(['', ' -crm'])
    colo = ''.join([co, cr, visible, rmenu])

    # AUCTION HOUSE
    ari = random.choice(['', ' -ari'])
    anca = random.choice(['', ' -anca'])
    adeh = random.choice(['', ' -adeh'])
    ah = ''.join([ari, anca, adeh])

    # MISC
    asprint = random.choice(['', ' -as'])
    ond = random.choice(['', ' -ond'])
    rr = random.choice(['', ' -rr'])
    scan = random.choice(['', ' -scan'])
    etimers = random.choice(['', ' -etr', ' -etn'])
    ychoices = [' -ymascot', ' -ycreature', ' -yimperial', ' -ymain', ' -yreflect', ' -ystone', ' -ysketch',
        ' -yrandom', ' -yremove', '']
    ychoice = random.choice(ychoices)
    misc = ''.join([asprint, ond, rr, scan, etimers, ychoice])

    # CHALLENGES
    nmc = random.choice(['', ' -nmc'])
    nee = random.choice(['', ' -nee'])
    nil = random.choice(['', ' -nil'])
    nfps = random.choice(['', ' -nfps'])
    nu = random.choice(['', ' -nu'])
    nfp = random.choice(['', ' -nfp'])
    kthr = random.choice(['', ' -kthr'])
    pd = random.choice(['', ' -pd'])
    challenges = ''.join([nmc, nee, nil, nfps, nu, nfp, kthr, pd])

    # BUG FIXES
    fs = random.choice(['', ' -fs'])
    fe = random.choice(['', ' -fe'])
    fvd = random.choice(['', ' -fvd'])
    fr = random.choice(['', ' -fr'])
    fj = random.choice(['', ' -fj'])
    fbs = random.choice(['', ' -fbs'])
    fedc = random.choice(['', ' -fedc'])
    bugfixes = ''.join([fs, fe, fvd, fr, fj, fbs, fedc])

    other = ''.join([colo, ah, challenges, misc, bugfixes])

    flagset = game + party + battle + magic + items + other
    return flagset

# print(chaos())