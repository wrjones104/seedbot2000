import random
from portraits import id_portrait
from sprites import id_sprite
from palettes import id_palette

ffiv = " -name Rydia.CecilP.CecilD.Edge.Palom.Porom.Rosa.Tellah.RydiaC.Cid.Kain.Edward.FuSoYa.Yang" \
       " -cpal 98.110.30.87.109.33.61 -cpor 74.36.34.41.66.67.72.77.73.38.53.42.47.80.46" \
       " -cspr 110.41.40.50.99.100.108.121.109.43.80.51.63.134.119.62.18.19.91.73" \
       " -cspp 0.1.2.2.3.3.1.4.0.5.2.3.4.5.5.3.0.5.4.6"
tmnt = " -name VENUS.CASEY.LEO.MIKEY.BEBOP.RAPH.APRIL.SPLINT.SHREDR.DONNY.KRANG.BARON.FOOT.ROCK" \
       " -cpal 131.96.88.142.0.47.3" \
       " -cspr 3.32.3.3.33.3.6.82.56.3.129.61.97.13.14.15.18.19.20.21" \
       " -cspp 4.2.5.0.2.2.3.1.3.1.5.4.4.4.1.0.0.1.0.6"
badguys = " -name EDEA.BOMB.LEO.GOLBEZ.VICKS.WEDGE.KUJA.GEST.KEFKA.EXDETH.SEYMOR.GREG.GHOST.IMP" \
          " -cpor 100.33.15.50.18.18.82.48.56.102.105.104.17.14.11" \
          " -cspr 49.38.16.73.14.14.138.71.21.56.117.72.20.15.2.11.49.1.6.123" \
          " -cspp 3.3.0.1.1.0.1.3.3.4.4.3.0.0.4.3.6.1.0.2"
moogles = " -name KUPEK.KUMAMA.KUPOP.KUSHU.KUKU.KAMOG.KURIN.KURU.KUPO.KUTAN.MOG.KUPAN.GOGO.UMARO" \
          " -cpor 10.10.10.10.10.10.10.10.10.10.10.10.12.13.14" \
          " -cspr 10.10.10.10.10.10.10.10.10.10.10.10.12.13.82.15.10.19.20.82" \
          " -cspp 5.5.5.5.5.5.5.5.5.5.5.5.3.5.1.0.6.1.0.3"
mario = " -name DAISY.MARIO.HMRBRO.PAULIN.KAMEK.BOWSER.PEACH.TOAD.TOADET.JUNIOR.KNGBOO.LUIGI.GOOMBA.YOSHI" \
        " -cpal 138.34.88.37.62.137.64" \
        " -cspr 103.120.119.145.132.56.115.149.149.61.38.42.128.39.155.59.95.149.146.153" \
        " -cspp 3.1.4.3.4.2.5.3.5.2.5.2.3.0.6.3.3.1.5.6"


def spraypaint():
    cpalf = random.choices(list(id_palette.keys()), k=7)
    cporf = random.choices(list(id_portrait.keys()), k=15)
    csprf = random.choices(list(id_sprite.keys()), k=20)
    csppf = random.choices(list(range(0, 6)), k=14)
    csppf2 = random.choices(list(range(0, 7)), k=6)

    cpal = ' '.join([' -cpal', '.'.join([str(cpalf[0]), str(cpalf[1]), str(cpalf[2]), str(cpalf[3]), str(cpalf[4]),
                     str(cpalf[5]), str(cpalf[6])])])
    cpor = ' '.join([' -cpor', '.'.join([str(cporf[0]), str(cporf[1]), str(cporf[2]), str(cporf[3]), str(cporf[4]),
                     str(cporf[5]), str(cporf[6]), str(cporf[7]), str(cporf[8]), str(cporf[9]), str(cporf[10]),
                     str(cporf[11]), str(cporf[12]), str(cporf[13]), str(cporf[14])])])
    cspr = ' '.join([' -cspr', '.'.join([str(csprf[0]), str(csprf[1]), str(csprf[2]), str(csprf[3]), str(csprf[4]),
                     str(csprf[5]), str(csprf[6]), str(csprf[7]), str(csprf[8]), str(csprf[9]), str(csprf[10]),
                     str(csprf[11]), str(csprf[12]), str(csprf[13]), str(csprf[14]), str(csprf[15]), str(csprf[16]),
                     str(csprf[17]), str(csprf[18]), str(csprf[19])])])
    cspp = ' '.join([' -cspp', '.'.join([str(csppf[0]), str(csppf[1]), str(csppf[2]), str(csppf[3]), str(csppf[4]),
                     str(csppf[5]), str(csppf[6]), str(csppf[7]), str(csppf[8]), str(csppf[9]), str(csppf[10]),
                     str(csppf[11]), str(csppf[12]), str(csppf[13]), str(csppf2[0]), str(csppf2[1]), str(csppf2[2]),
                     str(csppf2[3]), str(csppf2[4]), str(csppf2[5])])])

    custom_select = random.choice([ffiv, moogles, tmnt, badguys, mario, ''.join([cpal, cspp]), ''.join([cpal, cpor, cspr,
                                                                                                 cspp])])
    return custom_select


