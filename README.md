# analysis_nba: STAT 405 Final

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is a fast, condensed program to query NBA box score data, advanced box score data, and game reprots such as individual game summaries and officals' data.
A single year takes roughly 6-8 hours to fully process.

For the year entered, three csv formmated files are filled:
- box_score_plus: Per game data on each player for every game in the season
- game_summaries: Game-by-game summary data on the teams that played, the broadcasting network, the game time, the game date, and the attendence
- total_officials: The names of the officials that refereed

box_score_plus is formatted as follows: 

<table>
<tr><th>Basic Info</th><th>Box Score</th><th>Adv. Box Score</th><th>Misc. Box Score</th></tr>
<tr><td>

|Header|
|--|
|'GAME_ID'|
|'TEAM_ID'|
|'TEAM_ABBREVIATION'|
|'TEAM_CITY'|
|'PLAYER_ID'|
|'PLAYER_NAME'|
|'START_POSITION'|
|'COMMENT'|

</td><td>

|Header|Definition|
|--|--|
|'MIN'|Minutes per game|
|'FGM'|Field Goals made|
|'FGA'|Field Goals attempted|
|'FG_PCT'|Field Goal %|
|'FG3A'|3 point attempts|
|'FG3M'|3 point makes|
|'FG3_PCT'|3 point %|
|'FTM'|Free Throws made|
|'FTA'|Free Throws attempted|
|'FT_PCT'|Free Throw %|
|'DREB'|Defensive Rebounds|
|'OREB'|Offensive Rebounds|
|'REB'|Rebounds|
|'AST'|Assists|
|'STL'|Steals|
|'BLK'|Blocks|
|'TO'|Turnovers|
|'PF'|Personal Fouls|
|'PTS'|Points|
|'PLUS_MINUS'||

</td><td>

|Header|Definition| 
|--|--|
|'OPP_OREB_PCT'|Opponent's Offensive Rebound %|
|'OPP_TOV_PCT'|Opponent's Turnover %|
|'OREB_PCT'|Player's Offensive Rebound %|
|'TM_TOV_PCT'|Team Turnover %|
|'BLKA'|Player's # Block Attempts|
|'OPP_PTS_2ND_CHANCE'|Opponent's 2nd chance points scored|

</td><td>

|Header|Definition| 
|--|--|
|'OPP_PTS_FB'|Opponent Fast Break Points|
|'OPP_PTS_OFF_TOV'|Opponent Points Off Turnovers|
|'OPP_PTS_PAINT'|Opponent Points in the Paint|
|'PFD'|Player's Personal fouls drawn|
|'PTS_2ND_CHANCE'|Player's 2nd chance points scored|
|'PTS_FB'|Player's Fast Break Points|
|'PTS_OFF_TOV'|Player's Points Off Turnovers|
|'PTS_PAINT'|Player's Points in the Paint|
	
</td></tr> </table>

game_summaries and total_officials are formatted as follows:

<table>
<tr><th>Officals</th><th>Game Summaries/th></tr>
<tr><td>

|Header|
|--|
|'GAMECODE'|
|'GAME_ID'|
|'GAME_DATE'|
|'OFFICIAL_ID'|
|'FIRST_NAME'|
|'LAST_NAME'|
|'JERSEY_NUM'|

</td><td>

|Header|
|--|
|'GAME_DATE_EST'|
|'GAME_ID'|
|'GAME_STATUS_ID'|
|'GAMECODE'|
|'HOME_TEAM_ID'|
|'VISITOR_TEAM_ID'|
|'SEASON'|
|'LIVE_PERIOD'|
|'NATL_TV_BROADCASTER_ABBREVIATION'|
|'LIVE_PERIOD_TIME_BCAST'|
|'WH_STATUS'|
|'GAME_DATE'|
|'ATTENDANCE'|

</td></tr> </table>
	
## Technologies
Project is created with:
* Python 3.6, R
* py_ball: For NBA API Calls
* matplotlib: Dependency for the py_ball package
* pandas: For dataframe formatting
* requests_cache: For API calls, SQLite storing
* dyplr: For dataframe concatenation and processing
	
## Setup
The following instructions are for Mac OS.

Follow the instructions and run the commands in Terminal:

Step 0: cd into a folder that you want to store the code/files generated
```
$ cd /Users/{Insert username}/Documents/{Whatever path you want to use}
```
Step 0: Clone the repository
```
$ git clone https://github.com/awx1/analysis_nba.git
```

Step 1: Install pip
```
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python get-pip.py
```

Step 0: Install virtualenv
```
$ python3 -m pip install --user virtualenv
$ pip3 install virtualenv
```

Step 3: Access virtual env
```
$ python3 -m venv nba
$ source env/bin/activate
```

Step 4: Install packages
```
$ pip3 install cairosvg==2.2.1
$ pip3 install matplotlib==3.2.1
$ pip3 install pkginfo==1.5.0.1
$ pip3 install requests==2.20.0
$ pip3 install py_ball
$ pip3 install matplotlib
$ pip3 install pandas
$ pip3 install requests_cache
```

Step 5: Install homebrew
```
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

Step 6: Install cairo
```
$ brew install cairo
```
 
Step 7: Place this line of code at the bottom of final_copy.py (Specify the YEAR)
```
### Change the year here
get_year_boxscores({YEAR_HERE})
```

Step 9: Run the program using the command
```
python3 final_copy.py
```

Step 10: To concatenate the csv's using the R script, change the path to the correct path to run
