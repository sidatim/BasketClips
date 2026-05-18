from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.endpoints import leaguegamefinder


gamefinder = leaguegamefinder.LeagueGameFinder()
games = gamefinder.get_data_frames()[0]
seasons = games['SEASON_ID'].unique().tolist()
SEASON_TYPES = {
    "1": "regular_season",
    "2": "preseason",
    "3": "playoffs",
    "4": "finals",
    "5": "play_in",
    "6": "other"
}
dict = {
    "2025": {},
    "2024": {},
    "2023": {},
    "2022": {},
    "2021": {},
    "2020": {},
    "2019": {},
    "2018": {},
    "2017": {},
    "2016": {},
    "2015": {},
}
for season in seasons:
    season_year = season[1:5] 
    if season[0]=="1":
        dict[season_year].update({SEASON_TYPES[season[0]]: season})
    elif season[0]=="2":
        dict[season_year].update({SEASON_TYPES[season[0]]: season})
    elif season[0]=="3":
        dict[season_year].update({SEASON_TYPES[season[0]]: season})
    elif season[0]=="4":
        dict[season_year].update({SEASON_TYPES[season[0]]: season})
    elif season[0]=="5":
        dict[season_year].update({SEASON_TYPES[season[0]]: season})
    elif season[0]=="6":
        dict[season_year].update({SEASON_TYPES[season[0]]: season})

        

"""
with open('seasons.json', 'w') as f:
    json.dump(dict, f, indent=4)
"""


