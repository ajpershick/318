import pandas as pd
import sys
import gzip
import numpy as np

stations = sys.argv[1]
city_data = sys.argv[2]
output = sys.argv[3]

station_fh = gzip.open(stations, 'rt', encoding='utf-8')
stations = pd.read_json(station_fh, lines=True)
stations['avg_tmax'] = stations['avg_tmax']/10
city_data = pd.read_csv(city_data)
city_data = city_data.dropna()
city_data['area'] = city_data['area']/1000000
city_data = city_data[city_data['area'] <= 10000]

# Reusing from e3
def haversine_np(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6371 * c
    return km

def distance(city, stations):
    dist = haversine_np(city['longitude'], city['latitude'],
                        stations['longitude'], stations['latitude'])
    dist = np.sum(dist)
    return dist

def best_tmax(city, stations):
    closest_city = distance(city, stations).argmin()
    return closest_city

closest = best_tmax(city_data, stations )

s