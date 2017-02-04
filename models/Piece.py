""" Piece - logical design of a single piece """


class Piece():
    """Defines a Level"""

    _name = ""
    _display_name = ""
    _index = -1
    _type = ""

    def __init__(self, args={}):
        if 'name' in args:
            self.setName(args['name']);
        if 'type' in args:
            self.setType(args['type'])
        if 'display_name' in args:
            self.setDisplayName(args['display_name'])
        if 'index' in args:
            self.setIndex(args['index'])

    def setName(self, name):
        self._name = name

    def setType(self, type):
        self._type = type

    def setDisplayName(self, display_name):
        self._display_name = display_name

    def setIndex(self, index):
        self._index = index

    def getName(self):
        return self._name

    def getType(self):
        return self._type

    def getDisplayName(self):
        return self._display_name

    def getIndex(self):
        return self._index

    def toJson(self):
        return {
            "name": self.getName(),
            "display_name": self.getDisplayName(),
            "index": self.getIndex(),
            "type": self.getType()
        }
