""" Levels - logical design of single level and game levels

    These definitions will propegate to each platform and the ui will be
    built from this accordingly.
"""

from protorpc import (
    messages
)
from Piece import (
    Piece
)


class Level():
    """Defines a Level"""

    _name = "new-game"
    _pieces = []
    _solutions = []
    _board_structure = {}
    _solution_score = 0

    # name
    def setName(self, name):
        self._name = name

    def getName(self):
        return self._name or ""

    # pieces
    def setPieces(self, pieces):
        self._pieces = pieces

    def getPieces(self):
        return self._pieces or []

    # solutions
    def setSolutions(self, solutions):
        self._solutions = solutions

    def getSolutions(self):
        return self._solutions or []

    # board structure
    def setBoardStructure(self, structure):
        self._board_structure = structure

    def getBoardStructure(self):
        return self._board_structure or []

    # set score for solving
    def setSolutionScore(self, score):
        self._solution_score = score

    def getSolutionScore(self):
        return self._solution_score or 0

    # functions
    def isSolution(self, str):
        """returns true if provided solution matches level solution"""

        for solution in self.getSolutions():
            if solution == str:
                return True
        return False


class All_Levels():
    """ stores levels and defines structure for a game.

        This defines how multiple levels come together. Also provides
        some various logic related to levels such as getNextLevel and
        getLevelByIndex
    """

    levels = []

    
    # Level One

    #   pieces
    startPiece = Piece({"name": "start", "display_name": "Start", "index": 0, "type": "start"}).toJson()
    printPiece = Piece({"name": "print", "display_name": "Print", "index": 1, "type": "action"}).toJson()
    gamePiece = Piece({"name": "game", "display_name": "'Game'", "index": 2,  "type": "string"}).toJson()
    endPiece = Piece({"name": "end", "display_name": "End", "index": 3, "type" : "end"}).toJson()
    #   level
    level_one = Level()
    level_one.setName("level_one")
    level_one.setPieces("start,print,game,end")
    level_one.setSolutions(["start,print,game,end"])
    level_one.setSolutionScore(10)
    level_one.setBoardStructure({
        "rows": [{
                "pieces": [startPiece]
            },
            {
                "pieces": [printPiece, gamePiece]
            },
            {
                "pieces": [endPiece]
            }
        ]
    })
    levels.append(level_one)

    # Level Two

    #   pieces
    startPiece = Piece({"name": "start", "display_name": "Start", "index": 0, "type": "start"}).toJson()
    endPiece = Piece({"name": "end", "display_name": "End", "index": 1, "type" : "end"}).toJson()
    #   level
    level_two = Level()
    level_two.setName("level_two")
    level_two.setPieces("start,end")
    level_two.setSolutions(["start,end"])
    level_two.setSolutionScore(15)
    level_two.setBoardStructure({
        "rows": [{
                "pieces": [startPiece],
                "rows": []  # this is how nested rows are defined,
            },
            {
                "pieces": [endPiece]
            }
        ]
    })
    levels.append(level_two)


    # Level Three

    #   pieces
    startPiece = Piece({"name": "start", "display_name": "Start", "index": 0, "type": "start"}).toJson()
    returnPiece = Piece({"name": "return", "display_name": "Start", "index": 1, "type": "action"}).toJson()
    xPiece = Piece({"name": "x", "display_name": "X", "index": 2, "type": "value"}).toJson()
    endPiece = Piece({"name": "end", "display_name": "End", "index": 3, "type" : "end"}).toJson()
    #   level
    level_three = Level()
    level_three.setName("level_three")
    level_three.setPieces("start,return,x,end")
    level_three.setSolutions(["start,return,x,end"])
    level_three.setSolutionScore(20)
    level_three.setBoardStructure({
        "rows": [{
                "pieces": [startPiece]
            },
            {
                "pieces": [returnPiece, xPiece]
            },
            {
                "pieces": [endPiece]
            }
        ]
    })
    levels.append(level_three)


    # Level Four

    #   pieces
    startPiece = Piece({"name": "start", "display_name": "Start", "index": 0, "type": "start"}).toJson()
    returnPiece = Piece({"name": "return", "display_name": "Start", "index": 1, "type": "action"}).toJson()
    xPiece = Piece({"name": "x", "display_name": "X", "index": 2, "type": "value"}).toJson()
    endPiece = Piece({"name": "end", "display_name": "End", "index": 3, "type" : "end"}).toJson()
    #   level
    level_four = Level()
    level_four.setName("level_four")
    level_four.setPieces("start,return,x,end")
    level_four.setSolutions(["start,return,x,end"])
    level_four.setSolutionScore(20)
    level_four.setBoardStructure({
        "rows": [{
                "pieces": [startPiece]
            },
            {
                "pieces": [returnPiece, xPiece]
            },
            {
                "pieces": [endPiece]
            }
        ]
    })
    levels.append(level_four)

    def getLevel(self, level_name):
        """ returns a specific level from name """

        for level in self.levels:
            if level.getName() == level_name:
                return level
        return False

    def getLevelByIndex(self, index):
        """ returns a specific level by index """

        if self.levels[index]:
            return self.levels[index]
        return self.levels[0]

    def getNextLevel(self, current_level_name):
        """ returns the next level after a given level name """

        index = 0
        for level in self.levels:
            index += 1
            if level.getName() == current_level_name:
                break
        if index > (len(self.levels) - 1):
            return False
        else:
            return self.levels[index]


class LevelForm(messages.Message):
    """LevelForm for outbound level information"""

    name = messages.StringField(1, required=True)
    pieces = messages.StringField(2, required=True)
    solutions = messages.StringField(3, required=True)
    board_structure = messages.StringField(4, required=True)
