from espn_api.football import League as fb_league
from espn_api.basketball import League as bb_league
from spontit import SpontitResource
from ssl import SSLError
from requests.exceptions import Timeout, ConnectionError
from urllib3.exceptions import ReadTimeoutError
import logging
import time
import sys

n_players = 100
starttime = time.time()
resource = SpontitResource('jwill24', 'QC1I1NE14I2XHBW55Q04OEHCTDR5RELMHAFZUKT4OCBHJ25VZ2WV0OZUDJL6LGKVVHI2YV3E84P3CCVJEMCNMC4ZOSC2QO38UISK')
goat_league = fb_league(league_id=90359061, year=2020, espn_s2='AEBV%2BW%2F%2F1DGOy1iiBpocpFpegxEcV4ZhLWoeTzr%2BNQ8pCwar1AqPMqmI8u%2FA%2BIv0ii7WFXRM1e%2FTU3B6YNbn1sgisIdAOIMzpW2PFGFHJpQfBor%2BL5xdqw78xQZhbbxMZDonn4xo0xW%2BbqLwOEv0dc%2BHjWz8NNBfST6f0z9%2BT13LXh77Sln5cs\
dofCEPm2n2LoXe2cUOXLB6rW4rB4N4czYFWgH70TDFMUIT1dDZ%2FMrCrwXE%2BJ9ej5NaAoz9XoJC6B3SPbQaksTpq4KeaVQz6eeH', swid='{9404E72D-02B1-41C9-84E7-2D02B191C9FC}' )
kt_league = bb_league(league_id=79672, year=2021, espn_s2='AEAwMtmo2csfHtJSQ0OszgBeGKp79MilJy3qBU60MI0vC0zRasKoy0%2B83ts9R8TNGCaH3e5v10AInul%2FEUTRSW%2BxRL%2Bx5Widcgnkw0%2FiR0SNc9bLP7txlkQf2A0c9XVJIvMCt7VbCqne7eRYg%2BGfSPTAQXY%2BHpjmvG45ubw6AGgK%2FLp2xEOdIYsK02TeicS8lynRl6WxrJkCQnXdzs0c%2BFLB7%2BbtVmXleIrUcN1fzr1%2BeZ%2F8iqIFVECaaGx5yGPKzjqdgP%2FCCbm1ywEi1ZDJmYIZ', swid='{9404E72D-02B1-41C9-84E7-2D02B191C9FC}')


#-------------------------

def sendMessage(activity):

    a = activity.split(',')
    addition = True if len(a) > 3 else False

    team = a[0][a[0].find('Team(')+5:a[0].find(')')]
    if addition:
        if 'ADDED' in a[1]: n_a, n_d = 2, 4
        elif 'ADDED' in a[3]: n_a, n_d = 4, 2
        else:
            resource.push('TRADE ALERT!')
            return
        add = a[n_a][:a[n_a].find(')')]
        drop = a[n_d][:a[n_d].find(')')]
        activity_string = team + ' added ' + add + ' and dropped ' + drop
    else:
        drop = a[2][:a[2].find(')')]
        activity_string = team + ' dropped ' + drop
        
    resource.push(activity_string)
    

#-------------------------

def sendDailyReport(player_list):
    updated_players = kt_league.free_agents(size = n_players)
    names = []
    info = []
    
    for up in updated_players: names.append(up.name) # make a list of player names
    
    for player in player_list:
        try: ind = names.index(player[0]) # get the index of the player
        except: continue
        
        try: player_total = updated_players[ind].stats['002021']['total'] # get the players updated total stats
        except: player_total = {'PTS': 0.0, 'BLK': 0.0, 'STL': 0.0, 'AST': 0.0, 'REB': 0.0, 'PF': 0.0, 'TO': 0.0, 'FGM': 0.0, 'FGA': 0.0, 'FTM': 0.0, 'FTA': 0.0, 'GP': 0.0} # if they haven't played, set stats to 0

        print('Player name:', player[0], 'Old GP:', player[1]['GP'], 'New GP:', player_total['GP'])
        
        if player_total['GP'] > player[1]['GP']: # check if the player played a game today
            fanPoints = calculateFantasyPoints(player[1], player_total)
            print('--> fantasy points:', fanPoints)
            if fanPoints >= 15: info.append([player[0], fanPoints]) # if fanPoints are above the threshold, add the player to the report

    information = '----- Daily FA Update -----\n\n'
    for item in info: information += '%s had %i fantasy points\n' % (item[0], item[1])

    resource.push(information) # push the notification
    #print(information)
    print('\nDaily report sent!\n')
    pl = buildPlayerList() 
    return pl # return the updated player list for tomorrow

