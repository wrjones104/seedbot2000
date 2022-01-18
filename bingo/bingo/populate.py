from Character import Character
from Check import Check
from Dragon import Dragon


def populate() -> dict:
    NoChar = Character("No Character Needed", [], 1)
    Terra = Character("Terra", [], 0)
    Sabin = Character("Sabin", [], 5)
    Celes = Character("Celes", [], 0)
    Shadow = Character("Shadow", [], 2)
    Cyan = Character("Cyan", [], 0)
    Relm = Character("Relm", [], 0)
    Mog = Character("Mog", [], 0)

    Setzer = Character("Setzer", [], 1)
    Gau = Character("Gau", [], 0)
    Edgar = Character("Edgar", [], 2)
    Locke = Character("Locke", [], 0)
    Strago = Character("Strago", [], 0)
    Umaro = Character("Umaro", [], 1)
    Gogo = Character("Gogo", [], 0)

    # Check init format is: name, owner, canBeChar, canBeEsper, canBeItem, requiredCheck, time, desirability
    # No Character Checks
    AH1 = Check("Auction House 1", NoChar, False, True, True, None, 1, 1)
    AH2 = Check("Auction House 2", NoChar, False, True, True, None, 1, 1)
    KN = Check("Kefka at Narshe", NoChar, True, True, True, None, 1, 1)
    Tritoch = Check("Tritoch", NoChar, False, True, True, None, 1, 1)
    Tzen = Check("Tzen Thief", NoChar, False, True, True, None, 1, 1)
    DoomGaze = Check("Doom Gaze", NoChar, False, True, True, None, 1, 1)
    NoChar.checks = (AH1, AH2, KN, Tritoch, Tzen, DoomGaze)

    # Terra Checks
    Lete = Check("Lete", Terra, True, True, True, None, 1, 1)
    SealedGate = Check("Sealed Gate", Terra, True, True, True, None, 1, 1)
    Whelk = Check("Lete", Terra, True, True, True, None, 1, 1)
    Zozo = Check("Lete", Terra, True, True, True, None, 1, 1)
    Mobliz = Check("Mobliz", Terra, True, True, True, None, 1, 1)
    Terra.checks = (Lete, SealedGate, Whelk, Zozo, Mobliz)

    # Sabin Checks
    BarrenFalls = Check("Barren Falls", Sabin, True, True, True, None, 1, 1)
    ImperialCamp = Check("Imperial Camp", Sabin, True, True, True, None, 1, 1)
    MtKolts = Check("Mt. Kolts", Sabin, True, True, True, None, 1, 1)
    PhantomTrain = Check("Phantom Train", Sabin, True, True, True, None, 1, 1)
    CollapsingHouse = Check("Collapsing House", Sabin, True, True, True, None, 1, 1)
    Sabin.checks = (BarrenFalls, ImperialCamp, MtKolts, PhantomTrain, CollapsingHouse)

    # Celes Checks
    Opera = Check("Opera House", Celes, True, True, True, None, 1, 1)
    Basement = Check("South Figaro Basement", Celes, True, True, True, None, 1, 1)
    MTek1 = Check("Magitek 1", Celes, False, True, True, None, 1, 1)
    MTek2 = Check("Magitek 2", Celes, False, True, True, MTek1, 1, 1)
    MTek3 = Check("Magitek 3", Celes, True, True, False, MTek2, 1, 1)
    Celes.checks = (Opera, Basement, MTek1, MTek2, MTek3)

    # Shadow Checks
    GauManor = Check("Gau Manor", Shadow, True, True, True, None, 1, 1)
    VeldtCave = Check("Veldt Cave", Shadow, True, True, True, None, 1, 1)
    FC1 = Check("Floating Continent 1", Shadow, True, True, False, None, 1, 1)
    FC2 = Check("Floating Continent 2", Shadow, False, True, True, FC1, 1, 1)
    FC3 = Check("Floating Continent 3", Shadow, True, True, False, FC2, 1, 1)
    Shadow.checks = (GauManor, VeldtCave, FC1, FC2, FC3)

    # Cyan Checks
    Doma = Check("Doma Siege", Cyan, True, True, True, None, 1, 1)
    MtZozo = Check("Mt. Zozo", Cyan, True, True, True, None, 1, 1)
    Dream1 = Check("Cyan's Dream 1", Cyan, False, True, True, None, 1, 1)
    Dream2 = Check("Cyan's Dream 2", Cyan, True, True, False, Dream1, 1, 1)
    Dream3 = Check("Cyan's Dream 3", Cyan, False, True, True, Dream2, 1, 1)
    Cyan.checks = (Doma, MtZozo, Dream1, Dream2, Dream3)

    # Relm Checks
    EsperMountain = Check("Esper Mountain", Relm, True, True, True, None, 1, 1)
    Owzer = Check("Owzer's Mansion", Relm, True, True, True, None, 1, 1)
    Relm.checks = (EsperMountain, Owzer)

    # Mog Checks
    LoneWolf = Check("Lone Wolf", Mog, True, True, True, None, 1, 1)
    Mog.checks = (LoneWolf,)

    # Setzer Checks
    Tomb = Check("Daryl's Tomb", Setzer, True, True, True, None, 1, 1)
    Cafe = Check("Kohlingen Cafe", Setzer, True, True, True, None, 1, 1)
    Setzer.checks = (Tomb, Cafe)

    # Gau Checks
    Trench = Check("Serpent Trench", Gau, True, True, True, None, 1, 1)
    Veldt = Check("Veldt", Gau, True, True, False, None, 1, 1)
    Gau.checks = (Trench, Veldt)

    # Edgar Checks
    Throne = Check("Figaro Castle Throne", Edgar, True, True, True, None, 1, 1)
    Engine = Check("Figaro Castle Engine Room", Edgar, True, True, True, None, 1, 1)
    Ancient = Check("Ancient Castle", Edgar, True, True, True, None, 1, 1)
    Edgar.checks = (Throne, Engine, Ancient)

    # Locke Checks
    SFCave = Check("South Figaro Cave", Locke, True, True, True, None, 1, 1)
    Narshe = Check("Narshe WOR", Locke, False, True, True, None, 1, 1)
    PCave = Check("Phoenix Cave", Locke, True, True, True, None, 1, 1)
    Locke.checks = (SFCave, Narshe, PCave)

    # Strago Checks
    House = Check("Burning House", Strago, True, True, True, None, 1, 1)
    Ebot = Check("Ebot's Rock", Strago, True, True, True, None, 1, 1)
    Tower = Check("Fanatic's Tower", Strago, True, True, True, None, 1, 1)
    Strago.checks = (House, Ebot, Tower)

    # Umaro Checks
    UCave = Check("Umaro's Cave", Umaro, True, True, True, NoChar.checks["Tritoch"], 1, 1)
    Umaro.checks = (UCave,)

    # Gogo Checks
    Zone = Check("Zone Eater", Gogo, True, True, True, None, 1, 1)
    Gogo.checks = (Zone,)

    ### Dragons
    StormDragon = Dragon("Storm Dragon", Cyan, 1)
    IceDragon = Dragon("Ice Dragon", NoChar, 1)
    WhiteDragon = Dragon("White Dragon", NoChar, 1)
    BlueDragon = Dragon("Blue Dragon", Edgar, 1)
    RedDragon = Dragon("Red Dragon", Locke, 1)
    DirtDragon = Dragon("Dirt Dragon", NoChar, 1)
    GoldDragon = Dragon("Gold Dragon", NoChar, 1)
    DoomDragon = Dragon("Doom Dragon", NoChar, 1)

    drgn_list = (StormDragon, IceDragon, WhiteDragon, BlueDragon, RedDragon, DirtDragon, GoldDragon, DoomDragon)

    dragons = {}
    data = {}
    characters = {}
    checks = {}

    char_to_drgn = {}
    for drgn in drgn_list:
        if drgn.owner not in char_to_drgn.keys():
            char_to_drgn[drgn.owner.name] = []
        char_to_drgn[drgn.owner.name].append(drgn)
        dragons[drgn.name] = drgn

    # Populate dictionaries to return
    char_list = [NoChar, Terra, Sabin, Celes, Shadow, Cyan, Relm, Mog, Setzer, Gau, Edgar, Locke, Strago, Umaro, Gogo]

    for i in range(len(char_list)):
        char = char_list[i]
        if char.name in char_to_drgn:
            char.dragons = char_to_drgn[char.name]
        characters[char.name] = char

        for check in char.checks:
            checks[check] = char.checks[check]

        char_list[i] = char

    data["Characters"] = characters
    data["Checks"] = checks
    data["Dragons"] = dragons

    return data
