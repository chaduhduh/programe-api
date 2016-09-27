""" Levels - logical design of each level.

    These definitions will propegate to each platform and the ui will be
    built from this accordingly.
"""


class Level():
    """  """
    
    _name = "new-game"
    _pieces = []
    _solutions = []
    _board_structure = {};


    # name

    def setName(self, name):
        self._name = name;

    def getName(self):
        return self._name or ""


    # pieces

    def setPieces(self, pieces):
        self._pieces = pieces;

    def getPieces(self):
        return self._pieces or []


    # solutions

    def setSolutions(self, solutions):
        self._solutions = solutions;

    def getSolutions(self):
        return self._solutions or []


    # board structure

    def setBoardStructure(self, structure):
        self._board_structure = structure;

    def getBoarStructure(self):
        return self._board_structure or []



class All_Levels():

    
    levels = []

    # Level One
    level_one = Level()
    level_one.setName("level_one")
    level_one.setPieces(["start","print","'game'","end"]);
    level_one.setSolutions([["start","print","'game'","end"]]);
    level_one.setBoardStructure({
        "main" : {
            "row" : {
                "pieces" : ["start"]
            }
            "row" : {
                "pieces" : ["print", "'game'"]
                "row" : {
                    "pieces" : []       # this is how nested rows are defined
                }
            }
            "row" : {
                "pieces" : ["end"]
            }
        }
    });
    levels.append(level_one)


    def getLevel(self, level_name):
        """ returns a specific level from name """

        for level in self.levels:
            if level.getName() is level_name:
                return level
        return False