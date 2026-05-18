# 🏀 BasketClips
BasketClips is a Streamlit app for extracting and previewing NBA player event clips from official NBA play-by-play data.

## Features
- Upload an NBA play-by-play CSV file (stats.nba.com format).
- Search by team matchup using NBA API data.
- Select a player and filter by event type.
- Generate clips for the selected player events.
- Preview clip videos directly in the app.
- Optional experimental FFmpeg export for combined video playback.

## Requirements
- Python 3.10+ recommended
- Streamlit
- `requirements.txt` contains the project dependencies

## Installation
1. Clone the repository:
   ```powershell
   git clone <repo-url>
   cd BasketClips
   ```
2. Activate the virtual environment:
   ```powershell
   .\env\Scripts\Activate.ps1
   ```
3. Install the dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Run the app
```powershell
streamlit run app.py
```

## How to use
1. Open the app in your browser after Streamlit starts.
2. Choose between:
   - `Team Matchup` to search NBA matchups using the built-in NBA API integration.
   - `Upload CSV` to provide your own NBA play-by-play CSV file.
3. Select a player from the extracted events list.
4. Apply event filters such as shot made, shot missed, foul, steal, turnover, assist, free throw, or rebound.
5. Generate clips and preview videos directly in the app.
6. If enabled, the experimental FFmpeg export option will attempt to export combined videos.

## Notes
- The CSV uploader currently supports play-by-play data in the stats.nba.com format.
- The FFmpeg export feature is experimental and may not work for every video or event.
- The repository includes a sample `play_by_play.csv` for testing.

## Files of interest
- `app.py` — Streamlit app entry point
- `extractpbp.py` — Parse and extract events from play-by-play data
- `filterEvents.py` — Filter extracted events
- `generateVideo.py` — Retrieve video clips for events
- `exportVideo.py` — Export videos with FFmpeg
- `loadTeams.py` — Load NBA team and season metadata

## License
This project is provided as-is. Modify and extend it for your own NBA clip generation workflows.
