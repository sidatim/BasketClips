import streamlit as st
from extractpbp import extractEventsfromCSV
from filterEvents import filterSelected
from generateVideo import get_play_videos
import pprint as pp
st.title("NBA Play-by-Play Clips")
st.markdown("""
    <h1 style="font-size: 22px;">This app analyzes NBA play-by-play data to extract player events and statistics.</h1>
    <p class="intro-text">Upload a CSV file containing play-by-play data to get started. (supports only NBA_API play-by-play format)</p>
""", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
player=None
if uploaded_file is not None and uploaded_file.name.endswith('.csv'):
    file=uploaded_file.name
    playerEvents=extractEventsfromCSV(file)
    player=st.selectbox("Select a player to view their events", options=playerEvents.keys(), placeholder="Select a player", format_func=lambda name: f"{name} - {playerEvents[name][0]['teamTricode']}" if playerEvents[name] else name)
filteredEvents=None
submit_button=None
if player:
    with st.form("filter_form"):
        filter=st.multiselect("Filter events by type (assists not working for now)", options=['shot made', 'shot missed', 'foul', 'steal', 'turnover', 'assist', 'free throw', 'rebound'], default=None)
        submit_button=st.form_submit_button("Apply Filters")
        


videoEvents=None
if submit_button:
    filteredEvents=filterSelected(playerEvents[player], filter, [])
    if not filteredEvents:
        st.warning(f"No events found for {player} with the selected filters.")
    st.subheader(f"Filtered Events for {player}", anchor=None)
    videoEvents, retryArr=get_play_videos(filteredEvents)
    newEvents=[]
    if retryArr:
        retry_message = f"Note: {len(retryArr)} events could not be retrieved due to server errors and were skipped."
        st.warning(retry_message)
        newEvents = filterSelected(playerEvents[player], filter, retryArr)
        if newEvents:
            st.subheader(f"Retrying Failed Events for {player}", anchor=None)
            videoEvents, retryArr = get_play_videos(newEvents)
            if retryArr:
                st.warning(f"Note: {len(retryArr)} events still could not be retrieved after retrying.")
    for event in videoEvents:
        st.markdown(f"**{event['player']}**")
        st.markdown(f"Type: {event['desc']}")
        video_url = event['videoUrl']
        if not video_url:
            st.warning("Video URL not found for this event.")
            continue
        print(video_url)
        st.video(video_url)

#note: 