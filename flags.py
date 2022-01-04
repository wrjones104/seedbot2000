import random


def standard():
    # -----GAME-----
    # SETTINGS
    mode = random.choices(["-ow", "-cg"], weights=([1, 15]), k=1)[0]
    slog = random.choices(['', ' -sl'], weights=([1, 0]), k=1)[0]
    settings = ''.join([mode, slog])

    # KEFKA'S TOWER & STATUE SKIP
    ktcr1 = random.randint(5, 7)
    ktcr2 = random.randint(ktcr1, 10)
    kter1 = random.randint(7, 11)
    kter2 = random.randint(kter1, 13)
    ktdr1 = random.randint(0, 1)
    ktdr2 = random.randint(ktdr1, 1)
    stcr1 = random.randint(6, 8)
    stcr2 = random.randint(stcr1, 11)
    ster1 = random.randint(8, 12)
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
    sc4 = random.choices([' -sc4 random', ' -sc4 randomngu', ''], weights=([0, 0, 1]), k=1)[0]
    sparty = ''.join([sc1, sc2, sc3, sc4])

    # SWORDTECHS
    fst = random.choices([' -fst', ''], weights=([1, 0]), k=1)[0]
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
    lmprp1 = random.randint(75, 100)
    lmprp2 = random.randint(lmprp1, 125)
    lmprv1 = random.randint(20, 40)
    lmprv2 = random.randint(lmprv1, 75)
    lmprp = ' '.join([' -lmprp', str(lmprp1), str(lmprp2)])
    lmprv = ' '.join([' -lmprv', str(lmprv1), str(lmprv2)])
    loremp = random.choices(['', ' -lmps', lmprp, lmprv], weights=([1, 3, 10, 3]), k=1)[0]
    lel = random.choices([' -lel', ''], weights=([1, 0]), k=1)[0]
    lores = ''.join([slr, loremp, lel])

    # RAGES
    srr1 = random.randint(0, 10)
    srr2 = random.randint(srr1, 25)
    srr = ' '.join([' -srr', str(srr1), str(srr2)])
    srages = random.choices(['', srr], weights=([1, 13]), k=1)[0]
    rnl = random.choices([' -rnl', ''], weights=([1, 0]), k=1)[0]
    rnc = random.choices([' -rnc', ''], weights=([15, 1]), k=1)[0]
    rage = ''.join([srages, rnl, rnc])

    # DANCES
    sdr1 = random.randint(0, 2)
    sdr2 = random.randint(sdr1, 4)
    sdr = ' '.join([' -sdr', str(sdr1), str(sdr2)])
    das = random.choices([' -das', ''], weights=([1, 0]), k=1)[0]
    dda = random.choices([' -dda', ''], weights=([1, 0]), k=1)[0]
    dns = random.choices([' -dns', ''], weights=([1, 0]), k=1)[0]
    d_el = random.choices([' -del', ''], weights=([0, 1]), k=1)[0]
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
    rec1 = random.choices([' -rec1 28', ''], weights=([1, 0]), k=1)[0]
    rec2 = random.choices([' -rec2 23', ''], weights=([1, 0]), k=1)[0]
    rec3 = random.choices([' '.join([' -rec3', random.choice(recskills)]), ''], weights=([0, 1]), k=1)[0]
    rec4 = random.choices([' '.join([' -rec4', random.choice(recskills)]), ''], weights=([0, 1]), k=1)[0]
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
    bnu = random.choices([' -bnu', ''], weights=([10, 1]), k=1)[0]
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
    ier1 = random.randint(7, 14)
    ier2 = random.randint(ier1, 14)
    ier = ' '.join([' -ier', str(ier1), str(ier2)])
    iebr = ' '.join([' -iebr', str(random.randint(7, 14))])
    ieor = ' '.join([' -ieor', str(random.randint(33, 100))])
    iesr = ' '.join([' -iesr', str(random.randint(33, 100))])
    iequip = random.choices(['', ier, iebr, ieor, iesr], weights=([1, 1, 1, 13, 1]), k=1)[0]
    ierr1 = random.randint(7, 14)
    ierr2 = random.randint(ierr1, 14)
    ierr = ' '.join([' -ierr', str(ierr1), str(ierr2)])
    ierbr = ' '.join([' -ierbr', str(random.randint(7, 14))])
    ieror = ' '.join([' -ieror', str(random.randint(33, 100))])
    iersr = ' '.join([' -iersr', str(random.randint(33, 100))])
    requip = random.choices(['', ierr, ierbr, ieror, iersr], weights=([1, 1, 1, 13, 1]), k=1)[0]
    csb1 = random.randint(1, 32)
    csb2 = random.randint(csb1, 32)
    csb = ' '.join([' -csb', str(csb1), str(csb2)])
    mca = random.choices([' -mca', ''], weights=([1, 0]), k=1)[0]
    stra = random.choices([' -stra', ''], weights=([1, 0]), k=1)[0]
    saw = random.choices([' -saw', ''], weights=([1, 0]), k=1)[0]
    equips = ''.join([iequip, requip, csb, mca, stra, saw])

    # SHOPS
    sisr = ' '.join([' -sisr', str(random.randint(20, 40))])
    shopinv = random.choices(['', sisr, ' -sirt', ' -sie'], weights=([1, 13, 3, 0]), k=1)[0]
    sprv1 = random.randint(0, 65535)
    sprv2 = random.randint(sprv1, 65535)
    sprp1 = random.randint(75, 100)
    sprp2 = random.randint(sprp1, 125)
    sprv = ' '.join([' -sprv', str(sprv1), str(sprv2)])
    sprp = ' '.join([' -sprp', str(sprp1), str(sprp2)])
    shopprices = random.choices(['', sprv, sprp], weights=([1, 2, 15]), k=1)[0]
    ssf = random.choices(['', ' -ssf4', ' -ssf8', ' -ssf0'], weights=([13, 1, 1, 0]), k=1)[0]
    sdm = ' '.join([' -sdm', str(random.randint(4, 5))])
    npi = random.choices(['', ' -npi'], weights=([0, 1]), k=1)[0]
    snbr = random.choices(['', ' -snbr'], weights=([13, 1]), k=1)[0]
    snes = random.choices(['', ' -snes'], weights=([13, 1]), k=1)[0]
    snsb = random.choices(['', ' -snsb'], weights=([13, 1]), k=1)[0]
    shops = ''.join([shopinv, shopprices, ssf, sdm, npi, snbr, snes, snsb])

    # CHESTS
    ccontents = random.choices(['', ' -ccrt', ' -cce', ' '.join([' -ccsr', str(random.randint(20, 40))])],
                               weights=([1, 3, 0, 13]), k=1)[0]
    cms = random.choices(['', ' -cms'], weights=([0, 1]), k=1)[0]
    chests = ''.join([ccontents, cms])

    items = ''.join([s_inv, equips, shops, chests])

    # -----CUSTOM-----
    # SEE CUSTOM_SPRITES_PORTRAITS.PY

    # -----OTHER-----
    # COLISEUM
    co = random.choices(['', ' -cor', ' -cos'], weights=([0, 13, 1]), k=1)[0]
    cr = random.choices(['', ' -crs', ' -crr'], weights=([0, 1, 13]), k=1)[0]
    crvr1 = random.randint(30, 50)
    crvr2 = random.randint(crvr1, 75)
    visible = random.choices(['', ' '.join([' -crvr', str(crvr1), str(crvr2)])], weights=([0, 1]), k=1)[0]
    rmenu = random.choices(['', ' -crm'], weights=([1, 13]), k=1)[0]
    colo = ''.join([co, cr, visible, rmenu])

    # AUCTION HOUSE
    ari = random.choices(['', ' -ari'], weights=([0, 1]), k=1)[0]
    anca = random.choices(['', ' -anca'], weights=([0, 1]), k=1)[0]
    adeh = random.choices(['', ' -adeh'], weights=([0, 1]), k=1)[0]
    ah = ''.join([ari, anca, adeh])

    # MISC
    asprint = random.choices(['', ' -as'], weights=([0, 1]), k=1)[0]
    ond = random.choices(['', ' -ond'], weights=([0, 1]), k=1)[0]
    rr = random.choices(['', ' -rr'], weights=([0, 1]), k=1)[0]
    scan = random.choices(['', ' -scan'], weights=([1, 0]), k=1)[0]
    etimers = random.choices(['', ' -etr', ' -etn'], weights=([5, 1, 0]), k=1)[0]
    ychoices = [' -ymascot', ' -ycreature', ' -yimperial', ' -ymain', ' -yreflect', ' -ystone', ' -ysketch',
                ' -yrandom', ' -yremove', '']
    ychoice = random.choices(ychoices, weights=([1, 1, 1, 1, 1, 1, 1, 1, 1, 13]), k=1)[0]
    misc = ''.join([asprint, ond, rr, scan, etimers, ychoice])

    # CHALLENGES
    nmc = random.choices(['', ' -nmc'], weights=([1, 5]), k=1)[0]
    nee = random.choices(['', ' -nee'], weights=([13, 1]), k=1)[0]
    nil = random.choices(['', ' -nil'], weights=([1, 5]), k=1)[0]
    nfps = random.choices(['', ' -nfps'], weights=([0,1]), k=1)[0]
    nu = random.choices(['', ' -nu'], weights=([1, 10]), k=1)[0]
    nfp = random.choices(['', ' -nfp'], weights=([13, 1]), k=1)[0]
    kthr = random.choices(['', ' -kthr'], weights=([1, 0]), k=1)[0]
    pd = random.choices(['', ' -pd'], weights=([1, 0]), k=1)[0]
    challenges = ''.join([nmc, nee, nil, nfps, nu, nfp, kthr, pd])

    # BUG FIXES
    fs = random.choices(['', ' -fs'], weights=([0, 1]), k=1)[0]
    fe = random.choices(['', ' -fe'], weights=([0, 1]), k=1)[0]
    fvd = random.choices(['', ' -fvd'], weights=([0, 1]), k=1)[0]
    fr = random.choices(['', ' -fr'], weights=([0, 1]), k=1)[0]
    fj = random.choices(['', ' -fj'], weights=([0, 1]), k=1)[0]
    fbs = random.choices(['', ' -fbs'], weights=([0, 1]), k=1)[0]
    fedc = random.choices(['', ' -fedc'], weights=([0, 1]), k=1)[0]
    bugfixes = ''.join([fs, fe, fvd, fr, fj, fbs, fedc])

    other = ''.join([colo, ah, challenges, misc, bugfixes])

    flagset = ''.join([game, party, battle, magic, items, other])
    return flagset

