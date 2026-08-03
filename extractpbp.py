
import io
import csv
import re
from nba_api.stats.endpoints import playbyplayv3
import streamlit as st
def validate_csv(csv_file):
    gameIDRegex=r"^\d{10}$"
    requiredColumns=['gameId', 'actionNumber', 'clock', 'period', 'teamId', 'teamTricode', 'personId', 'playerName', 'playerNameI', 'xLegacy', 'yLegacy', 'shotDistance', 'shotResult', 'isFieldGoal', 'scoreHome', 'scoreAway', 'pointsTotal', 'location', 'description', 'actionType', 'subType', 'videoAvailable', 'actionId']
    try:
        reader=None
        fields=None
        if isinstance(csv_file, (bytes, bytearray)):
            reader=csv.DictReader(io.StringIO(csv_file.decode('utf-8')))
            fields=reader.fieldnames
        else:
            reader=csv.DictReader(open(csv_file, "r", encoding='utf-8'))
            fields=reader.fieldnames
        if not reader:
            raise ValueError("CSV file is empty or invalid.")
        missing_columns = [col for col in requiredColumns if col not in fields]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        row=next(reader,None)
        if not re.match(gameIDRegex, row['gameId']):
            raise ValueError(f"Invalid gameId format: {row['gameId']}")
    except Exception as e:
        st.error(f"Invalid CSV file: {e}")
        st.stop()
        return

@st.cache_data(show_spinner=False)
def getEventsforGame(event):
        game_id = event['GAME_ID']
        pbp = playbyplayv3.PlayByPlayV3(game_id=game_id, timeout=10)
        data = pbp.get_data_frames()[0].to_csv(index=False).encode('utf-8')  
        return data
        
@st.cache_data(show_spinner=False)     
def extractEventsfromCSV(csvExport):
    playerEvents = dict()
    validate_csv(csvExport)
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
            'playerNameI':   row['playerNameI'],
            'playerName':   row['playerName'],
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
@st.cache_data(show_spinner=False)
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