#-------------------------

def calculateFantasyPoints(stats_old, stats_new):
    p = stats_new['PTS'] - stats_old['PTS'] 
    r = stats_new['REB'] - stats_old['REB'] 
    b = stats_new['BLK'] - stats_old['BLK'] 
    s = stats_new['STL'] - stats_old['STL'] 
    a = stats_new['AST'] - stats_old['AST'] 
    t = stats_new['TO'] - stats_old['TO'] 
    fgm = stats_new['FGM'] - stats_old['FGM'] 
    fga = stats_new['FGA'] - stats_old['FGA'] 
    ftm = stats_new['FTM'] - stats_old['FTM'] 
    fta = stats_new['FTA'] - stats_old['FTA'] 
    bonus = 0
    if p >= 10 and r >= 10: bonus = 3
    if p >= 10 and a >= 10: bonus = 3
    if p>= 10 and (a >= 10 and r >= 10): bonus = 5
    fanPoints = p + r + b + s + a - t + fgm - fga + ftm - fta + bonus
    return fanPoints

#-------------------------

def buildPlayerList():
    player_list = []
    players = kt_league.free_agents(size = n_players) # Get the top 100 Free Agents

    for player in players:
        name = player.name
        try: stats_total = player.stats['002021']['total'] # Get the player's total stats from 2021
        except: stats_total = {'PTS': 0.0, 'BLK': 0.0, 'STL': 0.0, 'AST': 0.0, 'REB': 0.0, 'PF': 0.0, 'TO': 0.0, 'FGM': 0.0, 'FGA': 0.0, 'FTM': 0.0, 'FTA': 0.0, 'GP': 0.0} # if they haven't played, set stats to 0
        player_list.append([name, stats_total]) 
    return player_list

#-------------------------



tmp_goat_act = goat_league.recent_activity()[0]
tmp_kt_act = kt_league.recent_activity()[0] 
player_list = buildPlayerList() # Get the Free Agent stats

    
while True:
    try: # Get the recent activity in the leagues
        activity_goat = goat_league.recent_activity()
        activity_kt = kt_league.recent_activity() 
    except (Timeout, SSLError, ReadTimeoutError, ConnectionError) as e:
        print("Network error occurred. Keep calm and carry on.")
    except Exception as e:
        print("Unexpected error!")
    finally:
        logging.info("Stream has crashed. System will restart twitter stream!")

    # Check GOAT League
    if str(tmp_goat_act) != str(activity_goat[0]):
        print('Alert!')
        sendMessage(str(activity_goat[0]))
        tmp_goat_act = activity_goat[0]

    # Check KT League
    if str(tmp_kt_act) != str(activity_kt[0]):
        print()
        print('Alert!')
        print()
        sendMessage(str(activity_kt[0]))
        tmp_kt_act = activity_kt[0]


    lt = time.localtime()
    #print()
    #print(lt.tm_hour,lt.tm_min,lt.tm_sec)
    if (lt.tm_hour == 5 and lt.tm_min == 00) and (lt.tm_sec >= 0 and lt.tm_sec <= 15): # if the time is 5:00 am
        player_list = sendDailyReport(player_list) # send the daily report

    # Get the duration of time the code has been running and print it
    duration = time.time()-starttime
    if duration <= 60: denom, unit = 1.0, 'seconds'
    elif duration > 60 and duration <= 3600: denom, unit = 60.0, 'minutes '
    elif duration > 3600: denom, unit = 3600, 'hours   '
    str_time = round(duration/float(denom),0)
    sys.stdout.write("\rTime running: {} {}".format(str_time, unit))
    sys.stdout.flush()
    time.sleep(15.0 - ((time.time() - starttime) % 15.0)) # check every 15 seconds

    
