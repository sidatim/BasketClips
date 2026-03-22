
import csv
from nba_api.stats.endpoints import playbyplayv3
from pprint import pprint

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
    pprint(playerEvents['L. James'])

    print(playerEvents.keys())
else:    
    def extractEventsfromCSV(csv_file):
        playerEvents = dict()
        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['playerNameI'] not in playerEvents:
                    playerEvents[row['playerNameI']] = []
                playerEvents[row['playerNameI']].append({
                    'gameId': row['gameId'],
                    'teamId': row['teamId'],
                    'teamTricode': row['teamTricode'],
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
        playerEvents.pop('')
        return playerEvents