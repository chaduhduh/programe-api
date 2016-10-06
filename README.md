# programe-api

Api built on google app engine for managing programe saved games and scores. 
See https://github.com/chaduhduh/ProGrAME for game itself. To browse api explorer go
to: http://programe-api.appspot.com/_ah/api/explorer

Programe is a puzzle game that helps to teach some basic programming logic. Programe-api serves 
as an interface to manage games, levels and users.

Cloud Endpoints
===============
create_user() - creates a new user from username and email, requires a unique username
create_game() - creates a new game for the given user, see game Model for properties
get_game() - returns the current game state including current level, score, and attempts remaining - <String>urlsafe_game_key
get_all_games() - returns list of all games for a given user - Resources: <String>username
get_high_scores() - returns 'the scoreboard'. Resources: <Integer>number_of_results(default=10, required=False)
get_user_ranks() - returns list of all top games for all users
get_game_history() - returns all game history for a given user, used to view an 'instant replay' of games. Resources: <String>username
delete_game() - deletes an existing game. Resources: <String>usersafe_game_key, <String>username
submit_board() - validates submitted solution then pushes move history. Resources: <String>urlsafe_game_key, <String>solution_attempt
get_wins() - returns all winning games (finished)
get_user_wins() - returns all winning games for a given user 
get_level() - Returns a single level for the given level name, this is used to create the UI. We dont allow skipping forward or back >;). Resources: <String>level_name

Models
===============
List of our datastore entities below. see Models.py for specific class data
User - represents user profile
Game - represents a single game
GameHistory - represents various history actions in a game
User - represents user profile
Win - represents a ended game (reached last level)

Classes
===============
Level - Level.py - logical design of single level and game levels. These definitions will propegate to each platform and the ui will be built from this accordingly. See Level.py for specific properties.

Methods
===============
_push_game_history() - api.py - pushes history for the given user, this is invoked via task and is not invoked directly
get_by_urlsafe - utils.py - Returns an ndb.Model entity that the urlsafe key points to. Checks that the type of entity returned is of the correct kind.

Tasks/Crons  (cron.yaml, app.yaml, main.py)
===============
SendReminderEmail(/crons/send_reminder) - send reminder email every 24 hours for any users who have failed a challenge. This will serve to encourage people to continue. Time limit updated in cron.yaml
pushGameHistory(/tasks/push_game_history) - invokes the _push_game_history() function to add this move to the task queue. We queue these since generally history is not needed to complete/continue playing.





