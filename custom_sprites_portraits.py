import random
import portraits
import sprites

avnames = set(list(portraits.id_portrait.values())).intersection(sprites.id_sprite.values())

def roll_custom():
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

    #print(avnames)

    custom_chars = random.sample(range(len(custom_ps)), 20)
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

#print(char1name, char1sprite, char1portrait)
