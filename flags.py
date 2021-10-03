import random
from palettes import id_palette
from portraits import id_portrait
from sprites import id_sprite

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
    # SPRITE PALETTES + CUSTOMIZATIONS !!![This whole section is a dumpster fire]!!!
    cpalf = random.choices(list(id_palette.keys()), k=7)
    cporf = random.choices(list(id_portrait.keys()), k=15)
    csprf = random.choices(list(id_sprite.keys()), k=20)
    csppf = random.choices(list(range(0, 5)), k=20)
    cpal = ' -cpal ' + str(cpalf[0]) + "." + str(cpalf[1]) + "." + str(cpalf[2]) + "." + str(cpalf[3]) + "." \
           + str(cpalf[4]) + "." + str(cpalf[5]) + "." + str(cpalf[6])
    cpor = ' -cpor ' + str(cporf[0]) + "." + str(cporf[1]) + "." + str(cporf[2]) + "." + str(cporf[3]) + "." \
           + str(cporf[4]) + "." + str(cporf[5]) + "." + str(cporf[6]) + "." + str(cporf[7]) + "." + str(
        cporf[8]) + "." + \
           str(cporf[9]) + "." + str(cporf[10]) + "." + str(cporf[11]) + "." + str(cporf[12]) + "." + str(cporf[13]) \
           + "." + str(cporf[14])
    cspr = ' -cspr ' + str(csprf[0]) + "." + str(csprf[1]) + "." + str(csprf[2]) + "." + str(csprf[3]) + "." \
           + str(csprf[4]) + "." + str(csprf[5]) + "." + str(csprf[6]) + "." + str(csprf[7]) + "." + str(
        csprf[8]) + "." + \
           str(csprf[9]) + "." + str(csprf[10]) + "." + str(csprf[11]) + "." + str(csprf[12]) + "." + str(csprf[13]) \
           + "." + str(csprf[14]) + "." + str(csprf[15]) + "." + str(csprf[16]) + "." + str(csprf[17]) + "." + \
           str(csprf[18]) + "." + str(csprf[19])
    cspp = ' -cspp ' + str(csppf[0]) + "." + str(csppf[1]) + "." + str(csppf[2]) + "." + str(csppf[3]) + "." \
           + str(csppf[4]) + "." + str(csppf[5]) + "." + str(csppf[6]) + "." + str(csppf[7]) + "." + str(
        csppf[8]) + "." + \
           str(csppf[9]) + "." + str(csppf[10]) + "." + str(csppf[11]) + "." + str(csppf[12]) + "." + str(csppf[13]) \
           + "." + str(csppf[14]) + "." + str(csppf[15]) + "." + str(csppf[16]) + "." + str(csppf[17]) + "." + \
           str(csppf[18]) + "." + str(csppf[19])

    custom = cspp+cpal+cspr+cpor

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

    flagset = game + party + battle + magic + items + other + custom
    return (flagset)


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
    # SPRITE PALETTES + CUSTOMIZATIONS !!![This whole section is a dumpster fire]!!!
    cpalf = random.choices(list(range(0, 125)), k=7)
    cporf = random.choices(list(range(0, 56)), k=15)
    csprf = random.choices(list(range(0, 137)), k=20)
    csppf = random.choices(list(range(0, 5)), k=20)
    cpal = ' -cpal ' + str(cpalf[0]) + "." + str(cpalf[1]) + "." + str(cpalf[2]) + "." + str(cpalf[3]) + "." \
           + str(cpalf[4]) + "." + str(cpalf[5]) + "." + str(cpalf[6])
    cpor = ' -cpor ' + str(cporf[0]) + "." + str(cporf[1]) + "." + str(cporf[2]) + "." + str(cporf[3]) + "." \
           + str(cporf[4]) + "." + str(cporf[5]) + "." + str(cporf[6]) + "." + str(cporf[7]) + "." + str(
        cporf[8]) + "." + \
           str(cporf[9]) + "." + str(cporf[10]) + "." + str(cporf[11]) + "." + str(cporf[12]) + "." + str(cporf[13]) \
           + "." + str(cporf[14])
    cspr = ' -cspr ' + str(csprf[0]) + "." + str(csprf[1]) + "." + str(csprf[2]) + "." + str(csprf[3]) + "." \
           + str(csprf[4]) + "." + str(csprf[5]) + "." + str(csprf[6]) + "." + str(csprf[7]) + "." + str(
        csprf[8]) + "." + \
           str(csprf[9]) + "." + str(csprf[10]) + "." + str(csprf[11]) + "." + str(csprf[12]) + "." + str(csprf[13]) \
           + "." + str(csprf[14]) + "." + str(csprf[15]) + "." + str(csprf[16]) + "." + str(csprf[17]) + "." + \
           str(csprf[18]) + "." + str(csprf[19])
    cspp = ' -cspp ' + str(csppf[0]) + "." + str(csppf[1]) + "." + str(csppf[2]) + "." + str(csppf[3]) + "." \
           + str(csppf[4]) + "." + str(csppf[5]) + "." + str(csppf[6]) + "." + str(csppf[7]) + "." + str(
        csppf[8]) + "." + \
           str(csppf[9]) + "." + str(csppf[10]) + "." + str(csppf[11]) + "." + str(csppf[12]) + "." + str(csppf[13]) \
           + "." + str(csppf[14]) + "." + str(csppf[15]) + "." + str(csppf[16]) + "." + str(csppf[17]) + "." + \
           str(csppf[18]) + "." + str(csppf[19])

    custom = cspp

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

    other = ''.join([colo, ah, challenges, misc, custom, bugfixes])

    flagset = game + party + battle + magic + items + other
    return (flagset)

# print(chaos())