"""
avnames = set(list(portraits.id_portrait.values())).intersection(sprites.id_sprite.values())      


custom_ps = {0: {'avname':'Magus-MetroidQuest-EC',  'sindex': 90, 'pindex':59, 'cname':'MAGUS'},
             1: {'avname':'Schala-HoxNorf-CT', 'sindex': 115, 'pindex':75, 'cname':'SCHALA'},
             2: {'avname':'PajaMog-CDude-FF', 'sindex': 155, 'pindex':95, 'cname':'MOGKID'},
             3: {'avname':'Reimu-HoxNorf-Touhou', 'sindex': 139, 'pindex':83, 'cname':'REIMU'},
             4: {'avname':'Strago', 'sindex': 7, 'pindex':7, 'cname':'STRAGO'},
             5: {'avname':'Uni-HoxNorf-Neptunia', 'sindex': 130, 'pindex': 79, 'cname': 'UNI'},
             6: {'avname':'Iffy-HoxNorf-Neptunia', 'sindex': 74, 'pindex':52, 'cname':'IFFY'},
             7: {'avname':'Toadette-HoxNorf-Mario', 'sindex': 149, 'pindex':90, 'cname':'TOADET'},
             8: {'avname':'Katt-ATinySpook-BOF2', 'sindex': 151, 'pindex':92, 'cname':'KATT'},
             9: {'avname':'Cecil (Dark Knight)-MetroidQuest-EC', 'sindex': 40, 'pindex':35, 'cname':'CECIL'},
             10: {'avname':'Gestahl-MetroidQuest-EC', 'sindex': 71, 'pindex':48, 'cname':'GEST'},
             11: {'avname':'Rom-HoxNorf-Neptunia', 'sindex': 141, 'pindex':85, 'cname':'ROM'},
             12: {'avname':'Terra',  'sindex': 0, 'pindex':0, 'cname':'TERRA'},
             13: {'avname':'Celes',  'sindex': 6, 'pindex':6, 'cname':'CELES'},
             14: {'avname':'Rumia-HoxNorf-Touhou', 'sindex': 147, 'pindex':87, 'cname':'RUMIA'},
             15: {'avname':'Umaro', 'sindex': 13, 'pindex':13, 'cname':'UMARO'},
             16: {'avnmae':'Bomb-JamesWhite89-FF6', 'sindex': 38, 'pindex':33, 'cname':'BOMB'},
             17: {'avname':'Edgar', 'sindex': 4, 'pindex':4, 'cname':'EDGAR'},
             18: {'avname':'Marisa-HoxNorf-Touhou', 'sindex': 145, 'pindex':86, 'cname':'MARISA'},
             19: {'avname':'Imp', 'sindex': 15, 'pindex':14, 'cname':'KAPPA'},
             20: {'avname':'Gogo', 'sindex': 12, 'pindex':12, 'cname':'GOGO'},
             21: {'avname':'Emperor-HoxNorf-FF2', 'sindex': 157, 'pindex':101, 'cname':'EMPROR'},
             22: {'avname':'Locke', 'sindex': 1, 'pindex':1, 'cname':'LOCKE'},
             23: {'avname':'Frog-MetroidQuest-EC', 'sindex': 62, 'pindex':46, 'cname':'FROG'},
             24: {'avname':'Mog', 'sindex': 10, 'pindex':10, 'cname':'MOG'},
             25: {'avname':'Nepgear-HoxNorf-Neptunia', 'sindex': 94, 'pindex':61, 'cname':'NEP'},
             26: {'avname':'Exdeath-CtrlxZ-FF5', 'sindex': 56, 'pindex':102, 'cname':'EXDETH'},
             27: {'avname':'GrimLocke-Taloswind-FF6', 'sindex': 156, 'pindex':96, 'cname':'LOCKE'},
             28: {'avname':'Soldier-LoneRedMage-FF4', 'sindex': 119, 'pindex':76, 'cname':'TROOP'},
             29: {'avname':'Sabin', 'sindex': 5, 'pindex':5, 'cname':'SABIN'},
             30: {'avname':'Edea-CtrlxZ-FF8', 'sindex': 49, 'pindex':100, 'cname':'EDEA'},
             31: {'avname':'Ghost', 'sindex': 20, 'pindex':17, 'cname':'GHOST'},
             32: {'avname':'Neptune-HoxNorf-Neptunia', 'sindex': 96, 'pindex':64, 'cname':'NEPTUNE'},
             33: {'avname':'Tonberry King-CDude-FF', 'sindex': 153, 'pindex':93, 'cname':'TKING'},
             34: {'avname':'Talim-HoxNorf-SC4', 'sindex': 150, 'pindex':91, 'cname':'TALIM'},
             35: {'avname':'Cecil (Paladin)-MetroidQuest-EC', 'sindex': 41, 'pindex':37, 'cname':'CECIL'},
             36: {'avname':'Papyrus-LoneRedMage-Undertale', 'sindex': 146, 'pindex':88, 'cname':'PAPY'},
             37: {'avname':'Lenna (White Mage)-HoxNorf-FF5', 'sindex': 86, 'pindex':58, 'cname':'LENNA'},
             38: {'avname':'Kuja-HoxNorf-FF9', 'sindex': 138, 'pindex':82, 'cname':'KUJA'},
             39: {'avname':'Sans-LoneRedMage-Undertale', 'sindex': 148, 'pindex':89, 'cname':'SANS'},
             40: {'avname':'Gau', 'sindex': 11, 'pindex':11, 'cname':'GAU'},
             41: {'avname':'Terra-MetroidQuest-EC', 'sindex': 125, 'pindex':78, 'cname':'TERRA'},
             42: {'avname':'Setzer', 'sindex': 9, 'pindex':9, 'cname':'SETZER'},
             43: {'avname':'Relm', 'sindex': 8, 'pindex':8, 'cname':'RELM'},
             44: {'avname':'Bird-JamesWhite89-FF6', 'sindex': 36, 'pindex':32, 'cname':'BIRD'},
             45: {'avname':'Kain-MetroidQuest-EC', 'sindex': 79, 'pindex':54, 'cname':'KAIN'},
             46: {'avname':'Cyan', 'sindex': 2, 'pindex':2, 'cname':'CYAN'},
             47: {'avname':'Relm-MetroidQuest-EC', 'sindex': 105, 'pindex':69, 'cname':'RELM'},
             48: {'avname':'Ram-HoxNorf-Neptunia', 'sindex': 140, 'pindex':84, 'cname':'RAM'},
             49: {'avname':'General Leo', 'sindex': 16, 'pindex':15, 'cname':'LEO'},
             50: {'avname':'Robo-Badass-CT', 'sindex': 107, 'pindex':71, 'cname':'ROBO'},
             51: {'avname':'Shadow', 'sindex': 3, 'pindex':3, 'cname':'SHADOW'},
             52: {'avname':'Cirno-HoxNorf-Touhou', 'sindex': 44, 'pindex':40, 'cname':'CIRNO'}
             }


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


#print(avnames)

def roll_custom():
    custom_chars = random.sample(range(len(custom_ps)), 20)
    return custom_chars


#print(char1name, char1sprite, char1portrait)
"""