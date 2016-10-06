# programe-api

Api built on google app engine for managing programe saved games and scores. <br />
See https://github.com/chaduhduh/ProGrAME for game itself. <br />
To browse api explorer go to: <a href="http://programe-api.appspot.com/_ah/api/explorer" target="_blank">http://programe-api.appspot.com/_ah/api/explorer</a><br />

Programe is a puzzle game that helps to teach some basic programming logic. Programe-api serves <br />
as an interface to manage games, levels and users.<br />

Cloud Endpoints
===============
<b>create_user()</b> - creates a new user from username and email, requires a unique username<br />
<b>create_game()</b> - creates a new game for the given user, see game Model for properties<br />
<b>get_game()</b> - returns the current game state including current level, score, and attempts remaining - &lt;String&gt;urlsafe_game_key<br />
<b>get_all_games()</b> - returns list of all games for a given user - Resources: &lt;String&gt;username<br />
<b>get_high_scores()</b> - returns 'the scoreboard'. Resources: &lt;Integer&gt;number_of_results(default=10, required=False)<br />
<b>get_user_ranks()</b> - returns list of all top games for all users<br />
<b>get_game_history()</b> - returns all game history for a given user, used to view an 'instant replay' of games. Resources: &lt;String&gt;username<br />
<b>delete_game()</b> - deletes an existing game. Resources: <String>usersafe_game_key, &lt;String&gt;username<br />
<b>submit_board()</b> - validates submitted solution then pushes move history. Resources: &lt;String&gt;urlsafe_game_key, &lt;String&gt;solution_attempt<br />
<b>get_wins()</b> - returns all winning games (finished)<br />
<b>get_user_wins()</b> - returns all winning games for a given user <br />
<b>get_level()</b> - Returns a single level for the given level name, this is used to create the UI. We dont allow skipping forward or back >;). Resources: &lt;String&gt;level_name<br />

Models
===============
List of our datastore entities below. see Models.py for specific class data<br />
<b>User</b> - represents user profile<br />
<b>Game</b> - represents a single game<br />
<b>Game History</b> - represents various history actions in a game<br />
<b>User</b> - represents user profile<br />
<b>Win </b>- represents a ended game (reached last level)<br />

Classes
===============
<b>Level</b> - Level.py - logical design of single level and game levels. These definitions will propegate to each platform and the ui will be built from this accordingly. See Level.py for specific properties.<br />

Methods
===============
<b>_push_game_history()</b> - api.py - pushes history for the given user, this is invoked via task and is not invoked directly<br />
<b>get_by_urlsafe</b> - utils.py - Returns an ndb.Model entity that the urlsafe key points to. Checks that the type of entity returned is of the correct kind.<br />

Tasks/Crons  (cron.yaml, app.yaml, main.py)
===============
<b>SendReminderEmail(/crons/send_reminder)</b> - send reminder email every 24 hours for any users who have failed a challenge. This will serve to encourage people to continue. Time limit updated in cron.yaml<br />
<b>pushGameHistory(/tasks/push_game_history)</b> - invokes the _push_game_history() function to add this move to the task queue. We queue these since generally history is not needed to complete/continue playing.<br />