def chaos():
    # -----GAME-----
    # SETTINGS
    mode = random.choices(["-ow", "-cg"], weights=([1, 7]), k=1)[0]
    slog = random.choices(['', ' -sl'], weights=([13, 1]), k=1)[0]
    settings = ''.join([mode, slog])

    # KEFKA'S TOWER & STATUE SKIP
    ktcr1 = random.randint(3, 9)
    ktcr2 = random.randint(ktcr1, 12)
    kter1 = random.randint(5, 14)
    kter2 = random.randint(kter1, 16)
    ktdr1 = random.randint(0, 2)
    ktdr2 = random.randint(ktdr1, 3)
    stcr1 = random.randint(4, 10)
    stcr2 = random.randint(stcr1, 13)
    ster1 = random.randint(6, 15)
    ster2 = random.randint(ster1, 17)
    stdr1 = random.randint(1, 3)
    stdr2 = random.randint(stdr1, 4)
    stno = random.choices([True, False], weights=([4, 1]), k=1)[0]

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
    sc4 = random.choices([' -sc4 random', ' -sc4 randomngu', ''], weights=([1, 1, 10]), k=1)[0]
    sparty = ''.join([sc1, sc2, sc3, sc4])

    # SWORDTECHS
    fst = random.choices([' -fst', ''], weights=([1, 0]), k=1)[0]
    sel = random.choices([' -sel', ''], weights=([1, 3]), k=1)[0]
    swdtech = ''.join([fst, sel])

    # BLITZES
    brl = random.choices([' -brl', ''], weights=([5, 1]), k=1)[0]
    bel = random.choices([' -bel', ''], weights=([1, 5]), k=1)[0]
    blitz = ''.join([brl, bel])

    # LORES
    slr1 = random.randint(0, 12)
    slr2 = random.randint(slr1, 16)
    slrr = ' '.join([' -slr', str(slr1), str(slr2)])
    slr = random.choices([slrr, ''], weights=([5, 1]), k=1)[0]
    lmprp1 = random.randint(25, 125)
    lmprp2 = random.randint(lmprp1, 175)
    lmprv1 = random.randint(10, 60)
    lmprv2 = random.randint(lmprv1, 80)
    lmprp = ' '.join([' -lmprp', str(lmprp1), str(lmprp2)])
    lmprv = ' '.join([' -lmprv', str(lmprv1), str(lmprv2)])
    loremp = random.choices(['', ' -lmps', lmprp, lmprv], weights=([1, 3, 5, 3]), k=1)[0]
    lel = random.choices([' -lel', ''], weights=([13, 1]), k=1)[0]
    lores = ''.join([slr, loremp, lel])

    # RAGES
    srr1 = random.randint(0, 25)
    srr2 = random.randint(srr1, 50)
    srr = ' '.join([' -srr', str(srr1), str(srr2)])
    srages = random.choices(['', srr], weights=([1, 10]), k=1)[0]
    rnl = random.choices([' -rnl', ''], weights=([1, 0]), k=1)[0]
    rnc = random.choices([' -rnc', ''], weights=([10, 1]), k=1)[0]
    rage = ''.join([srages, rnl, rnc])

    # DANCES
    sdr1 = random.randint(0, 4)
    sdr2 = random.randint(sdr1, 6)
    sdr = ' '.join([' -sdr', str(sdr1), str(sdr2)])
    das = random.choices([' -das', ''], weights=([1, 0]), k=1)[0]
    dda = random.choices([' -dda', ''], weights=([1, 0]), k=1)[0]
    dns = random.choices([' -dns', ''], weights=([1, 0]), k=1)[0]
    d_el = random.choices([' -del', ''], weights=([1, 13]), k=1)[0]
    dance = ''.join([sdr, das, dda, dns, d_el])

    # CHARACTERS
    sal = random.choices([' -sal', ''], weights=([7, 1]), k=1)[0]
    sn = random.choices([' -sn', ''], weights=([1, 7]), k=1)[0]
    eu = random.choices([' -eu', ''], weights=([7, 1]), k=1)[0]
    csrp1 = random.randint(50, 120)
    csrp2 = random.randint(csrp1, 160)
    csrp = ' '.join([' -csrp', str(csrp1), str(csrp2)])
    cstats = ''.join([sal, sn, eu, csrp])

    # COMMANDS
    scc = random.choices([' -scc', ''], weights=([1, 5]), k=1)[0]
    com = random.choices([' -com 99999999999999999999999999', '', ' -com 98989898989898989898989898'],
                         weights=([7, 1, 7]), k=1)[0]
    recskills = ['10', '6', '14', '19', '24', '26', '22', '12', '3', '28', '16', '11', '27', '13', '15', '5',
                 '7', '8', '9', '23']
    rec1 = random.choices([' -rec1 28', ''], weights=([10, 1]), k=1)[0]
    rec2 = random.choices([' -rec2 23', ''], weights=([7, 1]), k=1)[0]
    rec3 = random.choices([' '.join([' -rec3', random.choice(recskills)]), ''], weights=([1, 10]), k=1)[0]
    rec4 = random.choices([' '.join([' -rec4', random.choice(recskills)]), ''], weights=([1, 10]), k=1)[0]
    rec5 = random.choices([' '.join([' -rec5', random.choice(recskills)]), ''], weights=([1, 10]), k=1)[0]
    commands = ''.join([scc, com, rec1, rec2, rec3, rec4, rec5])

    party = ''.join([sparty, swdtech, blitz, lores, rage, dance, cstats, commands])

    # -----BATTLE-----
    xpm = ' '.join([' -xpm', str(random.choices([2, 3, 4, 5, 6], weights=([2, 10, 6, 3, 1]), k=1)[0])])
    gpm = ' '.join([' -gpm', str(random.choices([3, 4, 5, 6, 7, 8, 9, 10], weights=([1, 2, 10, 6, 3, 2, 1, 1]),
                                                k=1)[0])])
    mpm = ' '.join([' -mpm', str(random.choices([3, 4, 5, 6, 7, 8, 9, 10], weights=([1, 2, 10, 6, 3, 2, 1, 1]),
                                                k=1)[0])])
    nxppd = random.choices([' -nxppd', ''], weights=([7, 1]), k=1)[0]
    xpmpgp = ''.join([xpm, gpm, mpm, nxppd])

    # BOSSES
    bb = random.choices([' -bbr', ' -bbs', ''], weights=([5, 10, 1]), k=1)[0]
    bmbd = random.choices([' -bmbd', ''], weights=([1, 10]), k=1)[0]
    srp3 = random.choices([' -srp3', ''], weights=([1, 10]), k=1)[0]
    bnds = random.choices([' -bnds', ''], weights=([1, 8]), k=1)[0]
    be = random.choices([' -be', ''], weights=([13, 1]), k=1)[0]
    bnu = random.choices([' -bnu', ''], weights=([10, 1]), k=1)[0]
    bosses = ''.join([bb, bmbd, srp3, bnds, be, bnu])

    # BOSS AI
    dgne = random.choices([' -dgne', ''], weights=([10, 1]), k=1)[0]
    wnz = random.choices([' -wnz', ''], weights=([10, 1]), k=1)[0]
    mmnu = random.choices([' -mmnu', ''], weights=([13, 1]), k=1)[0]
    cmd = random.choices([' -cmd', ''], weights=([1, 0]), k=1)[0]
    b_ai = ''.join([dgne, wnz, mmnu, cmd])

    # SCALING
    scale_opt = ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5']
    lspf = ' '.join([' -lsp', random.choices(scale_opt, weights=([0, 1, 1, 10, 5, 3, 1, 0, 0, 0]), k=1)[0]])
    lsaf = ' '.join([' -lsa', random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    lshf = ' '.join([' -lsh', random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    lstf = ' '.join([' -lst', random.choices(scale_opt, weights=([0, 1, 5, 10, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    hmpf = ' '.join([' -hmp', random.choices(scale_opt, weights=([0, 1, 1, 10, 5, 3, 1, 0, 0, 0]), k=1)[0]])
    hmaf = ' '.join([' -hma', random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    hmhf = ' '.join([' -hmh', random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    hmtf = ' '.join([' -hmt', random.choices(scale_opt, weights=([0, 1, 5, 10, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    xgpf = ' '.join([' -xgp', random.choices(scale_opt, weights=([0, 1, 1, 10, 5, 3, 1, 0, 0, 0]), k=1)[0]])
    xgaf = ' '.join([' -xga', random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    xghf = ' '.join([' -xgh', random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    xgtf = ' '.join([' -xgt', random.choices(scale_opt, weights=([0, 1, 5, 10, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    asrf = ' '.join([' -asr', random.choices(scale_opt, weights=([0, 0, 3, 10, 2, 1, 0, 0, 0, 0]), k=1)[0]])
    asef = ' '.join([' -ase', random.choices(scale_opt, weights=([0, 0, 3, 10, 2, 1, 0, 0, 0, 0]), k=1)[0]])
    lscale = random.choices([lspf, lsaf, lshf, lstf, ''], weights=([7, 2, 2, 1, 0]), k=1)[0]
    hmscale = random.choices([hmpf, hmaf, hmhf, hmtf, ''], weights=([7, 2, 2, 1, 0]), k=1)[0]
    xgscale = random.choices([xgpf, xgaf, xghf, xgtf, ''], weights=([7, 2, 2, 1, 0]), k=1)[0]
    ascale = random.choices([asrf, asef, ''], weights=([1, 7, 0]), k=1)[0]
    msl = ' '.join([' -msl', str(random.randint(45, 80))])
    eel = ' '.join([' -eel', str(random.randint(0, 15))])
    sfb = random.choices([' -sfb', ''], weights=([0, 1]), k=1)[0]
    sed = random.choices([' -sed', ''], weights=([7, 1]), k=1)[0]
    scaling = ''.join([lscale, hmscale, xgscale, ascale, msl, eel, sfb, sed])

    # ENCOUNTERS
    renc = random.choices(['', ' -res', ' '.join([' -rer', str(random.randint(0, 33))])], weights=([1, 10, 10]), k=1)[0]
    fenc = random.choices(['', ' '.join([' -fer', str(random.randint(0, 33))])], weights=([1, 10]), k=1)[0]
    escr = ' '.join([' -escr', str(random.randint(75, 100))])
    encounters = ''.join([renc, fenc, escr])

    battle = ''.join([bosses, b_ai, scaling, encounters, xpmpgp])

    # -----MAGIC-----
    # ESPERS
    esr1 = random.randint(1, 3)
    esr2 = random.randint(esr1, 5)
    esr = ' '.join([' -esr', str(esr1), str(esr2)])
    ess = random.choices(['', esr, ' -esrr', ' -ess', ' -essrr', ' -esrt'], weights=([1, 7, 2, 2, 2, 3]), k=1)[0]
    ebonus = random.choices(['', ' '.join([' -ebr', str(random.randint(67, 100))]), ' -ebs'], weights=([1, 7, 3]),
                            k=1)[0]
    emprp1 = random.randint(50, 125)
    emprp2 = random.randint(emprp1, 150)
    emprv1 = random.randint(50, 99)
    emprv2 = random.randint(emprv1, 120)
    eer1 = random.randint(3, 8)
    eer2 = random.randint(eer1, 10)
    emprp = ' '.join([' -emprp', str(emprp1), str(emprp2)])
    emprv = ' '.join([' -emprv', str(emprv1), str(emprv2)])
    emp = random.choices(['', emprp, emprv, ' -emps'], weights=([1, 7, 3, 3]), k=1)[0]
    eer = ' '.join([' -eer', str(eer1), str(eer2)])
    eebr = ' '.join([' -eebr', str(random.randint(3, 9))])
    eeq = random.choices([eer, eebr, ''], weights=([1, 2, 7]), k=1)[0]
    ems = random.choices(['', ' -ems'], weights=([7, 1]), k=1)[0]
    espers = ''.join([ess, ebonus, emp, eeq, ems])

    # NATURAL MAGIC
    nm1 = random.choices(['', ' -nm1 random'], weights=([1, 10]), k=1)[0]
    nm2 = random.choices(['', ' -nm2 random'], weights=([1, 10]), k=1)[0]
    rnl1 = random.choices(['', ' -rnl1'], weights=([0, 1]), k=1)[0]
    rnl2 = random.choices(['', ' -rnl2'], weights=([0, 1]), k=1)[0]
    rns1 = random.choices(['', ' -rns1'], weights=([0, 1]), k=1)[0]
    rns2 = random.choices(['', ' -rns2'], weights=([0, 1]), k=1)[0]
    m_indicator = random.choices(['', ' -nmmi'], weights=([0, 1]), k=1)[0]
    nmagic = ''.join([nm1, nm2, rnl1, rnl2, rns1, rns2, m_indicator])

    magic = ''.join([espers, nmagic])

    # -----ITEMS-----
    # STARTING GOLD/ITEMS
    gp = ' '.join([' -gp', str(random.randint(0, 100000))])
    smc = ' '.join([' -smc', random.choices(['1', '2', '3'], weights=([1, 2, 7]), k=1)[0]])
    sws = ' '.join([' -sws', str(random.randint(0, 10))])
    sfd = ' '.join([' -sfd', str(random.randint(0, 10))])
    sto = ' '.join([' -sto', str(random.randint(0, 6))])
    s_inv = ''.join([gp, smc, sfd, sto, sws])

    # ITEMS
    ier1 = random.randint(4, 8)
    ier2 = random.randint(ier1, 10)
    ier = ' '.join([' -ier', str(ier1), str(ier2)])
    iebr = ' '.join([' -iebr', str(random.randint(4, 10))])
    ieor = ' '.join([' -ieor', str(random.randint(15, 75))])
    iesr = ' '.join([' -iesr', str(random.randint(15, 75))])
    iequip = random.choices(['', ier, iebr, ieor, iesr], weights=([1, 2, 2, 7, 2]), k=1)[0]
    ierr1 = random.randint(4, 8)
    ierr2 = random.randint(ierr1, 10)
    ierr = ' '.join([' -ierr', str(ierr1), str(ierr2)])
    ierbr = ' '.join([' -ierbr', str(random.randint(4, 10))])
    ieror = ' '.join([' -ieror', str(random.randint(15, 75))])
    iersr = ' '.join([' -iersr', str(random.randint(15, 75))])
    requip = random.choices(['', ierr, ierbr, ieror, iersr], weights=([1, 2, 2, 7, 2]), k=1)[0]
    csb1 = random.randint(1, 32)
    csb2 = random.randint(csb1, 32)
    csb = ' '.join([' -csb', str(csb1), str(csb2)])
    mca = random.choices([' -mca', ''], weights=([13, 1]), k=1)[0]
    stra = random.choices([' -stra', ''], weights=([1, 0]), k=1)[0]
    saw = random.choices([' -saw', ''], weights=([1, 0]), k=1)[0]
    equips = ''.join([iequip, requip, csb, mca, stra, saw])

    # SHOPS
    sisr = ' '.join([' -sisr', str(random.randint(10, 80))])
    shopinv = random.choices(['', sisr, ' -sirt', ' -sie'], weights=([3, 10, 5, 1]), k=1)[0]
    sprv1 = random.randint(0, 65535)
    sprv2 = random.randint(sprv1, 65535)
    sprp1 = random.randint(25, 125)
    sprp2 = random.randint(sprp1, 175)
    sprv = ' '.join([' -sprv', str(sprv1), str(sprv2)])
    sprp = ' '.join([' -sprp', str(sprp1), str(sprp2)])
    shopprices = random.choices(['', sprv, sprp], weights=([1, 2, 7]), k=1)[0]
    ssf = random.choices(['', ' -ssf4', ' -ssf8', ' -ssf0'], weights=([7, 1, 1, 0]), k=1)[0]
    sdm = ' '.join([' -sdm', str(random.randint(3, 5))])
    npi = random.choices(['', ' -npi'], weights=([1, 13]), k=1)[0]
    snbr = random.choices(['', ' -snbr'], weights=([7, 1]), k=1)[0]
    snes = random.choices(['', ' -snes'], weights=([7, 1]), k=1)[0]
    snsb = random.choices(['', ' -snsb'], weights=([7, 1]), k=1)[0]
    shops = ''.join([shopinv, shopprices, ssf, sdm, npi, snbr, snes, snsb])

    # CHESTS
    ccontents = random.choices(['', ' -ccrt', ' -cce', ' '.join([' -ccsr', str(random.randint(10, 80))])],
                               weights=([1, 6, 1, 13]), k=1)[0]
    cms = random.choices(['', ' -cms'], weights=([1, 13]), k=1)[0]
    chests = ''.join([ccontents, cms])

    items = ''.join([s_inv, equips, shops, chests])

    # -----CUSTOM-----
    # SEE CUSTOM_SPRITES_PORTRAITS.PY

    # -----OTHER-----
    # COLISEUM
    co = random.choices(['', ' -cor', ' -cos'], weights=([1, 7, 1]), k=1)[0]
    cr = random.choices(['', ' -crs', ' -crr'], weights=([1, 1, 7]), k=1)[0]
    crvr1 = random.randint(20, 80)
    crvr2 = random.randint(crvr1, 150)
    visible = random.choices(['', ' '.join([' -crvr', str(crvr1), str(crvr2)])], weights=([1, 10]), k=1)[0]
    rmenu = random.choices(['', ' -crm'], weights=([1, 13]), k=1)[0]
    colo = ''.join([co, cr, visible, rmenu])

    # AUCTION HOUSE
    ari = random.choices(['', ' -ari'], weights=([0, 1]), k=1)[0]
    anca = random.choices(['', ' -anca'], weights=([0, 1]), k=1)[0]
    adeh = random.choices(['', ' -adeh'], weights=([1, 13]), k=1)[0]
    ah = ''.join([ari, anca, adeh])

    # MISC
    asprint = random.choices(['', ' -as'], weights=([0, 1]), k=1)[0]
    ond = random.choices(['', ' -ond'], weights=([1, 13]), k=1)[0]
    rr = random.choices(['', ' -rr'], weights=([1, 13]), k=1)[0]
    scan = random.choices(['', ' -scan'], weights=([13, 1]), k=1)[0]
    etimers = random.choices(['', ' -etr', ' -etn'], weights=([2, 3, 1]), k=1)[0]
    ychoices = [' -ymascot', ' -ycreature', ' -yimperial', ' -ymain', ' -yreflect', ' -ystone', ' -ysketch',
                ' -yrandom', ' -yremove', '']
    ychoice = random.choices(ychoices, weights=([1, 1, 1, 1, 1, 1, 1, 1, 2, 10]), k=1)[0]
    misc = ''.join([asprint, ond, rr, scan, etimers, ychoice])

    # CHALLENGES
    nmc = random.choices(['', ' -nmc'], weights=([1, 5]), k=1)[0]
    nee = random.choices(['', ' -nee'], weights=([7, 1]), k=1)[0]
    nil = random.choices(['', ' -nil'], weights=([1, 7]), k=1)[0]
    nfps = random.choices(['', ' -nfps'], weights=([1, 13]), k=1)[0]
    nu = random.choices(['', ' -nu'], weights=([1, 6]), k=1)[0]
    nfp = random.choices(['', ' -nfp'], weights=([7, 1]), k=1)[0]
    kthr = random.choices(['', ' -kthr'], weights=([13, 1]), k=1)[0]
    pd = random.choices(['', ' -pd'], weights=([13, 1]), k=1)[0]
    challenges = ''.join([nmc, nee, nil, nfps, nu, nfp, kthr, pd])

    # BUG FIXES
    fs = random.choices(['', ' -fs'], weights=([0, 1]), k=1)[0]
    fe = random.choices(['', ' -fe'], weights=([1, 13]), k=1)[0]
    fvd = random.choices(['', ' -fvd'], weights=([1, 13]), k=1)[0]
    fr = random.choices(['', ' -fr'], weights=([1, 13]), k=1)[0]
    fj = random.choices(['', ' -fj'], weights=([0, 1]), k=1)[0]
    fbs = random.choices(['', ' -fbs'], weights=([1, 13]), k=1)[0]
    fedc = random.choices(['', ' -fedc'], weights=([0, 1]), k=1)[0]
    bugfixes = ''.join([fs, fe, fvd, fr, fj, fbs, fedc])

    other = ''.join([colo, ah, challenges, misc, bugfixes])

    flagset = ''.join([game, party, battle, magic, items, other])
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
    kter1 = random.randint(0, 27)
    kter2 = random.randint(kter1, 27)
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
    skills = ['10', '06', '14', '19', '24', '26', '22', '12', '03', '28', '16', '11', '27', '13', '15', '05',
              '07', '08', '09', '23', '97', '98', '99', '00']
    nmskills = ['10', '06', '14', '19', '24', '26', '22', '12', '28', '16', '11', '27', '13', '15', '05',
                '07', '08', '09', '23', '97', '98', '99', '00']
    recskills = ['10', '06', '14', '19', '24', '26', '22', '12', '03', '28', '16', '11', '27', '13', '15', '05',
                 '07', '08', '09', '23']
    scc = random.choice([' -scc', ''])
    mcount = 0
    ccount = 0
    coms = ""
    while mcount < 2 and ccount < 13:
        rc = random.choice(skills)
        if rc == '03':
            mcount += 1
        ccount += 1
        coms += random.choice(skills)
    if len(coms) < 26:
        while ccount < 13:
            ccount += 1
            coms += random.choice(nmskills)
    com = ''.join([' -com ', coms])
    rec1 = random.choice(['', ' -rec1 ' + random.choice(recskills)])
    rec2 = random.choice(['', ' -rec2 ' + random.choice(recskills)])
    rec3 = random.choice(['', ' -rec3 ' + random.choice(recskills)])
    rec4 = random.choice(['', ' -rec4 ' + random.choice(recskills)])
    rec5 = random.choice(['', ' -rec5 ' + random.choice(recskills)])
    commands = scc + com + rec1 + rec2 + rec3 + rec4 + rec5

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
    msl = ' -msl ' + str(random.randint(3, 99))
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


def rated():
    # -----GAME-----
    # SETTINGS
    mode = random.choices(["-ow", "-cg"], weights=([1, 7]), k=1)[0]
    slog = random.choice([" -sl", ""])
    settings = mode + slog

    # KEFKA'S TOWER & STATUE SKIP
    # i = range(3, 15)
    # j = [.925 ** k for k in i]
    # ktcr1 = random.choices(i, weights=j, k=1)[0]
    # ktcr2 = int((14-(round(14-ktcr1))/2))
    # stcr1 = random.choices(i, weights=j, k=1)[0]
    # stcr2 = int((14-(round(14-stcr1))/2))
    # i = range(0, 28)
    # j = [.925 ** k for k in i]
    # kter1 = random.choices(i, weights=j, k=1)[0]
    # kter2 = int((27-(round(27-kter1))/2))
    # ster1 = random.choices(i, weights=j, k=1)[0]
    # ster2 = int((27-(round(27-ster1))/2))
    # i = range(0, 9)
    # j = [.5 ** k for k in i]
    # ktdr1 = random.choices(i, weights=j, k=1)[0]
    # ktdr2 = int((8-(round(8-ktdr1))/2))
    # stdr1 = random.choices(i, weights=j, k=1)[0]
    # stdr2 = int((8-(round(8-ktdr1))/2))
    # stno = random.choice([True, False])
    #
    # if stno:
    #     kt = ' -ktcr ' + str(ktcr1) + " " + str(ktcr2) + ' -kter ' + str(kter1) + " " + str(kter2) + ' -ktdr ' + str(
    #     ktdr1) + " " + \
    #      str(ktdr2) + ' -stno'
    # else:
    #     kt = ' -ktcr ' + str(ktcr1) + " " + str(ktcr2) + ' -kter ' + str(kter1) + " " + str(kter2) + ' -ktdr ' + str(
    #     ktdr1) + " " + \
    #      str(ktdr2) + ' -stcr ' + str(stcr1) + " " + str(stcr2) + ' -ster ' + str(ster1) + " " + str(ster2) + \
    #      ' -stdr ' + str(stdr1) + " " + str(stdr2)

    kt = None
    while kt is None:
        try:
            i = range(3, 15)
            j = [.8 ** k for k in i]
            ktcr1 = random.choices(i, weights=j, k=1)[0]
            ktcr2 = random.choice(range(ktcr1, int((15 - (round(14 - ktcr1)) / 2))))
            stcr1 = random.choices(i, weights=j, k=1)[0]
            stcr2 = random.choice(range(stcr1, int((15 - (round(14 - stcr1)) / 2))))
            i = range(0, 28)
            j = [.8 ** k for k in i]
            kter1 = random.choices(i, weights=j, k=1)[0]
            kter2 = random.choice(range(kter1, int((28 - (round(27 - kter1)) / 2))))
            ster1 = random.choices(i, weights=j, k=1)[0]
            ster2 = random.choice(range(ster1, int((28 - (round(27 - ster1)) / 2))))
            i = range(0, 9)
            j = [.5 ** k for k in i]
            ktdr1 = random.choices(i, weights=j, k=1)[0]
            ktdr2 = random.choice(range(ktdr1, int((9 - (round(8 - ktdr1)) / 2))))
            stdr1 = random.choices(i, weights=j, k=1)[0]
            stdr2 = random.choice(range(stdr1, int((9 - (round(8 - ktdr1)) / 2))))
            stno = random.choice([True, False])

            if stno:
                kt = ' -ktcr ' + str(ktcr1) + " " + str(ktcr2) + ' -kter ' + str(kter1) + " " + str(
                    kter2) + ' -ktdr ' + str(
                    ktdr1) + " " + \
                     str(ktdr2) + ' -stno'
            else:
                kt = ' -ktcr ' + str(ktcr1) + " " + str(ktcr2) + ' -kter ' + str(kter1) + " " + str(
                    kter2) + ' -ktdr ' + str(
                    ktdr1) + " " + \
                     str(ktdr2) + ' -stcr ' + str(stcr1) + " " + str(stcr2) + ' -ster ' + str(ster1) + " " + str(
                    ster2) + \
                     ' -stdr ' + str(stdr1) + " " + str(stdr2)
        except:
            pass

    game = settings + kt

    # -----PARTY-----
    # STARTING PARTY
    sc1 = random.choice([' -sc1 random', ' -sc1 randomngu'])
    sc2 = random.choice([' -sc2 random', ' -sc2 randomngu', ''])
    sc3 = random.choice([' -sc3 random', ' -sc3 randomngu', ''])
    sc4 = random.choice([' -sc4 random', ' -sc4 randomngu', ''])
    sparty = sc1 + sc2 + sc3 + sc4

    # SWORDTECHS
    fst = ' -fst'
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
    rnl = ' -rnl'
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
    skills = ['10', '06', '14', '19', '24', '26', '22', '12', '03', '28', '16', '11', '27', '13', '15', '05',
              '07', '08', '09', '23', '97', '98', '99', '00']
    nmskills = ['10', '06', '14', '19', '24', '26', '22', '12', '28', '16', '11', '27', '13', '15', '05',
                '07', '08', '09', '23', '97', '98', '99', '00']
    recskills = ['10', '06', '14', '19', '24', '26', '22', '12', '03', '28', '16', '11', '27', '13', '15', '05',
                 '07', '08', '09', '23']
    scc = random.choice([' -scc', ''])
    mcount = 0
    ccount = 0
    coms = ""
    while mcount < 2 and ccount < 13:
        rc = random.choice(skills)
        if rc == '03':
            mcount += 1
        ccount += 1
        coms += random.choice(skills)
        pass
        if len(coms) < 26:
            while ccount < 13:
                ccount += 1
                coms += random.choice(nmskills)
    com = ''.join([' -com ', coms])
    rec1 = random.choice(['', ' -rec1 ' + random.choice(recskills)])
    rec2 = random.choice(['', ' -rec2 ' + random.choice(recskills)])
    rec3 = random.choice(['', ' -rec3 ' + random.choice(recskills)])
    rec4 = random.choice(['', ' -rec4 ' + random.choice(recskills)])
    rec5 = random.choice(['', ' -rec5 ' + random.choice(recskills)])
    commands = scc + com + rec1 + rec2 + rec3 + rec4 + rec5

    party = sparty + swdtech + blitz + lores + rage + dance + cstats + commands

    # -----BATTLE-----
    i = range(1, 256)
    j = [.8 ** k for k in i]
    xpm = ' -xpm ' + str((random.choices(i, weights=j, k=1))[0])
    gpm = ' -gpm ' + str((random.choices(i, weights=j, k=1))[0])
    mpm = ' -mpm ' + str((random.choices(i, weights=j, k=1))[0])
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
    msl = ' -msl ' + str(random.randint(3, 99))
    eel = ' -eel ' + str(random.randint(0, 99))
    sfb = random.choice([' -sfb', ''])
    sed = random.choice([' -sed', ''])
    scaling = lscale + hmscale + xgscale + ascale + msl + eel + sfb + sed

    # ENCOUNTERS
    i = range(1, 99)
    j = [.925 ** k for k in i]
    renc = random.choice(['', ' -res', ' -rer ' + str(random.choices(i, weights=j, k=1)[0])])
    fenc = random.choice(['', ' -fer ' + str(random.choices(i, weights=j, k=1)[0])])
    i = range(1, 101)
    j = [1.1 ** k for k in i]
    escr = ' -escr ' + str(random.choices(i, weights=j, k=1)[0])
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
    i = range(1, 256)
    j = [.91 ** k for k in i]
    csb1 = random.choices(i, weights=j, k=1)[0]
    if csb1 < 240:
        csb2 = csb1 + random.randint(0, 15)
    else:
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
    anca = ' -anca'
    adeh = random.choice(['', ' -adeh'])
    ah = ''.join([ari, anca, adeh])

    # MISC
    asprint = ' -as'
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
    fs = ' -fs'
    fe = random.choice(['', ' -fe'])
    fvd = random.choice(['', ' -fvd'])
    fr = random.choice(['', ' -fr'])
    fj = ' -fj'
    fbs = random.choice(['', ' -fbs'])
    fedc = random.choice(['', ' -fedc'])
    bugfixes = ''.join([fs, fe, fvd, fr, fj, fbs, fedc])

    other = ''.join([colo, ah, challenges, misc, bugfixes])

    flagset = game + party + battle + magic + items + other
    return flagset

# print(chaos())

skill_index = {
    '00': 'Fight',
    '10': 'Blitz',
    '06': 'Capture',
    '14': 'Control',
    '19': 'Dance',
    '24': 'GP Rain',
    '26': 'Health',
    '22': 'Jump',
    '12': 'Lore',
    '03': 'Morph',
    '28': 'Possess',
    '16': 'Rage',
    '11': 'Runic',
    '27': 'Shock',
    '13': 'Sketch',
    '15': 'Slot',
    '05': 'Steal',
    '07': 'SwdTech',
    '08': 'Throw',
    '09': 'Tools',
    '23': 'X-Magic',
    '97': 'None',
    '98': 'Random Unique',
    '99': 'Random'
}

#useskills = list(skill_index.keys())
#useskills.remove('00')
recskills = ['10', '06', '14', '19', '24', '26', '22', '12', '03', '28', '16', '11', '27', '13', '15', '05',
             '07', '08', '09', '23']

# Create a dictionary with all flag options
flag_list = {
    # SETTINGS
    "mode": ['ow', 'cg'],
    "sl": [True, False], # spoiler log

    # KT ENTRANCE REQUIREMENTS (by convention, process as [min, max].
    "ktcr": [True, False], # modify KT character requirements
    "ktcr_1": [str(i) for i in range(3, 15)],
    "ktcr_2": [str(i) for i in range(3, 15)],
    "kter": [True, False], # modify KT esper requirements
    "kter_1": [str(i) for i in range(0, 28)],
    "kter_2": [str(i) for i in range(0, 28)],
    "ktdr": [True, False], # modify KT dragon requirements
    "ktdr_1": [str(i) for i in range(0, 9)],
    "ktdr_2": [str(i) for i in range(0, 9)],

    # KT SKIP REQUIREMENTS (by convention, process as [min, max].
    "stno": [True, False], # no KT skip
    "stcr": [True, False], # modify skip character requirements
    "stcr_1": [str(i) for i in range(3, 15)],
    "stcr_2": [str(i) for i in range(3, 15)],
    "ster": [True, False], # modify skip esper requirements
    "ster_1": [str(i) for i in range(0, 28)],
    "ster_2": [str(i) for i in range(0, 28)],
    "stdr": [True, False], # modify skip dragon requirements
    "stdr_1": [str(i) for i in range(0, 9)],
    "stdr_2": [str(i) for i in range(0, 9)],

    # STARTING PARTY (technically, can include "terra", etc.
    "sc1": ["random", "randomngu"],   # sc1 is required
    "sc2": [True, False],
    "sc2_1": ['random', 'randomngu'],
    "sc3": [True, False],
    "sc3_1": ['random', 'randomngu'],
    "sc4": [True, False],
    "sc4_1": ['random', 'randomngu'],

    "fst": [True, False],  # SWORDTECHS fast
    "sel": [True, False],  # everyone learns

    "brl": [True, False],  # BLITZES bum rush last
    "bel": [True, False],  # everyone learns

    "slr": [True, False],  # LORES random vs original
    "slr_1": [str(i) for i in range(25)], # LORES starting lores random
    "slr_2": [str(i) for i in range(25)], #
    "loremp": ['', 'lmps', 'lmprp', 'lmprv'],  # lore MP original, shuffle, random %, random value
    "lmprp_1": [str(i) for i in range(201)], # lore MP random percent
    "lmprp_2": [str(i) for i in range(201)], #
    "lmprv_1": [str(i) for i in range(100)], # lore MP random value
    "lmprv_2": [str(i) for i in range(100)], #
    "lel": [True, False],  # lore everyone learns

    "srr": [True, False],  # starting rages random
    "srr_1": [str(i) for i in range(256)], # RAGES starting rages random
    "srr_2": [str(i) for i in range(256)], #
    "rnl": [True, False],  # rage no leap
    "rnc": [True, False],  # rage no charm

    "sdr":  [True, False],  # starting dances random
    "sdr_1": [str(i) for i in range(9)], # DANCES starting dances random
    "sdr_2": [str(i) for i in range(9)],
    "das": [True, False], # Dance ability shuffle
    "dda": [True, False], # Dance display abilities
    "dns": [True, False], # Dance no stumble
    "del": [True, False], # Dance everybody learns

    "sal": [True, False], # CHARACTERS:  Start average level
    "sn": [True, False],  # start naked
    "eu": [True, False], # equippable Umaro
    "csrp": [True, False], # non-vanilla character stats
    "csrp_1": [str(i) for i in range(201)], # Character stats %
    "csrp_2": [str(i) for i in range(201)],

    "scc": [True, False], # COMMANDS: Shuffle commands
    "com_01": list(skill_index.keys()), # command string values
    "com_02": list(skill_index.keys()),
    "com_03": list(skill_index.keys()),
    "com_04": list(skill_index.keys()),
    "com_05": list(skill_index.keys()),
    "com_06": list(skill_index.keys()),
    "com_07": list(skill_index.keys()),
    "com_08": list(skill_index.keys()),
    "com_09": list(skill_index.keys()),
    "com_10": list(skill_index.keys()),
    "com_11": list(skill_index.keys()),
    "com_12": list(skill_index.keys()),
    "com_13": list(skill_index.keys()),

    "rec1": [True, False],
    "rec1_1": recskills,  # Random exclude commands
    "rec2": [True, False],
    "rec2_1": recskills,
    "rec3": [True, False],
    "rec3_1": recskills,
    "rec4": [True, False],
    "rec4_1": recskills,
    "rec5": [True, False],
    "rec5_1": recskills,

    # -----BATTLE-----
    "xpm": [str(i) for i in range(256)], # xp multiplier
    "gpm": [str(i) for i in range(256)], # gp multiplier
    "mpm": [str(i) for i in range(256)], # MP multiplier
    "nxppd": [True, False], # no XP party divide

    "bb": ['', 'bbr', 'bbs'], # BOSSES original, shuffle, random
    "bmbd": [True, False], # mix bosses & dragons
    "srp3": [True, False], # shuffle/random Phunbaba 3
    "bnds": [True, False], # normalize & distort stats
    "be": [True, False], # Boss experience
    "bnu": [True, False], # Bosses no undead

    "dgne": [True, False], # BOSS AI:  doomgaze no escape
    "wnz": [True, False], # Wrexsoul no zinger
    "mmnu": [True, False], # magimaster no ultima
    "cmd": [True, False], # chadarnook more demon

    "ls": ['', 'lsa', 'lsh', 'lsp', 'lst'],  # level scaling options
    "lsp_1": ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'],
    "lsa_1": ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'],
    "lsh_1": ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'],
    "lst_1": ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'],

    "hm": ['', 'hma', 'hmh', 'hmp', 'hmt'],  # level scaling options
    "hmp_1": ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'],
    "hma_1": ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'],
    "hmh_1": ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'],
    "hmt_1": ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'],

    "xg": ['', 'xga', 'xgh', 'xgp', 'xgt'],  # level scaling options
    "xgp_1": ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'],
    "xga_1": ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'],
    "xgh_1": ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'],
    "xgt_1": ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'],

    "ascale":  ['', 'asr', 'ase'],   # ability scaling options
    "asr_1": ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'],
    "ase_1": ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'],

    "msl": [str(i) for i in range(3,100)], # max scale level
    "eel": [str(i) for i in range(100)], # extra enemy levels
    "sfb": [True, False], # scale final battles
    "sed": [True, False], # scale dragons

    "renc": ['', 'res', 'rer'],  # ENCOUNTERS random entounter original/shuffle/random
    "rer_1": [str(i) for i in range(101)],  # random encounter boss
    "fer": [True, False],  # Fixed encounter random
    "fer_1": [str(i) for i in range(101)], # fixed encounter random + boss %
    "escr": [True, False],  # escapable encounters random
    "escr_1": [str(i) for i in range(101)], # escapable encounters random + %

    # -----MAGIC-----,
    "es": ['', 'esr', 'esrr', 'ess', 'essrr', 'esrt'], # ESPER options
    "esr_1": [str(i) for i in range(6)], # ESPERS, esper spells random
    "esr_2": [str(i) for i in range(6)],

    "ebonus": ['', 'ebr', 'ebs'],  # esper bonus options
    "ebr_1": [str(i) for i in range(101)],

    "emp": ['', 'emprp', 'emprv', 'emps'], # esper MP value options
    "emprp_1": [str(i) for i in range(201)],
    "emprp_2": [str(i) for i in range(201)],
    "emprv_1": [str(i) for i in range(1,129)],
    "emprv_2": [str(i) for i in range(1,129)],

    "eeq": ['', 'eer', 'eebr'], # esper equippability options
    "eer_1": [str(i) for i in range(13)],
    "eer_2": [str(i) for i in range(13)],
    "eebr_1": [str(i) for i in range(13)],

    "ems": [True, False],  # esper multisummon

    "nm1": ['', 'random'], # NATURAL MAGIC none, random (can technically be any character too)
    "nm2": ['', 'random'],
    "rnl1": [True, False], # natural magic random levels
    "rnl2": [True, False],
    "rns1": [True, False], # natural magic random spells
    "rns2": [True, False],
    "nmmi": [True, False], # show menu indicator

    # -----ITEMS-----
    "gp": [str(i) for i in range(1000000)],  # STARTING GOLD/ITEMS
    "smc": [str(i) for i in range(4)],   # starting moogle charms
    "sws": [str(i) for i in range(11)],  # starting warp stones
    "sfd": [str(i) for i in range(11)],  # starting fenix downs
    "sto": [str(i) for i in range(9)],  # starting tools

    "iequip": ['', 'ier', 'iebr', 'ieor', 'iesr'], # equipable options
    "ier_1": [str(i) for i in range(15)], # equipable on # characters
    "ier_2": [str(i) for i in range(15)],
    "iebr_1": [str(i) for i in range(15)], # balanced random
    "ieor_1": [str(i) for i in range(-100, 101)], # original + random %
    "iesr_1": [str(i) for i in range(-100, 101)], # shuffle + random %

    "requip": ['', 'ierr', 'ierbr', 'ieror', 'iersr'], # equipable relics
    "ierr_1": [str(i) for i in range(15)], # equipable relics on # characters
    "ierr_2": [str(i) for i in range(15)],
    "ierbr_1": [str(i) for i in range(15)], # balanced random
    "ieror_1": [str(i) for i in range(-100, 101)],  # original + random %
    "iersr_1": [str(i) for i in range(-100, 101)],  # shuffle + random %

    # Note: this is an implicit sub-flag.  Here and elsewhere, should this be made explicit with, e.g.:
    "csb": [True, False],  # use cursed shield battle flag   ??
    "csb_1": [str(i) for i in range(1, 257)],  # cursed shield battles
    "csb_2": [str(i) for i in range(1, 257)],

    "mca": [True, False], # moogle charm all
    "stra": [True, False], # SwdTech Runic all
    "saw": [True, False], # stronger atma weapon

    "shopinv": ['', 'sisr', 'sirt', 'sie'], # Shop inventory options
    "sisr_1": [str(i) for i in range(101)], # random %

    "shopprices": ['', 'sprv', 'sprp'], # Shop prices options
    "sprv_1": [str(i) for i in range(65536)], # random value 1
    "sprv_2": [str(i) for i in range(65536)],  # random value 2
    "sprp_1": [str(i) for i in range(201)], # random percent
    "sprp_2": [str(i) for i in range(201)], # random percent

    "ssf": ['', 'ssf4', 'ssf8', 'ssf0'], # shop sell fraction (default is 1/2)
    "sdm": [str(i) for i in range(6)], # shop dried meats
    "npi": [True, False], # no priceless items
    "snbr": [True, False], # no breakable rods
    "snes": [True, False], # no elemental shields
    "snsb": [True, False], # no superballs

    "ccontents": ['', 'ccrt', 'cce', 'ccsr'], # chest content options
    "ccsr_1": [str(i) for i in range(101)], # chest content random %
    "cms": [True, False], # Chest monster-in-a-box shuffle

    # -----OTHER-----
    "co": ['', 'cor', 'cos'], # COLISEUM opponents options
    "cr": ['', 'crs', 'crr'], # Coliseum rewards options
    "crvr": [True, False], # Coliseum rewards visible
    "crvr_1": [str(i) for i in range(256)], # Coliseum rewards visible #
    "crvr_2": [str(i) for i in range(256)],  # Coliseum rewards visible #
    "crm": [True, False], # Coliseum rewards menu

    "ari": [True, False], # Auction house randomize items
    "anca": [True, False], # no chocobo / airship
    "adeh": [True, False], # door esper hint

    "as": [True, False], # auto sprint
    "ond": [True, False], # original name display
    "rr": [True, False], # Random RNG
    "scan": [True, False], # everyone has scan

    "etimers": ['', 'etr', 'etn'], # event timer options
    "ychoices": ['ymascot', 'ycreature', 'yimperial', 'ymain', 'yreflect', 'ystone', 'ysketch',
            'yrandom', 'yremove', ''],

    # CHALLENGES
    "nmc": [True, False], # no moogle charms
    "nee": [True, False], # no exp eggs
    "nil": [True, False], # no illuminas
    "nfps": [True, False], # no free paladin shields
    "nu": [True, False], # no Ultima
    "nfp": [True, False], #  no free progression
    "kthr": [True, False], # hide requirements
    "pd": [True, False], # permadeath

    # BUG FIXES
    "fs": [True, False], # fix sketch glitch
    "fe": [True, False], # fix evade glitch
    "fvd": [True, False], # fix vanish/doom glitch
    "fr": [True, False], # fix retort glitch
    "fj": [True, False], # fix jump glitches
    "fbs": [True, False], # fix boss skip in KT
    "fedc": [True, False] # fix enemy damage counter
}

flag_groups = {
    "mode": ["ow", "cg"],  # game mode
    "loremp": ['lmps', 'lmprp', 'lmprv'],  # LORE MP original, shuffle, random %, random value
    "bb": ['bbr', 'bbs'], # BOSSES original, shuffle, random
    "ls": ['lsa', 'lsh', 'lsp', 'lst'],  # level scaling options
    "hm": ['hma', 'hmh', 'hmp', 'hmt'],  # HP/MP scaling options
    "xg": ['xga', 'xgh', 'xgp', 'xgt'],  # XP/gold scaling options
    "ascale":  ['asr', 'ase'],   # ability scaling options
    "renc": ['res', 'rer'],  # ENCOUNTERS random entounter original/shuffle/random
    "es": ['esr', 'esrr', 'ess', 'essrr', 'esrt'], # ESPER options
    "ebonus": ['ebr', 'ebs'],  # esper bonus options
    "emp": ['emprp', 'emprv', 'emps'], # esper MP value options
    "eeq": ['eer', 'eebr'], # esper equippability options
    "iequip": ['ier', 'iebr', 'ieor', 'iesr'], # equipable options
    "requip": ['ierr', 'ierbr', 'ieror', 'iersr'], # equipable relics
    "shopinv": ['sisr', 'sirt', 'sie'], # Shop inventory options
    "shopprices": ['sprv', 'sprp'], # Shop prices options
    "ssf": ['ssf4', 'ssf8', 'ssf0'], # shop sell fraction (default is 1/2)
    "ccontents": ['ccrt', 'cce', 'ccsr'], # chest content options
    "co": ['cor', 'cos'], # COLISEUM opponents options
    "cr": ['crs', 'crr'], # Coliseum rewards options
    "etimers": ['etr', 'etn'], # event timer options
    "ychoices": ['ymascot', 'ycreature', 'yimperial', 'ymain', 'yreflect', 'ystone', 'ysketch', 'yrandom', 'yremove']
}

# Generate dictionary to look up flag group
flag_group_lookup = {}
for f in flag_groups.keys():
    for fl in flag_groups[f]:
        flag_group_lookup[fl] = f


def RandomSeed():
    # Generate a fully random seed object
    seed = {}
    for i in flag_list.keys():
        seed[i]  = random.choice(list(flag_list[i]))
    return seed


def DefaultSeed():
    # Return the default seed values for each setting
    seed = {
        "mode": 'ow', # Note, can't generate a seed without mode setting
        "sl": False, # spoiler log
        # KT REQUIREMENTS
        "ktcr": False,
        "ktcr_1": '3',
        "ktcr_2": '3',
        "kter": False,
        "kter_1": '0',
        "kter_2": '0',
        "ktdr": False,
        "ktdr_1": '0',
        "ktdr_2": '0',
        # KT SKIP REQUIREMENTS (by convention, process as [min, max].
        "stno": False,
        "stcr": True,
        "stcr_1": '3',
        "stcr_2": '3',
        "ster": True,
        "ster_1": '0',
        "ster_2": '0',
        "stdr": True,
        "stdr_1": '0',
        "stdr_2": '0',
        # STARTING PARTY (technically, can include "terra", etc.
        "sc1": "random",  # sc1 is required.  Note that if you submit without any starting party, it defaults to sc1 = "random".
        "sc2": False,
        "sc2_1": 'random',
        "sc3": False,
        "sc3_1": 'random',
        "sc4": False,
        "sc4_1": 'random',
        # SKILL MODIFIERS
        "fst": False,
        "sel": False,
        "brl": False,
        "bel": False,
        "slr": False,
        "slr_1": '0',
        "slr_2": '24',
        "loremp": '',
        "lmprp_1": '0',
        "lmprp_2": '200',
        "lmprv_1": '0',
        "lmprv_2": '99',
        "lel":  False,
        "srr": False,  # RAGES starting rages random
        "srr_1": '15',
        "srr_2": '255',
        "rnl": False,
        "rnc": False,
        "sdr":  False,  # DANCES starting dances random
        "sdr_1": '0',
        "sdr_2": '0',
        "das": False,
        "dda": False,
        "dns": False,
        "del": False,
        # CHARACTER STATS
        "sal": False,
        "sn": False,
        "eu": False,
        "csrp": False, # non-vanilla character stats
        "csrp_1": '100', # Character stats %
        "csrp_2": '100',
        # COMMANDS:
        "scc": False, # Shuffle commands
        "com_01": '03', # command string values
        "com_02": '05',
        "com_03": '07',
        "com_04": '08',
        "com_05": '09',
        "com_06": '10',
        "com_07": '11',
        "com_08": '12',
        "com_09": '13',
        "com_10": '15',
        "com_11": '19',
        "com_12": '16',
        "com_13": '17',
        "rec1": False,  # Random exclude commands
        "rec1_1": '28', # default exclude possess
        "rec2": False,
        "rec2_1": '28',  # default exclude possess
        "rec3": False,
        "rec3_1": '28',  # default exclude possess
        "rec4": False,
        "rec4_1": '28',  # default exclude possess
        "rec5": False,
        "rec5_1": '28',  # default exclude possess
        # -----BATTLE-----
        "xpm": '1', # xp multiplier
        "gpm": '1', # gp multiplier
        "mpm": '1', # MP multiplier
        "nxppd": False, # no XP party divide
        "bb": '', # BOSSES original
        "bmbd": False, # mix bosses & dragons
        "srp3": False, # shuffle/random Phunbaba 3
        "bnds": False, # normalize & distort stats
        "be": False, # Boss experience
        "bnu": False, # Bosses no undead
        "dgne": False, # BOSS AI:  doomgaze no escape
        "wnz":  False, # Wrexsoul no zinger
        "mmnu": False, # magimaster no ultima
        "cmd": False, # chadarnook more demon
        "ls": '',  # level scaling options
        "lsp_1": '2',
        "lsa_1": '0.5',
        "lsh_1": '0.5',
        "lst_1": '5',
        "hm": '',  # level scaling options
        "hmp_1": '2',
        "hma_1": '1',
        "hmh_1": '0.5',
        "hmt_1": '2',
        "xg": '',  # level scaling options
        "xgp_1": '2',
        "xga_1": '1',
        "xgh_1": '1',
        "xgt_1": '2',
        "ascale": '',   # ability scaling options
        "asr_1": '0.5',
        "ase_1": '2',
        "msl": '99', # max scale level
        "eel": '0', # extra enemy levels
        "sfb": False, # scale final battles
        "sed": False, # scale dragons
        "renc": '',  # ENCOUNTERS random entounter original/shuffle/random
        "rer_1": '100',  # random encounter boss
        "fer": False,  # Fixed encounter random
        "fer_1": '51', # fixed encounter random + boss %
        "escr": False,  # escapable encounters random
        "escr_1": '100', # escapable encounters random + %
        # -----MAGIC-----,
        "es": '', # ESPER spells
        "esr_1": '0', # ESPERS, esper spells random
        "esr_2": '5',
        "ebonus": '',  # esper bonus options
        "ebr_1": '100',
        "emp": '', # esper MP value options
        "emprp_1": '0',
        "emprp_2": '200',
        "emprv_1": '1',
        "emprv_2": '128',
        "eeq": '', # esper equippability options
        "eer_1": '12',
        "eer_2": '12',
        "eebr_1": '0',
        "ems": False,  # esper multisummon
        "nm1": '', # NATURAL MAGIC none, random (can technically be any character too)
        "nm2": '',
        "rnl1": False, # natural magic random levels
        "rnl2": False,
        "rns1": False, # natural magic random spells
        "rns2": False,
        "nmmi": False, # show menu indicator
        # -----ITEMS-----
        "gp": '0',  # STARTING GOLD/ITEMS
        "smc": '0',   # starting moogle charms
        "sws": '0',  # starting warp stones
        "sfd": '0',  # starting fenix downs
        "sto": '0',  # starting tools
        "iequip": '', # equipable options
        "ier_1": '1', # equipable on # characters
        "ier_2": '14',
        "iebr_1": '14', # balanced random
        "ieor_1": '-100', # original + random %
        "iesr_1": '-100', # shuffle + random %
        "requip": '', # equipable relics
        "ierr_1": '14', # equipable relics on # characters
        "ierr_2": '14',
        "ierbr_1": '0', # balanced random
        "ieror_1": '-100',  # original + random %
        "iersr_1": '33',  # shuffle + random %
        "csb": False,  # use cursed shield battle flag   ??
        "csb_1": '256',  # cursed shield battles
        "csb_2": '256',
        "mca": False, # moogle charm all
        "stra": False, # SwdTech Runic all
        "saw": False, # stronger atma weapon
        "shopinv": '', # Shop inventory options
        "sisr_1": '10', # random %
        "shopprices": '', # Shop prices options
        "sprv_1": '0', # random value 1
        "sprv_2": '65535',  # random value 2
        "sprp_1": '75', # random percent
        "sprp_2": '125', # random percent
        "ssf": '', # shop sell fraction (default is 1/2)
        "sdm": False, # shop dried meats
        "npi": False, # no priceless items
        "snbr": False, # no breakable rods
        "snes": False, # no elemental shields
        "snsb": False, # no superballs
        "ccontents": '', # chest content options
        "ccsr_1": '10', # chest content random %
        "cms": False, # Chest monster-in-a-box shuffle
        # -----OTHER-----
        "co": '', # COLISEUM opponents options
        "cr": '', # Coliseum rewards options
        "crvr": False, # Coliseum rewards visible
        "crvr_1": '0', # Coliseum rewards visible #
        "crvr_2": '255',  # Coliseum rewards visible #
        "crm": False, # Coliseum rewards menu
        "ari": False, # Auction house randomize items
        "anca": False, # no chocobo / airship
        "adeh": False, # door esper hint
        "as": False, # auto sprint
        "ond": False, # original name display
        "rr": False, # Random RNG
        "scan": False, # everyone has scan
        "etimers": '', # event timer options
        "ychoices": '',
        # CHALLENGES
        "nmc": False, # no moogle charms
        "nee":  False, # no exp eggs
        "nil": False, # no illuminas
        "nfps": False, # no free paladin shields
        "nu": False, # no Ultima
        "nfp": False, #  no free progression
        "kthr": False, # hide requirements
        "pd": False, # permadeath
        # BUG FIXES
        "fs": False, # fix sketch glitch
        "fe": False, # fix evade glitch
        "fvd": False, # fix vanish/doom glitch
        "fr": False, # fix retort glitch
        "fj": False, # fix jump glitches
        "fbs": False, # fix boss skip in KT
        "fedc": False # fix enemy damage counter
    }
    return seed

def CopySeed(s):
    # Generate a fully random seed object
    seed = {}
    for i in s.keys():
        seed[i] = s[i]
    return seed

def Flagstring2Seedlet(fstr):
    # Create a seed object from an incomplete flagstring fl
    # initialize random seed
    seed = {}

    # preprocess fstr to remove extra whitespace
    fstr = " ".join(fstr.split())

    # process fstr
    flags = fstr.split('-')  ### ERROR: some flags can have negative values!!!  e.g. "-iesr -100"
    flags.remove('')

    # handle read-in errors:
    checklist = ['iesr', 'ieor', 'ieror', 'iersr']
    for fi in range(len(flags)):
        if flags[fi] != '':
            this = flags[fi].split(' ')
            if '' in this:
                this.remove('')
            if this[0] in checklist:
                this2 = flags[fi+1].split(' ')
                if '' in this2:
                    this2.remove('')
                #print(this, flags[fi + 1], this2)
                if this2[0] not in flag_list.keys() and this2[0] not in flag_group_lookup.keys():
                    # was a parsing error.  correct it.
                    flags[fi] = flags[fi] + '-' + flags[fi+1]
                    flags[fi+1] = ''
                    #print(flags[fi], flags[fi+1])

    while '' in flags:
        flags.remove('')

    for f in flags:
        i = f.split(' ')
        if '' in i:
            i.remove('')
        # print(i)

        # handle special cases
        if i[0] == 's':  # seed name
            pass # do nothing

        elif i[0] == '': # empty flag
            pass # do nothing

        elif i[0] == 'com':  # command string
            vals = [i[1][2 * k:2 * k + 2] for k in range(0, 13)]
            nums = ['0' + str(i) for i in range(1, 10)] + ['10', '11', '12', '13']
            for k in range(13):
                seed['com_'+nums[k]] = vals[k]

        else:
            # Handle explicit group declarations
            if i[0] in flag_groups.keys():
                # Note this will not typically be used when parsing flagstrings, which imply groups by declaring only which option is chosen.
                # This is included here to allow an explicit declaration of "original" settings.
                #thisgroup = flag_groups[i[0]]
                if i[1] in ['false', 'False', 'FALSE', 'orig', 'Orig', 'ORIG', 'original', 'Original', 'ORIGINAL', 'off', 'Off', 'OFF']:
                    seed[i[0]] = ''
                else:
                    # Note: argument must be declared without hyphen!!!
                    seed[i[0]] = i[1]
                    # set default values, if required
                    #k = 1
                    #default = DefaultSeed()
                    #while i[1] + '_' + str(k) in flag_list.keys():
                    #    seed[i[1] + '_' + str(k)] = default[i[1] + '_' + str(k)]
                    #    k += 1

            # Handle flags that are in a group:
            elif i[0] in flag_group_lookup.keys():
                # Flags that are members of a group
                seed[flag_group_lookup[i[0]]] = i[0]

                # if in a group with number values:
                if len(i) > 1:
                    # flags with number values
                    nums = [str(i) for i in range(1,len(i))]
                    for k in range(len(nums)):
                        seed[i[0]+'_'+nums[k]] = i[1 + k]

            # Handle flags not in a group
            else:
                try:
                    if flag_list[i[0]] == [True, False]:
                        # this is a binary flag
                        seed[i[0]] = True

                        # handle subflags
                        if len(i) > 1:
                            if i[1] in ['false', 'False', 'FALSE', 'off', 'Off', 'OFF']:
                                # This is a patch to allow declaration that a binary values should be False.  It has not been tested comprehensively.
                                seed[i[0]] = False
                            else:
                                nums = [str(i) for i in range(1, len(i))]
                                for k in range(len(nums)):
                                    seed[i[0] + '_' + nums[k]] = i[1 + k]

                    # not a binary flag, not in a group
                    elif len(i) == 2:
                        seed[i[0]] = i[1]

                    # not in a group, has more than one value
                    elif len(i) > 2:
                        print('This happened and I think it should not.')
                        nums = [str(i) for i in range(1, len(i))]
                        for k in range(len(nums)):
                            seed[i[0] + '_' + nums[k]] = i[1 + k]

                    # that should handle everything
                    else:
                        print('error: ', i)
                except KeyError:
                    pass

    return seed


def Flagstring2Seed(fstr):
    # Create a seed object from a flagstring fl representing the state of all flags
    # initialize random seed
    seed = DefaultSeed()
    seedlet = Flagstring2Seedlet(fstr)
    for s in seedlet.keys():
        seed[s] = seedlet[s]

    return seed

# Make a list of the flags in the typical order.  This order will control the order they are written in flagstr
writeorder = ["mode", "sl", "ktcr", "kter", "ktdr", "stno", "stcr", "ster", "stdr", "sc1", "sc2", "sc3", "sc4",
              "sal", "sn", "eu", "csrp",
              "fst","sel", "brl", "bel", "slr", "loremp", "lel", "srr", "rnl", "rnc", "sdr", "das", "dda", "dns", "del",
              "scc", "com", "rec1", "rec2", "rec3", "rec4", "rec5", "xpm", "mpm", "gpm", "nxppd",
              "ls", "hm", "xg", "ascale", "msl", "eel", "sfb", "sed",
              "bb", "bmbd", "srp3", "bnds", "be", "bnu",
              "renc", "fer", "escr",
              "dgne", "wnz", "mmnu", "cmd",
              "es", "ebonus", "emp", "eeq", "ems", "nm1", "nm2", "rnl1",
              "rnl2", "rns1", "rns2", "nmmi", "gp", "smc", "sws", "sfd", "sto", "iequip", "requip",
              "csb", "mca", "stra", "saw", "shopinv", "shopprices", "ssf", "sdm", "npi", "snbr", "snes", "snsb",
              "ccontents", "cms", "co", "cr", "crvr", "crm", "ari", "anca", "adeh",
              "nmc", "nee", "nil", "nfps", "nu", "nfp", "kthr", "pd", "fs", "fe", "fvd", "fr", "fj", "fbs", "fedc",
              "as", "ond", "rr", "scan", "etimers", "ychoices"]

def Seed2Flagstring(seed):
    # Process a seed object to return the flagstring
    fstr = ''
    for f in writeorder:
        temp = ''
        if seed['stno'] and f in ['stcr', 'ster', 'stdr']:
            pass  # don't write skip requirements if stno is off

        # special case: com string
        elif f == 'com':
            temp = temp + '-com '
            k = 1
            while k < 10:
                temp = temp + str(seed['com_0'+str(k)])
                k += 1
            while k < 14:
                temp = temp + str(seed['com_'+str(k)])
                k += 1
            if temp == '-com 03050708091011121315191617':
                temp = ''  # this is the default value, doesn't need to be written.
            else:
                temp = temp + ' '

        elif f in flag_groups.keys():
            if seed[f] == '':
                pass # don't write a default value

            else:
                temp = temp + '-' + seed[f] + ' '
                k = 1
                subf = []
                val = []
                while seed[f]+'_'+str(k) in seed.keys():
                    subf.append(seed[f]+'_'+str(k))
                    k += 1
                if len(subf) == 2:
                    # sort multiple subflag values
                    for sf in subf:
                        val.append(int(seed[sf]))
                    val.sort()
                elif len(subf) == 1:
                    val.append(seed[subf[0]])

                for v in val:
                    temp = temp + str(v) + ' '

        else:
            # Handle binary flags
            if flag_list[f] == [True, False]:
                if seed[f]:
                    temp = temp + '-' + f + ' '
                    # write subvalues
                    k = 1
                    subf = []
                    val = []
                    while f+'_'+str(k) in seed.keys():
                        subf.append(f+'_'+str(k))
                        k += 1
                    if len(subf) == 2:
                        # sort multiple subflag values
                        for sf in subf:
                            val.append(int(seed[sf]))
                        val.sort()
                    elif len(subf) == 1:
                        val.append(seed[subf[0]])

                    for v in val:
                        temp = temp + str(v) + ' '

            # Handle non-binary flags
            else:
                if seed[f] == '':
                    pass  # don't write a default value
                else:
                    temp = temp + '-' + f + ' ' + str(seed[f]) + ' '

        #print(temp)
        fstr = fstr + temp

    return fstr

def UpdateFlag(seed_in, flag, newval):
    # Take an input seed object, flag, and new value, and return a modified seed object
    seed_out = seed_in
    seed_out[flag] = newval

    return seed_out