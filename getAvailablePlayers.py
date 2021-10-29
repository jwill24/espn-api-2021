from espn_api.basketball import League as bb_league
from espn_api.basketball.box_player import BoxPlayer
import sys
import pandas as pd

year = 2021
kt_league = bb_league(league_id=79672, year=year, espn_s2='AEAwMtmo2csfHtJSQ0OszgBeGKp79MilJy3qBU60MI0vC0zRasKoy0%2B83ts9R8TNGCaH3e5v10AInul%2FEUTRSW%2BxRL%2Bx5Widcgnkw0%2FiR0SNc9bLP7txlkQf2A0c9XVJIvMCt7VbCqne7eRYg%2BGfSPTAQXY%2BHpjmvG45ubw6AGgK%2FLp2xEOdIYsK02TeicS8lynRl6WxrJkCQnXdzs0c%2BFLB7%2BbtVmXleIrUcN1fzr1%2BeZ%2F8iqIFVECaaGx5yGPKzjqdgP%2FCCbm1ywEi1ZDJmYIZ', swid='{9404E72D-02B1-41C9-84E7-2D02B191C9FC}')
acceptable_positions = ['PG', 'SG', 'SF', 'PF', 'C']
week = kt_league.current_week
pro_schedule = kt_league._get_pro_schedule(week)
positional_rankings = kt_league._get_positional_ratings(week)

    
def prunePositions(l):
    nl = []
    for p in l:
       if p in acceptable_positions: nl.append(p) 
    return nl

players = kt_league.free_agents(size = 200)

player_list = []
for player in players:
    name = player.name
    position_list = player.eligibleSlots
    positions = prunePositions(position_list)
    p_str = '/'.join([str(elem) for elem in positions])
    team = player.proTeam

    print('Player:', name, 'POS:', p_str)
    print()
    #print('Stats:', BoxPlayer(player, pro_schedule, positional_rankings, week, year))
    sys.exit()
    
    #player_list.append( [name, p_str, team] )

df = pd.DataFrame(player_list, columns = ['Name','Position(s)','Team'])

print(df)

df.to_csv('available_players.csv', index=False)
