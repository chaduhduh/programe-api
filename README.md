#Programe-api

Api built on google app engine for managing programe saved games and scores. <br />
See https://github.com/chaduhduh/ProGrAME for game rules and info on playing the game. <br />
To browse api explorer go to: <a href="http://programe-api.appspot.com/_ah/api/explorer" target="_blank">http://programe-api.appspot.com/_ah/api/explorer</a><br />

Programe is a puzzle game that helps to teach some basic programming logic. Programe-api serves <br />
as an interface to manage games, levels and users.<br />

##Setup Instructions:
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
10. After openining chrome with the previous flag set and navigating to the "/_ah/api/explorer" directory you are ready to begin testing your endpoints!!

##Game Description:
Programe is a an educational puzzle game that is designed to teach some basic programming 
logic. Although intented for beginners some of the puzzles can become quite challenging! 
In the game the user is presented with an available set of pieces and a puzzle board. The object
of the game is to arrange the pieces to that the simulated program will 'compile'. When the user
gets the correct solution they recieve a score and move to the next level! Level objectives are given
for each level and new pieces get added as the game progresses. Players can not skip levels as each
one is helpful for the next level. To win the game player MUST complete ALL levels in the current game. 
Games can contain differing multiples of levels. High scores track the game with the highest score and 
lowest number of attempts. 

##Api Description:
The create_user and create_game endpoints are used to create a new user and a new game. Once a game is initialized
for a valid user the get_level endpoint can be called to get all the details of the current level. This information
will be used to build the UI for the game. Level structure is built it standard JSON so it can be parsed for any platform.
The submit_board enpoint will receive the users solution and will check that against the current levels solution. Response will
indicate the result of the guess and will update the level accordingly. get_all_highscores (aka the scoreboard) is used to 
build a scoreboard of the top ranking players. Typical flow will be: 
create_user -> create_game -> get_level -> submit_board -> get_level -> submit_board -> get_user_rank -> create_game etc.

##Files Included:
 - api.py: Contains endpoints and invokes our game functions.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.
 - main.py: Handler for taskqueue handler.
 - models.py: Entity and message definitions including helper methods.
 - utils.py: Helper function for retrieving ndb.Models by urlsafe Key string.
 - Levels.py: Levels class contains logical design of single level and game levels.

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
    - Parameters: user_name, attempts_remaining, attempts_used, score, current_level
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

- **get_all_games**
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
    - Parameters: number_of_results(optional limiter) 
    - Returns: WinForms
    - Description: Returns 'the scoreboard'. 

##Models:
 - **User**
    - Represents unique User profile
    
 - **Game**
    - Stores single game states. Associated with User model via KeyProperty.

 - **GameHistory**
    - Stores single game move. This is used to generate 'replays' and possibly 
    reverting games. Associated with Game model via KeyProperty.
    
 - **Win**
    - represents a ended game (reached last level). Associated with Users model via KeyProperty.

##Classes:
 - **Level** 
    - Level.py - logical design of single level.
    - Properties: name, pieces, solutions, board_structure, solution_score
    - isSolution() - Accepts a list that represents solution and compares against solution, returns,
    True if success False if failure.
 - **All_Levels** 
    - Level.py - logical design of all game levels. These definitions will propegate to each platform and the ui will be built from this accordingly. Level definitions may eventually move.<br />
    - Properties: levels
    - getLevel() - accepts level_name and returns that level information
    - getLevelByIndex() - accetps and integer index and returns that level of the game
    - getNextLevel() - accepts level_name and returns the next level in the game

##Methods
- **_push_game_history()** 
    - api.py, pushes history for the given user, this is invoked via task and is not invoked directly
- **get_by_urlsafe()** 
    - utils.py, Returns an ndb.Model entity that the urlsafe key points to. Checks that the type of entity returned is of the correct kind.<br />

##Tasks/Crons  (cron.yaml, app.yaml, main.py)
 - **SendReminderEmail(/crons/send_reminder)** 
    - send reminder email every 24 hours for any users who have failed a challenge. This will serve to encourage people to continue. Time limit updated in cron.yaml
 - **pushGameHistory(/tasks/push_game_history)** 
    - invokes the _push_game_history() function to add this move to the task queue. We queue these since generally history is not needed to complete/continue playing.

##Forms Included:
- **GameForm**
    - Representation of a Game's state (urlsafe_key, attempts_remaining,
    attempts_used, game_over flag, message, user_name, current_level, score).
- **GameFormList**
    - List of GameForms
- **GameHistoryForm**
    - Representation of a users history (user_name, date,
    action, score, submission, program_compiled, level).
- **AllHistoryForm**
    - List of GameHistoryForm
- **NewGameForm**
    - Used to create a new game (user_name, attempts_remaning, attempts_used, 
    score, current_level)
- **SubmitBoardForm**
    - Inbound puzzle submission
- **WinForm**
    - Representation of a completed game's results (user_name, date, won flag,
    attempts_used, score).
- **WinForms**
    - List of WinForm
- **LevelForms**
    - Representation of a single level (name, pieces, solutions, board_structure)
- **Rank**
    - Representation of a single user rank (user_name, date, attempts_used, score, 
    rank int)
- **RankForm**
    - List of Rank
- **StringMessage**
    - General purpose String container.





