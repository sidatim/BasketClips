import streamlit as st
import random
if 'proxy' not in st.session_state:
    st.session_state['proxy']=random.choice(st.secrets["PROXY_LIST"]) if "PROXY_LIST" in st.secrets else None 
from nba_api.stats.endpoints import leaguegamefinder
from extractpbp import extractEventsfromCSV, getEventsforGame, getTeamEvents
from filterEvents import filterSelected, sort_events
from generateVideo import get_play_videos
from loadTeams import load_teams, load_seasons
from exportVideo import export_video
import pandas as pd
import time
@st.cache_data(show_spinner=False) ##here, make sure to only cache the data if we get a successful response from the API
def getGames(team1, team2, season=None):
        gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team1, vs_team_id_nullable=team2, season_nullable=season, timeout=10)
        return gamefinder
  
if 'matchup_df' not in st.session_state:
    st.session_state['matchup_df'] = ''

def filterChangeCallback():
     st.session_state["matchup_df"]=""

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
teams=load_teams()
seasons=load_seasons()
videoEvents=None

gameKeys=["Regular Season", "Preseason", "Playoffs", "Finals", "Play In", "Other"]
season_options = list(([season['seasonYear'] for season in seasons]))
options = ["Team Matchup", "Upload CSV"]
choice = st.selectbox("Select an option", options, index=None)
if choice == "Team Matchup":
    st.markdown("<h2 style='font-size: 18px;'>Select Teams for Matchup</h2>", unsafe_allow_html=True)
    team1 = st.selectbox("Select Team 1", options=[team['teamName'] for team in teams], index=None, key="team1_selectbox", on_change=filterChangeCallback)
    team2 = st.selectbox("Select Team 2", options=[team['teamName'] for team in teams if team['teamName'] != team1], index=None, key="team2_selectbox", on_change=filterChangeCallback)
    ffmpegCheck=st.checkbox("Export videos with FFMPEG", key="ffmpeg_checkbox")
    if st.checkbox("Additional Filters"):
        seasonSelectStart=st.selectbox("Select Season", options=season_options, index=0, key="season_selectbox", on_change=filterChangeCallback)
    if st.button("Find Matchups"):
        if not team1 or not team2:
            st.warning("Please select both teams to find matchups.")
            st.stop()
        st.session_state['team1']=team1
        st.session_state['team2']=team2
        team1_id = next(team['teamId'] for team in teams if team['teamName'] == team1)
        team2_id = next(team['teamId'] for team in teams if team['teamName'] == team2)
        try:
            gamefinder = getGames(team1_id, team2_id, seasonSelectStart)
        except Exception as e:
            print(f"Error fetching games: {e}")
            st.error(f"Error fetching games: please try again later.")
            st.stop()
        games = gamefinder.get_data_frames()[0]
        df = pd.DataFrame(games)
        st.session_state['matchup_df'] = games
        
    if 'matchup_df' in st.session_state and type(st.session_state['matchup_df'])==pd.DataFrame:
        st.subheader(f"Matchups for {st.session_state['team1_selectbox']} vs {st.session_state['team2_selectbox']}")

        selected_game=st.dataframe(st.session_state['matchup_df'][['GAME_DATE', 'MATCHUP', 'WL', 'PTS', 'REB', 'AST']], on_select="rerun", selection_mode="single-row")
        if selected_game.selection.rows:
            selected_df=st.session_state['matchup_df'].iloc[selected_game.selection.rows[0]]
            try:
                generateFile=getEventsforGame(selected_df)
            except Exception as e:
                st.error(f"Error fetching play-by-play data for game {selected_df['GAME_ID']}. Please try again later.")
                st.stop()
if generateFile:
    playerEvents=extractEventsfromCSV(generateFile)
    player=st.selectbox("Select a player to view their events", options=playerEvents.keys(), placeholder="Select a player", format_func=lambda name: f"{name} - {playerEvents[name][0]['teamTricode']}" if playerEvents[name] else name)

if choice == "Upload CSV":
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        ffmpegCheck=st.checkbox("Export videos with FFMPEG", key="ffmpeg_checkbox")
        if uploaded_file is not None and uploaded_file.name.endswith('.csv'):
            file = uploaded_file.read()
            playerEvents=extractEventsfromCSV(file)
            player=st.selectbox("Select a player to view their events", options=playerEvents.keys(), placeholder="Select a player", format_func=lambda name: f"{name} - {playerEvents[name][0]['teamTricode']}" if playerEvents[name] else name)


if player:
    with st.form("filter_form"):
        filter=st.multiselect("Filter events by type", options=['shot made', 'shot missed', 'foul', 'steal', 'turnover', 'assist', 'free throw', 'rebound'], default=None)
        submit_button=st.form_submit_button("Apply Filters")
        



if submit_button:
    team=playerEvents[player][0]['teamTricode']
    teamEvents=getTeamEvents(playerEvents, team)
    filteredEvents=filterSelected(playerEvents[player], filter, teamEvents)
    if not filteredEvents:
        st.warning(f"No events found for {player} with the selected filters.")
        st.stop()
    st.subheader(f"Filtered Events for {player}", anchor=None)
    with st.spinner("Generating video URLs for events...", show_time=False):
        videoEvents, failedEvents=get_play_videos(filteredEvents)
    missingVideos=[]
    if failedEvents:
        st.warning(f"Note: {len(failedEvents)} events could not be retrieved, retrying.")
        time.sleep(2)
        missingVideos, retry=get_play_videos(failedEvents)
        if retry:
                st.warning(f"Note: {len(retry)} events still could not be retrieved after retrying.")
    if missingVideos:
            videoEvents.extend(missingVideos)
            videoEvents=sort_events(videoEvents)            
    if "ffmpeg_checkbox" in st.session_state and st.session_state["ffmpeg_checkbox"]==True and videoEvents:
        with st.spinner("Exporting videos with ffmpeg...", show_time=False):
            combinedVideos=export_video(videoEvents)
        if combinedVideos==-1:
            st.error("FFmpeg export failed.")
        else:
            st.success("Video was exported successfully")
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
