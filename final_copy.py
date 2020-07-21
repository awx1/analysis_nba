from py_ball import league, image, boxscore
import matplotlib.pyplot as plt
import time
import pandas as pd
import sys
import requests_cache

HEADERS = {'Host': 'stats.nba.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
           'Accept': 'application/json, text/plain, */*',
           'Accept-Language': 'en-US,en;q=0.5',
           'Accept-Encoding': 'gzip, deflate, br',
           'x-nba-stats-origin': 'stats',
           'x-nba-stats-token': 'true',
           'Connection': 'keep-alive',
           'Referer': 'https://stats.nba.com/',
           'Pragma': 'no-cache',
           'Cache-Control': 'no-cache'}

def pad_id(num):
    """ pad_id adds the requisite number of leading
    zeroes to a game number to form a valid game_id

    @param num (int): Regular season game number

    Returns:

        num_str (str): Regular season game number
        with leading zeroes
    """
    
    num_str = str(num)
    while len(num_str) < 4:
        num_str = '0' + num_str
        
    return num_str

def get_year_boxscores(year):
    """ get_year_boxscores pulls data from the
    boxscores endpoint of the stats.nba.com API

    @param year (int): year corresponding to the year
    in which the season began. For example, the 2017-2018
    NBA season is represented as the year 2017.

    Returns:

        Saves two .csv files of the player and team boxscore data to the
        current working directory with a name formatted
        as player_boxscores_[year].csv and team_boxscores_[year].csv
    """
    requests_cache.install_cache('nba_cache_' +str(year))
        
    year_sub = str(year)[-2:]

    base = '002' + year_sub + '0'

    box_score_plus = pd.DataFrame({})
    game_summaries = pd.DataFrame({})
    total_officals = pd.DataFrame({})
    
    if year == 2019:
        num_games = 706
    elif year > 2011:
        num_games = 41 * 30
    elif year == 2011:
        num_games = 990
    elif year > 2003:
        num_games = 41 * 30
    elif year > 1998:
        num_games = 41 * 29
    elif year == 1998:
        num_games = 25 * 29
    elif year > 1994:
        num_games = 41 * 29
    elif year > 1989:
        num_games = 41 * 27
    elif year > 1987:
        num_games = 41 * 25
    else:
        num_games = 41 * 23
        
    for x in range(1, num_games + 1):
        print(str(year) + ': Game #' + str(x))
        game_id_here = base + pad_id(x)

        t0 = time.time()

        success = 0
        counter = 0
        while ((not success) and (counter < 10)):
            try:
                trad = boxscore.BoxScore(headers=HEADERS, game_id=game_id_here, endpoint='boxscoretraditionalv2')
                time.sleep(2)
                
                if (year > 1995):
                    ff = boxscore.BoxScore(headers=HEADERS, game_id=game_id_here, endpoint='boxscorefourfactorsv2')
                    time.sleep(2)

                    misc = boxscore.BoxScore(headers=HEADERS, game_id=game_id_here, endpoint='boxscoremiscv2')
                    time.sleep(2)

                summary = boxscore.BoxScore(headers=HEADERS, game_id=game_id_here, endpoint='boxscoresummaryv2')
                success = 1
            except:
                print("Trying again")
                time.sleep(2)
                success = 0
                counter += 1
        if counter == 10:
            continue
        
        box_score_headers = [
            'GAME_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_CITY',
            'PLAYER_ID', 'PLAYER_NAME', 'START_POSITION', 'COMMENT',
            'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3A', 'FG3M', 'FG3_PCT',
            'FTA', 'FTM', 'FT_PCT',  'DREB', 'OREB', 'REB',
            'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS'
            ]
        player_box = pd.DataFrame(trad.data['PlayerStats'])
        player_box = player_box[box_score_headers]
        new_player_box = player_box.sort_values(['TEAM_CITY','PLAYER_ID'])

        if (year > 1995):
            ff_headers = [
                'EFG_PCT', 'FTA_RATE', 'OPP_EFG_PCT', 'OPP_FTA_RATE', 
                'OPP_OREB_PCT', 'OPP_TOV_PCT', 'OREB_PCT', 'TM_TOV_PCT']
            new_ff = pd.DataFrame(ff.data['sqlPlayersFourFactors']).sort_values(['TEAM_CITY','PLAYER_ID'])[ff_headers]

            misc_headers = ['BLKA', 'OPP_PTS_2ND_CHANCE',
                   'OPP_PTS_FB', 'OPP_PTS_OFF_TOV', 'OPP_PTS_PAINT', 'PFD',
                   'PTS_2ND_CHANCE', 'PTS_FB', 'PTS_OFF_TOV',
                   'PTS_PAINT']
            new_misc = pd.DataFrame(misc.data['sqlPlayersMisc']).sort_values(['TEAM_CITY','PLAYER_ID'])[misc_headers]

            new_box = pd.concat([new_player_box, new_ff, new_misc], axis=1)
        else:
            new_box = new_player_box
        
        game_summary = pd.DataFrame(summary.data['GameSummary'])
        game_info = pd.DataFrame(summary.data['GameInfo'])

        new_summary = pd.concat([game_summary, 
                                 game_info],
                                axis=1)

        new_summary['HOME_TEAM_ID'] = new_summary['HOME_TEAM_ID'].apply(str)
        new_summary['VISITOR_TEAM_ID'] = new_summary['VISITOR_TEAM_ID'].apply(str)
        
        officals = pd.DataFrame(summary.data['Officials'])
        officals['GAMECODE'] = pd.DataFrame(game_summary)['GAMECODE'][0]
        officals['GAME_ID'] = pd.DataFrame(game_summary)['GAME_ID'][0]
        officals['GAME_DATE'] = pd.DataFrame(game_info)['GAME_DATE'][0]
        
        delay = time.time() - t0
        print('Waiting ' + str(10*delay) + 's')
        time.sleep(delay)

        box_score_plus = pd.concat([box_score_plus, new_box], axis=0).reset_index(drop=True)
        game_summaries = pd.concat([game_summaries, new_summary], axis=0).reset_index(drop=True)
        total_officals = pd.concat([total_officals, officals], axis=0).reset_index(drop=True)

    box_score_plus.to_csv('box_score_plus_'+str(year)+'.csv', index=False)
    game_summaries.to_csv('game_summaries_'+str(year)+'.csv', index=False)
    total_officals.to_csv('total_officals_'+str(year)+'.csv', index=False)