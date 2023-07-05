# import pandas as pd
# import requests

# def get_laps():
#     # Last Metadata
#     r = requests.get('https://ergast.com/api/f1/current/last.json', params={'limit': 100000})
#     current_last = pd.DataFrame(r.json()['MRData']['RaceTable']['Races'])
#     season = current_last.season.item()
#     round = current_last['round'].item()

#     # Laps
#     r_laps = requests.get('https://ergast.com/api/f1/current/last/laps.json', params={'limit': 100000})
#     r_laps = pd.DataFrame(r_laps.json()['MRData']['RaceTable']['Races'][0]['Laps'])

#     tot_laps = int(r_laps.number.iloc[-1])
#     laps = pd.DataFrame()
#     for lap in range(tot_laps):
#         new = pd.DataFrame(r_laps.loc[lap, 'Timings'])
#         new.insert(0, 'lap', lap+1)
#         laps = pd.concat([laps, new])

#     dtimes = pd.to_datetime(laps.time, format="%M:%S.%f")
#     ms = dtimes.dt.minute * 60 * 1000 + dtimes.dt.second * 1000 + dtimes.dt.microsecond // 1000
#     laps['ms'] = ms

#     return laps

# def get_positions(laps):

#     positions = pd.DataFrame()
#     for driver in laps.driverId.unique():
#         positions[driver] = laps.loc[laps.driverId == driver, ['position']].astype(int).reset_index(drop=True)
#     positions.index = range(1, 72)

#     return positions

# def get_lapTimes(laps):

#     lapTimes = pd.DataFrame()
#     for driver in laps.driverId.unique():
#         lapTimes[driver] = laps.loc[laps.driverId == driver, ['ms']].astype(int).reset_index(drop=True)
#     lapTimes.index = range(1, 72)

#     return lapTimes

import pandas as pd
import requests

def get_currentMetadata():

    # Last Metadata
    r = requests.get('https://ergast.com/api/f1/current/last.json', params={'limit': 100000})
    current_last = pd.DataFrame(r.json()['MRData']['RaceTable']['Races'])
    season = current_last.season.item()
    round = current_last['round'].item()

    current_metadata = pd.DataFrame(current_last.Circuit.item()['Location'], index=[0]).rename(columns={'long':'lon'})
    current_metadata['Season'] = current_last['season'].item()
    current_metadata['Round'] = current_last['round'].item()
    current_metadata['raceName'] = current_last['raceName'].item()
    current_metadata['circuitName'] = current_last.Circuit.item()['circuitName']

    return current_metadata


def get_results(season, round):

    r_results = requests.get(f'https://ergast.com/api/f1/{season}/{round}/results.json')
    results = pd.DataFrame(r_results.json()['MRData']['RaceTable']['Races'][0]['Results'])
    results.Driver = results.Driver.apply(lambda x: x['driverId'])
    results.Constructor = results.Constructor.apply(lambda x: x['constructorId'])
    results.insert(0, 'round', round)
    results.insert(0, 'season', season)
    results.index += 1

    return results


def get_standings(season, round):

    r_driverStandings = requests.get(f'https://ergast.com/api/f1/{season}/{round}/driverStandings.json')
    driverStandings = pd.DataFrame(r_driverStandings.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'])
    driverStandings.Driver = driverStandings.Driver.apply(lambda x: x['driverId'])
    driverStandings.Constructors = driverStandings.Constructors.apply(lambda x: x[0]['constructorId'])
    driverStandings.index += 1

    r_constructorStandings = requests.get(f'https://ergast.com/api/f1/{season}/{round}/constructorStandings.json')
    constructorStandings = pd.DataFrame(r_constructorStandings.json()['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings'])
    constructorStandings.Constructor = constructorStandings.Constructor.apply(lambda x: x['constructorId'])
    constructorStandings.index += 1

    return driverStandings, constructorStandings


def get_laps():

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
