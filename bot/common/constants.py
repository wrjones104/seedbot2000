SNES_BYTE_ORDER = "little"
HEADER_SIZE = 0x200
MONSTER_COUNT = 384
ITEM_COUNT = 256
CHARACTER_COUNT = 64
MAGIC_COUNT = 54
ESPER_COUNT = 27
ATTACK_COUNT = 175
DANCE_COUNT = 8

# Monster Data
MONSTER_DATA_LOC = 0xF0000
MONSTER_DATA_SIZE = 0x20
MONSTER_RAGE_LOC = 0xF4600

# SwdTech Names
SWDTECH_NAME_LOC = 0xF3C40
SWDTECH_NAME_SIZE = 0xC
SWDTECH_NAME_COUNT = 8

# Monster Names
MONSTER_NAME_LOC = 0xFC050
MONSTER_NAME_SIZE = 10

# Monster Attack Names
MONSTER_ATTACK_NAME_LOC = 0xFD0D0
MONSTER_ATTACK_NAME_SIZE = 10

# Monster Drop/Steal
MONSTER_DROP_LOC = 0xF3000
MONSTER_DROP_SIZE = 0x4

# Event Battle Groups
EVENT_BATTLE_GROUP_LOC = 0x5000
EVENT_BATTLE_GROUP_SIZE = 0x04
EVENT_BATTLE_GROUP_COUNT = 256

# Character Names
CHAR_NAME_LOC = 0x478C0
CHAR_NAME_SIZE = 6

# Item Names
ITEM_NAME_LOC = 0x12B300
ITEM_NAME_SIZE = 13

# Magic Spell Names
MAGIC_NAME_LOC = 0x26F567
MAGIC_NAME_SIZE = 7

# Esper Names
ESPER_NAME_LOC = 0x26F6E1
ESPER_NAME_SIZE = 8

# Attack Names
ATTACK_NAME_LOC = 0x26F7B9
ATTACK_NAME_SIZE = 10

# Esper Attack Names
ESPER_ATTACK_NAME_LOC = 0x26FE8F
ESPER_ATTACK_NAME_SIZE = 10

# Dance Names
DANCE_NAME_LOC = 0x26FF9D
DANCE_NAME_SIZE = 12

# Packs in FF3usme
## Each byte is the formation number starting upper left and going right
RANDOM_BATTLE_GROUP_LOC = 0xF4800
RANDOM_BATTLE_GROUP_SIZE = 0x08

# Zoning in FF3usme
## Each byte is the formation number starting upper left and going right
BATTLE_GROUP_LOC = 0xF5400

# Formations in FF3usme

BATTLE_DATA_LOC = 0xF6200

# Text for non-events. This is sometimes called TXT2
## Starting with 198, we use ASCII code 161 + (n-198) to represent the special characters. For example, 198 is ascii(161) = ¡
## 216 is the dirk symbol
## 217 is the sword symbol
## 218 is the lance symbol
## 219 is the knife symbol
## 220 is the rod symbol
## 221 is the brush symbol
## 222 is the throwing star symbol
## 223 is the throwing weapon (sniper) symbol
## 224 is the dice symbol
## 225 is the claw symbol
## 226 is the shield symbol
## 227 is the helm symbol
## 228 is the armor symbol
## 229 is the tool symbol
## 230 is the edge symbol
## 231 is the relic symbol
## 232 is the white dot for healing spells
## 233 is the black dot for offensive spells
## 234 is the grey dot for effect spells

GAMETEXT = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!?/:\"'-.¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×Ø "
CHAR_TO_CODE = {'': 255, '_': 255}
CODE_TO_CHAR = {255: '_'}
for i in range(len(GAMETEXT)):
    CHAR_TO_CODE[GAMETEXT[i]] = i + 0x80
    CODE_TO_CHAR[i + 0x80] = GAMETEXT[i]

