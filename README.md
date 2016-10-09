#Programe-api

Api built on google app engine for managing programe saved games and scores. <br />
See https://github.com/chaduhduh/ProGrAME for game ui and live demo. <br />
To browse api explorer go to: <a href="http://programe-api.appspot.com/_ah/api/explorer" target="_blank">http://programe-api.appspot.com/_ah/api/explorer</a><br />

Programe is a puzzle game that helps to teach some basic programming logic. Programe-api serves <br />
as an interface to manage games, levels and users.<br />

![Alt text](https://raw.githubusercontent.com/chaduhduh/ProGrAME/master/images/programe-example.jpg?raw=true "Example Level")

##Api Local Setup Instructions:
1. Download the Google App Engine SDK for python (python is required to run App Engine SDk)<br />
2. After install launch Google App Engine SDK<br />
3. Clone the programe-api repo to your machine (or download the zip) to the location of your choice<br />
4. Update the value of application in app.yaml to the app ID you have registered in the App Engine admin console and would like to use to host your instance of this sample.
5. Once App Engine is open and files are cloned click 'File>Add Existing Application' on the prompt and select the folder where you cloned the programe-api repo
6. Set the ports or use the default settings
7. Once the status off the app is green (green start button) local app instance has been launched! Console will also let you know when launch is complete.
8. Click the browse button to open the url, typically: http://localhost:{port}
9. To view the api explorer navigate to "/_ah/api/explorer" relative to your app. Typically, http://localhost:{port}/_ah/api/explorer<br />
**note** to view the api explorer on localhost you will need to launch chrome from the command line with the --unsafely-treat-insecure-origin-as-secure flag set. 
To do this navigate to the directory you have chrome installed (find chrome.exe). And run the following command: 
<i>"chrome.exe --user-data-dir=test --unsafely-treat-insecure-origin-as-secure=http://localhost:8080"</i><br />
10. After opening chrome with the previous flag set and navigating to the "/_ah/api/explorer" directory you are ready to begin testing your endpoints!!

##Game Description:
Programe is a an educational puzzle game that is designed to teach some basic programming 
logic. Although intended for beginners some of the puzzles can become quite challenging! 
In the game the user is presented with an available set of pieces and a puzzle board. The object
of the game is to arrange the pieces to that the simulated program will 'compile'. When the user
gets the correct solution they receive a score and move to the next level! Level objectives are given
for each level and new pieces get added as the game progresses. Players can not skip levels as each
one is helpful for the next level. To win the game player MUST complete ALL levels in the current game. 
Games can contain differing multiples of levels. High scores track the game with the highest score and 
lowest number of attempts. <br />
To see how the game is played view the live demo here: http://programe.chaddmyers.com/

## Game Scoring:
1. Each new game a player creates keeps its own running score. <br />
2. Points are achieved by correctly solving each puzzle.<br />
3. puzzles are decoded from top to bottom left to right. For example, the solution for the puzzle in the 
image above would be start,print,game,end. The front end client will determine how that information is obtained
from their puzzle board<br />
4. the level solved determines the number of points a player receives.<br />
5. the total score when the player reaches the last level will be the final score.<br />
6. Users are ranked by the highest score with the lowest number of attempts. If two users have the
same score on a game the attempts used will determine the leader. Rank will show the users best game,
wins will show best of all games.

##Api Description:
The create_user and create_game endpoints are used to create a new user and a new game. Once a game is initialized
for a valid user the get_level endpoint can be called to get all the details of the current level. This information
will be used to build the UI for the game. Level structure is built it standard JSON so it can be parsed for any platform.
The submit_board endpoint will receive the users solution and will check that against the current levels solution. Response will
indicate the result of the guess and will update the level accordingly. get_all_highscores (aka the scoreboard) is used to 
build a scoreboard of the top ranking players. <br />
Typical flow will be:<br />
    1. <code>create_user</code><br />
    2. <code>create_game</code><br />
    3. <code>get_level</code><br />
    4. <code>submit_board</code> <br />
    5. <code>get_level</code><br />
    6. <code>submit_board</code><br />
    7. <code>get_user_rank</code><br />
    8. <code>create_game</code><br />
    9. etc

## Api Usage: 
1. navigate to the api explorer at http://localhost:{port}/_ah/api/explorer<br />
2. generate a new user using the <code>create_user</code><br />
3. create a new game or load an existing game with the <code>create_game</code> and <code>get_game</code> endpoints. The create game endpoint only requires a username<br />
5. call <code>get_level</code> with the game level name from the previous response to build out a user interface<br />
4. Using the url safe key from the previous response submit a move on the board using the <code>submit_board</code> function.<br />
5. Put the key into the key field and in the solution field enter "start,print,game,end" which is the solution for level one<br />
6. submit that request and the response will return the updated game and the new level!<br />
7. once the user reaches the last level they will get a registered win.<br />
9. <code>get_user_wins</code> will display all wins for a given user and <code>get_wins</code> will display all wins.<br />
10. Once some moves have been made game history can be viewed using the <code>get_game_history</code> function<br />
11. ** note ** currently levels are in progress. For the meantime there are only three levels. 'level_one', 'level_two', 'level_three'
    
##Cloud Endpoints
- **create_user**
    - Path: 'user'
    - Method: POST
    - Parameters: user_name, email (optional)
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. user_name provided must be unique. Will 
    raise a ConflictException if a User with that user_name already exists.
    
- **create_game**
    - Path: 'game'
    - Method: POST
    - Parameters: user_name, attempts_remaining(default=5), attempts_used(default=0), score(default=0), 
    current_level(default='level_one')
    - Returns: GameForm with initial game state.
    - Description: Creates a new Game. user_name provided must correspond to an
    existing user - will raise a NotFoundException if not. attempts_remaining 
    is the allowed # of attempts. Attempts_used is how many have been used total.
    Score and current level typically will initialize at 0 and level_one, however, 
    if continue game is needed this way you can continue from an existing point.
     
- **get_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: GameForm with current game state.
    - Description: Returns the current state of a game.

- **get_user_games**
    - Path: 'games/{username}'
    - Method: GET
    - Parameters: username
    - Returns: GameFormList
    - Description: Returns a list of all games for a given user. This allows
    a sinlge user to have multiple games at the same time.

- **delete_game**
    - Path: 'game/'
    - Method: DELETE
    - Parameters: urlsafe_game_key, username
    - Returns: LevelForm
    - Description: Deletes the provided game if the username and game exist. Will 
    raise a NotFoundException if the User or game does not exist.

- **get_game_history**
    - Path: 'games/history/{username}'
    - Method: GET
    - Parameters: username
    - Returns: AllHistoryForm
    - Description: Returns all game history for a given user, used to view an 'instant 
    replay' of their game and top ranked games.

- **get_level**
    - Path: 'level/{level_name}'
    - Method: GET
    - Parameters: level_name
    - Returns: LevelForm
    - Description: Returns a single level for the given level name, this is used
    to create the UI
    
- **submit_board**
    - Path: 'game/{urlsafe_game_key}'
    - Method: PUT
    - Parameters: urlsafe_game_key, solution_attempt
    - Returns: GameForm with updated game state.
    - Description: Accepts 'solution_attempt' which is a list of pieces
    in order of the puzzle board (eg. start,print,game,end ). These are calculted
    left to right top to bottom. Game state will be updated, move will be pushed into
    game history, and the new game state will be retuned.
    
- **get_wins**
    - Path: 'wins'
    - Method: GET
    - Parameters: None
    - Returns: ScoreForms.
    - Description: Returns all wins in the database (unordered).
    
- **get_user_wins**
    - Path: 'win/user/{user_name}'
    - Method: GET
    - Parameters: user_name
    - Returns: ScoreForms. 
    - Description: Returns all Wins recorded by the provided player (unordered).
    Will raise a NotFoundException if the User does not exist.

- **get_user_ranks**
    - Path: 'user/ranks'
    - Method: GET
    - Returns: RankForm
    - Description: Returns list of all top players by rank

- **get_high_scores**
    - Path: 'the-scoreboard'
    - Method: GET
    - Parameters: number_of_results(optional limiter, default=10) 
    - Returns: WinForms
    - Description: Returns 'the scoreboard'. 

##Files Included:
 - api.py: Contains endpoints and invokes our game functions.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.
 - main.py: Handler for taskqueue handler.
 - utils.py: Helper function for retrieving ndb.Models by urlsafe Key string.
 - Levels.py: Levels class contains logical design of single level and game levels.
 - User.py: User entity definitions.
 - Win.py: Win entity definitions.
 - Game.py: Game entity definitions.
 - GameHistory.py: GameHistory entity definitions.
 - Rank.py: Rank class definition.

##Tasks/Crons  (cron.yaml, app.yaml, main.py)
 - **SendReminderEmail(/crons/send_reminder)** 
    - send reminder email every 24 hours for any users who have failed a challenge. This will serve to encourage people to continue. Time limit updated in cron.yaml
 - **pushGameHistory(/tasks/push_game_history)** 
    - invokes the _push_game_history() function to add this move to the task queue. We queue these since generally history is not needed to complete/continue playing.





