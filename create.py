import requests
import random
from flags import chaos
from flags import true_chaos
import urllib

def get_chaos():
    chaos_flags = chaos()
    flagstring = urllib.parse.quote(chaos_flags)
    wcurl = 'https://ff6wc.com/flags/'+flagstring
    r = requests.get(wcurl)
    data = r.json()
    return data

def get_truechaos():
    chaos_flags = true_chaos()
    flagstring = urllib.parse.quote(chaos_flags)
    wcurl = 'https://ff6wc.com/flags/'+flagstring
    r = requests.get(wcurl)
    data = r.json()
    return data

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
    flags = mode+kt+ss+sc+sal+sn+eu+csrp+brl+slr+lmprp+srr+fixed+rnc+sdr+xgm+ls+hm+xg+\
            ascale+msl+eel+sbd+bosses+commands+encounters+espers+nmag+startinv+items+\
            shops+chests+colo+challenges+events
    wcurl = 'https://ff6wc.com/flags/'+ flags

    #Get back and parse the data
    r = requests.get(url = wcurl)
    data = r.json()
    return data['flags']
#Print the results
#print(data)
#print('---')
#print(data["share_url"])