# DTE text for digraphs. This is sometimes called TXT1 - Sourced from FF3usME
## <EOC>        -- End of caption (optional)
## <A0> - <A12> -- Name of an actor (ie A0 = TERRA)
## <D>          -- A static delay of ~1 second
## <Ex>/<E$xx>  -- An event specified in decimal or hex
## <OP$12>      -- Opcode specifying the end of some events
## <EOP>        -- End of page
## <Sx>/<S$xx>  -- A number of spaces specified in decimal or hex
## <C>          -- A choice
## <Dx>/<D$xx>  -- A programmable delay specified in decimal or hex. Each unit is 1/4 of a second (ie 3 = 3/4 sec)
## <OP$17>      -- Unknown opcode
## <OP$18>      -- Unknown opcode
## <N>          -- A number to be displayed
## <I>          -- An item to be displayed
## <S>          -- A spell to be displayed
## <BKx$xx>     -- FF6J-only kanji

DTE_TO_TEXT = {0x00: "<EOC>", 0x01: "\n", 0x02: "<A0>", 0x03: "<A1>", 0x04: "<A2>", 0x05: "<A3>", 0x06: "<A4>",
               0x07: "<A5>", 0x08: "<A6>", 0x09: "<A7>", 0x0A: "<A8>", 0x0B: "<A9>", 0x0C: "<A10>", 0x0D: "<A11>",
               0x0E: "<A12>", 0x0F: "<A13>", 0x10: "<D>", 0x11: "<Ex> / <E$xx>", 0x12: "<OP$12>", 0x13: "<EOP>",
               0x14: "<Sx> / <S$xx>", 0x15: "<C>", 0x16: "<Dx> / <D$xx>", 0x17: "<OP$17>", 0x18: "<OP$18>", 0x19: "<N>",
               0x1A: "<I>", 0x1B: "<S>", 0x1C: "<BK1@xx>", 0x1D: "<BK2@xx>", 0x1E: "<BK3@xx>", 0x1F: "<BK4@xx>",
               0x20: "A", 0x21: "B", 0x22: "C", 0x23: "D", 0x24: "E", 0x25: "F", 0x26: "G", 0x27: "H", 0x28: "I",
               0x29: "J", 0x2A: "K", 0x2B: "L", 0x2C: "M", 0x2D: "N", 0x2E: "O", 0x2F: "P", 0x30: "Q", 0x31: "R",
               0x32: "S", 0x33: "T", 0x34: "U", 0x35: "V", 0x36: "W", 0x37: "X", 0x38: "Y", 0x39: "Z", 0x3A: "a",
               0x3B: "b", 0x3C: "c", 0x3D: "d", 0x3E: "e", 0x3F: "f", 0x40: "g", 0x41: "h", 0x42: "i", 0x43: "j",
               0x44: "k", 0x45: "l", 0x46: "m", 0x47: "n", 0x48: "o", 0x49: "p", 0x4A: "q", 0x4B: "r", 0x4C: "s",
               0x4D: "t", 0x4E: "u", 0x4F: "v", 0x50: "w", 0x51: "x", 0x52: "y", 0x53: "z", 0x54: "0", 0x55: "1",
               0x56: "2", 0x57: "3", 0x58: "4", 0x59: "5", 0x5A: "6", 0x5B: "7", 0x5C: "8", 0x5D: "9", 0x5E: "!",
               0x5F: "?", 0x60: "/", 0x61: ":", 0x62: "]", 0x63: "'", 0x64: "-", 0x65: ".", 0x66: ",", 0x67: "_",
               0x68: ";", 0x69: "#", 0x6A: "+", 0x6B: "(", 0x6C: ")", 0x6D: "%", 0x6E: "~", 0x6F: "*", 0x70: "@",
               0x71: "&", 0x72: "=", 0x73: "[", 0x74: "ÿ", 0x75: "þ", 0x76: "$", 0x77: "\\", 0x78: "^", 0x79: "±",
               0x7A: "£", 0x7B: "{", 0x7C: "}", 0x7D: "`", 0x7E: "|", 0x7F: " ", 0x80: "e ", 0x81: " t", 0x82: ": ",
               0x83: "th", 0x84: "t ", 0x85: "he", 0x86: "s ", 0x87: "er", 0x88: " a", 0x89: "re", 0x8A: "in",
               0x8B: "ou", 0x8C: "d ", 0x8D: " w", 0x8E: " s", 0x8F: "an", 0x90: "o ", 0x91: " h", 0x92: " o",
               0x93: "r ", 0x94: "n ", 0x95: "at", 0x96: "to", 0x97: " i", 0x98: ", ", 0x99: "ve", 0x9A: "ng",
               0x9B: "ha", 0x9C: " m", 0x9D: "Th", 0x9E: "st", 0x9F: "on", 0xA0: "yo", 0xA1: " b", 0xA2: "me",
               0xA3: "y ", 0xA4: "en", 0xA5: "it", 0xA6: "ar", 0xA7: "ll", 0xA8: "ea", 0xA9: "I ", 0xAA: "ed",
               0xAB: " f", 0xAC: " y", 0xAD: "hi", 0xAE: "is", 0xAF: "es", 0xB0: "or", 0xB1: "l ", 0xB2: " c",
               0xB3: "ne", 0xB4: "'s", 0xB5: "nd", 0xB6: "le", 0xB7: "se", 0xB8: " I", 0xB9: "a ", 0xBA: "te",
               0xBB: " l", 0xBC: "pe", 0xBD: "as", 0xBE: "ur", 0xBF: "u ", 0xC0: "al", 0xC1: " p", 0xC2: "g ",
               0xC3: "om", 0xC4: " d", 0xC5: "f ", 0xC6: " g", 0xC7: "ow", 0xC8: "rs", 0xC9: "be", 0xCA: "ro",
               0xCB: "us", 0xCC: "ri", 0xCD: "wa", 0xCE: "we", 0xCF: "Wh", 0xD0: "et", 0xD1: " r", 0xD2: "nt",
               0xD3: "m ", 0xD4: "ma", 0xD5: "I'", 0xD6: "li", 0xD7: "ho", 0xD8: "of", 0xD9: "Yo", 0xDA: "h ",
               0xDB: " n", 0xDC: "ee", 0xDD: "de", 0xDE: "so", 0xDF: "gh", 0xE0: "ca", 0xE1: "ra", 0xE2: "n'",
               0xE3: "ta", 0xE4: "ut", 0xE5: "el", 0xE6: "! ", 0xE7: "fo", 0xE8: "ti", 0xE9: "We", 0xEA: "lo",
               0xEB: "e!", 0xEC: "ld", 0xED: "no", 0xEE: "ac", 0xEF: "ce", 0xF0: "k ", 0xF1: " u", 0xF2: "oo",
               0xF3: "ke", 0xF4: "ay", 0xF5: "w ", 0xF6: "!!", 0xF7: "ag", 0xF8: "il", 0xF9: "ly", 0xFA: "co",
               0xFB: ". ", 0xFC: "ch", 0xFD: "go", 0xFE: "ge", 0xFF: "e_"}

