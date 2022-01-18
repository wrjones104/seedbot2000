from .Character import Character


class Dragon:
    """A dragon *spot* such as White Dragon in Fanatics Tower"""

    def __init__(self, name, owner, time):
        self.name = name
        self.owner = owner
        self.time = time

    @property
    def name(self) -> str:
        """The name of the Dragon"""
        return self._name

    @name.setter
    def name(self, input: str) -> None:
        """The name of the Dragon"""
        if not isinstance(input, str):
            message = "Input must be a string. Found: %s -- Type: %s" % (input, type(input))
            raise Exception(message)
        self._name = input

    @property
    def owner(self) -> Character:
        """The Character required to access the Dragon spot. Can be None"""
        return self._owner

    @owner.setter
    def owner(self, input: Character) -> None:
        """The Character required to access the Dragon spot. Can be None."""
        if input is not None and not isinstance(input, Character):
            message = "Input must be a Character. Found type: %s" % (type(input))
            raise Exception(message)
        self._owner = input

    @property
    def time(self) -> int:
        """The number of seconds getting to the dragon takes, on average"""
        return self._time

    @time.setter
    def time(self, input: int) -> None:
        """The number of seconds getting to the dragon takes, on average"""
        if not isinstance(input, int) or input <= 0:
            message = "Input must be a non-negative integer. Found %s" % (input)
            raise Exception(message)
        self._time = input

    def __str__(self):
        output = ""
        output += "Name: %s\n" % (self.name)
        output += "    Locked behind: %s\n" % (self.owner.name)
        output += "    Estimated time to dragon: %s second%s\n" % (self.time, 's' * (self.time > 1))
        output += "\n"
        return output
