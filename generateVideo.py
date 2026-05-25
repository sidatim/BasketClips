import requests
import time
from datetime import datetime
import re
eventPriority={
    "Made Shot": 4,
    "Missed Shot": 4,
    "Rebound": 3,
    "Steal": 3,
    "Turnover": 2,
    "Free Throw": 1,
}
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nba.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
}
def get_play_videos(events):
    print("Fetching video URLs for events...")
    event_videos = []
    retryArr=[]
    print(f"Total events to process: {len(events)}")
    url = "https://stats.nba.com/stats/videoeventsasset"
    for event in events:
        if event['videoAvailable']:
            game_id = event['gameId']
            event_id = event['actionNumber']
            player_name = event['playerNameI']
            description = event['description']
            timestamp = event['clock']
            action=event['actionType']
            period=event['period']
            params = {
            "GameEventID": event_id,
            "GameID": game_id
            }
            
            try:
                response = requests.get(url, headers=headers, params=params)
                print(f"Requesting video for GameID: {game_id}, EventID: {event_id} - Status Code: {response.status_code}")
                if response.status_code == 500:
                    print(f"Server error for GameID: {game_id}, EventID: {event_id}. Skipping.")
                    retryArr.append((game_id, event_id))
                    continue
                data = response.json()
                video_url = data["resultSets"]["Meta"]["videoUrls"][0]["lurl"]
                event_videos.append({
                'gameId': game_id,
                'eventId': event_id,
                'videoUrl': video_url,
                'desc': description,
                'player': player_name,
                'timestamp': timestamp,
                'action': action,
                'period': period,
                'priority': eventPriority[action] if action else 0
                })   
                time.sleep(0.5)
            except Exception as e:
                print(f"Error fetching video for GameID: {game_id}, EventID: {event_id} - {e}")
                retryArr.append((game_id, event_id))
                continue
        else:
            print(f"No video available for GameID: {event['gameId']}, EventID: {event['actionNumber']}. Skipping.")
            continue

    filteredEvents=filterDuplicateClips(event_videos)
    return filteredEvents, retryArr




def convertTimeStamp(duration):
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:([\d.]+)S)?', duration)
    h, m, s = (float(x or 0) for x in match.groups())
    return h * 3600 + m * 60 + s

def filterDuplicateClips(events):
    time_window = 5
    filtered_events = []

    for event in events:
        currentTime = convertTimeStamp(event['timestamp'])
        currentPeriod = event['period']
        currentAction = event['action']
        currentPriority = event['priority']

        if filtered_events:
            lastEvent = filtered_events[-1]
            lastSeenTime = convertTimeStamp(lastEvent['timestamp'])
            lastSeenPeriod = lastEvent['period']
            lastAction = lastEvent['action']
            lastPriority = lastEvent['priority']
            is_duplicate = (
                currentPeriod == lastSeenPeriod and abs(lastSeenTime - currentTime) < time_window and currentAction != 'Free Throw'and lastAction != 'Free Throw'
            )
            if is_duplicate:
                if currentPriority > lastPriority:
                    filtered_events[-1] = event  
                continue
        filtered_events.append(event)

    return filtered_events


# def download_video(video_url):
#     output_path = video_url.split("/")[-1]  # Extract filename from URL
    
#     try:
#         response = requests.get(video_url, headers=headers, stream=True)
#         response.raise_for_status()
#         with open(output_path, 'wb') as f:
#             for chunk in response.iter_content(chunk_size=8192):
#                 f.write(chunk)
#         print(f"Downloaded video to {output_path}")
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to download video: {e}")