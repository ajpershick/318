import pandas as pd
import sys
import gzip
import numpy as np
import matplotlib.pyplot as plt

stations = sys.argv[1]
city_data = sys.argv[2]
output = sys.argv[3]

station_fh = gzip.open(stations, 'rt', encoding='utf-8')
stations = pd.read_json(station_fh, lines=True)
stations['avg_tmax'] = stations['avg_tmax']/10
city_data = pd.read_csv(city_data)
city_data = city_data.dropna()
city_data['area'] = city_data['area']/1000000
city_data = city_data[city_data['area'] <= 10000].reset_index()
city_data = city_data.drop('index', 1)

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
    return dist

def best_tmax(city, stations):
    dist = distance(city, stations)
    return stations.get_value(index=dist.argmin(), col='avg_tmax')

Calgary = city_data.iloc[0]
calgTmax = best_tmax(Calgary, stations)
city_data['best_tmax'] = city_data.apply(best_tmax, stations=stations, axis=1)
city_data['population_density'] = city_data['population']/city_data['area']

plt.plot(city_data['best_tmax'], city_data['population_density'], 'b.', alpha=0.5)
plt.ylabel('Population Density (people/km\u00b2)')
plt.xlabel('Avg Max Temperature (\u00b0C)')
plt.savefig(output)

