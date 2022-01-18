import os
import unittest

from common import constants
from common.ff6_rom import FF6_ROM
from common.functions import text_to_bytes, bytes_to_text, format_hex


class TestFunctions(unittest.TestCase):
    """Test the common functions from functions.py"""

    def testTextToBytes(self):
        """Test text_to_bytes"""
        with self.assertRaises(Exception):
            text_to_bytes()
        with self.assertRaises(Exception):
            text_to_bytes(5)
        with self.assertRaises(Exception):
            text_to_bytes("test", "3")
        with self.assertRaises(Exception):
            text_to_bytes("test", -1)
        with self.assertRaises(Exception):
            text_to_bytes("@#$%")
        assert text_to_bytes("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!?/:\"'-.") == \
               b'\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96' + \
               b'\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad' + \
               b'\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5'
        assert text_to_bytes("A", 5) == b'\x80\xFF\xFF\xFF\xFF'

    def testBytesToText(self):
        """Test bytes_to_text"""
        with self.assertRaises(Exception):
            bytes_to_text()
        with self.assertRaises(Exception):
            bytes_to_text(3)
        with self.assertRaises(Exception):
            bytes_to_text("A")
        with self.assertRaises(Exception):
            bytes_to_text(b'\x7F')

        byte_str = b'\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96' + \
                   b'\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad' + \
                   b'\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5'

        assert bytes_to_text(byte_str) == "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!?/:\"'-."
        assert bytes_to_text(b'\x80\xc5') == "A."

    def testFormatHex(self):
        """Test format_hex"""
        with self.assertRaises(Exception):
            format_hex()
        with self.assertRaises(Exception):
            format_hex(b'\x00')
        with self.assertRaises(Exception):
            format_hex("Q", 10)
        with self.assertRaises(Exception):
            format_hex(b'\x00', "10")
        with self.assertRaises(Exception):
            format_hex(-1, 10)
        with self.assertRaises(Exception):
            format_hex(256, 10)
        assert format_hex(b'\x00', 5) == "00"
        assert format_hex(0, 5) == "00"
        assert format_hex(17, 5) == "11"
        assert format_hex(b'\x00\x00\x00\x00\x00', 5) == "00 00 00 00 00"
        assert format_hex(b'\x00\x00\x00\x00\x00\x00', 5) == "00 00 00 00 00\n00"


class TestFF6ROM(unittest.TestCase):
    """Test the FF6_ROM class"""

    def testInit(self):
        """Test FF6_ROM __init__"""
        vanilla_rom_file = "./roms/FinalFantasy3e.smc"
        assert os.path.exists(vanilla_rom_file)

        with self.assertRaises(Exception):
            FF6_ROM()
        with self.assertRaises(Exception):
            FF6_ROM("FakePath")
        with self.assertRaises(Exception):
            FF6_ROM(6)
        rom = FF6_ROM(vanilla_rom_file)
        assert rom._has_header
        assert rom.is_FF6
        assert rom.is_vanilla
        assert rom.is_US
        assert len(rom.data) == constants.FF6_ROM_SIZE + (rom.has_header * constants.HEADER_SIZE)

    def testWriteGuards(self):
        """Test the guards that prevent incorrectly writing to the property variables"""
        rom_file = "./roms/wc.smc"
        assert os.path.exists(rom_file)

        rom = FF6_ROM(rom_file)
        with self.assertRaises(Exception):
            rom.rom_path = "A"
        with self.assertRaises(Exception):
            rom.is_vanilla = True
        with self.assertRaises(Exception):
            rom.has_header = True
        with self.assertRaises(Exception):
            rom.data = '5'
        with self.assertRaises(Exception):
            rom.is_FF6 = True
        with self.assertRaises(Exception):
            rom.is_US = True

    def testWriteFile(self):
        """Tests the write function"""
        rom_file = "./roms/wc.smc"
        output = "./output/test_output.smc"

        assert os.path.exists(rom_file)
        assert not os.path.exists(output)

        rom = FF6_ROM(rom_file)
        with self.assertRaises(Exception):
            rom.write()
        with self.assertRaises(Exception):
            rom.write(4)
        with self.assertRaises(Exception):
            rom.write(output, '4')
        assert rom.write(output)

        # The output file now exists
        assert rom.write(output, True)
        assert not rom.write(output)
        os.remove(output)
        assert not os.path.exists(output)