TEXT_TO_DTE = {}
for key in DTE_TO_TEXT.keys():
    new_key = DTE_TO_TEXT[key]
    if not new_key in TEXT_TO_DTE:
        TEXT_TO_DTE[new_key] = key

# HiROM header info
HiROM_HEADER_TITLE_OFFSET = 0xFFC0
HiROM_HEADER_TITLE_SIZE = 21
HiROM_HEADER_MAPPING_MODE_OFFSET = 0xFFD5
HiROM_HEADER_MAPPING_MODE_SIZE = 1
HiROM_HEADER_ROM_TYPE_OFFSET = 0xFFD6
HiROM_HEADER_ROM_TYPE_SIZE = 1

## Left shift by 0x400 to get size in bytes
HiROM_HEADER_ROM_SIZE_OFFSET = 0xFFD7
HiROM_HEADER_ROM_SIZE_SIZE = 1

## Left shift by 0x400 to get size in bytes
HiROM_HEADER_SRAM_SIZE_OFFSET = 0xFFD8
HiROM_HEADER_SRAM_SIZE_SIZE = 1

HiROM_HEADER_DEVELOPER_ID_OFFSET = 0xFFD9
HiROM_HEADER_DEVELOPER_ID_SIZE = 2
HiROM_HEADER_VERSION_OFFSET = 0xFFDB
HiROM_HEADER_VERSION_SIZE = 1
HiROM_HEADER_CHECKSUM_COMPLIMENT_OFFSET = 0xFFDC
HiROM_HEADER_CHECKSUM_COMPLIMENT_SIZE = 1
HiROM_HEADER_CHECKSUM_OFFSET = 0xFFDE
HiROM_HEADER_CHECKSUM_OFFSET_SIZE = 2
HiROM_EMULATION_MODE_RESET_VECTOR_OFFSET = 0xFFFC
HiROM_EMULATION_MODE_RESET_VECTOR_SIZE = 2

