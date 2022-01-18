import os

from ..common import constants


class FF6_ROM:
    """A Final Fantasy VI US or Worlds Collide ROM"""

    def __init__(self, rom_path: str) -> None:
        """Initializer for FF6_ROM

        Parameters
        ----------
        rom_path : str
            The path to the input ROM

        Returns
        -------
        None
        """
        error = ""
        if not isinstance(rom_path, str):
            error += "Input rom_path must be a string. Found type %s\n" % (type(rom_path))
        elif not os.path.exists(rom_path):
            error += "Could not find ROM path %s\n" % (rom_path)
        if error != "":
            raise Exception(error)

        self._rom_path = None
        self._has_header = False
        self._is_vanilla = True
        self._is_FF6 = True
        self._is_US = True
        self._rom_path = os.path.abspath(rom_path)
        self._data = None
        self.read()

    @property
    def rom_path(self) -> str:
        """The path to the ROM"""
        return self._rom_path

    @rom_path.setter
    def rom_path(self, in_path):
        """This can only be set by the initializer"""
        error = "The rom_path can only be set by the initializer"
        raise Exception(error)

    @property
    def has_header(self) -> bool:
        """Does the rom have a header?"""
        return self._has_header

    @has_header.setter
    def has_header(self, input):
        """This can only be set by the initializer"""
        error = "has_header can only be set by the initializer"
        raise Exception(error)

    @property
    def is_vanilla(self) -> bool:
        """Is the ROM vanilla?"""
        return self._is_vanilla

    @is_vanilla.setter
    def is_vanilla(self, input):
        """This can only be set by the initializer"""
        error = "is_vanilla can only be set by the initializer"
        raise Exception(error)

    @property
    def is_US(self) -> bool:
        """Is the ROM a US version of FF6?"""
        return self._is_US

    @is_US.setter
    def is_US(self, input):
        """This can only be set by the initializer"""
        error = "is_US can only be set by the initializer"
        raise Exception(error)

    @property
    def is_FF6(self) -> bool:
        """Is the ROM some version of FF6?"""
        return self._is_FF6

    @is_FF6.setter
    def is_FF6(self, input):
        """Is the ROM some version of FF6?"""
        error = "is_FF6 can only be set by the initializer"
        raise Exception(error)

    @property
    def data(self) -> bytes:
        """Raw ROM data"""
        return self._data

    @data.setter
    def data(self, input: bytes):
        """Set the data
        Parameters
        ----------
        input : bytes
            The content of a ROM

        Returns
        -------
        None
        """
        if not isinstance(input, (bytes, bytearray)):
            raise Exception("Data input must be bytes. Found type %s" % (type(input)))
        self._data = bytes(input)
        self.parse()

    def __str__(self) -> str:
        """Print-friendly information about this ROM"""
        offset = (self.has_header * constants.HEADER_SIZE)
        rom_title = self.data[constants.HiROM_HEADER_TITLE_OFFSET + offset: \
                              constants.HiROM_HEADER_TITLE_OFFSET + constants.HiROM_HEADER_TITLE_SIZE + offset]
        rom_title = rom_title.decode('utf-8')
        output = "ROM Information:\n"
        output += "    Path: %s\n" % (self.rom_path)
        output += f"    Size (bytes): {len(self.data):,}\n"
        output += "    Has Header: %s\n" % (self.has_header)
        output += "    Title: %s\n" % (rom_title)
        output += "    Is FF6: %s\n" % (self.is_FF6)
        output += "    Is US: %s\n" % (self.is_US)
        output += "    Is Vanilla: %s\n" % (self.is_vanilla)
        output += "\n"
        return output

    def read(self) -> None:
        """Reads in an FF6 ROM from ``self.rom_path``"""
        if not os.path.exists(self.rom_path):
            error = "Could not find ROM path %s\n" % (self.rom_path)
            raise Exception(error)
        data = None
        with open(self.rom_path, 'rb') as f:
            data = f.read()
        if not data:
            raise Exception("Unable to read data from %s" % (self.rom_path))
        self.data = data

    def parse(self) -> None:
        """Parses the data in ``self.data``"""
        # Check for a 0x200 byte header
        if len(self.data) == constants.FF6_ROM_SIZE + constants.HEADER_SIZE:
            self._has_header = True

        offset = (self.has_header * constants.HEADER_SIZE)

        # Check to see if the length of the SMC header is 512. If not, the header is malformed
        if len(self.data) % 0x400 != 512:
            self._is_vanilla = False

        # Check to see if the title of the ROM is 'FINAL FANTASY 3      '
        rom_title = self.data[constants.HiROM_HEADER_TITLE_OFFSET + offset: \
                              constants.HiROM_HEADER_TITLE_OFFSET + constants.HiROM_HEADER_TITLE_SIZE + offset]

        if rom_title not in (constants.FF6_HEADER_TITLE_DATA_US, constants.FF6_HEADER_TITLE_DATA_JP):
            self._is_FF6 = False
            self._is_vanilla = False
        elif rom_title == constants.FF6_HEADER_TITLE_DATA_JP:
            self._is_US = False

        # Check to see if the reset vector is equal to 0xFF00 and it contains FF6_HEADER_RESET_DATA
        reset_pointer_data_start = constants.HiROM_EMULATION_MODE_RESET_VECTOR_OFFSET + offset
        reset_pointer_data_end = reset_pointer_data_start + constants.HiROM_EMULATION_MODE_RESET_VECTOR_SIZE
        reset_pointer_data = self.data[reset_pointer_data_start: reset_pointer_data_end]
        if reset_pointer_data != constants.FF6_HEADER_RESET_VECTOR:
            self._is_FF6 = False
            self._is_vanilla = False

        reset_pointer_deref = int.from_bytes(reset_pointer_data, constants.SNES_BYTE_ORDER)
        header_reset_data = self.data[reset_pointer_deref + offset: reset_pointer_deref + 7 + offset]
        if header_reset_data != constants.FF6_HEADER_RESET_DATA:
            self._is_FF6 = False
            self._is_vanilla = False

        if not self.is_FF6:
            self._is_US = False
            self._is_vanilla = False

    def write(self, output_filename: str, overwrite=False) -> bool:
        """Writes the bytes in ``self.data`` to ``output_filename``. Will not overwrite unless specifically enabled
        Parameters
        ----------
        output_filename : str
            The file name to write to
        overwrite : bool, optional
            If the file already exists, should it be overwritten? Defaults to False

        Returns
        -------
        bool
            Was the file successfully written?
        """

        error = ""
        if not isinstance(output_filename, str):
            error += "output_filename must be a string. Found type %s\n" % (type(output_filename))
        if not isinstance(overwrite, bool):
            error += "overwrite must be a bool. Found type %s\n" % (type(overwrite))
        if error != "":
            raise Exception(error)

        # If the file exists and we're not supposed to overwrite, do nothing and return False
        if os.path.exists(output_filename) and not overwrite:
            return False

        with open(output_filename, 'wb') as f:
            f.write(self.data)

        # Make sure the file exists and is the right size
        if os.path.exists(output_filename) and os.path.getsize(output_filename) == len(self.data):
            return True

        # Something bad has happened, but no exceptions were raised
        return False
