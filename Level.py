""" Levels - logical design of each level.

    These definitions will propegate to each platform and the ui will be
    built from this accordingly.
"""

class Level():
    """  """
    
    _name = "new-game"

    def setName(self, name):
        self._name = name;

    def getName(self):
        return self._name or ""


class All_Levels():

    
    levels = []

    # Level One
    level_one = Level()
    level_one.setName("level_one")
    levels.append(level_one)


    def getLevel(self, level_name):
        """ returns a specific level from name """

        for level in self.levels:
            if level.getName() is level_name:
                return level
        return False