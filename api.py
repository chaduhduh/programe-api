# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""


import logging
import endpoints
from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue
from datetime import datetime
from Level import All_Levels as Levels
from Level import Level as Level
import json

from models import User, Game, Win
from models import StringMessage, NewGameForm, GameForm, SubmitBoardForm,\
    WinForms, LevelForm, GameFormList, RankForm, GameHistory, AllHistoryForm,\
    GameHistoryForm
from utils import get_by_urlsafe


levels = Levels()
NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(
    urlsafe_game_key=messages.StringField(1),
    )
GET_GAMES_REQUEST = endpoints.ResourceContainer(
    username=messages.StringField(1),
    )
GET_GAME_HISTORY_REQUEST = endpoints.ResourceContainer(
    username=messages.StringField(1),
    )
GET_HIGH_SCORE_REQUEST = endpoints.ResourceContainer(
    number_of_results=messages.IntegerField(1,required=False,default=10),
    )
GET_LEVEL_REQUEST = endpoints.ResourceContainer(
    level_name=messages.StringField(1),
    )
SUBMIT_BOARD_REQUEST = endpoints.ResourceContainer(
    SubmitBoardForm,
    urlsafe_game_key=messages.StringField(1)
    )
USER_REQUEST = endpoints.ResourceContainer(
    user_name=messages.StringField(1),
    email=messages.StringField(2)
    )
DELETE_GAME_REQUEST = endpoints.ResourceContainer(
    urlsafe_game_key=messages.StringField(1),
    user_name=messages.StringField(2)
    )




MEMCACHE_MOVES_REMAINING = 'MOVES_REMAINING'


