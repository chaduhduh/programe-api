# -*- coding: utf-8 -*-`
"""Programe API - Backend interface for ProGrAME - chaduhduh/ProGrAME

  Programe is a puzzle game that helps to teach some basic programming logic.
  Programe-api serves as an interface to manage games, levels and users.
"""


# imports

import endpoints
import json
from protorpc import (
    remote,
    messages
)
from datetime import(
    datetime
)
from models import(
    All_Levels as Levels,
    LevelForm,
    User,
    Game,
    GameForm,
    GameFormList,
    NewGameForm,
    SubmitBoardForm,
    AllHistoryForm,
    GameHistory,
    Win,
    WinForms,
    RankForm
)
from utils import(
    get_by_urlsafe,
    StringMessage
)


# declarations

levels = Levels()
NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(
    urlsafe_game_key=messages.StringField(1),
)
GET_DATA_FOR_USERNAME_REQUEST = endpoints.ResourceContainer(
    username=messages.StringField(1),
)
GET_HIGH_SCORE_REQUEST = endpoints.ResourceContainer(
    number_of_results=messages.IntegerField(1, default=10),
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
    username=messages.StringField(2)
)


# Programe Api

@endpoints.api(name='programe', version='v1', scopes=[endpoints.EMAIL_SCOPE])
class ProgrameApi(remote.Service):
    """Configures and Manages Programe users, games, levels,
    and game settings."""

    # create user
    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Creates a new User. Requires a unique username"""

        user = endpoints.get_current_user()
        user_name = user.email() if user else 'Anonymous'
        if user_name is 'Anonymous':
            raise endpoints.UnauthorizedException(
                    'Log in to create a user')
        if User.query(User.name == user_name).get():
            raise endpoints.ConflictException(
                    'A User with that name already exists!')
        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(message='User {} created!'.format(
                request.user_name))

    # create game
    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      path='game',
                      name='create_game',
                      http_method='POST')
    def create_game(self, request):
        """Creates new game for a given user"""

        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        try:
            game = Game.create_game(user.key, request.attempts_remaining,
                                    request.attempts_used, request.score,
                                    request.current_level)
        except ValueError:
            raise endpoints.BadRequestException('Maximum must be greater '
                                                'than minimum!')
        return game.to_form('Good luck playing programe')

    # get game
    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, request):
        """Returns the current game state including current level, score, and \
        attempts remaining"""

        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return game.to_form('Time to make a move!')
        else:
            raise endpoints.NotFoundException('Game not found!')

    # get all games
    @endpoints.method(request_message=GET_DATA_FOR_USERNAME_REQUEST,
                      response_message=GameFormList,
                      path='games/{username}',
                      name='get_user_games',
                      http_method='GET')
    def get_user_games(self, request):
        """Returns a list of all games for a given user"""

        user = User.query(User.name == request.username).get()
        if not user:
            raise endpoints.NotFoundException('No User Found.')

        games = Game.query(Game.user == user.key, Game.game_over == False)
        if not games:
            raise endpoints.NotFoundException('No Games Found.')
        games_list = [game.to_form("") for game in games] or []
        return GameFormList(games=games_list)

    # get high scores
    @endpoints.method(request_message=GET_HIGH_SCORE_REQUEST,
                      response_message=WinForms,
                      path='the-scoreboard',
                      name='get_high_scores',
                      http_method='GET')
    def get_high_scores(self, request):
        """Returns 'the scoreboard'. Optional: number_of_results limiter"""

        number_of_results = int(request.number_of_results) or 10
        all_wins = Win.query().order(-Win.score, Win.attempts_used)\
                              .fetch(number_of_results) or []
        return WinForms(wins=[win.to_form() for win in all_wins])

    # get user ranks
    @endpoints.method(response_message=RankForm,
                      path='user/ranks',
                      name='get_user_ranks',
                      http_method='GET')
    def get_user_ranks(self, request):
        """Returns list of all top players by rank (users single best game)"""

        user_wins = []
        users = []
        wins = Win.query().order(-Win.score, Win.attempts_used)
        for win in wins:
            name = win.user.get().name or ""
            print name
            if name not in users and name is not "":
                user_wins.append(win)
                users.append(name)
        user_highscores = []
        # sort by score
        for i, win in enumerate(user_wins):
            user_highscores.append(win.to_rank(i+1))
        return RankForm(ranks=user_highscores)

    # get game history
    @endpoints.method(request_message=GET_DATA_FOR_USERNAME_REQUEST,
                      response_message=AllHistoryForm,
                      path='games/history/{username}',
                      name='get_game_history',
                      http_method='GET')
    def get_game_history(self, request):
        """Returns all game history for a given user, used to view an 'instant \
           replay' of their game and top ranked games."""

        user = User.query(User.name == request.username).get()
        if not user:
            raise endpoints.NotFoundException('No User Found.')

        history = GameHistory.query(GameHistory.user == user.key)
        if not history:
            raise endpoints.NotFoundException('No History Found.')
        history_list = [item.to_form() for item in history] or []
        return AllHistoryForm(history=history_list)

    # delete game
    @endpoints.method(request_message=DELETE_GAME_REQUEST,
                      response_message=StringMessage,
                      path='game',
                      name='cancel_game',
                      http_method='DELETE')
    def delete_game(self, request):
        """Deletes an existing game"""

        user = User.query(User.name == request.username).get()
        if not user:
            raise endpoints.NotFoundException('A User with that name does not exist!')
        # check for existing game from same user

        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if not game:
            raise endpoints.NotFoundException('Unable to delete, game does not exist')
        if game.game_over is True:
            raise endpoints.NotFoundException('Game is already over')
        if user.name is not game.user.get().name:
            raise endpoints.NotFoundException('Game does not belong to this user')
        # do delete

        game.key.delete()
        return StringMessage(message="Game deleted")

    # submit board
    @endpoints.method(request_message=SUBMIT_BOARD_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='submit_board',
                      http_method='PUT')
    def submit_board(self, request):
        """Validates submitted solution then pushes game history"""

        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game.game_over:
            raise endpoints.ForbiddenException("The game is already over.")

        current_level = levels.getLevel(game.current_level)
        if current_level is False:    # if for some reason no level go to 1
            current_level = levels.getLevelByIndex(0)
            game.set_level(current_level.getName())
        # check solution, register move and push this move into history

        is_solution = current_level.isSolution(request.solution_attempt)
        if is_solution:
            game.register_score(current_level.getSolutionScore())
        game.register_move()
        game.push_history(request.solution_attempt,
                          'Run Program',
                          is_solution
                          )
        if not is_solution:
            if game.attempts_remaining is 0:
                game.end_game(True)
            game.put()
            return game.to_form("There was a bug in your code!!")
        # solved - register score and get the next level

        next_level = levels.getNextLevel(current_level.getName())
        if next_level is False:    # no levels left means win
            game.set_level("winner")
            game.end_game(True)
            return game.to_form("You have reached the end of the game,\
                                  click to view your ranks")
        # set next level and return game state

        game.set_level(next_level.getName())
        game.put()
        return game.to_form("Program Compiled!")

    # get wins - aka completed game
    @endpoints.method(response_message=WinForms,
                      path='wins',
                      name='get_wins',
                      http_method='GET')
    def get_wins(self, request):
        """Returns all wins"""

        all_wins = Win.query() or []
        return WinForms(wins=[win.to_form() for win in all_wins])

    # get user wins
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

    # get level
    @endpoints.method(request_message=GET_LEVEL_REQUEST,
                      response_message=LevelForm,
                      path='level/{level_name}',
                      name='get_level',
                      http_method='GET')
    def get_level(self, request):
        """Returns a single level for the given level name, this is used\
        to create the UI"""

        level = levels.getLevel(str(request.level_name))
        if not level:
            raise endpoints.NotFoundException(
                    'Level Not Found')
        return LevelForm(
                  name=level.getName(),
                  display_name=level.getDisplayName(),
                  pieces=level.getPieces(),
                  solutions=json.dumps(level.getSolutions()),
                  board_structure=json.dumps(level.getBoardStructure()),
                  instructions=level.getInstructions()
                  )

    # push game history
    @staticmethod
    def _push_game_history(request):
        """Pushes history for the given user"""

        user = User.query(User.name == request['user']).get()
        if not user:
            return False
        if request['program_compiled'].decode('utf_8') == 'True':
            request['program_compiled'] = True
        else:
            request['program_compiled'] = False
        history = GameHistory(
                    user=user.key, date=datetime.utcnow(),
                    action=request['action'], score=int(request['score']),
                    submission=request['submission'],
                    program_compiled=request['program_compiled'],
                    level=request['level']
                    )
        history.put()

# start api server with our api objects

api = endpoints.api_server([ProgrameApi])
