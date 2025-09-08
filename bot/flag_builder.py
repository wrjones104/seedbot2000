import random

def standard():
    # -----GAME-----
    # SETTINGS
    mode = random.choices(["-open", "-cg"], weights=([1, 15]), k=1)[0]
    slog = random.choices(["", " -sl"], weights=([1, 0]), k=1)[0]
    settings = "".join([mode, slog])

    # KEFKA'S TOWER & STATUE SKIP
    ktcr1 = random.randint(5, 7)
    ktcr2 = random.randint(ktcr1, 10)
    kter1 = random.randint(7, 11)
    kter2 = random.randint(kter1, 13)
    ktdr1 = random.randint(1, 3)
    ktdr2 = random.randint(ktdr1, 3)
    stcr1 = random.randint(6, 8)
    stcr2 = random.randint(stcr1, 11)
    ster1 = random.randint(8, 12)
    ster2 = random.randint(ster1, 14)
    stdr1 = random.randint(2, 4)
    stdr2 = random.randint(stdr1, 4)
    stno = random.choices([True, False], weights=([6, 1]), k=1)[0]

    if stno:
        kt = ".".join(
            [
                " -oa 2.2.2.2",
                str(ktcr1),
                str(ktcr2),
                "4",
                str(kter1),
                str(kter2),
                "6",
                str(ktdr1),
                str(ktdr2),
            ]
        )
    else:
        kt = ".".join(
            [
                " -oa 2.2.2.2",
                str(ktcr1),
                str(ktcr2),
                "4",
                str(kter1),
                str(kter2),
                "6",
                str(ktdr1),
                str(ktdr2),
            ]
        )
        kt += ".".join(
            [
                " -ob 3.2.2.2",
                str(stcr1),
                str(stcr2),
                "4",
                str(ster1),
                str(ster2),
                "6",
                str(stdr1),
                str(stdr2),
            ]
        )

    objectives = random.choices(
        [" -oc 0.1.1.1.r", " -oc 0.1.1.1.r -od 0.1.1.1.r"], weights=[4, 1], k=1
    )[0]
    game = "".join([settings, kt, objectives])

    # -----PARTY-----
    # STARTING PARTY
    sc1 = random.choice([" -sc1 random", " -sc1 randomngu"])
    sc2 = random.choice([" -sc2 random", " -sc2 randomngu"])
    sc3 = random.choices(
        [" -sc3 random", " -sc3 randomngu", ""], weights=([1, 1, 5]), k=1
    )[0]
    sc4 = random.choices(
        [" -sc4 random", " -sc4 randomngu", ""], weights=([0, 0, 1]), k=1
    )[0]
    sparty = "".join([sc1, sc2, sc3, sc4])

    # SWORDTECHS
    fst = random.choices([" -fst", ""], weights=([1, 0]), k=1)[0]
    sel = random.choices([" -sel", ""], weights=([1, 5]), k=1)[0]
    swdtech = "".join([fst, sel])

    # BLITZES
    brl = random.choices([" -brl", ""], weights=([10, 1]), k=1)[0]
    bel = random.choices([" -bel", ""], weights=([1, 10]), k=1)[0]
    blitz = "".join([brl, bel])

    # LORES
    slr1 = random.randint(0, 7)
    slr2 = random.randint(slr1, 10)
    slrr = " ".join([" -slr", str(slr1), str(slr2)])
    slr = random.choices([slrr, ""], weights=([10, 1]), k=1)[0]
    lmprp1 = random.randint(75, 100)
    lmprp2 = random.randint(lmprp1, 125)
    lmprv1 = random.randint(20, 40)
    lmprv2 = random.randint(lmprv1, 75)
    lmprp = " ".join([" -lmprp", str(lmprp1), str(lmprp2)])
    lmprv = " ".join([" -lmprv", str(lmprv1), str(lmprv2)])
    loremp = random.choices(["", " -lmps", lmprp, lmprv], weights=([1, 3, 10, 3]), k=1)[
        0
    ]
    lel = random.choices([" -lel", ""], weights=([1, 0]), k=1)[0]
    lores = "".join([slr, loremp, lel])

    # RAGES
    srr1 = random.randint(0, 10)
    srr2 = random.randint(srr1, 25)
    srr = " ".join([" -srr", str(srr1), str(srr2)])
    srages = random.choices(["", srr], weights=([1, 13]), k=1)[0]
    rnl = random.choices([" -rnl", ""], weights=([1, 0]), k=1)[0]
    rnc = random.choices([" -rnc", ""], weights=([15, 1]), k=1)[0]
    rage = "".join([srages, rnl, rnc])

    # DANCES
    sdr1 = random.randint(0, 2)
    sdr2 = random.randint(sdr1, 4)
    sdr = " ".join([" -sdr", str(sdr1), str(sdr2)])
    das = random.choices([" -das", ""], weights=([1, 0]), k=1)[0]
    dda = random.choices([" -dda", ""], weights=([1, 0]), k=1)[0]
    dns = random.choices([" -dns", ""], weights=([1, 0]), k=1)[0]
    d_el = random.choices([" -del", ""], weights=([0, 1]), k=1)[0]
    dance = "".join([sdr, das, dda, dns, d_el])

    # STEAL CHANCES
    steal = random.choice(["", " -sch", " -sch", " -sca", " -sca", " -sca"])

    # CHARACTERS
    sal = random.choices([" -sal", ""], weights=([13, 1]), k=1)[0]
    sn = random.choices([" -sn", ""], weights=([1, 13]), k=1)[0]
    eu = random.choices([" -eu", ""], weights=([13, 1]), k=1)[0]
    csrp1 = random.randint(90, 120)
    csrp2 = random.randint(csrp1, 130)
    csrp = " ".join([" -csrp", str(csrp1), str(csrp2)])
    cstats = "".join([sal, sn, eu, csrp])

    # COMMANDS
    scc = random.choices([" -scc", ""], weights=([1, 10]), k=1)[0]
    com = random.choices(
        [" -com 99999999999999999999999999", "", " -com 98989898989898989898989898"],
        weights=([2, 1, 13]),
        k=1,
    )[0]
    recskills = [
        "10",
        "6",
        "14",
        "19",
        "24",
        "26",
        "22",
        "12",
        "3",
        "28",
        "16",
        "11",
        "27",
        "13",
        "15",
        "5",
        "7",
        "8",
        "9",
        "23",
        "29",
    ]
    rec1 = random.choices([" -rec1 28", ""], weights=([1, 0]), k=1)[0]
    rec2 = random.choices([" -rec2 23", ""], weights=([1, 0]), k=1)[0]
    rec3 = random.choices(
        [" ".join([" -rec3", random.choice(recskills)]), ""], weights=([0, 1]), k=1
    )[0]
    rec4 = random.choices(
        [" ".join([" -rec4", random.choice(recskills)]), ""], weights=([0, 1]), k=1
    )[0]
    commands = "".join([scc, com, rec1, rec2, rec3, rec4])

    party = "".join(
        [sparty, swdtech, blitz, lores, rage, dance, cstats, commands, steal]
    )

    # -----BATTLE-----
    xpm = " ".join(
        [" -xpm", str(random.choices([2, 3, 4], weights=([1, 10, 1]), k=1)[0])]
    )
    gpm = " ".join(
        [" -gpm", str(random.choices([4, 5, 6], weights=([1, 10, 1]), k=1)[0])]
    )
    mpm = " ".join(
        [" -mpm", str(random.choices([4, 5, 6], weights=([1, 10, 1]), k=1)[0])]
    )
    nxppd = random.choices([" -nxppd", ""], weights=([13, 1]), k=1)[0]
    xpmpgp = "".join([xpm, gpm, mpm, nxppd])

    # BOSSES
    bb = random.choices([" -bbr", " -bbs", ""], weights=([1, 13, 1]), k=1)[0]
    bmbd = random.choices([" -drloc mix", ""], weights=([0, 1]), k=1)[0]
    srp3 = random.choices([" -srp3", ""], weights=([0, 1]), k=1)[0]
    bnds = random.choices([" -bnds", ""], weights=([1, 13]), k=1)[0]
    be = random.choices([" -be", ""], weights=([1, 0]), k=1)[0]
    bnu = random.choices([" -bnu", ""], weights=([10, 1]), k=1)[0]
    bosses = "".join([bb, bmbd, srp3, bnds, be, bnu])

    # BOSS AI
    dgne = random.choices([" -dgne", ""], weights=([1, 0]), k=1)[0]
    wnz = random.choices([" -wnz", ""], weights=([1, 0]), k=1)[0]
    mmnu = random.choices([" -mmnu", ""], weights=([1, 0]), k=1)[0]
    cmd = random.choices([" -cmd", ""], weights=([1, 0]), k=1)[0]
    b_ai = "".join([dgne, wnz, mmnu, cmd])

    # SCALING
    scale_opt = ["0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    lspf = " ".join(
        [
            " -lsced",
            random.choices(scale_opt, weights=([0, 1, 1, 10, 2, 1, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    lsaf = " ".join(
        [
            " -lsa",
            random.choices(scale_opt, weights=([0, 13, 1, 0, 0, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    lshf = " ".join(
        [
            " -lsh",
            random.choices(scale_opt, weights=([0, 13, 1, 0, 0, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    lstf = " ".join(
        [
            " -lst",
            random.choices(scale_opt, weights=([0, 1, 5, 10, 1, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    hmpf = " ".join(
        [
            " -hmced",
            random.choices(scale_opt, weights=([0, 1, 1, 10, 2, 1, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    hmaf = " ".join(
        [
            " -hma",
            random.choices(scale_opt, weights=([0, 13, 1, 0, 0, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    hmhf = " ".join(
        [
            " -hmh",
            random.choices(scale_opt, weights=([0, 13, 1, 0, 0, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    hmtf = " ".join(
        [
            " -hmt",
            random.choices(scale_opt, weights=([0, 1, 5, 10, 1, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    xgpf = " ".join(
        [
            " -xgced",
            random.choices(scale_opt, weights=([0, 1, 1, 10, 2, 1, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    xgaf = " ".join(
        [
            " -xga",
            random.choices(scale_opt, weights=([0, 13, 1, 0, 0, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    xghf = " ".join(
        [
            " -xgh",
            random.choices(scale_opt, weights=([0, 13, 1, 0, 0, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    xgtf = " ".join(
        [
            " -xgt",
            random.choices(scale_opt, weights=([0, 1, 5, 10, 1, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    asrf = " ".join(
        [
            " -asr",
            random.choices(scale_opt, weights=([0, 0, 1, 10, 2, 1, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    asef = " ".join(
        [
            " -ase",
            random.choices(scale_opt, weights=([0, 0, 1, 10, 2, 1, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    lscale = random.choices(
        [lspf, lsaf, lshf, lstf, ""], weights=([15, 2, 2, 1, 0]), k=1
    )[0]
    hmscale = random.choices(
        [hmpf, hmaf, hmhf, hmtf, ""], weights=([15, 2, 2, 1, 0]), k=1
    )[0]
    xgscale = random.choices(
        [xgpf, xgaf, xghf, xgtf, ""], weights=([15, 2, 2, 1, 0]), k=1
    )[0]
    ascale = random.choices([asrf, asef, ""], weights=([1, 13, 0]), k=1)[0]
    msl = " ".join([" -msl", str(random.randint(40, 60))])
    sfb = random.choices([" -sfb", ""], weights=([0, 1]), k=1)[0]
    sed = random.choices([" -sed", ""], weights=([13, 1]), k=1)[0]
    scaling = "".join([lscale, hmscale, xgscale, ascale, msl, sfb, sed])

    # ENCOUNTERS
    renc = random.choices(
        ["", " -res", " ".join([" -rer", str(random.randint(0, 10))])],
        weights=([1, 10, 10]),
        k=1,
    )[0]
    fenc = random.choices(
        ["", " ".join([" -fer", str(random.randint(0, 10))])], weights=([1, 13]), k=1
    )[0]
    escr = " -escr 100"
    encounters = "".join([renc, fenc, escr])

    battle = "".join([bosses, b_ai, scaling, encounters, xpmpgp])

    # -----MAGIC-----
    # ESPERS
    esr1 = random.randint(1, 3)
    esr2 = random.randint(esr1, 5)
    esr = " ".join([" -esr", str(esr1), str(esr2)])
    ess = random.choices(
        ["", esr, " -esrr", " -ess", " -essrr", " -esrt"],
        weights=([1, 13, 2, 2, 2, 3]),
        k=1,
    )[0]
    ebonus = random.choices(
        ["", " ".join([" -ebr", str(random.randint(67, 100))]), " -ebs"],
        weights=([1, 10, 2]),
        k=1,
    )[0]
    emprp1 = random.randint(75, 100)
    emprp2 = random.randint(emprp1, 125)
    emprv1 = random.randint(25, 75)
    emprv2 = random.randint(emprv1, 99)
    eer1 = random.randint(6, 12)
    eer2 = random.randint(eer1, 12)
    emprp = " ".join([" -emprp", str(emprp1), str(emprp2)])
    emprv = " ".join([" -emprv", str(emprv1), str(emprv2)])
    emp = random.choices(["", emprp, emprv, " -emps"], weights=([1, 10, 1, 3]), k=1)[0]
    eer = " ".join([" -eer", str(eer1), str(eer2)])
    eebr = " ".join([" -eebr", str(random.randint(6, 12))])
    eeq = random.choices([eer, eebr, ""], weights=([1, 1, 15]), k=1)[0]
    ems = random.choices(["", " -ems"], weights=([13, 1]), k=1)[0]
    espers = "".join([ess, ebonus, emp, eeq, ems])

    # NATURAL MAGIC
    nm1 = random.choices(["", " -nm1 random"], weights=([0, 1]), k=1)[0]
    nm2 = random.choices(["", " -nm2 random"], weights=([0, 1]), k=1)[0]
    rnl1 = random.choices(["", " -rnl1"], weights=([0, 1]), k=1)[0]
    rnl2 = random.choices(["", " -rnl2"], weights=([0, 1]), k=1)[0]
    rns1 = random.choices(["", " -rns1"], weights=([0, 1]), k=1)[0]
    rns2 = random.choices(["", " -rns2"], weights=([0, 1]), k=1)[0]
    m_indicator = random.choices(["", " -nmmi"], weights=([0, 1]), k=1)[0]
    nmagic = "".join([nm1, nm2, rnl1, rnl2, rns1, rns2, m_indicator])

    magic = "".join([espers, nmagic])

    # -----ITEMS-----
    # STARTING GOLD/ITEMS
    gp = " ".join([" -gp", str(random.randint(0, 20000))])
    smc = " -smc 3"
    sws = " ".join([" -sws", str(random.randint(0, 7))])
    sfd = " ".join([" -sfd", str(random.randint(0, 7))])
    sto = " ".join([" -sto", str(random.randint(0, 4))])
    s_inv = "".join([gp, smc, sfd, sto, sws])

    # ITEMS
    ier1 = random.randint(7, 14)
    ier2 = random.randint(ier1, 14)
    ier = " ".join([" -ier", str(ier1), str(ier2)])
    iebr = " ".join([" -iebr", str(random.randint(7, 14))])
    ieor = " ".join([" -ieor", str(random.randint(33, 100))])
    iesr = " ".join([" -iesr", str(random.randint(33, 100))])
    iequip = random.choices(
        ["", ier, iebr, ieor, iesr], weights=([1, 1, 1, 13, 1]), k=1
    )[0]
    ierr1 = random.randint(7, 14)
    ierr2 = random.randint(ierr1, 14)
    ierr = " ".join([" -ierr", str(ierr1), str(ierr2)])
    ierbr = " ".join([" -ierbr", str(random.randint(7, 14))])
    ieror = " ".join([" -ieror", str(random.randint(33, 100))])
    iersr = " ".join([" -iersr", str(random.randint(33, 100))])
    requip = random.choices(
        ["", ierr, ierbr, ieror, iersr], weights=([1, 1, 1, 13, 1]), k=1
    )[0]
    csb1 = random.randint(1, 32)
    csb2 = random.randint(csb1, 32)
    csb = " ".join([" -csb", str(csb1), str(csb2)])
    mca = random.choices([" -mca", ""], weights=([1, 0]), k=1)[0]
    stra = random.choices([" -stra", ""], weights=([1, 0]), k=1)[0]
    saw = random.choices([" -saw", ""], weights=([1, 0]), k=1)[0]
    equips = "".join([iequip, requip, csb, mca, stra, saw])

    # SHOPS
    sisr = " ".join([" -sisr", str(random.randint(20, 40))])
    shopinv = random.choices(
        ["", sisr, " -sirt", " -sie"], weights=([1, 13, 3, 0]), k=1
    )[0]
    sprv1 = random.randint(0, 65535)
    sprv2 = random.randint(sprv1, 65535)
    sprp1 = random.randint(75, 100)
    sprp2 = random.randint(sprp1, 125)
    sprv = " ".join([" -sprv", str(sprv1), str(sprv2)])
    sprp = " ".join([" -sprp", str(sprp1), str(sprp2)])
    shopprices = random.choices(["", sprv, sprp], weights=([1, 2, 15]), k=1)[0]
    ssf = random.choices(
        ["", " -ssf4", " -ssf8", " -ssf0"], weights=([13, 1, 1, 0]), k=1
    )[0]
    sdm = " ".join([" -sdm", str(random.randint(4, 5))])
    npi = random.choices(["", " -npi"], weights=([0, 1]), k=1)[0]
    snbr = random.choices(["", " -snbr"], weights=([13, 1]), k=1)[0]
    snes = random.choices(["", " -snes"], weights=([13, 1]), k=1)[0]
    snsb = random.choices(["", " -snsb"], weights=([13, 1]), k=1)[0]
    shops = "".join([shopinv, shopprices, ssf, sdm, npi, snbr, snes, snsb])

    # CHESTS
    ccontents = random.choices(
        ["", " -ccrt", " -cce", " ".join([" -ccsr", str(random.randint(20, 40))])],
        weights=([1, 3, 0, 13]),
        k=1,
    )[0]
    cms = random.choices(["", " -cms"], weights=([0, 1]), k=1)[0]
    chests = "".join([ccontents, cms])

    items = "".join([s_inv, equips, shops, chests])

    # -----CUSTOM-----
    # SEE CUSTOM_SPRITES_PORTRAITS.PY

    # -----OTHER-----
    # COLISEUM
    coper = random.randint(45, 85)
    crper = random.randint(45, 85)
    co = f" -cor {coper}"
    cr = f" -crr {crper}"
    crvr1 = random.randint(30, 50)
    crvr2 = random.randint(crvr1, 75)
    visible = random.choices(
        ["", " ".join([" -crvr", str(crvr1), str(crvr2)])], weights=([0, 1]), k=1
    )[0]
    rmenu = random.choices(["", " -crm"], weights=([1, 13]), k=1)[0]
    colo = "".join([co, cr, visible, rmenu])

    # AUCTION HOUSE
    ari = random.choices(["", " -ari"], weights=([0, 1]), k=1)[0]
    anca = random.choices(["", " -anca"], weights=([0, 1]), k=1)[0]
    adeh = random.choices(["", " -adeh"], weights=([0, 1]), k=1)[0]
    ah = "".join([ari, anca, adeh])

    # MISC
    asprint = random.choices(["", " -move as"], weights=([0, 1]), k=1)[0]
    ond = random.choices(["", " -ond"], weights=([0, 1]), k=1)[0]
    rr = random.choices(["", " -rr"], weights=([0, 1]), k=1)[0]
    scan = random.choices(["", " -scan"], weights=([1, 0]), k=1)[0]
    etimers = random.choices(["", " -etr", " -etn"], weights=([5, 1, 0]), k=1)[0]
    ychoices = [
        " -ymascot",
        " -ycreature",
        " -yimperial",
        " -ymain",
        " -yreflect",
        " -ystone",
        " -ysketch",
        " -yrandom",
        " -yremove",
        "",
    ]
    ychoice = random.choices(ychoices, weights=([1, 1, 1, 1, 1, 1, 1, 1, 1, 13]), k=1)[
        0
    ]
    flashes = random.choice(["", " -frm", " -frw"])
    misc = "".join([asprint, ond, rr, scan, etimers, ychoice, flashes])

    # CHALLENGES
    nmc = random.choices(["", " -nmc"], weights=([1, 5]), k=1)[0]
    nee = random.choices(["", " -nee"], weights=([13, 1]), k=1)[0]
    nil = random.choices(["", " -nil"], weights=([1, 5]), k=1)[0]
    nfps = random.choices(["", " -nfps"], weights=([0, 1]), k=1)[0]
    nu = random.choices(["", " -nu"], weights=([1, 10]), k=1)[0]
    nfp = random.choices(["", " -nfce"], weights=([13, 1]), k=1)[0]
    pd = random.choices(["", " -pd"], weights=([1, 0]), k=1)[0]
    challenges = "".join([nmc, nee, nil, nfps, nu, nfp, pd])

    # BUG FIXES
    fs = random.choices(["", " -fs"], weights=([0, 1]), k=1)[0]
    fe = random.choices(["", " -fe"], weights=([0, 1]), k=1)[0]
    fvd = random.choices(["", " -fvd"], weights=([0, 1]), k=1)[0]
    fr = random.choices(["", " -fr"], weights=([0, 1]), k=1)[0]
    fj = random.choices(["", " -fj"], weights=([0, 1]), k=1)[0]
    fbs = random.choices(["", " -fbs"], weights=([0, 1]), k=1)[0]
    fedc = random.choices(["", " -fedc"], weights=([0, 1]), k=1)[0]
    bugfixes = "".join([fs, fe, fvd, fr, fj, fbs, fedc])

    other = "".join([colo, ah, challenges, misc, bugfixes])

    flagset = "".join([game, party, battle, magic, items, other])
    return flagset


def chaos():
    # -----GAME-----
    # SETTINGS
    mode = random.choices(["-open", "-cg"], weights=([1, 7]), k=1)[0]
    slog = random.choices(["", " -sl"], weights=([13, 1]), k=1)[0]
    settings = "".join([mode, slog])

    # KEFKA'S TOWER & STATUE SKIP
    ktcr1 = random.randint(3, 9)
    ktcr2 = random.randint(ktcr1, 12)
    kter1 = random.randint(5, 14)
    kter2 = random.randint(kter1, 16)
    ktdr1 = random.randint(1, 6)
    ktdr2 = random.randint(ktdr1, 6)
    stcr1 = random.randint(4, 10)
    stcr2 = random.randint(stcr1, 13)
    ster1 = random.randint(6, 15)
    ster2 = random.randint(ster1, 17)
    stdr1 = random.randint(2, 7)
    stdr2 = random.randint(stdr1, 7)
    stno = random.choices([True, False], weights=([4, 1]), k=1)[0]

    if stno:
        kt = ".".join(
            [
                " -oa 2.2.2.2",
                str(ktcr1),
                str(ktcr2),
                "4",
                str(kter1),
                str(kter2),
                "6",
                str(ktdr1),
                str(ktdr2),
            ]
        )
    else:
        kt = ".".join(
            [
                " -oa 2.2.2.2",
                str(ktcr1),
                str(ktcr2),
                "4",
                str(kter1),
                str(kter2),
                "6",
                str(ktdr1),
                str(ktdr2),
            ]
        )
        kt += ".".join(
            [
                " -ob 3.2.2.2",
                str(stcr1),
                str(stcr2),
                "4",
                str(ster1),
                str(ster2),
                "6",
                str(stdr1),
                str(stdr2),
            ]
        )

    objectives = random.choice(
        [
            " -oc 0.1.1.1.r",
            " -oc 0.1.1.1.r -od 0.1.1.1.r",
            " -oc 0.1.1.1.r -od 0.1.1.1.r -oe 0.1.1.1.r",
            " -oc 0.1.1.1.r -od 0.1.1.1.r -oe 0.1.1.1.r -of 0.1.1.1.r",
        ]
    )
    objectives += " -og 59.1.1.1.r"
    game = "".join([settings, kt, objectives])

    # -----PARTY-----
    # STARTING PARTY
    sc1 = random.choice([" -sc1 random", " -sc1 randomngu"])
    sc2 = random.choice([" -sc2 random", " -sc2 randomngu"])
    sc3 = random.choices(
        [" -sc3 random", " -sc3 randomngu", ""], weights=([1, 1, 5]), k=1)[0]
    if sc3 == "":
        sc4 = random.choices(
            [" -sc3 random", " -sc3 randomngu", ""], weights=([1, 1, 10]), k=1)[0]
    else:
        sc4 = random.choices(
            [" -sc4 random", " -sc4 randomngu", ""], weights=([1, 1, 10]), k=1)[0]
    slevel = random.choices(
        ["", "".join([" -stl ", str(random.randint(3, 9))])], weights=([10, 1]), k=1
    )[0]
    sparty = "".join([sc1, sc2, sc3, sc4, slevel])

    # SWORDTECHS
    fst = random.choices([" -fst", ""], weights=([1, 0]), k=1)[0]
    sel = random.choices([" -sel", ""], weights=([1, 3]), k=1)[0]
    swdtech = "".join([fst, sel])

    # BLITZES
    brl = random.choices([" -brl", ""], weights=([5, 1]), k=1)[0]
    bel = random.choices([" -bel", ""], weights=([1, 5]), k=1)[0]
    blitz = "".join([brl, bel])

    # LORES
    slr1 = random.randint(0, 12)
    slr2 = random.randint(slr1, 16)
    slrr = " ".join([" -slr", str(slr1), str(slr2)])
    slr = random.choices([slrr, ""], weights=([5, 1]), k=1)[0]
    lmprp1 = random.randint(25, 125)
    lmprp2 = random.randint(lmprp1, 175)
    lmprv1 = random.randint(10, 60)
    lmprv2 = random.randint(lmprv1, 80)
    lmprp = " ".join([" -lmprp", str(lmprp1), str(lmprp2)])
    lmprv = " ".join([" -lmprv", str(lmprv1), str(lmprv2)])
    loremp = random.choices(["", " -lmps", lmprp, lmprv], weights=([1, 3, 5, 3]), k=1)[
        0
    ]
    lel = random.choices([" -lel", ""], weights=([13, 1]), k=1)[0]
    lores = "".join([slr, loremp, lel])

    # RAGES
    srr1 = random.randint(0, 25)
    srr2 = random.randint(srr1, 50)
    srr = " ".join([" -srr", str(srr1), str(srr2)])
    srages = random.choices(["", srr], weights=([1, 10]), k=1)[0]
    rnl = random.choices([" -rnl", ""], weights=([1, 0]), k=1)[0]
    rnc = random.choices([" -rnc", ""], weights=([10, 1]), k=1)[0]
    rage = "".join([srages, rnl, rnc])

    # DANCES
    sdr1 = random.randint(0, 4)
    sdr2 = random.randint(sdr1, 6)
    sdr = " ".join([" -sdr", str(sdr1), str(sdr2)])
    das = random.choices([" -das", ""], weights=([1, 0]), k=1)[0]
    dda = random.choices([" -dda", ""], weights=([1, 0]), k=1)[0]
    dns = random.choices([" -dns", ""], weights=([1, 0]), k=1)[0]
    d_el = random.choices([" -del", ""], weights=([1, 13]), k=1)[0]
    dance = "".join([sdr, das, dda, dns, d_el])

    # SKETCH & CONTROL
    scis = random.choice([" -scis", ""])

    # STEAL CHANCES
    steal = random.choice(["", " -sch", " -sch", " -sca", " -sca", " -sca"])

    # CHARACTERS
    sal = random.choices([" -sal", ""], weights=([7, 1]), k=1)[0]
    sn = random.choices([" -sn", ""], weights=([1, 7]), k=1)[0]
    eu = random.choices([" -eu", ""], weights=([7, 1]), k=1)[0]
    csrp1 = random.randint(50, 120)
    csrp2 = random.randint(csrp1, 160)
    csrp = " ".join([" -csrp", str(csrp1), str(csrp2)])
    cstats = "".join([sal, sn, eu, csrp])

    # COMMANDS
    scc = random.choices([" -scc", ""], weights=([1, 5]), k=1)[0]
    com = random.choices(
        [" -com 99999999999999999999999999", "", " -com 98989898989898989898989898"],
        weights=([7, 1, 7]),
        k=1,
    )[0]
    recskills = [
        "10",
        "6",
        "14",
        "19",
        "24",
        "26",
        "22",
        "12",
        "3",
        "28",
        "16",
        "11",
        "27",
        "13",
        "15",
        "5",
        "7",
        "8",
        "9",
        "23",
        "29",
    ]
    rec1 = random.choices([" -rec1 28", ""], weights=([10, 1]), k=1)[0]
    rec2 = random.choices([" -rec2 23", ""], weights=([7, 1]), k=1)[0]
    rec3 = random.choices(
        [" ".join([" -rec3", random.choice(recskills)]), ""], weights=([1, 10]), k=1
    )[0]
    rec4 = random.choices(
        [" ".join([" -rec4", random.choice(recskills)]), ""], weights=([1, 10]), k=1
    )[0]
    rec5 = random.choices(
        [" ".join([" -rec5", random.choice(recskills)]), ""], weights=([1, 10]), k=1
    )[0]
    commands = "".join([scc, com, rec1, rec2, rec3, rec4, rec5])

    party = "".join(
        [sparty, swdtech, blitz, lores, rage, dance, cstats, commands, steal, scis]
    )

    # -----BATTLE-----
    xpm = " ".join(
        [
            " -xpm",
            str(random.choices([2, 3, 4, 5, 6], weights=([2, 10, 6, 3, 1]), k=1)[0]),
        ]
    )
    gpm = " ".join(
        [
            " -gpm",
            str(
                random.choices(
                    [3, 4, 5, 6, 7, 8, 9, 10], weights=([1, 2, 10, 6, 3, 2, 1, 1]), k=1
                )[0]
            ),
        ]
    )
    mpm = " ".join(
        [
            " -mpm",
            str(
                random.choices(
                    [3, 4, 5, 6, 7, 8, 9, 10], weights=([1, 2, 10, 6, 3, 2, 1, 1]), k=1
                )[0]
            ),
        ]
    )
    nxppd = random.choices([" -nxppd", ""], weights=([7, 1]), k=1)[0]
    xpmpgp = "".join([xpm, gpm, mpm, nxppd])

    # BOSSES
    bb = random.choices([" -bbr", " -bbs", ""], weights=([5, 10, 1]), k=1)[0]
    bmbd = " ".join(
        [
            " -drloc",
            random.choices(["original", "shuffle", "mix"], weights=([1, 5, 1]), k=1)[0],
        ]
    )
    bmbd += " ".join(
        [
            " -stloc",
            random.choices(["original", "shuffle", "mix"], weights=([1, 2, 5]), k=1)[0],
        ]
    )
    srp3 = random.choices([" -srp3", ""], weights=([1, 10]), k=1)[0]
    bnds = random.choices([" -bnds", ""], weights=([1, 8]), k=1)[0]
    be = random.choices([" -be", ""], weights=([13, 1]), k=1)[0]
    bnu = random.choices([" -bnu", ""], weights=([10, 1]), k=1)[0]
    bosses = "".join([bb, bmbd, srp3, bnds, be, bnu])

    # BOSS AI
    dgne = random.choices([" -dgne", ""], weights=([10, 1]), k=1)[0]
    wnz = random.choices([" -wnz", ""], weights=([10, 1]), k=1)[0]
    mmnu = random.choices([" -mmnu", ""], weights=([13, 1]), k=1)[0]
    cmd = random.choices([" -cmd", ""], weights=([1, 0]), k=1)[0]
    b_ai = "".join([dgne, wnz, mmnu, cmd])

    # SCALING
    scale_opt = ["0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    lspf = " ".join(
        [
            " -lsced",
            random.choices(scale_opt, weights=([0, 1, 1, 10, 5, 3, 1, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    lsaf = " ".join(
        [
            " -lsa",
            random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    lshf = " ".join(
        [
            " -lsh",
            random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    lstf = " ".join(
        [
            " -lst",
            random.choices(scale_opt, weights=([0, 1, 5, 10, 1, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    hmpf = " ".join(
        [
            " -hmced",
            random.choices(scale_opt, weights=([0, 1, 1, 10, 5, 3, 1, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    hmaf = " ".join(
        [
            " -hma",
            random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    hmhf = " ".join(
        [
            " -hmh",
            random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    hmtf = " ".join(
        [
            " -hmt",
            random.choices(scale_opt, weights=([0, 1, 5, 10, 1, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    xgpf = " ".join(
        [
            " -xgced",
            random.choices(scale_opt, weights=([0, 1, 1, 10, 5, 3, 1, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    xgaf = " ".join(
        [
            " -xga",
            random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    xghf = " ".join(
        [
            " -xgh",
            random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    xgtf = " ".join(
        [
            " -xgt",
            random.choices(scale_opt, weights=([0, 1, 5, 10, 1, 0, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    asrf = " ".join(
        [
            " -asr",
            random.choices(scale_opt, weights=([0, 0, 3, 10, 2, 1, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    asef = " ".join(
        [
            " -ase",
            random.choices(scale_opt, weights=([0, 0, 3, 10, 2, 1, 0, 0, 0, 0]), k=1)[
                0
            ],
        ]
    )
    lscale = random.choices(
        [lspf, lsaf, lshf, lstf, ""], weights=([7, 2, 2, 1, 0]), k=1
    )[0]
    hmscale = random.choices(
        [hmpf, hmaf, hmhf, hmtf, ""], weights=([7, 2, 2, 1, 0]), k=1
    )[0]
    xgscale = random.choices(
        [xgpf, xgaf, xghf, xgtf, ""], weights=([7, 2, 2, 1, 0]), k=1
    )[0]
    ascale = random.choices([asrf, asef, ""], weights=([1, 7, 0]), k=1)[0]
    msl = " ".join([" -msl", str(random.randint(45, 80))])
    sfb = random.choices([" -sfb", ""], weights=([0, 1]), k=1)[0]
    sed = random.choices([" -sed", ""], weights=([7, 1]), k=1)[0]
    scaling = "".join([lscale, hmscale, xgscale, ascale, msl, sfb, sed])

    # ENCOUNTERS
    renc = random.choices(
        ["", " -res", " ".join([" -rer", str(random.randint(0, 33))])],
        weights=([1, 10, 10]),
        k=1,
    )[0]
    fenc = random.choices(
        ["", " ".join([" -fer", str(random.randint(0, 33))])], weights=([1, 10]), k=1
    )[0]
    escr = " ".join([" -escr", str(random.randint(75, 100))])
    encounters = "".join([renc, fenc, escr])

    battle = "".join([bosses, b_ai, scaling, encounters, xpmpgp])

    # -----MAGIC-----
    # ESPERS
    esr1 = random.randint(1, 3)
    esr2 = random.randint(esr1, 5)
    esr = " ".join([" -esr", str(esr1), str(esr2)])
    ess = random.choices(
        ["", esr, " -esrr", " -ess", " -essrr", " -esrt"],
        weights=([1, 7, 2, 2, 2, 3]),
        k=1,
    )[0]
    ebonus = random.choices(
        ["", " ".join([" -ebr", str(random.randint(67, 100))]), " -ebs"],
        weights=([1, 7, 3]),
        k=1,
    )[0]
    emprp1 = random.randint(50, 125)
    emprp2 = random.randint(emprp1, 150)
    emprv1 = random.randint(50, 99)
    emprv2 = random.randint(emprv1, 120)
    eer1 = random.randint(3, 8)
    eer2 = random.randint(eer1, 10)
    emprp = " ".join([" -emprp", str(emprp1), str(emprp2)])
    emprv = " ".join([" -emprv", str(emprv1), str(emprv2)])
    emp = random.choices(["", emprp, emprv, " -emps"], weights=([1, 7, 3, 3]), k=1)[0]
    eer = " ".join([" -eer", str(eer1), str(eer2)])
    eebr = " ".join([" -eebr", str(random.randint(3, 9))])
    eeq = random.choices([eer, eebr, ""], weights=([1, 2, 7]), k=1)[0]
    ems = random.choices(["", " -ems"], weights=([7, 1]), k=1)[0]
    espers = "".join([ess, ebonus, emp, eeq, ems])
    stespr1 = random.randint(1, 2)
    stespr2 = random.randint(stespr1, 4)
    stesp = random.choice(["", " ".join([" -stesp", str(stespr1), str(stespr2)])])
    espers += stesp

    # NATURAL MAGIC
    nm1 = random.choices(["", " -nm1 random"], weights=([1, 10]), k=1)[0]
    nm2 = random.choices(["", " -nm2 random"], weights=([1, 10]), k=1)[0]
    rnl1 = random.choices(["", " -rnl1"], weights=([0, 1]), k=1)[0]
    rnl2 = random.choices(["", " -rnl2"], weights=([0, 1]), k=1)[0]
    rns1 = random.choices(["", " -rns1"], weights=([0, 1]), k=1)[0]
    rns2 = random.choices(["", " -rns2"], weights=([0, 1]), k=1)[0]
    m_indicator = random.choices(["", " -nmmi"], weights=([0, 1]), k=1)[0]
    nmagic = "".join([nm1, nm2, rnl1, rnl2, rns1, rns2, m_indicator])
    mmprp1 = random.randint(50, 125)
    mmprp2 = random.randint(emprp1, 150)
    mmprv1 = random.randint(1, 50)
    mmprv2 = random.randint(emprv1, 99)
    mmp = random.choice(
        [
            "",
            " -mmps",
            " ".join([" -mmprv", str(mmprv1), str(mmprv2)]),
            " ".join([" -mmprp", str(mmprp1), str(mmprp2)]),
        ]
    )
    mmp += random.choices(["", " -u254"], weights=([10, 1]), k=1)[0]
    nmagic += mmp

    magic = "".join([espers, nmagic])

    # -----ITEMS-----
    # STARTING GOLD/ITEMS
    gp = " ".join([" -gp", str(random.randint(0, 100000))])
    smc = " ".join(
        [" -smc", random.choices(["1", "2", "3"], weights=([1, 2, 7]), k=1)[0]]
    )
    sws = " ".join([" -sws", str(random.randint(0, 10))])
    sfd = " ".join([" -sfd", str(random.randint(0, 10))])
    sto = " ".join([" -sto", str(random.randint(0, 6))])
    s_inv = "".join([gp, smc, sfd, sto, sws])

    # ITEMS
    ier1 = random.randint(4, 8)
    ier2 = random.randint(ier1, 10)
    ier = " ".join([" -ier", str(ier1), str(ier2)])
    iebr = " ".join([" -iebr", str(random.randint(4, 10))])
    ieor = " ".join([" -ieor", str(random.randint(15, 75))])
    iesr = " ".join([" -iesr", str(random.randint(15, 75))])
    iequip = random.choices(
        ["", ier, iebr, ieor, iesr], weights=([1, 2, 2, 7, 2]), k=1
    )[0]
    ierr1 = random.randint(4, 8)
    ierr2 = random.randint(ierr1, 10)
    ierr = " ".join([" -ierr", str(ierr1), str(ierr2)])
    ierbr = " ".join([" -ierbr", str(random.randint(4, 10))])
    ieror = " ".join([" -ieror", str(random.randint(15, 75))])
    iersr = " ".join([" -iersr", str(random.randint(15, 75))])
    requip = random.choices(
        ["", ierr, ierbr, ieror, iersr], weights=([1, 2, 2, 7, 2]), k=1
    )[0]
    csb1 = random.randint(1, 32)
    csb2 = random.randint(csb1, 32)
    csb = " ".join([" -csb", str(csb1), str(csb2)])
    mca = random.choices([" -mca", ""], weights=([13, 1]), k=1)[0]
    stra = random.choices([" -stra", ""], weights=([1, 0]), k=1)[0]
    saw = random.choices([" -saw", ""], weights=([1, 0]), k=1)[0]
    equips = "".join([iequip, requip, csb, mca, stra, saw])

    # SHOPS
    sisr = " ".join([" -sisr", str(random.randint(10, 80))])
    shopinv = random.choices(
        ["", sisr, " -sirt", " -sie"], weights=([3, 10, 5, 1]), k=1
    )[0]
    sprv1 = random.randint(0, 65535)
    sprv2 = random.randint(sprv1, 65535)
    sprp1 = random.randint(25, 125)
    sprp2 = random.randint(sprp1, 175)
    sprv = " ".join([" -sprv", str(sprv1), str(sprv2)])
    sprp = " ".join([" -sprp", str(sprp1), str(sprp2)])
    shopprices = random.choices(["", sprv, sprp], weights=([1, 2, 7]), k=1)[0]
    ssf = random.choices(
        ["", " -ssf4", " -ssf8", " -ssf0"], weights=([7, 1, 1, 0]), k=1
    )[0]
    sdm = " ".join([" -sdm", str(random.randint(3, 5))])
    npi = random.choices(["", " -npi"], weights=([1, 13]), k=1)[0]
    snbr = random.choices(["", " -snbr"], weights=([7, 1]), k=1)[0]
    snes = random.choices(["", " -snes"], weights=([7, 1]), k=1)[0]
    snsb = random.choices(["", " -snsb"], weights=([7, 1]), k=1)[0]
    shops = "".join([shopinv, shopprices, ssf, sdm, npi, snbr, snes, snsb])

    # CHESTS
    ccontents = random.choices(
        ["", " -ccrt", " -cce", " ".join([" -ccsr", str(random.randint(10, 80))])],
        weights=([1, 6, 1, 13]),
        k=1,
    )[0]
    cms = random.choices(["", " -cms"], weights=([1, 13]), k=1)[0]
    chests = "".join([ccontents, cms])

    items = "".join([s_inv, equips, shops, chests])

    # -----CUSTOM-----
    # SEE CUSTOM_SPRITES_PORTRAITS.PY
    wmhc = random.choice(["", " -wmhc"])

    # -----OTHER-----
    # COLISEUM
    coper = random.randint(45, 85)
    crper = random.randint(45, 85)
    co = f" -cor {coper}"
    cr = f" -crr {crper}"
    crvr1 = random.randint(20, 80)
    crvr2 = random.randint(crvr1, 150)
    visible = random.choices(
        ["", " ".join([" -crvr", str(crvr1), str(crvr2)])], weights=([1, 10]), k=1
    )[0]
    rmenu = random.choices(["", " -crm"], weights=([1, 13]), k=1)[0]
    colo = "".join([co, cr, visible, rmenu])

    # AUCTION HOUSE
    ari = random.choices(["", " -ari"], weights=([0, 1]), k=1)[0]
    anca = random.choices(["", " -anca"], weights=([0, 1]), k=1)[0]
    adeh = random.choices(["", " -adeh"], weights=([1, 13]), k=1)[0]
    ah = "".join([ari, anca, adeh])

    # MISC
    asprint = " ".join([" -move", random.choice(["as", "bd", "ssbd"])])
    ond = random.choices(["", " -ond"], weights=([1, 13]), k=1)[0]
    rr = random.choices(["", " -rr"], weights=([1, 13]), k=1)[0]
    scan = random.choices(["", " -scan"], weights=([13, 1]), k=1)[0]
    etimers = random.choices(["", " -etr", " -etn"], weights=([2, 3, 1]), k=1)[0]
    ychoices = [
        " -ymascot",
        " -ycreature",
        " -yimperial",
        " -ymain",
        " -yreflect",
        " -ystone",
        " -ysketch",
        " -yrandom",
        " -yremove",
        "",
    ]
    ychoice = random.choices(ychoices, weights=([1, 1, 1, 1, 1, 1, 1, 1, 2, 10]), k=1)[
        0
    ]
    flashes = random.choice(["", " -frm", " -frw"])
    warp = random.choice(["", " -warp"])
    misc = "".join([asprint, ond, rr, scan, etimers, ychoice, flashes, warp])

    # CHALLENGES
    nmc = random.choices(["", " -nmc"], weights=([1, 5]), k=1)[0]
    nee = random.choices(["", " -nee"], weights=([7, 1]), k=1)[0]
    nil = random.choices(["", " -nil"], weights=([6, 4]), k=1)[0]
    nfps = random.choices(["", " -nfps"], weights=([1, 13]), k=1)[0]
    if "-u254" in magic:
        nu = ""
    else:
        nu = random.choices(["", " -nu"], weights=([1, 13]), k=1)[0]
    rls = random.choices(
        ["", " -rls all", " -rls grey", " -rls black", " -rls white"],
        weights=([13, 1, 1, 1, 1]),
        k=1,
    )[0]
    nfp = random.choices(["", " -nfce"], weights=([7, 1]), k=1)[0]
    pd = random.choices(["", " -pd"], weights=([13, 1]), k=1)[0]
    challenges = "".join([nmc, nee, nil, nfps, nu, nfp, pd, rls])

    # BUG FIXES
    fs = random.choices(["", " -fs"], weights=([0, 1]), k=1)[0]
    fe = random.choices(["", " -fe"], weights=([1, 13]), k=1)[0]
    fvd = random.choices(["", " -fvd"], weights=([1, 13]), k=1)[0]
    fr = random.choices(["", " -fr"], weights=([1, 13]), k=1)[0]
    fj = random.choices(["", " -fj"], weights=([0, 1]), k=1)[0]
    fbs = random.choices(["", " -fbs"], weights=([1, 13]), k=1)[0]
    fedc = random.choices(["", " -fedc"], weights=([0, 1]), k=1)[0]
    fc = random.choices(["", " -fc"], weights=([1, 13]), k=1)[0]
    bugfixes = "".join([fs, fe, fvd, fr, fj, fbs, fedc, fc])

    other = "".join([colo, ah, challenges, misc, bugfixes])

    flagset = "".join([game, party, battle, magic, items, other, wmhc])
    return flagset


def true_chaos():
    # -----GAME-----
    # SETTINGS
    mode = random.choice(["-open", "-cg"])
    slog = random.choice([" -sl", ""])
    settings = mode + slog

    # KEFKA'S TOWER & STATUE SKIP
    ktcr1 = random.randint(3, 14)
    ktcr2 = random.randint(ktcr1, 14)
    kter1 = random.randint(1, 27)
    kter2 = random.randint(kter1, 27)
    ktdr1 = random.randint(1, 8)
    ktdr2 = random.randint(ktdr1, 8)
    stcr1 = random.randint(3, 14)
    stcr2 = random.randint(stcr1, 14)
    ster1 = random.randint(1, 24)
    ster2 = random.randint(ster1, 24)
    stdr1 = random.randint(1, 8)
    stdr2 = random.randint(stdr1, 8)
    stno = random.choice([True, False])

    if stno:
        kt = ".".join(
            [
                " -oa 2.2.2.2",
                str(ktcr1),
                str(ktcr2),
                "4",
                str(kter1),
                str(kter2),
                "6",
                str(ktdr1),
                str(ktdr2),
            ]
        )
    else:
        kt = ".".join(
            [
                " -oa 2.2.2.2",
                str(ktcr1),
                str(ktcr2),
                "4",
                str(kter1),
                str(kter2),
                "6",
                str(ktdr1),
                str(ktdr2),
            ]
        )
        kt += ".".join(
            [
                " -ob 3.2.2.2",
                str(stcr1),
                str(stcr2),
                "4",
                str(ster1),
                str(ster2),
                "6",
                str(stdr1),
                str(stdr2),
            ]
        )

    objectives_list = [
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
    ]
    objectives = ""
    for x in objectives_list:
        o_choice = random.choice([True, False])
        if o_choice:
            objectives += "".join([" -o", x, " 0.1.1.1.r"])

    game = settings + kt + objectives

    # -----PARTY-----
    # STARTING PARTY

    # Always roll one starting character, then up to 3 more with 50% chance each
    sc_values = [random.choice(['random', 'randomngu'])]
    for _ in range(3):
        if random.random() < 0.5:
            sc_values.append(random.choice(['random', 'randomngu']))
    sc_flags = [f" -sc{i+1} {val}" for i, val in enumerate(sc_values)]
    sparty = "".join(sc_flags)

    # SWORDTECHS
    fst = random.choice([" -fst", ""])
    sel = random.choice([" -sel", ""])
    swdtech = fst + sel

    # BLITZES
    brl = random.choice([" -brl", ""])
    bel = random.choice([" -bel", ""])
    blitz = brl + bel

    # LORES
    slr1 = random.randint(0, 24)
    slr2 = random.randint(slr1, 24)
    slrr = " -slr " + str(slr1) + " " + str(slr2)
    slr = random.choice([slrr, ""])
    lmprp1 = random.randint(0, 200)
    lmprp2 = random.randint(lmprp1, 200)
    lmprv1 = random.randint(0, 99)
    lmprv2 = random.randint(lmprv1, 99)
    lmprp = " -lmprp " + str(lmprp1) + " " + str(lmprp2)
    lmprv = " -lmprv " + str(lmprv1) + " " + str(lmprv2)
    loremp = random.choice(["", " -lmps", lmprp, lmprv])
    lel = random.choice([" -lel", ""])
    lores = slr + loremp + lel

    # RAGES
    srr1 = random.randint(0, 255)
    srr2 = random.randint(srr1, 255)
    srr = " -srr " + str(srr1) + " " + str(srr2)
    srages = random.choice(["", srr])
    rnl = random.choice([" -rnl", ""])
    rnc = random.choice([" -rnc", ""])
    rage = srages + rnl + rnc

    # DANCES
    sdr1 = random.randint(0, 8)
    sdr2 = random.randint(sdr1, 8)
    sdr = " -sdr " + str(sdr1) + " " + str(sdr2)
    das = random.choice([" -das", ""])
    dda = random.choice([" -dda", ""])
    dns = random.choice([" -dns", ""])
    d_el = random.choice([" -del", ""])
    dance = sdr + das + dda + dns + d_el

    # STEAL CHANCES
    steal = random.choice(["", " -sch", " -sca"])

    # CHARACTERS
    sal = random.choice([" -sal", ""])
    sn = random.choice([" -sn", ""])
    eu = random.choice([" -eu", ""])
    csrp1 = random.randint(0, 200)
    csrp2 = random.randint(csrp1, 200)
    csrp = " -csrp " + str(csrp1) + " " + str(csrp2)
    cstats = sal + sn + eu + csrp

    # COMMANDS
    skills = [
        "10",
        "06",
        "14",
        "19",
        "24",
        "26",
        "22",
        "12",
        "03",
        "28",
        "16",
        "11",
        "27",
        "13",
        "15",
        "05",
        "07",
        "08",
        "09",
        "23",
        "97",
        "98",
        "99",
        "00",
        "29",
    ]
    nmskills = [
        "10",
        "06",
        "14",
        "19",
        "24",
        "26",
        "22",
        "12",
        "28",
        "16",
        "11",
        "27",
        "13",
        "15",
        "05",
        "07",
        "08",
        "09",
        "23",
        "97",
        "98",
        "99",
        "00",
        "29",
    ]
    recskills = [
        "10",
        "06",
        "14",
        "19",
        "24",
        "26",
        "22",
        "12",
        "03",
        "28",
        "16",
        "11",
        "27",
        "13",
        "15",
        "05",
        "07",
        "08",
        "09",
        "23",
        "29",
    ]
    scc = random.choice([" -scc", ""])
    mcount = 0
    ccount = 0
    coms = ""
    while mcount == 0 and ccount < 13:
        rc = random.choice(skills)
        if rc == "03":
            mcount += 1
        ccount += 1
        coms += rc
    if len(coms) < 26:
        while ccount < 13:
            ccount += 1
            coms += random.choice(nmskills)
    com = "".join([" -com ", coms])
    rec1 = random.choice(["", " -rec1 " + random.choice(recskills)])
    rec2 = random.choice(["", " -rec2 " + random.choice(recskills)])
    rec3 = random.choice(["", " -rec3 " + random.choice(recskills)])
    rec4 = random.choice(["", " -rec4 " + random.choice(recskills)])
    rec5 = random.choice(["", " -rec5 " + random.choice(recskills)])
    commands = scc + com + rec1 + rec2 + rec3 + rec4 + rec5

    party = sparty + swdtech + blitz + lores + rage + dance + cstats + commands + steal

    # -----BATTLE-----
    i = range(1, 256)
    j = [0.96**k for k in i]
    xpm = " -xpm " + str((random.choices(i, weights=j, k=1))[0])
    gpm = " -gpm " + str((random.choices(i, weights=j, k=1))[0])
    mpm = " -mpm " + str((random.choices(i, weights=j, k=1))[0])
    nxppd = random.choice([" -nxppd", ""])
    xpmpgp = xpm + gpm + mpm + nxppd

    # # -----BATTLE----- /// THESE ARE THE ORIGINAL SETTINGS
    # xpm = ' -xpm ' + str(random.randint(1, 255))
    # gpm = ' -gpm ' + str(random.randint(1, 255))
    # mpm = ' -mpm ' + str(random.randint(1, 255))
    # nxppd = random.choice([' -nxppd', ''])
    # xpmpgp = xpm + gpm + mpm + nxppd

    # BOSSES
    bb = random.choice([" -bbr", " -bbs", ""])
    bmbd = random.choice([" -drloc mix", ""])
    srp3 = random.choice([" -srp3", ""])
    bnds = random.choice([" -bnds", ""])
    be = random.choice([" -be", ""])
    bnu = random.choice([" -bnu", ""])
    bosses = bb + bmbd + srp3 + bnds + be + bnu

    # BOSS AI
    dgne = random.choice([" -dgne", ""])
    wnz = random.choice([" -wnz", ""])
    mmnu = random.choice([" -mmnu", ""])
    cmd = random.choice([" -cmd", ""])
    b_ai = dgne + wnz + mmnu + cmd

    # SCALING
    scale_opt = ["0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    lspf = " -lsced " + random.choice(scale_opt)
    lsaf = " -lsa " + random.choice(scale_opt)
    lshf = " -lsh " + random.choice(scale_opt)
    lstf = " -lst " + random.choice(scale_opt)
    hmpf = " -hmced " + random.choice(scale_opt)
    hmaf = " -hma " + random.choice(scale_opt)
    hmhf = " -hmh " + random.choice(scale_opt)
    hmtf = " -hmt " + random.choice(scale_opt)
    xgpf = " -xgced " + random.choice(scale_opt)
    xgaf = " -xga " + random.choice(scale_opt)
    xghf = " -xgh " + random.choice(scale_opt)
    xgtf = " -xgt " + random.choice(scale_opt)
    asrf = " -asr " + random.choice(scale_opt)
    asef = " -ase " + random.choice(scale_opt)
    lscale = random.choice([lspf, lsaf, lshf, lstf, ""])
    hmscale = random.choice([hmpf, hmaf, hmhf, hmtf, ""])
    xgscale = random.choice([xgpf, xgaf, xghf, xgtf, ""])
    ascale = random.choice([asrf, asef, ""])
    msl = " -msl " + str(random.randint(3, 99))
    sfb = random.choice([" -sfb", ""])
    sed = random.choice([" -sed", ""])
    scaling = lscale + hmscale + xgscale + ascale + msl + sfb + sed

    # ENCOUNTERS
    renc = random.choice(["", " -res", " -rer " + str(random.randint(0, 100))])
    fenc = random.choice(["", " -fer " + str(random.randint(0, 100))])
    escr = " -escr " + str(random.randint(0, 100))
    encounters = renc + fenc + escr

    battle = bosses + b_ai + scaling + encounters + xpmpgp

    # -----MAGIC-----
    # ESPERS
    esr1 = random.randint(1, 5)
    esr2 = random.randint(esr1, 5)
    esr = " -esr " + str(esr1) + " " + str(esr2)
    ess = random.choice(["", esr, " -esrr", " -ess", " -essrr", " -esrt"])
    ebonus = random.choice(["", " -ebr " + str(random.randint(0, 100)), " -ebs"])
    emprp1 = random.randint(0, 200)
    emprp2 = random.randint(emprp1, 200)
    emprv1 = random.randint(1, 128)
    emprv2 = random.randint(emprv1, 128)
    eer1 = random.randint(0, 12)
    eer2 = random.randint(eer1, 12)
    emprp = " -emprp " + str(emprp1) + " " + str(emprp2)
    emprv = " -emprv " + str(emprv1) + " " + str(emprv2)
    emp = random.choice(["", emprp, emprv, " -emps"])
    eer = " -eer " + str(eer1) + " " + str(eer2)
    eebr = " -eebr " + str(random.randint(0, 12))
    eeq = random.choice([eer, eebr, ""])
    ems = random.choice(["", " -ems"])
    espers = ess + ebonus + emp + eeq + ems

    # NATURAL MAGIC
    nm1 = random.choice(["", " -nm1 random"])
    nm2 = random.choice(["", " -nm2 random"])
    rnl1 = random.choice(["", " -rnl1"])
    rnl2 = random.choice(["", " -rnl2"])
    rns1 = random.choice(["", " -rns1"])
    rns2 = random.choice(["", " -rns2"])
    m_indicator = random.choice(["", " -nmmi"])
    nmagic = nm1 + nm2 + rnl1 + rnl2 + rns1 + rns2 + m_indicator

    magic = espers + nmagic

    # -----ITEMS-----
    # STARTING GOLD/ITEMS
    gp = " -gp " + str(random.randint(0, 999999))
    smc = " -smc " + str(random.randint(0, 3))
    sws = " -sws " + str(random.randint(0, 10))
    sfd = " -sfd " + str(random.randint(0, 10))
    sto = " -sto " + str(random.randint(0, 8))
    s_inv = gp + smc + sfd + sto + sws

    # ITEMS
    ier1 = random.randint(0, 14)
    ier2 = random.randint(ier1, 14)
    ier = " -ier " + str(ier1) + " " + str(ier2)
    iebr = " -iebr " + str(random.randint(0, 14))
    ieor = " -ieor " + str(random.randint(0, 100))
    iesr = " -iesr " + str(random.randint(0, 100))
    iequip = random.choice(["", ier, iebr, ieor, iesr])
    ierr1 = random.randint(0, 14)
    ierr2 = random.randint(ierr1, 14)
    ierr = " -ierr " + str(ierr1) + " " + str(ierr2)
    ierbr = " -ierbr " + str(random.randint(0, 14))
    ieror = " -ieror " + str(random.randint(0, 100))
    iersr = " -iersr " + str(random.randint(0, 100))
    requip = random.choice(["", ierr, ierbr, ieror, iersr])
    csb1 = random.randint(1, 256)
    csb2 = random.randint(csb1, 256)
    csb = " -csb " + str(csb1) + " " + str(csb2)
    mca = random.choice([" -mca", ""])
    stra = random.choice([" -stra", ""])
    saw = random.choice([" -saw", ""])
    equips = iequip + requip + csb + mca + stra + saw

    # SHOPS
    sisr = " -sisr " + str(random.randint(0, 100))
    shopinv = random.choice(["", sisr, " -sirt", " -sie"])
    sprv1 = random.randint(0, 65535)
    sprv2 = random.randint(sprv1, 65535)
    sprp1 = random.randint(0, 200)
    sprp2 = random.randint(sprp1, 200)
    sprv = " -sprv " + str(sprv1) + " " + str(sprv2)
    sprp = " -sprp " + str(sprp1) + " " + str(sprp2)
    shopprices = random.choice(["", sprv, sprp])
    ssf = random.choice(["", " -ssf4", " -ssf8", " -ssf0"])
    sdm = " -sdm " + str(random.randint(0, 5))
    npi = random.choice(["", " -npi"])
    snbr = random.choice(["", " -snbr"])
    snes = random.choice(["", " -snes"])
    snsb = random.choice(["", " -snsb"])
    shops = shopinv + shopprices + ssf + sdm + npi + snbr + snes + snsb

    # CHESTS
    ccontents = random.choice(
        ["", " -ccrt", " -cce", " -ccsr " + str(random.randint(0, 100))]
    )
    cms = random.choice(["", " -cms"])
    chests = ccontents + cms

    items = s_inv + equips + shops + chests

    # -----CUSTOM-----
    # SEE CUSTOM_SPRITES_PORTRAITS.PY

    # -----OTHER-----
    # COLISEUM
    coper = random.randint(0, 100)
    crper = random.randint(0, 100)
    co = f" -cor {coper}"
    cr = f" -crr {crper}"
    crvr1 = random.randint(0, 255)
    crvr2 = random.randint(crvr1, 255)
    visible = random.choice(["", " -crvr " + str(crvr1) + " " + str(crvr2)])
    rmenu = random.choice(["", " -crm"])
    colo = "".join([co, cr, visible, rmenu])

    # AUCTION HOUSE
    ari = random.choice(["", " -ari"])
    anca = random.choice(["", " -anca"])
    adeh = random.choice(["", " -adeh"])
    ah = "".join([ari, anca, adeh])

    # MISC
    asprint = random.choice(["", " -move as"])
    ond = random.choice(["", " -ond"])
    rr = random.choice(["", " -rr"])
    scan = random.choice(["", " -scan"])
    etimers = random.choice(["", " -etr", " -etn"])
    ychoices = [
        " -ymascot",
        " -ycreature",
        " -yimperial",
        " -ymain",
        " -yreflect",
        " -ystone",
        " -ysketch",
        " -yrandom",
        " -yremove",
        "",
    ]
    ychoice = random.choice(ychoices)
    flashes = random.choice(["", " -frm", " -frw"])
    misc = "".join([asprint, ond, rr, scan, etimers, ychoice, flashes])

    # CHALLENGES
    nmc = random.choice(["", " -nmc"])
    nee = random.choice(["", " -nee"])
    nil = random.choice(["", " -nil"])
    nfps = random.choice(["", " -nfce"])
    nu = random.choice(["", " -nu"])
    nfp = random.choice(["", " -nfp"])
    pd = random.choice(["", " -pd"])
    challenges = "".join([nmc, nee, nil, nfps, nu, nfp, pd])

    # BUG FIXES
    fs = random.choice(["", " -fs"])
    fe = random.choice(["", " -fe"])
    fvd = random.choice(["", " -fvd"])
    fr = random.choice(["", " -fr"])
    fj = random.choice(["", " -fj"])
    fbs = random.choice(["", " -fbs"])
    fedc = random.choice(["", " -fedc"])
    bugfixes = "".join([fs, fe, fvd, fr, fj, fbs, fedc])

    other = "".join([colo, ah, challenges, misc, bugfixes])

    flagset = game + party + battle + magic + items + other
    return flagset

def practice(pargs):
    # NOTE: if adding new objectives, start with -op
    #defflags = "-open -oa 28.24.24.0.0 -ob 29.255.255.0.0 -oc 26.8.8.0.0 -od 30.8.8.0.0 -oe 31.54.54.0.0 -of 43.0.0 -og 59.0.0 -oh 67.0.0 -oi 68.0.0 -sc1 random -sc2 random -sc3 random -sc4 random -sal -eu -fst -brl -slr 3 5 -lmprp 75 125 -lel -srr 25 35 -rnl -rnc -sdr 1 2 -das -dda -dns -sch -scis -rec1 28 -rec2 27 -xpm 3 -mpm 5 -gpm 5 -nxppd -lsced 4 -hmced 4 -xgced 4 -ase 2 -sed -bbs -drloc shuffle -stloc mix -be -bnu -res -fer 0 -escr 100 -dgne -wnz -mmnu -cmd -stesp 27 27 -esr 2 5 -elrt -ebr 82 -emprp 75 125 -nm1 random -rnl1 -rns1 -nm2 random -rnl2 -rns2 -nmmi -mmprp 75 125 -gp 5000 -smc 3 -sto 1 -ieor 100 -ieror 100 -ir stronger -csb 6 14 -mca -stra -saw -sie -sprp 75 125 -sdm 5 -npi -sebr -snsb -snee -snil -ccsr 20 -chrm 0 0 -cms -frw -wmhc -cor 100 -crr 100 -crvr 100 120 -crm -ari -anca -adeh -ame 1 -nmc -noshoes -u254 -nfps -fs -fe -fvd -fr -fj -fbs -fedc -fc -ond -etn -kprac"
    defflags = "-open -sc1 random -sc2 random -sc3 random -sc4 random -sal -eu -fst -brl -lmprp 75 125 -lel -rnl -rnc -sdr 1 2 -das -dda -dns -sch -scis -xpm 3 -mpm 5 -gpm 5 -nxppd -lsced 4 -hmced 4 -xgced 4 -ase 2 -sed -bbs -drloc shuffle -stloc mix -be -bnu -res -fer 0 -escr 100 -dgne -wnz -mmnu -cmd -esr 2 5 -elrt -ebr 82 -emprp 75 125 -nm1 random -rnl1 -rns1 -nm2 random -rnl2 -rns2 -nmmi -mmprp 75 125 -gp 5000 -smc 3 -ir stronger -csb 6 14 -mca -stra -saw -sie -sprp 75 125 -sdm 5 -npi -sebr -snsb -snee -snil -ccsr 20 -chrm 0 0 -cms -frw -wmhc -cor 100 -crr 100 -crvr 100 120 -crm -ari -anca -adeh -ame 1 -nmc -noshoes -u254 -nfps -fs -fe -fvd -fr -fj -fbs -fedc -fc -ond -etn"
    # prime flagstring with default flags
    flagstring = defflags

    # get options from the user about practice mode
    nocalmness = pargs.find("--nocalmness")
    #fullmode = pargs.find("--full")
    ul = pargs.find("--ul")
    hardmode = pargs.find("--hard")
    waittrick = pargs.find("--waittrick")

    # command options
    noswdtech8 = pargs.find("--noswdtech8")
    nomagitekupgrade = pargs.find("--nomagitekupgrade")
    nobumrush = pargs.find("--nobumrush")
    swdtech = 0
    magitek = 0
    blitz = 0
    lores = " ".join(pargs.split("--lores")[1:]).split("--")[0].split("&")[0].strip()
    rages = " ".join(pargs.split("--rages")[1:]).split("--")[0].split("&")[0].strip()
    tools = " ".join(pargs.split("--tools")[1:]).split("--")[0].split("&")[0].strip()

    # magic options
    espers = " ".join(pargs.split("--espers")[1:]).split("--")[0].split("&")[0].strip()
    spells = " ".join(pargs.split("--spells")[1:]).split("--")[0].split("&")[0].strip()

    # party options
    partylevel = " ".join(pargs.split("--partylevel")[1:]).split("--")[0].split("&")[0].strip()
    bosslevel = " ".join(pargs.split("--bosslevel")[1:]).split("--")[0].split("&")[0].strip()
    stats = " ".join(pargs.split("--stats")[1:]).split("--")[0].split("&")[0].strip()
    equips = 0
    dragoon = 0
    throwables = 0
    restoratives = 0
    htw = 0
    hta = 0
    cmdexclude = ""

    # character options
    terra = " ".join(pargs.split("--terra")[1:]).split("--")[0].split("&")[0].strip()
    locke = " ".join(pargs.split("--locke")[1:]).split("--")[0].split("&")[0].strip()
    cyan = " ".join(pargs.split("--cyan")[1:]).split("--")[0].split("&")[0].strip()
    shadow = " ".join(pargs.split("--shadow")[1:]).split("--")[0].split("&")[0].strip()
    edgar = " ".join(pargs.split("--edgar")[1:]).split("--")[0].split("&")[0].strip()
    sabin = " ".join(pargs.split("--sabin")[1:]).split("--")[0].split("&")[0].strip()
    celes = " ".join(pargs.split("--celes")[1:]).split("--")[0].split("&")[0].strip()
    strago = " ".join(pargs.split("--strago")[1:]).split("--")[0].split("&")[0].strip()
    relm = " ".join(pargs.split("--relm")[1:]).split("--")[0].split("&")[0].strip()
    setzer = " ".join(pargs.split("--setzer")[1:]).split("--")[0].split("&")[0].strip()
    mog = " ".join(pargs.split("--mog")[1:]).split("--")[0].split("&")[0].strip()
    gau1 = " ".join(pargs.split("--gau1")[1:]).split("--")[0].split("&")[0].strip()
    gau2 = " ".join(pargs.split("--gau2")[1:]).split("--")[0].split("&")[0].strip()

    # if hardmode not specified & UL not specified
    if hardmode == -1 and ul == -1:
        # normal practice run
        flagstring += " -praca "
    else:
        # give only subset of items
        flagstring += " -prac "
        # if hard mode specified
        if hardmode != -1:
            # turn on nocalmness mode
            nocalmness = 1
            # only give subset of items & remove top learnable spells
            flagstring += " -rls top "

    # if no Calmness protection specified
    if nocalmness != -1:
        # indicate to FF6WorldsCollide to remove Fenrir/Golem/Phantom, remove Life 3
        flagstring += " -pracnc "

    # if wait trick practice requested
    if waittrick != -1:
        # give Auto-Condemned objective
        flagstring += " -oo 6.0.0 "

    # NOTE: options can override the practice mode
    # if lores specified
    if lores:
        # check individual parms
        lores1 = lores.split()[0]
        lores2 = lores.split()[1]
        # check for invalid values for lores1
        if not lores1.isdigit() or int(lores1) < 0 or int(lores1) > 24:
            # clear out values
            lores = ""
            # check for invalid values for lores2
        elif not lores2.isdigit() or int(lores2) < 0 or int(lores2) > 24:
            # clear out values
            lores = ""

    # if rages specified
    if rages:
        # check individual parms
        rages1 = rages.split()[0]
        rages2 = rages.split()[1]
        # check for invalid values for rages1
        if not rages1.isdigit() or int(rages1) < 0 or int(rages1) > 255:
            # clear out values
            rages = ""
            # check for invalid values for rages2
        elif not rages2.isdigit() or int(rages2) < 0 or int(rages2) > 255:
            # clear out values
            rages = ""

    # if rages specified
    if tools:
        # check individual parms
        tools1 = tools.split()[0]
        # check for invalid values for tools1
        if not tools1.isdigit() or int(tools1) < 0 or int(tools1) > 8:
            # clear out values
            tools = ""

    # if espers specified
    if espers:
        # check individual parms
        espers1 = espers.split()[0]
        espers2 = espers.split()[1]
        # check for invalid values for espers1
        if not espers1.isdigit() or int(espers1) < 0 or int(espers1) > 27:
            # clear out values
            espers = ""
            # check for invalid values for espers2
        elif not espers2.isdigit() or int(espers2) < 0 or int(espers2) > 27:
            # clear out values
            espers = ""

    # if spells specified
    if spells:
        # check individual parms
        spells1 = spells.split()[0]
        spells2 = spells.split()[1]
        # check for invalid values for spells1
        if not spells1.isdigit() or int(spells1) < 0 or int(spells1) > 54:
            # clear out values
            spells = ""
            # check for invalid values for spells2
        elif not spells2.isdigit() or int(spells2) < 0 or int(spells2) > 54:
            # clear out values
            spells = ""

    # if partylevel specified
    if partylevel:
        # check for invalid values for partylevel
        if not partylevel.isdigit() or int(partylevel) > 99 or int(partylevel) < 3:
            # clear out value
            partylevel = ""

    # if bosslevel specified
    if bosslevel:
        # check for invalid values for bosslevel
        if not bosslevel.isdigit() or int(bosslevel) > 99 or int(bosslevel) < 3:
            # clear out value
            bosslevel = ""

    # if stats specified
    if stats:
        stats1 = stats.split()[0]
        stats2 = stats.split()[1]
        # check for invalid values for stats1
        if not stats1.isdigit() or  int(stats1) < 0 or int(stats1) > 200:
            # clear out value
            stats = ""
            # check for invalid values for stats2
        if not stats2.isdigit() or int(stats2) < 0 or int(stats2) > 200:
            # clear out value
            stats = ""

    # if Ultros League type practice, use typical endgame settings
    if ul != -1:
        # party level between 35-45 if not already specified
        if not partylevel:
            partylevel = str(random.randint(35,45))
        # determine SwdTech upgrade: 
        # if noswdtech8 found, it's requested, do NOT give 8 SwdTechs
        # additionally, use 50% chance of not getting SwdTech upgrade to simulate whether Doma Dream completed
        if noswdtech8 != -1 or random.randint(0,1) == 0:
            # may not need this but check for SwdTech 7 unlock potential, otherwise unlock to SwdTech 6
            if int(partylevel) >= 44:
                swdtech = 7
            else:
                swdtech = 6
        # else SwdTech 8 requested or chosen by coin flip
        else:
            swdtech = 8
        # determine Magitek upgrade: 
        # if nomagitekupgrade not found, then grant Magitek upgrade
        # additionally, use 50% chance of not getting Magitek upgrade to simulate whether Magitek Factory completed
        if nomagitekupgrade == -1 or random.randint(0,1) == 0:
            magitek = 1
        # determine Bum Rush upgrade:
        # if party level >= 42 and nobumrush not requested, give 8 Blitzes
        if int(partylevel) >= 42 and nobumrush == -1:
            blitz = 8
        else:
            # may not need this, but give 7 Blitzes
            blitz = 7
        # give 6-14 starting lores
        if not lores:
            lores = "6 12"
        # give 30-50 rage abilities (25-35 to start, then more along the way in the seed)
        if not rages:
            rages = "30 50"
        # give 1-3 tools
        if not tools:
            tools = str(random.randint(1,3))
        # give 9-12 espers
        if not espers:
            espers = "9 12"
        # give 15-30 spells
        if not spells:
            spells = "15 25"
        # boss level between 30-40 if not already specified
        if not bosslevel:
            bosslevel = str(random.randint(30,40))
        # use UL settings for stats if not already specified
        if not stats:
            stats = "80 125"
        # equippable items/relics = original + 33% random
        equips = 33
        # 50% chance at a Dragoon objective -> Boots + Horn + Lance
        dragoon = random.randint(0,1)
        # grant a set of Throwables
        throwables = 1
        # Pick between 1-4 High Tier Weapon objectives to give player
        htw = random.randint(1,4)
        # Pick between 1-3 High Tier Armor objectives to give player
        hta = random.randint(1,3)
        # set commands Random Exclude list to be: Possess, Shock
        cmdexclude = " -rec1 28 -rec2 27 "

    # if hardmode requested, make things a bit more difficult to form a final party
    elif hardmode != -1:
        # no SwdTech upgrade, only go to SwdTech 6
        swdtech = 6
        # no magitek upgrade, do not need to add objective
        magitek = 0
        # no Bum Rush upgrade, give 7 Blitzes (Air Blade at level 30, so will always have it)
        blitz = 7
        # give 4-8 starting lores if not already specified
        if not lores:
            lores = "4 8"
        # give 25-30 rage abilities if not already specified
        if not rages:
            rages = "25 30"
        # give 1 tool if not already specified
        if not tools:
            tools = "1"
        # give 5-9 espers if not already specified
        if not espers:
            espers = "5 9"
        # give 10-20 spells if not already specified
        if not spells:
            spells = "10 20"
        # party level between 32-40 if not already specified
        if not partylevel:
            partylevel = str(random.randint(32,40))
        # boss level between 40-50 if not already specified
        if not bosslevel:
            bosslevel = str(random.randint(40,50))
        # use lower settings for stats if not already specified
        if not stats:
            stats = "70 100"
        # equippable items/relics = original + 10% random
        equips = "10"
        # 20% chance at a Dragoon objective -> Boots + Horn + Lance
        dragoon = random.randint(0,4)
        # 50% chance at High Tier Weapon objective
        htw = random.randint(0,1)
        # 50% chance at High Tier Armor objective
        hta = random.randint(0,1)
        # set commands Random exclude list to be: Possess, Shock, Throw
        cmdexclude = " -rec1 28 -rec2 27 -rec3 8 "

    # else full practice, give player everything
    else:
        # give all Lores, Rages, Blitzes, SwdTechs, Spells, Tools, Magitek Upgrade unless otherwise specified
        if noswdtech8 != -1:
            swdtech = 7
        else:
            swdtech = 8
        if nomagitekupgrade != -1:
            magitek = 0
        else:
            magitek = 1
        if nobumrush != -1:
            blitz = 7
        else:
            blitz = 8
        # if lores not specified
        if not lores:
            lores = "24 24"
        if not rages:
            rages = "255 255"
        if not tools:
            tools = "8"
        if not espers:
            espers = "27 27"
        if not spells:
            spells = "54 54"
        if not partylevel:
            partylevel = "40"
        if not bosslevel:
            bosslevel = "40"
        if not stats:
            stats = "80 125"
        # give throwables & restoratives
        throwables = 1
        restoratives = 1
        # max out equips
        equips = 100
        # only exclude Possess
        cmdexclude = " -rec1 28 "

    # next do the character & commands section by doing a dictionary lookup
    terracmd = str(command(terra))
    lockecmd = str(command(locke))
    cyancmd = str(command(cyan))
    shadowcmd = str(command(shadow))
    edgarcmd = str(command(edgar))
    sabincmd = str(command(sabin))
    celescmd = str(command(celes))
    stragocmd = str(command(strago))
    relmcmd = str(command(relm))
    setzercmd = str(command(setzer))
    mogcmd = str(command(mog))
    # Gau may have 2 commands...
    gaucmds = str(command(gau1)) + str(command(gau2))

    ##### build the flagstring
    # swdtech
    flagstring += " -oa 30." + str(swdtech) + "." + str(swdtech) + ".0.0 " 
    # blitz
    flagstring += " -ob 26." + str(blitz) + "." + str(blitz) + ".0.0 " 
    # magitek upgrade
    if magitek:
        flagstring += " -oc 59.0.0 "
    # lores
    flagstring += " -slr " + lores + " "
    # rages
    flagstring += " -srr " + rages + " "
    # tools
    flagstring += " -sto " + tools + " "
    # starting espers
    flagstring += " -stesp " + espers + " "
    # learn spells
    flagstring += " -od 31." + spells.split()[0] + "." + spells.split()[1] + ".0.0 "
    # party level
    flagstring += " -stl " + partylevel + " "
    # boss level
    flagstring += " -msl " + bosslevel + " "
    # party stats
    flagstring += " -csrp " + stats + " "
    # equippable item/relics
    flagstring += " -ieor " + str(equips) + " -ieror " + str(equips) + " "
    # give dragoon set
    if dragoon != 0:
        flagstring += " -oe 36.0.0 "
    # give throwables
    if throwables != 0:
        flagstring += " -of 67.0.0 "
    # give restoratives
    if restoratives != 0:
        flagstring += " -og 68.0.0 "
    # give up to 4 High Tier Weapons
    if htw > 0:
        i = htw - 1
        j = 0
        obj = ["h","i","j","k"]
        while j <= i:
            flagstring += " -o" + obj[j] + " 69.0.0 "
            j += 1
    # give up to 3 High Tier Armor
    if hta > 0:
        i = hta - 1
        j = 0
        obj = ["l","m","n"]
        while j <= i:
            flagstring += " -o" + obj[j] + " 70.0.0 "
            j += 1
    # add list of excluded commands
    flagstring += cmdexclude
    ### append all of the commands after the -com flag for the command string
    commandstring = " -com " + terracmd + lockecmd + cyancmd + shadowcmd + edgarcmd + sabincmd + celescmd + stragocmd + relmcmd + setzercmd + mogcmd + gaucmds
    flagstring += commandstring
        
    return flagstring
    
# input the command string, returns the command value
def command(cmd):
    # dictionary of command values for flags
    commands = {
        0   : "fight",
        3   : "morph",
        5   : "steal",
        6   : "capture",
        7   : "swdtech",
        8   : "throw",
        9   : "tools",
        10  : "blitz",
        11  : "runic",
        12  : "lore",
        13  : "sketch",
        14  : "control",
        15  : "slot",
        16  : "rage",
        17  : "leap",
        19  : "dance",
        22  : "jump",
        23  : "x magic",
        24  : "gp rain",
        26  : "health",
        27  : "shock",
        28  : "possess",
        29  : "magitek",
        97  : "none",
        98  : "random unique",
        99  : "random",
    }

    # reverse dictionary to look up by command name vs. ID
    command_id = {v: k for k, v in commands.items()}

    # if command not specified
    if not cmd:
        # command is random unique
        cmdnum = command_id["random unique"]
    # else some command specified
    else:
        # if invalid command, use Random Unique
        if cmd.lower() not in map(str.lower,commands.values()):
            cmdnum = command_id["random unique"]
        # else use the numerical value of input command
        else:
            cmdnum = command_id[cmd]
            # if the command is 1 digit, append a 0 in front
            if int(cmdnum) < 10:
                cmdnum = "0" + str(cmdnum)

    return cmdnum
