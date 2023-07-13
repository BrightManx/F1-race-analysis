# import streamlit as st
# import pandas as pd
# import requests
# import matplotlib.pyplot as plt
# from race_analysis import get_laps, get_positions, get_lapTimes, get_currentMetadata, get_results, get_standings

# st.set_page_config(
#     page_title="F1 Race Analysis",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# current_metadata = get_currentMetadata()
# season, round = current_metadata.Season.item(), current_metadata.Round.item()
# results = get_results(season, round)
# driverStandings, constructorStandings = get_standings(season, round)
# laps = get_laps()
# positions = get_positions(laps)
# lapTimes = get_lapTimes(laps)

# # METADATA
# st.write(f"<h1 style='text-align:center;'> Formula 1: \"{current_metadata.raceName.item()}\" Race Analysis </h1>", unsafe_allow_html=True)
# st.write('---')

# cols = st.columns(5)

# with cols[0]:
#     st.write(f'''      
#     - Season: **{current_metadata.Season.item()}**  
#     - Round: **{current_metadata.Round.item()}** 
#     - Race Name: **{current_metadata.raceName.item()}**  
#     - Circuit Name: **{current_metadata.circuitName.item()}** 
#     - Country: **{current_metadata.country.item()}**  
#     - Locality: **{current_metadata.locality.item()}**  
#     ''')


# with cols[1]:
#     st.map(current_metadata[['lat', 'lon']].astype(float), zoom=2)

# with cols[2]:
#     st.write("<h4 style='text-align:center;'> Results </h4>", unsafe_allow_html=True)
#     st.write(results[['Driver', 'points']])

# with cols[3]:
#     st.write("<h4 style='text-align:center;'> Drivers Standings </h4>", unsafe_allow_html=True)
#     st.write(driverStandings[['Driver', 'points', 'wins']])

# with cols[4]:
#     st.write("<h4 style='text-align:center;'> Constructors Standings </h4>", unsafe_allow_html=True)
#     st.write(constructorStandings[['Constructor', 'points', 'wins']])


# #### PLOTS
# st.write('---')
# col1, col2 = st.columns(2)

# with col1:
#     st.write("<h3 style='text-align:center;'> Positions By Lap </h3>", unsafe_allow_html=True)
#     positions_drivers = st.multiselect('Whose positions would you like to compare?', positions.columns)
#     st.line_chart(positions, y = positions_drivers)

# with col2:
#     st.write("<h3 style='text-align:center;'> Lap Times By Lap </h3>", unsafe_allow_html=True)
#     lapTimes_drivers = st.multiselect('Whose Lap Times would you like to compare?', lapTimes.columns)
#     st.line_chart(lapTimes, y = lapTimes_drivers)


# ###########
# st.write('---')
# st.write("<h4 style='text-align:center;'> new sections to come | work in progress... </h4>", unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from race_analysis import (
    get_laps,get_positions,
    get_lapTimes,
    get_lastMetadata,
    get_results,
    get_standings,
    get_seasonMetadata,
    get_roundMetadata
    )

st.set_page_config(
    page_title="F1 Race Analysis | Up to date standings, analysis and results from the last F1 Grand Prix",
    layout="wide",
    initial_sidebar_state="collapsed"
)

action = st.sidebar.radio('What GP would you like to Analyze?', ['Most recent', 'Custom'])

lastMetadata = get_lastMetadata()
last_season, last_round = lastMetadata.Season.item(), lastMetadata.Round.item()

if action == 'Most recent':
    season, round = last_season, last_round
    metadata = lastMetadata

if action == 'Custom':
    season = st.slider('Select season', min_value = 1950, max_value=int(last_season), step=1, value=int(last_season))
    seasonMetadata = get_seasonMetadata(season)
    round = st.selectbox('Select round', seasonMetadata.raceName)
    round = seasonMetadata.loc[seasonMetadata.raceName == round, 'Round'].item()
    metadata = get_roundMetadata(season, round)

results = get_results(season, round)
driverStandings, constructorStandings = get_standings(season, round)
laps = get_laps(season, round)
positions = get_positions(laps)
lapTimes = get_lapTimes(laps)

# metadata
st.write(metadata)
st.write(f"<h1 style='text-align:center;'> {season} {metadata.raceName.item()}</h1>", unsafe_allow_html=True)
st.write(f"<h5 style='text-align:center;'>results, analysis and standings</h5>", unsafe_allow_html=True)
st.write('---')

cols = st.columns(5)

with cols[0]:
    fmt_date = str(pd.to_datetime(metadata.date).dt.strftime('%e-%B-2023').item())
    st.write(f'''      
    - Season: **{metadata.Season.item()}**  
    - Round: **{metadata.Round.item()}**
    - Date: **{metadata.date.item()}** 
    - Race Name: **{metadata.raceName.item()}**  
    - Circuit Name: **{metadata.circuitName.item()}** 
    - Country: **{metadata.country.item()}**  
    - Locality: **{metadata.locality.item()}**  
    ''')


with cols[1]:
    st.map(metadata[['lat', 'lon']].astype(float), zoom=2)

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



####
st.write('---')
st.write(f"<h5 style='text-align:center;'>more section to come | work in progess...</h5>", unsafe_allow_html=True)
