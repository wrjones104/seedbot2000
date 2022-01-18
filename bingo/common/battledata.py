class Battle():
    # 576 battle formations
    def __init__(self):
        self.vrammap = None
        self.monsters_loaded_to_BG1 = None
        self.monsters_present = None
        self.monster_1_index = None
        self.monster_2_index = None
        self.monster_3_index = None
        self.monster_4_index = None
        self.monster_5_index = None
        self.monster_6_index = None
        self.monster_1_xy = None
        self.monster_2_xy = None
        self.monster_3_xy = None
        self.monster_4_xy = None
        self.monster_5_xy = None
        self.monster_6_xy = None
        # Is it a boss? 3F is yes, 3E is no
        self.msb = None
