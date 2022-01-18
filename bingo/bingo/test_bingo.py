import unittest

from bingo.Character import Character
from bingo.Check import Check
from bingo.Dragon import Dragon


class TestDragons(unittest.TestCase):
    """Test the Dragon class functions"""

    def testDragonInit(self):
        ch = Character("Name", {}, 7)
        with self.assertRaises(Exception):
            d = Dragon()
        with self.assertRaises(Exception):
            d = Dragon("Dragon")
        with self.assertRaises(Exception):
            d = Dragon("Dragon", ch)
        d = Dragon("Dragon", ch, 1)

    def testDragonName(self):
        ch = Character("Name", {}, 7)
        with self.assertRaises(Exception):
            d = Dragon(7, ch, 1)
        with self.assertRaises(Exception):
            d = Dragon(None, ch, 1)
        d = Dragon("Dragon", ch, 1)

    def testDragonOwner(self):
        ch = Character("Name", {}, 7)
        with self.assertRaises(Exception):
            d = Dragon("Dragon", "q", 1)
        with self.assertRaises(Exception):
            d = Dragon("Dragon", 7, 1)
        d = Dragon("Dragon", ch, 1)
        d = Dragon("Dragon", None, 1)

    def testDragonTime(self):
        ch = Character("Name", {}, 7)
        with self.assertRaises(Exception):
            d = Dragon("Dragon", ch, -1)
        with self.assertRaises(Exception):
            d = Dragon("Dragon", ch, 0)
        with self.assertRaises(Exception):
            d = Dragon("Dragon", ch, "a")
        with self.assertRaises(Exception):
            d = Dragon("Dragon", ch, None)
        d = Dragon("Dragon", ch, 1)


class TestCharacters(unittest.TestCase):
    """Test the Character class functions"""

    def testCharInit(self):
        with self.assertRaises(Exception):
            ch = Character()
        with self.assertRaises(Exception):
            ch = Character("Name")
        with self.assertRaises(Exception):
            ch = Character("Name", {})
        ch = Character("Name", {}, 7)

    def testCharName(self):
        with self.assertRaises(Exception):
            ch = Character(1, {}, 7)
        with self.assertRaises(Exception):
            ch = Character(None, {}, 7)
        ch = Character("Name", {}, 7)

    def testCharCheck(self):
        with self.assertRaises(Exception):
            ch = Character("Name", "4", 7)
        with self.assertRaises(Exception):
            ch = Character("Name", 7, 7)
        ch = Character("Name", {}, 7)
        c = Check("Name", ch, True, True, True, None, 1, 1)
        ch2 = Character("Name", [c], 7)
        ch3 = Character("Name", [c, c], 7)
        ch3 = Character("Name", (c, c), 7)
        ch3 = Character("Name", set([c, c]), 7)

    def testCharMIABCHeck(self):
        with self.assertRaises(Exception):
            ch = Character("Name", {}, -1)
        with self.assertRaises(Exception):
            ch = Character("Name", {}, None)
        with self.assertRaises(Exception):
            ch = Character("Name", {}, "a")
        ch = Character("Name", {}, 7)


class TestChecks(unittest.TestCase):
    """Test the Check class functions"""

    def testCheckInit(self):
        ch = Character("Name", {}, 7)
        with self.assertRaises(Exception):
            c = Check()
        with self.assertRaises(Exception):
            c = Check("Name")
        with self.assertRaises(Exception):
            c = Check("Name", ch)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True, True)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True, True, None)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True, True, None, 1)
        c = Check("Name", ch, True, True, True, None, 1, 1)

    def testCheckName(self):
        ch = Character("Name", {}, 7)
        with self.assertRaises(Exception):
            c = Check(None, ch, True, True, True, None, 1, 1)
        with self.assertRaises(Exception):
            c = Check(7, ch, True, True, True, None, 1, 1)
        with self.assertRaises(Exception):
            c = Check(ch, ch, True, True, True, None, 1, 1)
        c = Check("Name", ch, True, True, True, None, 1, 1)

    def testCheckOwner(self):
        ch = Character("Name", {}, 7)
        with self.assertRaises(Exception):
            c = Check("Name", "Owner", True, True, True, None, 1, 1)
        with self.assertRaises(Exception):
            c = Check("Name", 3, True, True, True, None, 1, 1)
        with self.assertRaises(Exception):
            c = Check("Name", None, True, True, True, None, 1, 1)
        c = Check("Name", ch, True, True, True, None, 1, 1)

    def testCheckCanBeChar(self):
        ch = Character("Name", {}, 7)
        with self.assertRaises(Exception):
            c = Check("Name", ch, 7, True, True, None, 1, 1)
        with self.assertRaises(Exception):
            c = Check("Name", ch, None, True, True, None, 1, 1)
        c = Check("Name", ch, True, True, True, None, 1, 1)
        c = Check("Name", ch, False, True, True, None, 1, 1)

    def testCheckCanBeEsper(self):
        ch = Character("Name", {}, 7)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, 7, True, None, 1, 1)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, None, True, None, 1, 1)
        c = Check("Name", ch, True, True, True, None, 1, 1)
        c = Check("Name", ch, True, False, True, None, 1, 1)

    def testCheckCanBeItem(self):
        ch = Character("Name", {}, 7)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True, 7, None, 1, 1)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True, None, None, 1, 1)
        c = Check("Name", ch, True, True, True, None, 1, 1)
        c = Check("Name", ch, True, True, False, None, 1, 1)

    def testCheckRequiredCheck(self):
        ch = Character("Name", {}, 7)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True, True, 7, 1, 1)
        c = Check("Name", ch, True, True, True, None, 1, 1)
        d = Check("Name", ch, True, True, True, c, 1, 1)

    def testCheckTime(self):
        ch = Character("Name", {}, 7)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True, True, None, 0, 1)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True, True, None, -33, 1)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True, True, None, 1.1, 1)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True, True, None, 'f', 1)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True, True, None, None, 1)
        c = Check("Name", ch, True, True, True, None, 1, 1)

    def testCheckDesirability(self):
        ch = Character("Name", {}, 7)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True, True, None, 1, 0)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True, True, None, 1, -4)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True, True, None, 1, 102)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True, True, None, 1, 77.7)
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True, True, None, 1, 'f')
        with self.assertRaises(Exception):
            c = Check("Name", ch, True, True, True, None, 1, None)
        c = Check("Name", ch, True, True, True, None, 1, 1)
