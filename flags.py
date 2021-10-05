import random

import custom_sprites_portraits
from palettes import id_palette
from portraits import id_portrait
from sprites import id_sprite
from custom_sprites_portraits import custom_ps as custom_ps

custom_chars = custom_sprites_portraits.roll_custom()
c1 = list(custom_chars)[0]
c2 = list(custom_chars)[1]
c3 = list(custom_chars)[2]
c4 = list(custom_chars)[3]
c5 = list(custom_chars)[4]
c6 = list(custom_chars)[5]
c7 = list(custom_chars)[6]
c8 = list(custom_chars)[7]
c9 = list(custom_chars)[8]
c10 = list(custom_chars)[9]
c11 = list(custom_chars)[10]
c12 = list(custom_chars)[11]
c13 = list(custom_chars)[12]
c14 = list(custom_chars)[13]
c15 = list(custom_chars)[14]
c16 = list(custom_chars)[15]
c17 = list(custom_chars)[16]
c18 = list(custom_chars)[17]
c19 = list(custom_chars)[18]
c20 = list(custom_chars)[19]

print(custom_chars)
char1name = custom_ps[c1]['cname']
char1sprite = custom_ps[c1]['sindex']
char1portrait = custom_ps[c1]['pindex']
char2name = custom_ps[c2]['cname']
char2sprite = custom_ps[c2]['sindex']
char2portrait = custom_ps[c2]['pindex']
char3name = custom_ps[c3]['cname']
char3sprite = custom_ps[c3]['sindex']
char3portrait = custom_ps[c3]['pindex']
char4name = custom_ps[c4]['cname']
char4sprite = custom_ps[c4]['sindex']
char4portrait = custom_ps[c4]['pindex']
char5name = custom_ps[c5]['cname']
char5sprite = custom_ps[c5]['sindex']
char5portrait = custom_ps[c5]['pindex']
char6name = custom_ps[c6]['cname']
char6sprite = custom_ps[c6]['sindex']
char6portrait = custom_ps[c6]['pindex']
char7name = custom_ps[c7]['cname']
char7sprite = custom_ps[c7]['sindex']
char7portrait = custom_ps[c7]['pindex']
char8name = custom_ps[c8]['cname']
char8sprite = custom_ps[c8]['sindex']
char8portrait = custom_ps[c8]['pindex']
char9name = custom_ps[c9]['cname']
char9sprite = custom_ps[c9]['sindex']
char9portrait = custom_ps[c9]['pindex']
char10name = custom_ps[c10]['cname']
char10sprite = custom_ps[c10]['sindex']
char10portrait = custom_ps[c10]['pindex']
char11name = custom_ps[c11]['cname']
char11sprite = custom_ps[c11]['sindex']
char11portrait = custom_ps[c11]['pindex']
char12name = custom_ps[c12]['cname']
char12sprite = custom_ps[c12]['sindex']
char12portrait = custom_ps[c12]['pindex']
char13name = custom_ps[c13]['cname']
char13sprite = custom_ps[c13]['sindex']
char13portrait = custom_ps[c13]['pindex']
char14name = custom_ps[c14]['cname']
char14sprite = custom_ps[c14]['sindex']
char14portrait = custom_ps[c14]['pindex']
char15sprite = custom_ps[c15]['sindex']
char15portrait = custom_ps[c15]['pindex']
char16sprite = custom_ps[c16]['sindex']
char17sprite = custom_ps[c17]['sindex']
char18sprite = custom_ps[c18]['sindex']
char19sprite = custom_ps[c19]['sindex']
char20sprite = custom_ps[c20]['sindex']

