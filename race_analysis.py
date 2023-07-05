import pandas as pd
import requests

def get_laps():
    # Last Metadata
    r = requests.get('https://ergast.com/api/f1/current/last.json', params={'limit': 100000})
    current_last = pd.DataFrame(r.json()['MRData']['RaceTable']['Races'])
    season = current_last.season.item()
    round = current_last['round'].item()

    # Laps
    r_laps = requests.get('https://ergast.com/api/f1/current/last/laps.json', params={'limit': 100000})
    r_laps = pd.DataFrame(r_laps.json()['MRData']['RaceTable']['Races'][0]['Laps'])

    tot_laps = int(r_laps.number.iloc[-1])
    laps = pd.DataFrame()
    for lap in range(tot_laps):
        new = pd.DataFrame(r_laps.loc[lap, 'Timings'])
        new.insert(0, 'lap', lap+1)
        laps = pd.concat([laps, new])

    dtimes = pd.to_datetime(laps.time, format="%M:%S.%f")
    ms = dtimes.dt.minute * 60 * 1000 + dtimes.dt.second * 1000 + dtimes.dt.microsecond // 1000
    laps['ms'] = ms

    return laps

def get_positions(laps):

    positions = pd.DataFrame()
    for driver in laps.driverId.unique():
        positions[driver] = laps.loc[laps.driverId == driver, ['position']].astype(int).reset_index(drop=True)
    positions.index = range(1, 72)

    return positions

def get_lapTimes(laps):

    lapTimes = pd.DataFrame()
    for driver in laps.driverId.unique():
        lapTimes[driver] = laps.loc[laps.driverId == driver, ['ms']].astype(int).reset_index(drop=True)
    lapTimes.index = range(1, 72)

    return lapTimes