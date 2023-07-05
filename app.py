import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from race_analysis import get_laps, get_positions, get_lapTimes

st.set_page_config(
    page_title="Word Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

laps = get_laps()
positions = get_positions(laps)
lapTimes = get_lapTimes(laps)

col1, col2 = st.columns(2)

with col1:
    st.write("<h1 style='text-align:center;'> Positions By Lap </h1>", unsafe_allow_html=True)
    positions_drivers = st.multiselect('Whose positions would you like to compare?', positions.columns)
    st.line_chart(positions, y = positions_drivers)

with col2:
    st.write("<h1 style='text-align:center;'> Lap Times By Lap </h1>", unsafe_allow_html=True)
    lapTimes_drivers = st.multiselect('Whose Lap Times would you like to compare?', lapTimes.columns)
    st.line_chart(lapTimes, y = lapTimes_drivers)
