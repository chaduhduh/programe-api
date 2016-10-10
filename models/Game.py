"""Game Model definitions for google datastore"""

from google.appengine.api import taskqueue
from google.appengine.ext import ndb
from protorpc import messages
from datetime import datetime
from Win import(
  Win
)


class Game(ndb.Model):
    """Game object"""

    attempts_remaining = ndb.IntegerProperty(required=True, default=5)
    attempts_used = ndb.IntegerProperty(required=True, default=0)
    game_over = ndb.BooleanProperty(required=True, default=False)
    user = ndb.KeyProperty(required=True, kind='User')
    current_level = ndb.StringProperty(required=True, default="level_one")
    score = ndb.IntegerProperty(required=True, default=0)

    @classmethod
    def create_game(self, user, attempts_remaining, attempts_used,
                    score, current_level):
        """Creates and returns a new game"""

        game = Game(user=user, attempts_remaining=attempts_remaining,
                    score=score, attempts_used=attempts_used,
                    current_level=current_level)
        game.put()
        return game

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""

        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.attempts_remaining = self.attempts_remaining
        form.attempts_used = self.attempts_used
        form.game_over = self.game_over
        form.current_level = self.current_level
        form.score = self.score
        form.message = message
        return form

    def end_game(self, won=False):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""

        self.game_over = True
        if not won:
            self.message = "Game Over"
        else:
            self.message = "Winner"
            game_win = Win(
                    user=self.user,
                    date=datetime.utcnow(),
                    won=True,
                    attempts_used=self.attempts_used,
                    score=self.score
                    )
            game_win.put()
        self.put()
        # Add the game to the score 'board'

    def register_move(self):
        """defines what happens when a player clicks submit """

        if self.attempts_remaining < 1:
            self.end_game(False)
        self.attempts_remaining -= 1
        self.attempts_used += 1

    def set_level(self, level_name):
        """sets the current game level **note** this does not write"""

        self.current_level = level_name

    def push_history(self, submission, action, program_compiled):
        """pushes this move into history"""

        history_data = {
            'user': self.user.get().name,
            'score': self.score,
            'action': action,
            'submission': submission,
            'program_compiled': program_compiled,
            'level': self.current_level
        }
        taskqueue.add(url='/tasks/push_game_history', params=history_data)

    def register_score(self, score):
        self.score += score
        self.attempts_remaining += 5  # + five moves a win


class GameForm(messages.Message):
    """GameForm for outbound game state information"""

    urlsafe_key = messages.StringField(1, required=True)
    attempts_remaining = messages.IntegerField(2, required=True)
    attempts_used = messages.IntegerField(3, required=True)
    game_over = messages.BooleanField(4, required=True)
    message = messages.StringField(5, required=True)
    user_name = messages.StringField(6, required=True)
    current_level = messages.StringField(7, required=True)
    score = messages.IntegerField(8, required=True)


class GameFormList(messages.Message):
    """List of GameForms for outbound information"""

    games = messages.MessageField(GameForm, 1, repeated=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""

    user_name = messages.StringField(1, required=True)
    attempts_remaining = messages.IntegerField(2, default=5)
    attempts_used = messages.IntegerField(3, default=0)
    score = messages.IntegerField(4, default=0)
    current_level = messages.StringField(5, default="level_one")


class SubmitBoardForm(messages.Message):
    """Used to make a move in an existing game"""

    solution_attempt = messages.StringField(1, required=True)
