import streamlit as st
from nba_api.stats.endpoints import leaguegamefinder
from extractpbp import extractEventsfromCSV, getEventsforGame
from filterEvents import filterSelected
from generateVideo import get_play_videos
from loadTeams import load_teams, load_seasons
from exportVideo import export_video
import pandas as pd

st.title("NBA Play-by-Play Clips")
st.markdown("""
    <h1 style="font-size: 22px;">This app analyzes NBA play-by-play data to extract player events and statistics.</h1>
    <p class="intro-text">Upload a CSV file containing play-by-play data to get started. (supports only data from stats.nba.com)</p>
    <p class="intro-text">Or choose 2 teams to get a matchup for them</p>
""", unsafe_allow_html=True)

generateFile=None
filteredEvents=None
submit_button=None
player=None
seasonSelectStart=None
seasonSelectEnd=None
teams=load_teams()
seasons=load_seasons()
videoEvents=None

gameKeys=["Regular Season", "Preseason", "Playoffs", "Finals", "Play In", "Other"]
season_options = list(([season['seasonYear'] for season in seasons]))
options = ["Team Matchup", "Upload CSV"]
choice = st.selectbox("Select an option", options, index=None)
if choice == "Team Matchup":
    st.markdown("<h2 style='font-size: 18px;'>Select Teams for Matchup</h2>", unsafe_allow_html=True)
    team1 = st.selectbox("Select Team 1", options=[team['teamName'] for team in teams], index=None)
    team2 = st.selectbox("Select Team 2", options=[team['teamName'] for team in teams if team['teamName'] != team1], index=None)
    ffmpegCheck=st.checkbox("Export videos with ffmpeg (experimental)", key="ffmpeg_checkbox")
    if st.checkbox("Additional Filters"):
        seasonSelectStart=st.selectbox("Select Season", options=season_options, index=0)
    if st.button("Find Matchups"):
        if not team1 or not team2:
            st.warning("Please select both teams to find matchups.")
            st.stop()
        team1_id = next(team['teamId'] for team in teams if team['teamName'] == team1)
        team2_id = next(team['teamId'] for team in teams if team['teamName'] == team2)
        gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team1_id, vs_team_id_nullable=team2_id, season_nullable=seasonSelectStart if seasonSelectStart else None)
        games = gamefinder.get_data_frames()[0]
        df = pd.DataFrame(games)
        st.session_state['matchup_df'] = games
        st.session_state['matchup_label'] = f"{team1} vs {team2}"
        
    if 'matchup_df' in st.session_state:
        st.subheader(f"Matchups for {st.session_state['matchup_label']}")

        selected_game=st.dataframe(st.session_state['matchup_df'][['GAME_DATE', 'MATCHUP', 'WL', 'PTS', 'REB', 'AST']], on_select="rerun", selection_mode="single-row")
        if selected_game.selection.rows:
            selected_df=st.session_state['matchup_df'].iloc[selected_game.selection.rows[0]]
            generateFile=getEventsforGame(selected_df)
if generateFile:
    playerEvents=extractEventsfromCSV(generateFile)
    player=st.selectbox("Select a player to view their events", options=playerEvents.keys(), placeholder="Select a player", format_func=lambda name: f"{name} - {playerEvents[name][0]['teamTricode']}" if playerEvents[name] else name)

if choice == "Upload CSV":
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        ffmpegCheck=st.checkbox("Export videos with ffmpeg (experimental)", key="ffmpeg_checkbox")
        if uploaded_file is not None and uploaded_file.name.endswith('.csv'):
            file=uploaded_file.name
            playerEvents=extractEventsfromCSV(file)
            player=st.selectbox("Select a player to view their events", options=playerEvents.keys(), placeholder="Select a player", format_func=lambda name: f"{name} - {playerEvents[name][0]['teamTricode']}" if playerEvents[name] else name)


if player:
    with st.form("filter_form"):
        filter=st.multiselect("Filter events by type (assists not working for now)", options=['shot made', 'shot missed', 'foul', 'steal', 'turnover', 'assist', 'free throw', 'rebound'], default=None)
        submit_button=st.form_submit_button("Apply Filters")
        



if submit_button:
    filteredEvents=filterSelected(playerEvents[player], filter, [])
    if not filteredEvents:
        st.warning(f"No events found for {player} with the selected filters.")
    st.subheader(f"Filtered Events for {player}", anchor=None)
    videoEvents, retryArr=get_play_videos(filteredEvents)
    newEvents=[]
    if retryArr:
        st.warning(f"Note: {len(retryArr)} events could not be retrieved due to server errors and were skipped.")
        newEvents = filterSelected(playerEvents[player], filter, retryArr)
        if newEvents:
            st.subheader(f"Retrying Failed Events for {player}", anchor=None)
            videoEvents, retryArr = get_play_videos(newEvents)
            if retryArr:
                st.warning(f"Note: {len(retryArr)} events still could not be retrieved after retrying.")
    if "ffmpeg_checkbox" in st.session_state and st.session_state["ffmpeg_checkbox"]==True and videoEvents:
        st.markdown("Exporting videos with ffmpeg...")
        combinedVideos=export_video(videoEvents)
        if combinedVideos==-1:
            st.error("FFmpeg export failed. Please check the console for more details.")
        else:
            st.video(combinedVideos)
    if not videoEvents:
        st.warning(f"No videos found for {player} with the selected filters.")
    if st.session_state["ffmpeg_checkbox"]==False and videoEvents:
        for event in videoEvents:
            st.markdown(f"**{event['player']}**")
            st.markdown(f"Type: {event['desc']}")
            video_url = event['videoUrl']
            if not video_url:
                st.warning("Video URL not found for this event.")
                continue
            st.video(video_url)