from constants import RANDOM_BATTLE_GROUP_SIZE


class Battlegroup:
    # Packs in FF3usme
    def __init__(self, inbytes=None) -> None:
        self.bytes = b''
        self.formation1 = -1
        self.formation2 = -1
        self.formation3 = -1
        self.rareformation = -1

        if inbytes:
            self.parse(inbytes)

    def parse(self, inbytes: bytes) -> None:
        if not isinstance(inbytes, bytes) or len(inbytes) != RANDOM_BATTLE_GROUP_SIZE:
            message = "Battlegroup object input must be a byte string of length %s. Found Type: %s -- Length: %s" % (
            hex(RANDOM_BATTLE_GROUP_SIZE), type(inbytes), hex(len(inbytes)))
            raise Exception(message)
        try:
            self.bytes = inbytes
        except Exception as e:
            raise e

        self.formation1 = self.bytes[0x00]
        self.formation2 = self.bytes[0x01]
        self.formation3 = self.bytes[0x02]
        self.rareformation = self.bytes[0x03]

    def __eq__(self, other):
        if not isinstance(other, Battlegroup):
            return NotImplemented
        return self.bytes == self.bytes

    def compare(self, other):
        if not isinstance(other, Battlegroup):
            return NotImplemented
        output = ""
        if self.formation1 != other.formation1:
            output += "self.formation1 = %s -- other.formation1 == %s\n" % (self.formation1, other.formation1)
        if self.formation2 != other.formation2:
            output += "self.formation2 = %s -- other.formation2 == %s\n" % (self.formation2, other.formation2)
        if self.formation3 != other.formation3:
            output += "self.formation3 = %s -- other.formation3 == %s\n" % (self.formation3, other.formation3)
        if self.rareformation != other.rareformation:
            output += "self.rareformation = %s -- other.rareformation == %s\n" % (
            self.rareformation, other.rareformation)
        if output == "":
            output = "Objects are identical"
        return output