FF6_HEADER_TITLE_DATA_US = b'\x46\x49\x4e\x41\x4c\x20\x46\x41\x4e\x54\x41\x53\x59\x20\x33\x20\x20\x20\x20\x20\x20'
FF6_HEADER_TITLE_DATA_JP = b'\x46\x49\x4e\x41\x4c\x20\x46\x41\x4e\x54\x41\x53\x59\x20\x36\x20\x20\x20\x20\x20\x20'
FF6_HEADER_RESET_VECTOR = b'\x00\xFF'
FF6_HEADER_RESET_DATA = b'\x78\x18\xfb\x5c\x19\x00\xc0'
FF6_ROM_SIZE = 0x300000

SPELLS = (
"ÄFire__", "ÄIce___", "ÄBolt__", "ÄPoison", "ÄDrain_", "ÄFire 2", "ÄIce 2_", "ÄBolt 2", "ÄBio___", "ÄFire 3", "ÄIce 3_",
"ÄBolt 3", "ÄBreak_", "ÄDoom__", "ÄPearl_", "ÄFlare_", "ÄDemi__", "ÄQuartr", "ÄX-Zone", "ÄMeteor", "ÄUltima", "ÄQuake_",
"ÄW Wind", "ÄMerton", "ÅScan__", "ÅSlow__", "ÅRasp__", "ÅMute__", "ÅSafe__", "ÅSleep_", "ÅMuddle", "ÅHaste_", "ÅStop__",
"ÅBserk_", "ÅFloat_", "ÅImp___", "ÅRflect", "ÅShell_", "ÅVanish", "ÅHaste2", "ÅSlow 2", "ÅOsmose", "ÅWarp__", "ÅQuick_",
"ÅDispel", "ÃCure__", "ÃCure 2", "ÃCure 3", "ÃLife__", "ÃLife 2", "ÃAntdot", "ÃRemedy", "ÃRegen_", "ÃLife 3")

