from espn_api.football import League as fb_league
from espn_api.basketball import League as bb_league
#from spontit import SpontitResource
import urllib3
from ssl import SSLError
import requests
from requests.exceptions import Timeout, ConnectionError
from urllib3.exceptions import ReadTimeoutError
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests
import pandas as pd
import os
import csv
import logging
import time
import sys

def getAverage(lst): 
    return sum(lst) / len(lst)

def getStd(lst):
    n = len(lst)
    c = getAverage(lst)
    ss = sum((x-c)**2 for x in lst)
    return (ss/n)**0.5


url = 'https://hashtagbasketball.com/fantasy-basketball-dynasty-rankings'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
html = requests.get(url,verify=False).content
df_list = pd.read_html(html)
df = df_list[-1]



kt_league = bb_league(league_id=79672, year=2021, espn_s2='AEAwMtmo2csfHtJSQ0OszgBeGKp79MilJy3qBU60MI0vC0zRasKoy0%2B83ts9R8TNGCaH3e5v10AInul%2FEUTRSW%2BxRL%2Bx5Widcgnkw0%2FiR0SNc9bLP7txlkQf2A0c9XVJIvMCt7VbCqne7eRYg%2BGfSPTAQXY%2BHpjmvG45ubw6AGgK%2FLp2xEOdIYsK02TeicS8lynRl6WxrJkCQnXdzs0c%2BFLB7%2BbtVmXleIrUcN1fzr1%2BeZ%2F8iqIFVECaaGx5yGPKzjqdgP%2FCCbm1ywEi1ZDJmYIZ', swid='{9404E72D-02B1-41C9-84E7-2D02B191C9FC}')
teams = kt_league.teams
v_teams, v_ages = [], []

for team in teams:
    ages = []
    for player in team.roster:
        player_list = df.loc[df['PLAYER'] == player.name].values.tolist()
        try: player_age = player_list[0][4]
        except: player_age = float(input('What is the age of %s?   ' % player.name))
        ages.append(player_age)
    v_ages.append(getAverage(ages))
    v_teams.append(str(team)[5:][:-1])


y_pos = np.arange(len(v_teams))
plt.barh(y_pos, v_ages, align='center', tick_label=v_teams, color=sns.color_palette("hls", 10))
plt.title('Average Team Age')
plt.xlim(20,32)
plt.show()
