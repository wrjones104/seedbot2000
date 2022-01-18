class Character:
    """A Worlds Collide Character such as Terra"""

    def __init__(self, name, checks, numMIAB):
        self.name = name
        self.checks = checks
        self.numMIAB = numMIAB
        self.dragons = None

    @property
    def name(self) -> str:
        """The name of the character"""
        return self._name

    @name.setter
    def name(self, input: str) -> None:
        """The name of the character"""
        if not isinstance(input, str):
            message = "Input must be a string. Found: %s -- Type: %s" % (input, type(input))
            raise Exception(message)
        self._name = input

    @property
    def checks(self) -> dict:
        """Dictionary of Check objects corresponding to the checks available to that character
           Keys are the name of the check, values are Check objects."""
        return self._checks

    @checks.setter
    def checks(self, input) -> None:
        """Dictionary of Check objects corresponding to the checks available to that character
           Keys are the name of the check, values are Check objects. Inputs are lists of Checks"""
        from .Check import Check

        input_list = []
        message = ""
        if not isinstance(input, (list, tuple, set)):
            message = "Input must be a list or convertable to a list and contain Checks. Found type %s\n" % (
                type(input))

        input_list = list(input)

        for item in input_list:
            if not isinstance(item, Check):
                message += "Found non-Check item in input: %s" % (item)
                raise Exception(message)

        self._checks = {}
        for check in input_list:
            self._checks[check.name] = check

    @property
    def numMIAB(self) -> int:
        """The number of Monsters in a Box locked behind this Character"""
        return self._numMIAB

    @numMIAB.setter
    def numMIAB(self, input: int) -> None:
        """The number of Monsters in a Box locked behind this Character"""
        if not isinstance(input, int) or input < 0:
            message = "Input must be a non-negative integer or convertable to one. Found: %s -- Type: %s" % (
            input, type(input))
            raise Exception(message)
        self._numMIAB = input

    @property
    def dragons(self) -> dict:
        """A dictionary of dragons gated by this character. Keys are names, values are Dragon objects. This is a dict
           in case someone somehow ever gates more than one dragon, which is unlikely."""
        return self._dragons

    @dragons.setter
    def dragons(self, input) -> None:
        """A dictionary of dragons gated by this character. Keys are names, values are Dragon objects. This is a dict
           in case someone somehow ever gates more than one dragon, which is unlikely."""
        from .Dragon import Dragon

        input_list = []
        message = ""
        try:
            input_list = list(input)
        except Exception as e:
            message = "Input must be a list or convertable to a list and contain Dragons. Found type %s\n" % (
                type(input))

        for item in input_list:
            if not isinstance(item, Dragon):
                message += "Found non-Check item in input: %s" % (item)
                raise Exception(message)

        self._dragons = {}
        for dragon in input_list:
            self._dragons[dragon.name] = dragon

    def __str__(self):
        output = "%s:\n" % self.name
        output += "    Number of Monsters in a box: %s\n" % self.numMIAB
        output += "    Dragons: "
        if len(self.dragons) == 0:
            output += "None\n"
        else:
            output += "\n"
            for dragon in self.dragons:
                output += "      %s" % dragon
            output += "\n"

        output += "    Checks:"
        if len(self.checks) == 0:
            output += "None\n"
        else:
            output += "\n"
            for checkname in self.checks:
                check = self.checks[checkname]
                for line in str(check).split('\n'):
                    output += "      " + line + '\n'
        return output
