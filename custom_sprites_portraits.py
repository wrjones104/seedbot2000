import random
import portraits
import sprites

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

#print(avnames)

def roll_custom():
    custom_chars = random.sample(range(len(custom_ps)), 20)
    return custom_chars


#print(char1name, char1sprite, char1portrait)