ENEMIES = (
"Guard_____", "Soldier___", "Templar___", "Ninja_____", "Samurai___", "Orog______", "Mag Roader", "Retainer__",
"Hazer_____", "Dahling___", "Rain Man__", "Brawler___", "Apokryphos", "Dark Force", "Whisper___", "Over-Mind_",
"Osteosaur_", "Commander_", "Rhodox____", "Were-Rat__", "Ursus_____", "Rhinotaur_", "Steroidite", "Leafer____",
"Stray Cat_", "Lobo______", "Doberman__", "Vomammoth_", "Fidor_____", "Baskervor_", "Suriander_", "Chimera___",
"Behemoth__", "Mesosaur__", "Pterodon__", "FossilFang", "White Drgn", "Doom Drgn_", "Brachosaur", "Tyranosaur",
"Dark Wind_", "Beakor____", "Vulture___", "Harpy_____", "HermitCrab", "Trapper___", "Hornet____", "CrassHoppr",
"Delta Bug_", "Gilomantis", "Trilium___", "Nightshade", "TumbleWeed", "Bloompire_", "Trilobiter", "Siegfried_",
"Nautiloid_", "Exocite___", "Anguiform_", "Reach Frog", "Lizard____", "ChickenLip", "Hoover____", "Rider_____",
"Chupon____", "Pipsqueak_", "M-TekArmor", "Sky Armor_", "Telstar___", "Lethal Wpn", "Vaporite__", "Flan______",
"Ing_______", "Humpty____", "Brainpan__", "Cruller___", "Cactrot___", "Repo Man__", "Harvester_", "Bomb______",
"Still Life", "Boxed Set_", "SlamDancer", "HadesGigas", "Pug_______", "Magic Urn_", "Mover_____", "Figaliz___",
"Buffalax__", "Aspik_____", "Ghost_____", "Crawler___", "Sand Ray__", "Areneid___", "Actaneon__", "Sand Horse",
"Dark Side_", "Mad Oscar_", "Crawly____", "Bleary____", "Marshal___", "Trooper___", "General___", "Covert____",
"Ogor______", "Warlock___", "Madam_____", "Joker_____", "Iron Fist_", "Goblin____", "Apparite__", "PowerDemon",
"Displayer_", "Vector Pup", "Peepers___", "Sewer Rat_", "Slatter___", "Rhinox____", "Rhobite___", "Wild Cat__",
"Red Fang__", "Bounty Man", "Tusker____", "Ralph_____", "Chitonid__", "Wart Puck_", "Rhyos_____", "SrBehemoth",
"Vectaur___", "Wyvern____", "Zombone___", "Dragon____", "Brontaur__", "Allosaurus", "Cirpius___", "Sprinter__",
"Gobbler___", "Harpiai___", "GloomShell", "Drop______", "Mind Candy", "WeedFeeder", "Luridan___", "Toe Cutter",
"Over Grunk", "Exoray____", "Crusher___", "Uroburos__", "Primordite", "Sky Cap___", "Cephaler__", "Maliga____",
"Gigan Toad", "Geckorex__", "Cluck_____", "Land Worm_", "Test Rider", "PlutoArmor", "Tomb Thumb", "HeavyArmor",
"Chaser____", "Scullion__", "Poplium___", "Intangir__", "Misfit____", "Eland_____", "Enuo______", "Deep Eye__",
"GreaseMonk", "NeckHunter", "Grenade___", "Critic____", "Pan Dora__", "SoulDancer", "Gigantos__", "Mag Roader",
"Spek Tor__", "Parasite__", "EarthGuard", "Coelecite_", "Anemone___", "Hipocampus", "Spectre___", "Evil Oscar",
"Slurm_____", "Latimeria_", "StillGoing", "Allo Ver__", "Phase_____", "Outsider__", "Barb-e____", "Parasoul__",
"Pm Stalker", "Hemophyte_", "Sp Forces_", "Nohrabbit_", "Wizard____", "Scrapper__", "Ceritops__", "Commando__",
"Opinicus__", "Poppers___", "Lunaris___", "Garm______", "Vindr_____", "Kiwok_____", "Nastidon__", "Rinn______",
"Insecare__", "Vermin____", "Mantodea__", "Bogy______", "Prussian__", "Black Drgn", "Adamanchyt", "Dante_____",
"Wirey Drgn", "Dueller___", "Psychot___", "Muus______", "Karkass___", "Punisher__", "Balloon___", "Gabbldegak",
"GtBehemoth", "Scorpion__", "Chaos Drgn", "Spit Fire_", "Vectagoyle", "Lich______", "Osprey____", "Mag Roader",
"Bug_______", "Sea Flower", "Fortis____", "Abolisher_", "Aquila____", "Junk______", "Mandrake__", "1st Class_",
"Tap Dancer", "Necromancr", "Borras____", "Mag Roader", "Wild Rat__", "Gold Bear_", "Innoc_____", "Trixter___",
"Red Wolf__", "Didalos___", "Woolly____", "Veteran___", "Sky Base__", "IronHitman", "Io________", "Pugs______",
"Whelk_____", "Presenter_", "Mega Armor", "Vargas____", "TunnelArmr", "Prometheus", "GhostTrain", "Dadaluma__",
"Shiva_____", "Ifrit_____", "Number 024", "Number 128", "Inferno___", "Crane_____", "Crane_____", "Umaro_____",
"Umaro_____", "Guardian__", "Guardian__", "Air Force_", "Tritoch___", "Tritoch___", "FlameEater", "AtmaWeapon",
"Nerapa____", "SrBehemoth", "Kefka_____", "Tentacle__", "Dullahan__", "Doom Gaze_", "Chadarnook", "Curley____",
"Larry_____", "Moe_______", "Wrexsoul__", "Hidon_____", "KatanaSoul", "L.30 Magic", "Hidonite__", "Doom______",
"Goddess___", "Poltrgeist", "Kefka_____", "L.40 Magic", "Ultros____", "Ultros____", "Ultros____", "Chupon____",
"L.20 Magic", "Siegfried_", "L.10 Magic", "L.50 Magic", "Head______", "Whelk Head", "Colossus__", "CzarDragon",
"Master Pug", "L.60 Magic", "Merchant__", "B.Day Suit", "Tentacle__", "Tentacle__", "Tentacle__", "RightBlade",
"Left Blade", "Rough_____", "Striker___", "L.70 Magic", "Tritoch___", "Laser Gun_", "Speck_____", "MissileBay",
"Chadarnook", "Ice Dragon", "Kefka_____", "Storm Drgn", "Dirt Drgn_", "Ipooh_____", "Leader____", "Grunt_____",
"Gold Drgn_", "Skull Drgn", "Blue Drgn_", "Red Dragon", "Piranha___", "Rizopas___", "Specter___", "Short Arm_",
"Long Arm__", "Face______", "Tiger_____", "Tools_____", "Magic_____", "Hit_______", "Girl______", "Sleep_____",
"Hidonite__", "Hidonite__", "Hidonite__", "L.80 Magic", "L.90 Magic", "ProtoArmor", "MagiMaster", "SoulSaver_",
"Ultros____", "Naughty___", "Phunbaba__", "Phunbaba__", "Phunbaba__", "Phunbaba__", "__________", "__________",
"__________", "Zone Eater", "__________", "__________", "__________", "Officer___", "Cadet_____", "__________",
"__________", "Soldier___", "__________", "__________", "__________", "Atma______", "__________", "__________")

