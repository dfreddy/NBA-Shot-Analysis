import numpy as np
import pandas as pd
import pickle
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import string
import requests

team_names = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM',
              'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
teams = []


# ITERATE URL THRU TEAM NAMES
def scrape_team(team_name, year):
    url = 'https://www.basketball-reference.com/teams/' + team_name + '/' + str(year) + '.html'
    print('Scraping ' + team_name + str(year))

    req = Request(url)
    res = urlopen(req)
    rawpage = res.read().decode("utf-8")
    page = rawpage.replace('<!--', '')
    page = page.replace('-->', '')
    soup = BeautifulSoup(page, 'html.parser')

    # find total shots by player
    totals = soup.find('table', {'id': 'totals'})
    totals_rows = totals.find('tbody').findAll('tr')
    team_attempts = totals.find('tfoot').findAll('tr')[0].find('td', {'data-stat': 'fga'}).text
    team_attempts = int(team_attempts)

    player_shots = []

    for i in range(len(totals_rows)):
        cell = totals_rows[i].find('td', {'data-stat': 'fga'})
        player_shots.append(int(cell.text))

    # find team distances
    shooting_table = soup.find('table', {'id': 'shooting'})
    shooting_rows = shooting_table.find('tbody').findAll('tr')

    team_dist = 0
    paint = 0
    midrange = 0
    threes = 0
    players_w_shots = 0
    for i in range(len(shooting_rows)):
        # avg distances
        cells = shooting_rows[i].findAll('td')

        # check if player has attempted shots
        if not cells[5].text == '':
            players_w_shots = players_w_shots + 1
            team_dist = team_dist + player_shots[i] * (float(cells[5].text))
            paint = paint + float(cells[7].text) + float(cells[8].text)
            midrange = midrange + float(cells[9].text) + float(cells[10].text)
            threes = threes + float(cells[11].text)

    avg_team_dist = team_dist / team_attempts
    paint = paint / players_w_shots
    midrange = midrange / players_w_shots
    threes = threes / players_w_shots

    # find team wins
    misc_table = soup.find('table', {'id': 'team_misc'})
    misc_rows = misc_table.find('tbody').findAll('tr')
    wins = int(misc_rows[0].findAll('td')[0].text)

    # save team data to array
    team_entry = {'name': team_name + str(year), 'avg_dist': avg_team_dist,
                  'paint_pct': paint, 'midrange_pct': midrange, 'threes_pct': threes, 'wins': wins}
    teams.append(team_entry)


# scraping team data
year = 2018
for i in range(len(team_names)):
    scrape_team(team_names[i], year)

year = year - 1
for i in range(len(team_names)):
    scrape_team(team_names[i], year)

year = year - 1
for i in range(len(team_names)):
    scrape_team(team_names[i], year)

year = year - 1
for i in range(len(team_names)):
    scrape_team(team_names[i], year)

# saving data in csv file
print('Saving data to csv file')
with open('teams.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['team', 'avg distance', 'paint', 'midrange', 'threes', 'wins'])
    for i in range(len(teams)):
        csv_writer.writerow([teams[i].get('name'), teams[i].get('avg_dist'),
                             teams[i].get('paint_pct'), teams[i].get('midrange_pct'),
                             teams[i].get('threes_pct'), teams[i].get('wins')])

# writing to txt (testing)
# f = open('teams.txt', 'w+')
# f.write('Team name: ' + teams[0].get('name') + '\nAverage shooting distance: ' + str(
#     teams[0].get('avg_dist')) + '\nWins: ' + str(teams[0].get('wins')) + '\n\n')
# f.write('Team name: ' + teams[1].get('name') + '\nAverage shooting distance: ' + str(
#     teams[1].get('avg_dist')) + '\nWins: ' + str(teams[1].get('wins')) + '\n\n')
# f.close()
