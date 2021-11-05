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
    commands = ''.join([scc, com, rec1, rec2, rec3, rec4])

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
    scc = random.choice([' -scc', ''])
    com = ''.join([' -com ', random.choice(skills), random.choice(skills), random.choice(skills), random.choice(skills),
                         random.choice(skills), random.choice(skills), random.choice(skills), random.choice(skills),
                         random.choice(skills), random.choice(skills), random.choice(skills), random.choice(skills),
                         random.choice(skills)])
    rec1 = random.choice(['', ' -rec1 ' + random.choice(skills)])
    rec2 = random.choice(['', ' -rec2 ' + random.choice(skills)])
    rec3 = random.choice(['', ' -rec3 ' + random.choice(skills)])
    rec4 = random.choice(['', ' -rec4 ' + random.choice(skills)])
    rec5 = random.choice(['', ' -rec5 ' + random.choice(skills)])
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


def cr_flags():
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
    scc = random.choice([' -scc', ''])
    com = ''.join([' -com ', random.choice(skills), random.choice(skills), random.choice(skills), random.choice(skills),
                         random.choice(skills), random.choice(skills), random.choice(skills), random.choice(skills),
                         random.choice(skills), random.choice(skills), random.choice(skills), random.choice(skills),
                         random.choice(skills)])
    rec1 = random.choice(['', ' -rec1 ' + random.choice(skills)])
    rec2 = random.choice(['', ' -rec2 ' + random.choice(skills)])
    rec3 = random.choice(['', ' -rec3 ' + random.choice(skills)])
    rec4 = random.choice(['', ' -rec4 ' + random.choice(skills)])
    rec5 = random.choice(['', ' -rec5 ' + random.choice(skills)])
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

# print(chaos())