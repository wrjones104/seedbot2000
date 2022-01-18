from constants import MONSTER_DATA_SIZE


class Monster():
    def __init__(self, name: str, inbytes=None) -> None:
        self.name = ''
        self.bytes = b''
        self.speed = -1
        self.vigor = -1
        self.hit_rate = -1
        self.evade_rate = -1
        self.magic_block_rate = -1
        self.defense = -1
        self.magic_defense = -1
        self.magic_power = -1
        self.hp = -1
        self.mp = -1
        self.xp = -1
        self.gold = -1
        self.level = -1
        self.ragnarok_metamorphosis_pack = -1
        self.ragnarok_hit_rate = -1
        self.dies_if_mp_becomes_0 = -1
        self.unknown1202 = -1
        self.no_name = -1
        self.unknown1208 = -1
        self.isHuman = -1
        self.unknown1220 = -1
        self.isCritIfImp = -1
        self.isUndead = -1
        self.isHardToRun = -1
        self.isAttackFirst = -1
        self.isBlockSuplex = -1
        self.isCantRun = -1
        self.isCantScan = -1
        self.isCantSketch = -1
        self.isSpecialEvent = -1
        self.isCantControl = -1
        self.blocked_status_1 = -1
        self.blocked_status_2 = -1
        self.blocked_status_3 = -1
        self.elements_absorbed = -1
        self.elements_no_effect = -1
        self.elements_weak = -1
        self.graphic_for_normal_attack = -1
        self.status1 = -1
        self.status2 = -1
        self.status3 = -1
        self.isTrueKnight = -1
        self.isRunic = -1
        self.isLife3 = -1
        self.unknown1E08 = -1
        self.unknown1E10 = -1
        self.unknown1E20 = -1
        self.unknown1E40 = -1
        self.isRemovableFloat = -1
        self.special_attack_setting = -1
        self.isNoDamage = -1
        self.isCantDodge = -1

        if not name or not isinstance(name, str):
            message = "Monster object name must be a string"
            raise Exception(message)
        self.name = name.replace("_", "")

        if inbytes:
            self.parse(inbytes)

    def parse(self, inbytes: bytes) -> None:
        if not isinstance(inbytes, bytes) or len(inbytes) != MONSTER_DATA_SIZE:
            message = "Monster object input must be a byte string of length %s. Found Type: %s -- Length: %s" % (
            hex(MONSTER_DATA_SIZE), type(inbytes), hex(len(inbytes)))
            raise Exception(message)
        try:
            self.bytes = inbytes
        except Exception as e:
            raise e

        self.speed = self.bytes[0x00]
        self.vigor = self.bytes[0x01]
        self.hit_rate = self.bytes[0x02]
        self.evade_rate = self.bytes[0x03]
        self.magic_block_rate = self.bytes[0x04]
        self.defense = self.bytes[0x05]
        self.magic_defense = self.bytes[0x06]
        self.magic_power = self.bytes[0x07]
        self.hp = self.bytes[0x08:0x0A]
        self.mp = self.bytes[0x0A:0x0C]
        self.xp = self.bytes[0x0C:0x0E]
        self.gold = self.bytes[0x0E:0x10]
        self.level = self.bytes[0x10]
        self.ragnarok_metamorphosis_pack = self.bytes[0x11] & 0x1F
        self.ragnarok_hit_rate = self.bytes[0x11] & 0xE0
        self.dies_if_mp_becomes_0 = self.bytes[0x12] & 0x01
        self.unknown1202 = self.bytes[0x12] & 0x02
        self.no_name = self.bytes[0x12] & 0x04
        self.unknown1208 = self.bytes[0x12] & 0x08
        self.isHuman = self.bytes[0x12] & 0x10
        self.unknown1220 = self.bytes[0x12] & 0x20
        self.isCritIfImp = self.bytes[0x12] & 0x40
        self.isUndead = self.bytes[0x12] & 0x80
        self.isHardToRun = self.bytes[0x13] & 0x01
        self.isAttackFirst = self.bytes[0x13] & 0x02
        self.isBlockSuplex = self.bytes[0x13] & 0x04
        self.isCantRun = self.bytes[0x13] & 0x08
        self.isCantScan = self.bytes[0x13] & 0x10
        self.isCantSketch = self.bytes[0x13] & 0x20
        self.isSpecialEvent = self.bytes[0x13] & 0x40
        self.isCantControl = self.bytes[0x13] & 0x80
        self.blocked_status_1 = self.bytes[0x14]
        self.blocked_status_2 = self.bytes[0x15]
        self.blocked_status_3 = self.bytes[0x16]
        self.elements_absorbed = self.bytes[0x17]
        self.elements_no_effect = self.bytes[0x18]
        self.elements_weak = self.bytes[0x19]
        self.graphic_for_normal_attack = self.bytes[0x1A]
        self.status1 = self.bytes[0x1B]
        self.status2 = self.bytes[0x1C]
        self.status3 = self.bytes[0x1D]
        self.isTrueKnight = self.bytes[0x1E] & 0x01
        self.isRunic = self.bytes[0x1E] & 0x02
        self.isLife3 = self.bytes[0x1E] & 0x04
        self.unknown1E08 = self.bytes[0x1E] & 0x08
        self.unknown1E10 = self.bytes[0x1E] & 0x10
        self.unknown1E20 = self.bytes[0x1E] & 0x20
        self.unknown1E40 = self.bytes[0x1E] & 0x40
        self.isRemovableFloat = self.bytes[0x1E] & 0x80
        self.special_attack_setting = self.bytes[0x1F] & 0x3F
        self.isNoDamage = self.bytes[0x1F] & 0x40
        self.isCantDodge = self.bytes[0x1F] & 0x80

    def __eq__(self, other):
        if not isinstance(other, Monster):
            return NotImplemented
        return self.bytes == self.bytes

    def compare(self, other):
        if not isinstance(other, Monster):
            return NotImplemented
        output = ""
        if self.speed != other.speed:
            output += "self.speed = %s -- other.speed == %s\n" % (self.speed, other.speed)
        if self.vigor != other.vigor:
            output += "self.vigor = %s -- other.vigor == %s\n" % (self.vigor, other.vigor)
        if self.hit_rate != other.hit_rate:
            output += "self.hit_rate = %s -- other.hit_rate == %s\n" % (self.hit_rate, other.hit_rate)
        if self.evade_rate != other.evade_rate:
            output += "self.evade_rate = %s -- other.evade_rate == %s\n" % (self.evade_rate, other.evade_rate)
        if self.magic_block_rate != other.magic_block_rate:
            output += "self.magic_block_rate = %s -- other.magic_block_rate == %s\n" % (
            self.magic_block_rate, other.magic_block_rate)
        if self.defense != other.defense:
            output += "self.defense = %s -- other.defense == %s\n" % (self.defense, other.defense)
        if self.magic_defense != other.magic_defense:
            output += "self.magic_defense = %s -- other.magic_defense == %s\n" % (
            self.magic_defense, other.magic_defense)
        if self.magic_power != other.magic_power:
            output += "self.magic_power = %s -- other.magic_power == %s\n" % (self.magic_power, other.magic_power)
        if self.hp != other.hp:
            output += "self.hp = %s -- other.hp == %s\n" % (self.hp, other.hp)
        if self.mp != other.mp:
            output += "self.mp = %s -- other.mp == %s\n" % (self.mp, other.mp)
        if self.xp != other.xp:
            output += "self.xp = %s -- other.xp == %s\n" % (self.xp, other.xp)
        if self.gold != other.gold:
            output += "self.gold = %s -- other.gold == %s\n" % (self.gold, other.gold)
        if self.level != other.level:
            output += "self.level = %s -- other.level == %s\n" % (self.level, other.level)
        if self.ragnarok_metamorphosis_pack != other.ragnarok_metamorphosis_pack:
            output += "self.ragnarok_metamorphosis_pack = %s -- other.ragnarok_metamorphosis_pack == %s\n" % (
            self.ragnarok_metamorphosis_pack, other.ragnarok_metamorphosis_pack)
        if self.ragnarok_hit_rate != other.ragnarok_hit_rate:
            output += "self.ragnarok_hit_rate = %s -- other.ragnarok_hit_rate == %s\n" % (
            self.ragnarok_hit_rate, other.ragnarok_hit_rate)
        if self.dies_if_mp_becomes_0 != other.dies_if_mp_becomes_0:
            output += "self.dies_if_mp_becomes_0 = %s -- other.dies_if_mp_becomes_0 == %s\n" % (
            self.dies_if_mp_becomes_0, other.dies_if_mp_becomes_0)
        if self.unknown1202 != other.unknown1202:
            output += "self.unknown1202 = %s -- other.unknown1202 == %s\n" % (self.unknown1202, other.unknown1202)
        if self.no_name != other.no_name:
            output += "self.no_name = %s -- other.no_name == %s\n" % (self.no_name, other.no_name)
        if self.unknown1208 != other.unknown1208:
            output += "self.unknown1208 = %s -- other.unknown1208 == %s\n" % (self.unknown1208, other.unknown1208)
        if self.isHuman != other.isHuman:
            output += "self.isHuman = %s -- other.isHuman == %s\n" % (self.isHuman, other.isHuman)
        if self.unknown1220 != other.unknown1220:
            output += "self.unknown1220 = %s -- other.unknown1220 == %s\n" % (self.unknown1220, other.unknown1220)
        if self.isCritIfImp != other.isCritIfImp:
            output += "self.isCritIfImp = %s -- other.isCritIfImp == %s\n" % (self.isCritIfImp, other.isCritIfImp)
        if self.isUndead != other.isUndead:
            output += "self.isUndead = %s -- other.isUndead == %s\n" % (self.isUndead, other.isUndead)
        if self.isHardToRun != other.isHardToRun:
            output += "self.isHardToRun = %s -- other.isHardToRun == %s\n" % (self.isHardToRun, other.isHardToRun)
        if self.isAttackFirst != other.isAttackFirst:
            output += "self.isAttackFirst = %s -- other.isAttackFirst == %s\n" % (
            self.isAttackFirst, other.isAttackFirst)
        if self.isBlockSuplex != other.isBlockSuplex:
            output += "self.isBlockSuplex = %s -- other.isBlockSuplex == %s\n" % (
            self.isBlockSuplex, other.isBlockSuplex)
        if self.isCantRun != other.isCantRun:
            output += "self.isCantRun = %s -- other.isCantRun == %s\n" % (self.isCantRun, other.isCantRun)
        if self.isCantScan != other.isCantScan:
            output += "self.isCantScan = %s -- other.isCantScan == %s\n" % (self.isCantScan, other.isCantScan)
        if self.isCantSketch != other.isCantSketch:
            output += "self.isCantSketch = %s -- other.isCantSketch == %s\n" % (self.isCantSketch, other.isCantSketch)
        if self.isSpecialEvent != other.isSpecialEvent:
            output += "self.isSpecialEvent = %s -- other.isSpecialEvent == %s\n" % (
            self.isSpecialEvent, other.isSpecialEvent)
        if self.isCantControl != other.isCantControl:
            output += "self.isCantControl = %s -- other.isCantControl == %s\n" % (
            self.isCantControl, other.isCantControl)
        if self.blocked_status_1 != other.blocked_status_1:
            output += "self.blocked_status_1 = %s -- other.blocked_status_1 == %s\n" % (
            self.blocked_status_1, other.blocked_status_1)
        if self.blocked_status_2 != other.blocked_status_2:
            output += "self.blocked_status_2 = %s -- other.blocked_status_2 == %s\n" % (
            self.blocked_status_2, other.blocked_status_2)
        if self.blocked_status_3 != other.blocked_status_3:
            output += "self.blocked_status_3 = %s -- other.blocked_status_3 == %s\n" % (
            self.blocked_status_3, other.blocked_status_3)
        if self.elements_absorbed != other.elements_absorbed:
            output += "self.elements_absorbed = %s -- other.elements_absorbed == %s\n" % (
            self.elements_absorbed, other.elements_absorbed)
        if self.elements_no_effect != other.elements_no_effect:
            output += "self.elements_no_effect = %s -- other.elements_no_effect == %s\n" % (
            self.elements_no_effect, other.elements_no_effect)
        if self.elements_weak != other.elements_weak:
            output += "self.elements_weak = %s -- other.elements_weak == %s\n" % (
            self.elements_weak, other.elements_weak)
        if self.graphic_for_normal_attack != other.graphic_for_normal_attack:
            output += "self.graphic_for_normal_attack = %s -- other.graphic_for_normal_attack == %s\n" % (
            self.graphic_for_normal_attack, other.graphic_for_normal_attack)
        if self.status1 != other.status1:
            output += "self.status1 = %s -- other.status1 == %s\n" % (self.status1, other.status1)
        if self.status2 != other.status2:
            output += "self.status2 = %s -- other.status2 == %s\n" % (self.status2, other.status2)
        if self.status3 != other.status3:
            output += "self.status3 = %s -- other.status3 == %s\n" % (self.status3, other.status3)
        if self.isTrueKnight != other.isTrueKnight:
            output += "self.isTrueKnight = %s -- other.isTrueKnight == %s\n" % (self.isTrueKnight, other.isTrueKnight)
        if self.isRunic != other.isRunic:
            output += "self.isRunic = %s -- other.isRunic == %s\n" % (self.isRunic, other.isRunic)
        if self.isLife3 != other.isLife3:
            output += "self.isLife3 = %s -- other.isLife3 == %s\n" % (self.isLife3, other.isLife3)
        if self.unknown1E08 != other.unknown1E08:
            output += "self.unknown1E08 = %s -- other.unknown1E08 == %s\n" % (self.unknown1E08, other.unknown1E08)
        if self.unknown1E10 != other.unknown1E10:
            output += "self.unknown1E10 = %s -- other.unknown1E10 == %s\n" % (self.unknown1E10, other.unknown1E10)
        if self.unknown1E20 != other.unknown1E20:
            output += "self.unknown1E20 = %s -- other.unknown1E20 == %s\n" % (self.unknown1E20, other.unknown1E20)
        if self.unknown1E40 != other.unknown1E40:
            output += "self.unknown1E40 = %s -- other.unknown1E40 == %s\n" % (self.unknown1E40, other.unknown1E40)
        if self.isRemovableFloat != other.isRemovableFloat:
            output += "self.isRemovableFloat = %s -- other.isRemovableFloat == %s\n" % (
            self.isRemovableFloat, other.isRemovableFloat)
        if self.special_attack_setting != other.special_attack_setting:
            output += "self.special_attack_setting = %s -- other.special_attack_setting == %s\n" % (
            self.special_attack_setting, other.special_attack_setting)
        if self.isNoDamage != other.isNoDamage:
            output += "self.isNoDamage = %s -- other.isNoDamage == %s\n" % (self.isNoDamage, other.isNoDamage)
        if self.isCantDodge != other.isCantDodge:
            output += "self.isCantDodge = %s -- other.isCantDodge == %s\n" % (self.isCantDodge, other.isCantDodge)
        if output == "":
            output = "Objects are identical"
        else:
            output = "Monster %s:\n" % (self.name) + output
        return output
