import pprint as p
import json
from nba_api.stats.static import teams
nba_teams = teams.get_teams()
with open("teams.json", "w") as f:
    try:
        json.dump(nba_teams, f, indent=4)
    except IOError as e:
        print(f"Error writing to file: {e}")
    
    f.close()


