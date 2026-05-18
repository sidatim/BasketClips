
import io
import csv
from nba_api.stats.endpoints import playbyplayv3
import streamlit as st
playerEvents= dict()
if __name__ == "__main__":
    with open("play_by_play.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['playerNameI'] not in playerEvents:
                playerEvents[row['playerNameI']] = []
                playerEvents[row['playerNameI']].append({
            'playerNameI': row['playerNameI'] if row['playerNameI'] else row['playerName'],
            'actionType':    row['actionType'],
        'subType':       row['subType'],
        'description':   row['description'],
        'shotResult':    row['shotResult'],
        'isFieldGoal':   row['isFieldGoal'] == '1',
        'pointsTotal':   int(row['pointsTotal']) if row['pointsTotal'] else 0,  
        'videoAvailable': row['videoAvailable'] == '1',
        'actionNumber': row['actionNumber']
    })
        """print(
            row['teamTricode'],
            row['actionType'],
            row['subType'],
            row['description'],
            row['playerName'],
            row['shotResult'],
            'FieldGoal:', row['isFieldGoal'],
            'Point Total:', row['pointsTotal'],
            'Video Available:', row['videoAvailable']
        )
        if row['videoAvailable'] == '1':
            print('Video is available for this play.')

        print('---')  # Separator for readability
        """

    print(playerEvents.keys())
else:    
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
            'actionNumber':  row['actionNumber']
        })

    playerEvents.pop('', None)
    playerEvents.pop('nan', None)
    return playerEvents        