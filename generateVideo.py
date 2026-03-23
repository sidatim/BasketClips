import requests
import pprint as pp
import time
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nba.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
}
def get_play_videos(events):
    event_videos = []
    retryArr=[]
    url = "https://stats.nba.com/stats/videoeventsasset"
    for event in events:
        if event['videoAvailable']:
            game_id = event['gameId']
            event_id = event['actionNumber']
            params = {
            "GameEventID": event_id,
            "GameID": game_id
            }
            response = requests.get(url, headers=headers, params=params)
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
            'desc':event['description'],
            'player': event['playerNameI'],
            })   
            time.sleep(0.5)
        else:
            continue
        pp.pprint(event_videos)    
    return event_videos, retryArr
   
   