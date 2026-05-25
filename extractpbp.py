
import io
import csv
from nba_api.stats.endpoints import playbyplayv3
import streamlit as st
@st.cache_data
def getEventsforGame(event):
        game_id = event['GAME_ID']
        try:
            pbp = playbyplayv3.PlayByPlayV3(game_id=game_id)
            data = pbp.get_data_frames()[0].to_csv(index=False).encode('utf-8')  # Convert DataFrame to CSV string
            ##player data isnt being extracted here only the headers, need to figure out how to extract the player data from the playbyplayv3 endpoint
            return data

        except Exception as e:
            print(f"Error fetching play-by-play data for game {event}: {e}")
            return None
        
def extractEventsfromCSV(csvExport):
    playerEvents = dict()
    if isinstance(csvExport, (bytes, bytearray)):
        reader = csv.DictReader(io.StringIO(csvExport.decode('utf-8')))
    else:
        f = open(csvExport, "r", encoding='utf-8')
        reader = csv.DictReader(f)

    for row in reader:
        if row['playerNameI'] not in playerEvents:
            playerEvents[row['playerNameI']] = []
        playerEvents[row['playerNameI']].append({
            'gameId':        row['gameId'],
            'teamId':        row['teamId'],
            'teamTricode':   row['teamTricode'],
            'playerNameI':   row['playerNameI'] if row['playerNameI'] else row['playerName'],
            'actionType':    row['actionType'],
            'subType':       row['subType'],
            'description':   row['description'],
            'shotResult':    row['shotResult'],
            'isFieldGoal':   row['isFieldGoal'] == '1',
            'pointsTotal':   int(row['pointsTotal']) if row['pointsTotal'] else 0,
            'videoAvailable': row['videoAvailable'] == '1',
            'actionNumber':  row['actionNumber'],
            'clock':          row['clock'],
            'period':  row['period']
        })

    playerEvents.pop('', None)
    playerEvents.pop('nan', None)
    return playerEvents        

def getTeamEvents(playerEvents, team):
    teamEvents=[]
    for event in playerEvents:
        try:
            if playerEvents[event][0]['teamTricode'] == team:
                teamEvents.append(playerEvents[event])
        except Exception as e:
            print(f"Error processing event for player {event}: {e}")
            continue

    return teamEvents