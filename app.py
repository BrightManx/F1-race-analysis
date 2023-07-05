import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from race_analysis import get_laps, get_positions, get_lapTimes, get_currentMetadata, get_results, get_standings

st.set_page_config(
    page_title="F1 Race Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

current_metadata = get_currentMetadata()
season, round = current_metadata.Season.item(), current_metadata.Round.item()
results = get_results(season, round)
driverStandings, constructorStandings = get_standings(season, round)
laps = get_laps()
positions = get_positions(laps)
lapTimes = get_lapTimes(laps)

# METADATA
st.write(f"<h1 style='text-align:center;'> Formula 1: \"{current_metadata.raceName.item()}\" Race Analysis </h1>", unsafe_allow_html=True)
st.write('---')

cols = st.columns(5)

with cols[0]:
    st.write(f'''      
    - Season: **{current_metadata.Season.item()}**  
    - Round: **{current_metadata.Round.item()}** 
    - Race Name: **{current_metadata.raceName.item()}**  
    - Circuit Name: **{current_metadata.circuitName.item()}** 
    - Country: **{current_metadata.country.item()}**  
    - Locality: **{current_metadata.locality.item()}**  
    ''')


with cols[1]:
    st.map(current_metadata[['lat', 'lon']].astype(float), zoom=2)

with cols[2]:
    st.write("<h4 style='text-align:center;'> Results </h4>", unsafe_allow_html=True)
    st.write(results[['Driver', 'points']])

with cols[3]:
    st.write("<h4 style='text-align:center;'> Drivers Standings </h4>", unsafe_allow_html=True)
    st.write(driverStandings[['Driver', 'points', 'wins']])

with cols[4]:
    st.write("<h4 style='text-align:center;'> Constructors Standings </h4>", unsafe_allow_html=True)
    st.write(constructorStandings[['Constructor', 'points', 'wins']])


#### PLOTS
st.write('---')
col1, col2 = st.columns(2)

with col1:
    st.write("<h3 style='text-align:center;'> Positions By Lap </h3>", unsafe_allow_html=True)
    positions_drivers = st.multiselect('Whose positions would you like to compare?', positions.columns)
    st.line_chart(positions, y = positions_drivers)

with col2:
    st.write("<h3 style='text-align:center;'> Lap Times By Lap </h3>", unsafe_allow_html=True)
    lapTimes_drivers = st.multiselect('Whose Lap Times would you like to compare?', lapTimes.columns)
    st.line_chart(lapTimes, y = lapTimes_drivers)
