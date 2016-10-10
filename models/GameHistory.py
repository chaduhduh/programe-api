"""GameHistory Model definitions for google datastore"""

from protorpc import messages
from google.appengine.ext import ndb


class GameHistory(ndb.Model):
    """History object"""

    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)      # auto_now_add=True
    action = ndb.StringProperty(required=True)
    score = ndb.IntegerProperty(required=True)
    submission = ndb.StringProperty(required=True)
    program_compiled = ndb.BooleanProperty(required=True)
    level = ndb.StringProperty(required=True)

    def to_form(self):
        """Returns a GameForm representation of the Game"""
        history = GameHistoryForm()
        history.user_name = self.user.get().name
        history.date = str(self.date)
        history.action = self.action
        history.score = self.score
        history.submission = self.submission
        history.level = self.level
        history.program_compiled = self.program_compiled
        return history


class GameHistoryForm(messages.Message):
    """single move in game history outbound information"""

    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    action = messages.StringField(3, required=True)
    score = messages.IntegerField(4, required=True)
    submission = messages.StringField(5, required=True)
    program_compiled = messages.BooleanField(6, required=True)
    level = messages.StringField(7, required=True)


class AllHistoryForm(messages.Message):
    """all game history for a given user outbound information"""

    history = messages.MessageField(GameHistoryForm, 1, repeated=True)
