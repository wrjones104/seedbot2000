from .Character import Character


class Check:
    """A Worlds Collide Check, such as Lone Wolf"""

    def __init__(self, name, owner, canBeChar, canBeEsper, canBeItem, requiredCheck, time, desirability):
        self.name = name
        self.owner = owner
        self.canBeChar = canBeChar
        self.canBeEsper = canBeEsper
        self.canBeItem = canBeItem
        self.requiredCheck = requiredCheck
        self.time = time
        self.desirability = desirability

    @property
    def name(self) -> str:
        """The name of the check"""
        return self._name

    @name.setter
    def name(self, input: str) -> None:
        """The name of the check"""
        if not isinstance(input, str):
            message = "Input must be a string. Found: %s -- Type: %s" % (input, type(input))
            raise Exception(message)
        self._name = input

    @property
    def owner(self) -> Character:
        """The Character required to access the rewards of the Check"""
        return self._owner

    @owner.setter
    def owner(self, input: Character) -> None:
        """The Character required to access the rewards of the Check"""
        if not isinstance(input, Character):
            message = "Input must be a Character. Found type: %s" % (type(input))
            raise Exception(message)
        self._owner = input

    @property
    def canBeChar(self) -> bool:
        """Boolean representing whether the check can be a character"""
        return self._canBeChar

    @canBeChar.setter
    def canBeChar(self, input: bool) -> None:
        """Boolean representing whether the check can be a character"""
        if not isinstance(input, bool):
            message = "Input must be a bool. Found type: %s" % (type(input))
            raise Exception(message)
        self._canBeChar = input

    @property
    def canBeEsper(self) -> bool:
        """Boolean representing whether the check can be an Esper"""
        return self._canBeEsper

    @canBeEsper.setter
    def canBeEsper(self, input: bool) -> None:
        """Boolean representing whether the check can be an Esper"""
        if not isinstance(input, bool):
            message = "Input must be a bool. Found type: %s" % (type(input))
            raise Exception(message)
        self._canBeEsper = input

    @property
    def canBeItem(self) -> bool:
        """Boolean representing whether the check can be an Item"""
        return self._canBeItem

    @canBeItem.setter
    def canBeItem(self, input: bool) -> None:
        """Boolean representing whether the check can be an Item"""
        if not isinstance(input, bool):
            message = "Input must be a bool. Found type: %s" % (type(input))
            raise Exception(message)
        self._canBeItem = input

    @property
    def requiredCheck(self):
        """The most immediate Check required to do this Check. For example, Magitek 3 requires Magitek 2. Can be None."""
        return self._requiredCheck

    @requiredCheck.setter
    def requiredCheck(self, input) -> None:
        """The most immediate Check required to do this Check. For example, Magitek 3 requires Magitek 2. Can be None."""
        if input is not None and not isinstance(input, Check):
            message = "Input must be a Check. Found type: %s" % (type(input))
            raise Exception(message)
        self._requiredCheck = input

    @property
    def time(self) -> int:
        """The number of seconds the check takes, on average"""
        return self._time

    @time.setter
    def time(self, input: int) -> None:
        """The number of seconds the check takes, on average"""
        if not isinstance(input, int) or input <= 0:
            message = "Input must be a non-negative integer. Found %s" % (input)
            raise Exception(message)
        self._time = input

    @property
    def desirability(self) -> int:
        """The desirability of the check, on a scale from 1 to 100 inclusive"""
        return self._desirability

    @desirability.setter
    def desirability(self, input: int) -> None:
        """The desirability of the check, on a scale from 1 to 100 inclusive"""
        if not isinstance(input, int) or not 0 < input <= 100:
            message = "Input must be an integer between 1 and 100 inclusive. Found %s" % (input)
            raise Exception(message)
        self._desirability = input

    def __str__(self):
        output = ""
        output += "%s\n" % self.name
        output += "    Locked behind: %s\n" % self.owner.name
        output += "    Locked behind check: "
        if self.requiredCheck is not None:
            output += "%s\n" % self.requiredCheck.name
        else:
            output += "%s\n" % self.requiredCheck
        output += "    Can be Character: %s\n" % self.canBeChar
        output += "    Can be Esper: %s\n" % self.canBeEsper
        output += "    Can be Item: %s\n" % self.canBeItem
        output += "    Estimated time to boss: %s second%s\n" % (self.time, 's' * (self.time > 1))
        output += "    Estimated desirability: %s/100\n" % self.desirability
        output += "\n"
        return output