ITEMS = {0x00: "³Dirk________", 0x01: "³MithrilKnife", 0x02: "³Guardian____", 0x03: "³Air Lancet__",
         0x04: "³ThiefKnife__", 0x05: "³Assassin____", 0x06: "³Man Eater___", 0x07: "³SwordBreaker",
         0x08: "³Graedus_____", 0x09: "³ValiantKnife", 0x0A: "´MithrilBlade", 0x0B: "´RegalCutlass",
         0x0C: "´Rune Edge___", 0x0D: "´Flame Sabre_", 0x0E: "´Blizzard____", 0x0F: "´ThunderBlade",
         0x10: "´Epee________", 0x11: "´Break Blade_", 0x12: "´Drainer_____", 0x13: "´Enhancer____",
         0x14: "´Crystal_____", 0x15: "´Falchion____", 0x16: "´Soul Sabre__", 0x17: "´Ogre Nix____",
         0x18: "´Excalibur___", 0x19: "´Scimitar____", 0x1A: "´Illumina____", 0x1B: "´Ragnarok____",
         0x1C: "´Atma Weapon_", 0x1D: "µMithril Pike", 0x1E: "µTrident_____", 0x1F: "µStout Spear_",
         0x20: "µPartisan____", 0x21: "µPearl Lance_", 0x22: "µGold Lance__", 0x23: "µAura Lance__",
         0x24: "µImp Halberd_", 0x25: "³Imperial____", 0x26: "³Kodachi_____", 0x27: "³Blossom_____",
         0x28: "³Hardened____", 0x29: "³Striker_____", 0x2A: "³Stunner_____", 0x2B: "¶Ashura______",
         0x2C: "¶Kotetsu_____", 0x2D: "¶Forged______", 0x2E: "¶Tempest_____", 0x2F: "¶Murasame____",
         0x30: "¶Aura________", 0x31: "¶Strato______", 0x32: "¶Sky Render__", 0x33: "·Heal Rod____",
         0x34: "·Mithril Rod_", 0x35: "·Fire Rod____", 0x36: "·Ice Rod_____", 0x37: "·Thunder Rod_",
         0x38: "·Poison Rod__", 0x39: "·Pearl Rod___", 0x3A: "·Gravity Rod_", 0x3B: "·Punisher____",
         0x3C: "·Magus Rod___", 0x3D: "¸Chocobo Brsh", 0x3E: "¸DaVinci Brsh", 0x3F: "¸Magical Brsh",
         0x40: "¸Rainbow Brsh", 0x41: "¹Shuriken____", 0x42: "¹Ninja Star__", 0x43: "¹Tack Star___",
         0x44: "ºFlail_______", 0x45: "ºFull Moon___", 0x46: "ºMorning Star", 0x47: "ºBoomerang___",
         0x48: "ºRising Sun__", 0x49: "ºHawk Eye____", 0x4A: "ºBone Club___", 0x4B: "ºSniper______",
         0x4C: "ºWing Edge___", 0x4D: "»Cards_______", 0x4E: "»Darts_______", 0x4F: "»Doom Darts__",
         0x50: "»Trump_______", 0x51: "»Dice________", 0x52: "»Fixed Dice__", 0x53: "¼MetalKnuckle",
         0x54: "¼Mithril Claw", 0x55: "¼Kaiser______", 0x56: "¼Poison Claw_", 0x57: "¼Fire Knuckle",
         0x58: "¼Dragon Claw_", 0x59: "¼Tiger Fangs_", 0x5A: "½Buckler_____", 0x5B: "½Heavy Shld__",
         0x5C: "½Mithril Shld", 0x5D: "½Gold Shld___", 0x5E: "½Aegis Shld__", 0x5F: "½Diamond Shld",
         0x60: "½Flame Shld__", 0x61: "½Ice Shld____", 0x62: "½Thunder Shld", 0x63: "½Crystal Shld",
         0x64: "½Genji Shld__", 0x65: "½TortoiseShld", 0x66: "½Cursed Shld_", 0x67: "½Paladin Shld",
         0x68: "½Force Shld__", 0x69: "¾Leather Hat_", 0x6A: "¾Hair Band___", 0x6B: "¾Plumed Hat__",
         0x6C: "¾Beret_______", 0x6D: "¾Magus Hat___", 0x6E: "¾Bandana_____", 0x6F: "¾Iron Helmet_",
         0x70: "¾Coronet_____", 0x71: "¾Bard's Hat__", 0x72: "¾Green Beret_", 0x73: "¾Head Band___",
         0x74: "¾Mithril Helm", 0x75: "¾Tiara_______", 0x76: "¾Gold Helmet_", 0x77: "¾Tiger Mask__",
         0x78: "¾Red Cap_____", 0x79: "¾Mystery Veil", 0x7A: "¾Circlet_____", 0x7B: "¾Regal Crown_",
         0x7C: "¾Diamond Helm", 0x7D: "¾Dark Hood___", 0x7E: "¾Crystal Helm", 0x7F: "¾Oath Veil___",
         0x80: "¾Cat Hood____", 0x81: "¾Genji Helmet", 0x82: "¾Thornlet____", 0x83: "¾Titanium____",
         0x84: "¿LeatherArmor", 0x85: "¿Cotton Robe_", 0x86: "¿Kung Fu Suit", 0x87: "¿Iron Armor__",
         0x88: "¿Silk Robe___", 0x89: "¿Mithril Vest", 0x8A: "¿Ninja Gear__", 0x8B: "¿White Dress_",
         0x8C: "¿Mithril Mail", 0x8D: "¿Gaia Gear___", 0x8E: "¿Mirage Vest_", 0x8F: "¿Gold Armor__",
         0x90: "¿Power Sash__", 0x91: "¿Light Robe__", 0x92: "¿Diamond Vest", 0x93: "¿Red Jacket__",
         0x94: "¿Force Armor_", 0x95: "¿DiamondArmor", 0x96: "¿Dark Gear___", 0x97: "¿Tao Robe____",
         0x98: "¿Crystal Mail", 0x99: "¿Czarina Gown", 0x9A: "¿Genji Armor_", 0x9B: "¿Imp's Armor_",
         0x9C: "¿Minerva_____", 0x9D: "¿Tabby Suit__", 0x9E: "¿Chocobo Suit", 0x9F: "¿Moogle Suit_",
         0xA0: "¿Nutkin Suit_", 0xA1: "¿BehemothSuit", 0xA2: "¿Snow Muffler", 0xA3: "ÀNoiseBlaster",
         0xA4: "ÀBio Blaster_", 0xA5: "ÀFlash_______", 0xA6: "ÀChain Saw___", 0xA7: "ÀDebilitator_",
         0xA8: "ÀDrill_______", 0xA9: "ÀAir Anchor__", 0xAA: "ÀAutoCrossbow", 0xAB: "ÁFire Skean__",
         0xAC: "ÁWater Edge__", 0xAD: "ÁBolt Edge___", 0xAE: "ÁInviz Edge__", 0xAF: "ÁShadow Edge_",
         0xB0: "ÂGoggles_____", 0xB1: "ÂStar Pendant", 0xB2: "ÂPeace Ring__", 0xB3: "ÂAmulet______",
         0xB4: "ÂWhite Cape__", 0xB5: "ÂJewel Ring__", 0xB6: "ÂFairy Ring__", 0xB7: "ÂBarrier Ring",
         0xB8: "ÂMithrilGlove", 0xB9: "ÂGuard Ring__", 0xBA: "ÂRunningShoes", 0xBB: "ÂWall Ring___",
         0xBC: "ÂCherub Down_", 0xBD: "ÂCure Ring___", 0xBE: "ÂTrue Knight_", 0xBF: "ÂDragoonBoots",
         0xC0: "ÂZephyr Cape_", 0xC1: "ÂCzarina Ring", 0xC2: "ÂCursed Ring_", 0xC3: "ÂEarrings____",
         0xC4: "ÂAtlas Armlet", 0xC5: "ÂBlizzard Orb", 0xC6: "ÂRage Ring___", 0xC7: "ÂSneak Ring__",
         0xC8: "ÂPod Bracelet", 0xC9: "ÂHero Ring___", 0xCA: "ÂRibbon______", 0xCB: "ÂMuscle Belt_",
         0xCC: "ÂCrystal Orb_", 0xCD: "ÂGold Hairpin", 0xCE: "ÂEconomizer__", 0xCF: "ÂThief Glove_",
         0xD0: "ÂGauntlet____", 0xD1: "ÂGenji Glove_", 0xD2: "ÂHyper Wrist_", 0xD3: "ÂOffering____",
         0xD4: "ÂBeads_______", 0xD5: "ÂBlack Belt__", 0xD6: "ÂCoin Toss___", 0xD7: "ÂFakeMustache",
         0xD8: "ÂGem Box_____", 0xD9: "ÂDragon Horn_", 0xDA: "ÂMerit Award_", 0xDB: "ÂMemento Ring",
         0xDC: "ÂSafety Bit__", 0xDD: "ÂRelic Ring__", 0xDE: "ÂMoogle Charm", 0xDF: "ÂCharm Bangle",
         0xE0: "ÂMarvel Shoes", 0xE1: "ÂBack Guard__", 0xE2: "ÂGale Hairpin", 0xE3: "ÂSniper Sight",
         0xE4: "ÂExp. Egg____", 0xE5: "ÂTintinabar__", 0xE6: "ÂSprint Shoes", 0xE7: "_Rename Card_",
         0xE8: "_Tonic_______", 0xE9: "_Potion______", 0xEA: "_X-Potion____", 0xEB: "_Tincture____",
         0xEC: "_Ether_______", 0xED: "_X-Ether_____", 0xEE: "_Elixir______", 0xEF: "_Megalixir___",
         0xF0: "_Fenix Down__", 0xF1: "_Revivify____", 0xF2: "_Antidote____", 0xF3: "_Eyedrop_____",
         0xF4: "_Soft________", 0xF5: "_Remedy______", 0xF6: "_Sleeping Bag", 0xF7: "_Tent________",
         0xF8: "_Green Cherry", 0xF9: "_Magicite____", 0xFA: "_Super Ball__", 0xFB: "_Echo Screen_",
         0xFC: "_Smoke Bomb__", 0xFD: "_Warp Stone__", 0xFE: "_Dried Meat__", 0xFF: "_Empty_______"}