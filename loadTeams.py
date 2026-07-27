import json
import streamlit as st
@st.cache_data
def load_teams():
    teams=[]
    with open("nba_teams.json", "r") as f:
        data = json.load(f)
    for team in data:
            teams.append({
                "teamId": team["id"],
                "teamName": team["full_name"],
                "abbrevation": team["abbreviation"],
                "nickname": team["nickname"],
            })
    return teams

@st.cache_data 
def load_seasons():
    seasons=[]
    with open("seasons.json", "r") as f:
        data = json.load(f)
    for season in data:
        seasons.append({
            "seasonYear": season,
            "seasonTypes": data[season]
        })
    return seasons