@endpoints.api(name='programe', version='v1')
class ProgrameApi(remote.Service):
    """Configures and Manages Programe users, games, levels, and game settings."""

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                    'A User with that name already exists!')
        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(message='User {} created!'.format(
                request.user_name))


    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      path='game',
                      name='create_game',
                      http_method='POST')
    def create_game(self, request):
        """Creates new game"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        try:
            game = Game.create_game(user.key, request.attempts_remaining, request.score)
        except ValueError:
            raise endpoints.BadRequestException('Maximum must be greater '
                                                'than minimum!')
        # Use a task queue to update the average attempts remaining.
        # This operation is not needed to complete the creation of a new game
        # so it is performed out of sequence.

        # TODO: do this
        # taskqueue.add(url='/tasks/cache_average_attempts')
        return game.to_form('Good luck playing programe')


    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, request):
        """Return the current game state."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return game.to_form('Time to make a move!')
        else:
            raise endpoints.NotFoundException('Game not found!')


    @endpoints.method(request_message=GET_GAMES_REQUEST,
                      response_message=GameFormList,
                      path='games/{username}',
                      name='get_games',
                      http_method='GET')
    def get_games(self, request):
        """Return the current game state."""
        user = User.query(User.name == request.username).get()
        if not user:
          raise endpoints.NotFoundException('No User Found.')

        games = Game.query(Game.user == user.key)
        if not games:
            raise endpoints.NotFoundException('No Games Found.')
        games_list = [game.to_form("") for game in games] or []
        return GameFormList(games=games_list)


    # get_high_scores

    @endpoints.method(request_message=GET_HIGH_SCORE_REQUEST,
                      response_message=WinForms,
                      path='the-scoreboard',
                      name='get_high_scores',
                      http_method='GET')
    def get_high_scores(self, request):
        """Return the scoreboard. Optional: number_of_results limiter"""
        number_of_results = int(request.number_of_results) or 10
        all_wins = Win.query().order(-Win.score, Win.attempts_used).fetch(number_of_results) or []
        return WinForms(wins=[win.to_form() for win in all_wins])


    # get_user_ranks

    @endpoints.method(response_message=RankForm,
                      path='user/ranks',
                      name='get_user_ranks',
                      http_method='GET')
    def get_ranks_scores(self, request):
        """returns list of all top players by rank"""
        user_wins = []
        users = User.query()
        for user in users:
            user_wins.append(Win.query(Win.user == user.key).order(-Win.score, Win.attempts_used).get())

        user_highscores = []
        for i, win in enumerate(user_wins):
          user_highscores.append(win.to_rank(i+1))
        return RankForm(ranks=user_highscores)


    # get_game_history - store guess attempt with level + date

    @endpoints.method(request_message=GET_GAME_HISTORY_REQUEST,
                      response_message=AllHistoryForm,
                      path='games/history/{username}',
                      name='get_game_history',
                      http_method='GET')
    def get_game_history(self, request):
        """Return the current game state."""
        user = User.query(User.name == request.username).get()
        if not user:
          raise endpoints.NotFoundException('No User Found.')

        history = GameHistory.query(GameHistory.user == user.key)
        if not history:
            raise endpoints.NotFoundException('No History Found.')
        history_list = [item.to_form() for item in history] or []
        return AllHistoryForm(history=history_list)


    @endpoints.method(request_message=DELETE_GAME_REQUEST,
                      response_message=StringMessage,
                      path='game',
                      name='cancel_game',
                      http_method='DELETE')
    def delete_game(self, request):
        """Deletes an existing game"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        # check for existing game from same user

        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if not game or user.name is not game.user.get().name:
          raise endpoints.NotFoundException(
                    'Unable to delete or game does not exist')
        # do delete

        game.key.delete()
        return StringMessage(message="Game deleted")


    @endpoints.method(request_message=SUBMIT_BOARD_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='submit_board',
                      http_method='PUT')
    def submit_board(self, request):
        """Makes a move. Returns a game state with message"""

        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game.game_over:
            return game.to_form('Game already over!')

        game.attempts_remaining -= 1
        game.attempts_used += 1
        current_level = levels.getLevel(game.current_level)

        if current_level is False:
          current_level = levels.getLevelByIndex(0)
          game.current_level = current_level.getName()

        # do task stuff this will move
        history_data = { 
            'user': game.user.get().name,
            'score': game.score,
            'action': 'program ran', 
            'submission': request.solution_attempt,
            'program_compiled' : current_level.isSolution(request.solution_attempt),
            'level' : game.current_level
            }
        taskqueue.add(url='/tasks/push_game_history',params=history_data)

        if not current_level.isSolution(request.solution_attempt):
          game.put()
          return game.to_form("There was a bug in your code!!")
        # solved - register score and get the next level

        game.score += current_level.getSolutionScore();
        game.attempts_remaining += 5
        next_level = levels.getNextLevel(current_level.getName())
        
        if next_level is False:    # no levels left
          game.current_level = "Winner"
          game.end_game(True)
          return game.to_form("You have reached the end of the game, click to view your ranks")

        game.current_level =  next_level.getName();
        # end game or update game datad

        if game.attempts_remaining < 1:
            game.end_game(False)
            return game.to_form('Game over!')
        else:
            game.put()
            return game.to_form("Program Compiled!")


    @endpoints.method(response_message=WinForms,
                      path='wins',
                      name='get_wins',
                      http_method='GET')
    def get_wins(self, request):
        """Return all wins"""
        all_wins = Win.query() or []
        return WinForms(wins=[win.to_form() for win in all_wins])


    @endpoints.method(request_message=USER_REQUEST,
                      response_message=WinForms,
                      path='win/user/{user_name}',
                      name='get_user_wins',
                      http_method='GET')
    def get_user_wins(self, request):
        """Returns all of an individual User's wins"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        all_wins = Win.query(Win.user == user.key) or []
        return WinForms(wins=[win.to_form() for win in all_wins])


    @endpoints.method(response_message=StringMessage,
                      path='games/average_attempts',
                      name='get_average_attempts_remaining',
                      http_method='GET')
    def get_average_attempts(self, request):
        """Get the cached average moves remaining"""
        return StringMessage(message=memcache.get(MEMCACHE_MOVES_REMAINING) or '')


    @endpoints.method(request_message=GET_LEVEL_REQUEST,
                      response_message=LevelForm,
                      path='level/{level_name}',
                      name='get_level',
                      http_method='GET')
    def get_level(self, request):
        """Return the current game state."""
        level = levels.getLevel(str(request.level_name));
        if not level:
          raise endpoints.NotFoundException(
                    'Level Not Found')
        return LevelForm(name=level.getName(), pieces=json.dumps(level.getPieces()), solutions=str(level.getSolutions()), board_structure=str(level.getBoardStructure()))


    @staticmethod
    def _cache_average_attempts():
        """Populates memcache with the average moves remaining of Games"""
        games = Game.query(Game.game_over == False).fetch()
        if games:
            count = len(games)
            total_attempts_remaining = sum([game.attempts_remaining
                                        for game in games])
            average = float(total_attempts_remaining)/count
            memcache.set(MEMCACHE_MOVES_REMAINING,
                         'The average moves remaining is {:.2f}'.format(average))

    @staticmethod
    def _push_game_history(request):
        """Pushes history"""
        user = User.query(User.name==request['user']).get()
        if not user:
          return False

        if request['program_compiled'].decode('utf_8') == 'True':
          request['program_compiled'] = True
        else:
          request['program_compiled'] = False
        history = GameHistory(user=user.key, date=datetime.utcnow(), action=request['action'], 
                              score=int(request['score']), submission=request['submission'], program_compiled=request['program_compiled'],
                              level=request['level']
                              )
        history.put()


api = endpoints.api_server([ProgrameApi])