def rollseed():
    #-----Game Mode-----
    #Open World or Character Gated
    mode = random.choice(['-ow','-cg','-cg','-cg','-cg','-cg','-cg','-cg','-cg','-cg','-cg'])

    #-----Kefka's Tower Requirements-----
    #Characters
    ktcr1 = random.randint(3,8)
    ktcr2 = random.randint(ktcr1,14)
    ktcr = ' -ktcr '+str(ktcr1)+' '+str(ktcr2)

    #Espers
    kter1 = random.randint(0,10)
    kter2 = random.randint(kter1,24)
    kter = ' -kter '+str(kter1)+' '+str(kter2)

    #Dragons (50% chance to enable)
    ktdr1 = random.randint(0,4)
    ktdr2 = random.randint(ktdr1,8)
    ktdr3 = ' -ktdr '+str(ktdr1)+' '+str(ktdr2)
    ktdr = random.choice(["",ktdr3])

    #Put it all together!
    kt = ktcr + kter + ktdr

    #-----Statue Requirements (50% chance to enable)-----
    #Characters
    stcr1 = random.randint(3,8)
    stcr2 = random.randint(stcr1,14)
    stcr = ' -stcr '+str(stcr1)+' '+str(stcr2)

    #Espers
    ster1 = random.randint(0,10)
    ster2 = random.randint(ster1,24)
    ster = ' -ster '+str(ster1)+' '+str(ster2)

    #Dragons
    stdr1 = random.randint(0,4)
    stdr2 = random.randint(stdr1,8)
    stdr = ' -stdr '+str(stdr1)+' '+str(stdr2)

    #Put it all together!
    ss = random.choice([" -stno",stcr + ster + stdr])

    #-----Characters-----
    sc1 = random.choice([' -sc1 random',' -sc1 randomngu'])
    sc2 = random.choice([' -sc2 random',' -sc2 randomngu'])
    sc3 = random.choice([' -sc3 random',' -sc3 randomngu'])
    sc4 = random.choice([' -sc4 random',' -sc4 randomngu'])
    sc = random.choice([sc1+sc2,sc1+sc2,sc1+sc2,sc1+sc2+sc3,sc1+sc2+sc3,sc1+sc2+sc3+sc4])

    #-----Start Average Level----
    sal = random.choice([' -sal',' -sal',' -sal',' -sal',' -sal',''])

    #-----Start Naked----
    sn = random.choice([' -sn','','','','',''])

    #-----Equippable Umaro----
    eu = random.choice([' -eu',' -eu',' -eu',' -eu',' -eu',''])

    #-----Character Stats (Floor @ 25% so things don't totally suck)-----
    csrp1 = random.randint(25,125)
    csrp2 = random.randint(csrp1,200)
    csrp = " -csrp "+str(csrp1)+" "+str(csrp2)

    #-----Bum Rush Last----
    brl = random.choice([' -brl',' -brl',' -brl',' -brl',' -brl',''])

    #-----Starting Lores-----
    slr1 = random.randint(0,12)
    slr2 = random.randint(slr1,24)
    slr = ' -slr '+str(slr1)+' '+str(slr2)

    #-----Lore MP Cost-----
    lmprp1 = random.randint(0,100)
    lmprp2 = random.randint(lmprp1,200)
    lmprp = ' -lmprp '+str(lmprp1)+' '+str(lmprp2)

    #-----Starting Rages-----
    srr1 = random.randint(0,10)
    srr2 = random.randint(srr1,50)
    srr = ' -srr '+str(srr1)+' '+str(srr2)

    #----Rage No Charm-----
    rnc = random.choice([' -rnc',' -rnc',' -rnc',' -rnc',' -rnc',''])

    #-----Starting Dances-----
    sdr1 = random.randint(0,4)
    sdr2 = random.randint(sdr1,8)
    sdr = ' -sdr '+str(sdr1)+' '+str(sdr2)

    #-----Commands-----
    scc = ' -scc'
    rucom = ' -com 98989898989898989898989898'
    rcom = ' -com 99999999999999999999999999'
    rec1 = ' -rec1 28'
    rec2 = ' -rec2 23'
    rec = random.choice([rec1+rec2,rec1+rec2,rec1+rec2,rec1+rec2,rec1,rec2,""])
    commands = random.choice([scc,rucom,rucom,rucom,rucom,rcom,rcom,""])+rec

    #-----EXP, GP & MP Modifiers-----
    xpm = random.choice(['1','2','2','3','3','3','3','3','4','5'])
    gpm = random.choice(['2','3','3','4','4','5','5','5','5','6','7','8'])
    mpm = random.choice(['2','3','3','4','4','5','5','5','5','6','7','8'])
    nxppd = random.choice([' -nxppd',' -nxppd',' -nxppd',' -nxppd',' -nxppd',' -nxppd',''])
    xgm = ' -xpm '+str(xpm)+' -gpm '+str(gpm)+' -mpm '+str(mpm)+nxppd

    #-----Level Scaling-----
    lsp = ' -lsp '+ random.choice(['1','2','2','2','2','3','3','4'])
    lsa = ' -lsa '+ random.choice(['.5','1','1','1','1.5','1.5','2'])
    lsh = ' -lsh '+ random.choice(['.5','1','1','1','1.5','1.5','2'])
    lst = ' -lst '+ random.choice(['.5','1','1.5','2','2','2','2.5','3'])
    ls = random.choice([lsp,lsp,lsa,lsh,lst])

    #-----HP/MP Scaling-----
    hmp = ' -hmp '+ random.choice(['1','2','2','2','2','3','3','4'])
    hma = ' -hma '+ random.choice(['.5','1','1','1','1.5','1.5','2'])
    hmh = ' -hmh '+ random.choice(['.5','1','1','1','1.5','1.5','2'])
    hmt = ' -hmt '+ random.choice(['.5','1','1.5','2','2','2','2.5','3'])
    hm = random.choice([hmp,hmp,hma,hmh,hmt])

    #-----EXP/GP Scaling-----
    xgp = ' -xgp '+ random.choice(['1','2','2','2','2','3','3','4'])
    xga = ' -xga '+ random.choice(['.5','1','1','1','1.5','1.5','2'])
    xgh = ' -xgh '+ random.choice(['.5','1','1','1','1.5','1.5','2'])
    xgt = ' -xgt '+ random.choice(['.5','1','1.5','2','2','2','2.5','3'])
    xg = random.choice([xgp,xgp,xga,xgh,xgt])

    #-----Ability Scaling-----
    ase = ' -ase '+random.choice(['1','1.5','2','2','2','2.5','3'])
    asr = ' -ase '+random.choice(['1','1.5','2','2','2','2.5','3'])
    ascale = random.choice([ase,ase,ase,ase,ase,asr,asr,asr,""])

    #-----Max Scaling Level-----
    msl = ' -msl '+str(random.randint(40,99))

    #-----Extra Enemy Levels-----
    eel = random.choice(["","","","","",' -eel '+str(random.randint(1,10))])

    #-----Final Boss & Dragon Scaling-----
    sfb = random.choice(['','','','','','','','',' -sfb'])
    sed = random.choice([' -sed',' -sed',' -sed',''])
    sbd = sfb+sed

    #-----Bosses-----
    boss = random.choice([' -bbs',' -bbs',' -bbs',' -bbs',' -bbr',' -bbr',''])
    bmbd = random.choice([' -bmbd','','','',''])
    srp3 = random.choice([' -srp3','','','',''])
    bnds = random.choice([' -bnds','','','',''])
    be = random.choice([' -be',' -be',' -be',' -be',' -be',' -be',' -be',' -be',' -be'''])
    bnu = random.choice([' -bnu','','','',''])
    dgne = random.choice([' -dgne',' -dgne',' -dgne',' -dgne',' -dgne',' -dgne',' -dgne',' -dgne',' -dgne'''])
    wnz = random.choice([' -wnz',' -wnz',' -wnz',' -wnz',' -wnz',' -wnz',' -wnz',' -wnz',' -wnz'''])
    mmnu = random.choice([' -mmnu',' -mmnu',' -mmnu',' -mmnu',' -mmnu',' -mmnu',' -mmnu',' -mmnu',' -mmnu'''])
    cmd = random.choice([' -cmd',' -cmd',' -cmd',' -cmd',' -cmd',' -cmd',' -cmd',' -cmd',' -cmd'''])
    bosses = boss+bmbd+srp3+bnds+be+bnu+dgne+wnz+mmnu+cmd

    #-----Encounters-----
    res = ' -res'
    rer = ' -rer 0'
    rerb = ' -rer ' + str(random.randint(0,100))
    fer = ' -fer 0'
    ferb = ' -fer ' + str(random.randint(0,100))
    escr = ' -escr 100'
    escr2 = ' -escr ' + str(random.randint(0,100))
    encounters = random.choice([res,res,res,res,rer,rer,rer,rerb,''])+random.choice([fer,fer,fer,fer,fer,ferb,''])+\
                 random.choice([escr,escr,escr,escr,escr,escr,escr2,''])

    #-----Espers-----
    esrr = ' -esrr'
    ess = ' -ess'
    essrr = ' -essrr'
    esrint = random.randint(0,5)
    esr = ' -esr ' + str(esrint) + ' ' + str(random.randint(esrint,5))
    esrt = ' -esrt'
    espells = random.choice([esrr,"",ess,essrr,esr,esr,esr,esr,esr,esrt,esrt])
    ebs = ' -ebs'
    ebr75 = ' -ebr 75'
    ebr100 = ' -ebr 100'
    ebr = ' -ebr ' + str(random.randint(0,100))
    ebonus = random.choice(['',ebs,ebr75,ebr75,ebr75,ebr100,ebr,ebr])
    emps = ' -emps'
    emprvint = random.randint(0,125)
    emprpint = random.randint(0,100)
    emprv = ' -emprv ' + str(emprvint) + ' ' + str(random.randint(emprvint,125))
    emprp = ' -emprp ' + str(emprpint) + ' ' + str(random.randint(emprpint,200))
    empr = ' -emprp 75 150'
    emp = random.choice(['',emps,emprv,emprp,empr,empr,empr])
    eerint = random.randint(1,12)
    eer = ' -eer ' + str(eerint) + ' ' + str(random.randint(eerint,12))
    eebr = ' -eebr ' + str(random.randint(1,12))
    eequip = random.choice(['','','','','',eer,eebr,])
    espers = espells+ebonus+emp+eequip

    #-----Natural Magic-----
    nm1 = random.choice([' -nm1 random',' -nm1 random',' -nm1 random',' -nm1 random',' -nm1 random',''])
    nm2 = random.choice([' -nm2 random',' -nm2 random',' -nm2 random',' -nm2 random',' -nm2 random',''])
    nmag = nm1+nm2

    #-----Starting Inventory-----
    gp = random.choice(['',' -gp '+str(random.randint(0,50000))])
    smc1 = ' -smc 3'
    smc = random.choice([smc1,smc1,smc1,smc1,smc1,smc1,smc1,smc1,smc1,smc1,' -smc '+str(random.randint(0,3))])
    sws = ' -sws ' + str(random.randint(0,10))
    sfd = ' -sfd ' + str(random.randint(0,10))
    sto = ' -sto ' + str(random.randint(0,8))
    startinv = gp+smc+sws+sfd+sto

    #-----Items-----
    ierint = random.randint(1,14)
    ier = ' -ier ' + str(ierint) + ' ' + str(random.randint(ierint,14))
    iebr = ' -iebr ' + str(random.randint(1,14))
    ieor = ' -ieor ' + str(random.randint(1,100))
    ieorn = ' -ieor 33'
    iesr = ' -iesr ' + str(random.randint(1,100))
    eitem = random.choice(['',ier,iebr,ieor,ieorn,ieorn,ieorn,iesr])
    ierrint = random.randint(1,14)
    ierr = ' -ierr ' + str(ierrint) + ' ' + str(random.randint(ierrint,14))
    ierbr = ' -ierbr ' + str(random.randint(1,14))
    ieror = ' -ieror ' + str(random.randint(1,100))
    ierorn = ' -ieror 33'
    iersr = ' -iersr ' + str(random.randint(1,100))
    erelic = random.choice(['',ierr,ierbr,ieror,ierorn,ierorn,ierorn,iersr])
    csb1 = random.randint(1,10)
    csb = ' -csb ' + str(csb1) + ' ' + str(random.randint(csb1,32))
    items = eitem+erelic+csb

    #-----Shops-----
    sisr = ' -sisr ' + str(random.randint(0,100))
    sirt = ' -sirt'
    sie = ' -sie'
    shopinv = random.choice(['',sie,sirt,sirt,sirt,sisr,sisr,sisr,sisr,sisr,sisr])
    sprp1 = random.randint(0,100)
    sprp = ' -sprp ' + str(sprp1) + ' ' + str(random.randint(sprp1,200))
    sprv = ' -sprv 1 65535'
    sprice = random.choice(['',sprp,sprp,sprp,sprp,sprv])
    npi = random.choice([' -npi',' -npi',' -npi',' -npi',' -npi',' -npi',' -npi',' -npi',' -npi',''])
    snbr = random.choice([' -snbr',''])
    snes = random.choice([' -snes',''])
    snsb = random.choice([' -snsb',''])
    shops = shopinv+sprice+npi+snbr+snes+snsb

    #-----Chests-----
    ccsr = ' -ccsr ' + str(random.randint(0,100))
    ccrt = ' -ccrt'
    cce = ' -cce'
    ccontents = random.choice([ccsr,ccsr,ccsr,ccsr,ccrt,ccrt,ccsr,ccsr,ccrt,cce,''])
    cms = random.choice([' -cms',' -cms',' -cms',' -cms',' -cms',''])
    chests = ccontents+cms

    # -----CUSTOM-----
    cpalf = random.choices(list(id_palette.keys()), k=7)
    cporf = random.choices(list(id_portrait.keys()), k=15)
    csprf = random.choices(list(id_sprite.keys()), k=20)
    csppf = random.choices(list(range(0, 6)), k=14)
    csppf2 = random.choices(list(range(0, 7)), k=6)

    cpal = ' -cpal ' + str(cpalf[0]) + "." + str(cpalf[1]) + "." + str(cpalf[2]) + "." + str(cpalf[3]) + "." \
           + str(cpalf[4]) + "." + str(cpalf[5]) + "." + str(cpalf[6])
    cpor = ' -cpor ' + '.'.join(
        [str(char1portrait), str(char2portrait), str(char3portrait), str(char4portrait),
         str(char5portrait), str(char6portrait), str(char7portrait), str(char8portrait),
         str(char9portrait),
         str(char10portrait), str(char11portrait), str(char12portrait), str(char13portrait),
         str(char14portrait),
         str(char15portrait)])
    cspr = ' -cspr ' + '.'.join([str(char1sprite), str(char2sprite), str(char3sprite), str(char4sprite),
                                 str(char5sprite), str(char6sprite), str(char7sprite), str(char8sprite),
                                 str(char9sprite),
                                 str(char10sprite), str(char11sprite), str(char12sprite), str(char13sprite),
                                 str(char14sprite),
                                 str(char15sprite), str(char16sprite), str(char17sprite), str(char18sprite),
                                 str(char19sprite),
                                 str(char20sprite)])
    cspp = ' -cspp ' + str(csppf[0]) + "." + str(csppf[1]) + "." + str(csppf[2]) + "." + str(csppf[3]) + "." \
           + str(csppf[4]) + "." + str(csppf[5]) + "." + str(csppf[6]) + "." + str(csppf[7]) + "." + str(
        csppf[8]) + "." + \
           str(csppf[9]) + "." + str(csppf[10]) + "." + str(csppf[11]) + "." + str(csppf[12]) + "." + str(csppf[13]) \
           + "." + str(csppf2[0]) + "." + str(csppf2[1]) + "." + str(csppf2[2]) + "." + str(csppf2[3]) + "." + \
           str(csppf2[4]) + "." + str(csppf2[5])
    cname = ' -name ' + '.'.join([str(char1name), str(char2name), str(char3name), str(char4name), str(char5name),
            str(char6name), str(char7name), str(char8name), str(char9name), str(char10name), str(char11name),
            str(char12name), str(char13name), str(char14name)])

    custom = cspp + cpal + cspr + cpor + cname

    #-----Coliesuem-----
    cors = random.choice([' -cos',' -cor','',' -cor',' -cor',' -cor',' -cor',' -cor',' -cor'])
    crewards = random.choice([' -crs','',' -crr',' -crr',' -crr',' -crr',' -crr',' -crr',' -crr'])
    crvr1 = random.randint(0,100)
    crvr = ' -crvr ' + str(crvr1) + ' ' + str(random.randint(crvr1,255))
    visible = random.choice(['',crvr,crvr,crvr])
    crm = random.choice(['',' -crm',' -crm',' -crm'])
    colo = cors+crewards+crm+visible

    #-----Challenges-----
    nmc = random.choice(['',' -nmc'])
    nee = random.choice(['',' -nee'])
    nil = random.choice(['',' -nil'])
    nfps = random.choice(['',' -nfps',' -nfps',' -nfps',' -nfps',' -nfps'])
    nu = random.choice(['',' -nu',' -nu',' -nu'])
    kthr = random.choice(['','','','','','','','','','',' -kthr'])
    nfp = random.choice(['','','','',' -nfp'])
    pd = random.choice(['','','','','','','','','','','','','',' -pd'])
    challenges = nmc+nee+nil+nfps+nu+kthr+nfp+pd

    #-----Events-----
    timers = random.choice(['',' -etr',' -etn'])
    ynpc = random.choice(['','','',' -yremove'])
    events = timers+ynpc

    #-----Fixed Flags (things that are always on)-----
    fixed = ' -fst -rnl -das -dda -dns -nmmi -rnl1 -rns1 -rnl2 -rns2 -mca -stra -saw' \
            ' -ari -anca -adeh -fs -fe -fvd -fr -fj -fbs -fedc -as -ond -rr -sdm 4' \
            ' -lel'

    #Send everything to the FF6WC API
    flagset = mode+kt+ss+sc+sal+sn+eu+csrp+brl+slr+lmprp+srr+fixed+rnc+sdr+xgm+ls+hm+xg+\
            ascale+msl+eel+sbd+bosses+commands+encounters+espers+nmag+startinv+items+\
            shops+chests+colo+challenges+events+custom
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
    cpalf = random.choices(list(id_palette.keys()), k=7)
    cporf = random.choices(list(id_portrait.keys()), k=15)
    csprf = random.choices(list(id_sprite.keys()), k=20)
    csppf = random.choices(list(range(0, 6)), k=14)
    csppf2 = random.choices(list(range(0, 7)), k=6)

    cpal = ' -cpal ' + str(cpalf[0]) + "." + str(cpalf[1]) + "." + str(cpalf[2]) + "." + str(cpalf[3]) + "." \
           + str(cpalf[4]) + "." + str(cpalf[5]) + "." + str(cpalf[6])
    cpor = ' -cpor ' + '.'.join(
        [str(char1portrait), str(char2portrait), str(char3portrait), str(char4portrait),
         str(char5portrait), str(char6portrait), str(char7portrait), str(char8portrait),
         str(char9portrait),
         str(char10portrait), str(char11portrait), str(char12portrait), str(char13portrait),
         str(char14portrait),
         str(char15portrait)])
    cspr = ' -cspr ' + '.'.join([str(char1sprite), str(char2sprite), str(char3sprite), str(char4sprite),
                                 str(char5sprite), str(char6sprite), str(char7sprite), str(char8sprite),
                                 str(char9sprite),
                                 str(char10sprite), str(char11sprite), str(char12sprite), str(char13sprite),
                                 str(char14sprite),
                                 str(char15sprite), str(char16sprite), str(char17sprite), str(char18sprite),
                                 str(char19sprite),
                                 str(char20sprite)])
    cspp = ' -cspp ' + str(csppf[0]) + "." + str(csppf[1]) + "." + str(csppf[2]) + "." + str(csppf[3]) + "." \
           + str(csppf[4]) + "." + str(csppf[5]) + "." + str(csppf[6]) + "." + str(csppf[7]) + "." + str(
        csppf[8]) + "." + \
           str(csppf[9]) + "." + str(csppf[10]) + "." + str(csppf[11]) + "." + str(csppf[12]) + "." + str(csppf[13]) \
           + "." + str(csppf2[0]) + "." + str(csppf2[1]) + "." + str(csppf2[2]) + "." + str(csppf2[3]) + "." + \
           str(csppf2[4]) + "." + str(csppf2[5])
    cname = ' -name ' + '.'.join(
        [str(char1name), str(char2name), str(char3name), str(char4name), str(char5name),
         str(char6name), str(char7name), str(char8name), str(char9name), str(char10name),
         str(char11name),
         str(char12name), str(char13name), str(char14name)])

    custom = cspp + cpal + cspr + cpor + cname

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
    cpalf = random.choices(list(id_palette.keys()), k=7)
    cporf = random.choices(list(id_portrait.keys()), k=15)
    csprf = random.choices(list(id_sprite.keys()), k=20)
    csppf = random.choices(list(range(0, 6)), k=14)
    csppf2 = random.choices(list(range(0, 7)), k=6)

    cpal = ' -cpal ' + str(cpalf[0]) + "." + str(cpalf[1]) + "." + str(cpalf[2]) + "." + str(cpalf[3]) + "." \
           + str(cpalf[4]) + "." + str(cpalf[5]) + "." + str(cpalf[6])
    cpor = ' -cpor ' + '.'.join(
        [str(char1portrait), str(char2portrait), str(char3portrait), str(char4portrait),
         str(char5portrait), str(char6portrait), str(char7portrait), str(char8portrait),
         str(char9portrait),
         str(char10portrait), str(char11portrait), str(char12portrait), str(char13portrait),
         str(char14portrait),
         str(char15portrait)])
    cspr = ' -cspr ' + '.'.join([str(char1sprite), str(char2sprite), str(char3sprite), str(char4sprite),
                                 str(char5sprite), str(char6sprite), str(char7sprite), str(char8sprite),
                                 str(char9sprite),
                                 str(char10sprite), str(char11sprite), str(char12sprite), str(char13sprite),
                                 str(char14sprite),
                                 str(char15sprite), str(char16sprite), str(char17sprite), str(char18sprite),
                                 str(char19sprite),
                                 str(char20sprite)])
    cspp = ' -cspp ' + str(csppf[0]) + "." + str(csppf[1]) + "." + str(csppf[2]) + "." + str(csppf[3]) + "." \
           + str(csppf[4]) + "." + str(csppf[5]) + "." + str(csppf[6]) + "." + str(csppf[7]) + "." + str(
        csppf[8]) + "." + \
           str(csppf[9]) + "." + str(csppf[10]) + "." + str(csppf[11]) + "." + str(csppf[12]) + "." + str(csppf[13]) \
           + "." + str(csppf2[0]) + "." + str(csppf2[1]) + "." + str(csppf2[2]) + "." + str(csppf2[3]) + "." + \
           str(csppf2[4]) + "." + str(csppf2[5])
    cname = ' -name ' + '.'.join([str(char1name), str(char2name), str(char3name), str(char4name), str(char5name),
            str(char6name), str(char7name), str(char8name), str(char9name), str(char10name), str(char11name),
            str(char12name), str(char13name), str(char14name)])

    custom = cspp + cpal + cspr + cpor + cname

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
    return flagset

# print(chaos())