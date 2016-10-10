"""Win Model definitions for google datastore"""

from protorpc import messages
from google.appengine.ext import ndb
from Rank import(
    Rank
)


class Win(ndb.Model):
    """Score object"""

    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    attempts_used = ndb.IntegerProperty(required=True)
    score = ndb.IntegerProperty(required=True)

    def to_form(self):
        return WinForm(user_name=self.user.get().name, won=self.won,
                       date=str(self.date), attempts_used=self.attempts_used,
                       score=self.score
                       )

    def to_rank(self, rank_index):
        return Rank(user_name=self.user.get().name, date=str(self.date),
                    attempts_used=self.attempts_used, score=self.score,
                    rank=rank_index
                    )


class WinForm(messages.Message):
    """WinForm for outbound Win information ..scoreboard perhaps?"""

    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    attempts_used = messages.IntegerField(4, required=True)
    score = messages.IntegerField(5, required=True)


class WinForms(messages.Message):
    """Return multiple WinForms"""

    wins = messages.MessageField(WinForm, 1, repeated=True)
