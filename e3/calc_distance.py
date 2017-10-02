import xml.etree.ElementTree as ET
import math
import pandas as pd
import numpy as np
import sys
from xml.dom.minidom import parse, parseString
from pykalman import KalmanFilter

def read_gpx(systemarg):

    filename = systemarg
    data = parse(filename)

    ext_data = data.getElementsByTagName("trkpt")

    # Latitude list
    lats = []
    # Longitude list
    lons = []

    # Parse lat/long, elevation and times
    for trkpt in ext_data:
        # Latitude
        lat = float(trkpt.attributes["lat"].value)
        # Longitude
        lon = float(trkpt.attributes["lon"].value)
        lats.append(lat)
        lons.append(lon)

    return pd.DataFrame({'lat':lats, 'lon':lons})

# Taken from https://stackoverflow.com/questions/40452759/pandas-latitude-longitude-to-distance-between-successive-rows
def haversine_np(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6371 * c
    return km

def distance(points):
    dist = haversine_np(points['lon'].shift(), points['lat'].shift(),
                 points.loc[1:, 'lon'], points.loc[1:, 'lat'])
    dist = np.sum(dist)
    return dist * 1000

def smooth(points):
    kalman_data = points
    initial_state = kalman_data.iloc[0]
    observation_covariance = np.diag([0.25, 0.25]) ** 2  # TODO: shouldn't be zero
    transition_covariance = np.diag([0.1, 0.1]) ** 2  # TODO: shouldn't be zero
    transition = np.identity(2)  # TODO: shouldn't (all) be zero
    kf = KalmanFilter(initial_state_mean=initial_state,
                      initial_state_covariance=observation_covariance,
                      observation_covariance=observation_covariance,
                      transition_covariance=transition_covariance,
                      transition_matrices=transition)
    kalman_smoothed, _ = kf.smooth(kalman_data)

    kalmanDF = pd.DataFrame({
        'lat': kalman_smoothed[:, 0],
        'lon': kalman_smoothed[:, 1]
    })
    return kalmanDF


def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)

    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)

    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)

    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')

def main():
    points = read_gpx(sys.argv[1])
    print('Unfiltered distance: %0.2f' % (distance(points)))
    smoothed_points = smooth(points)
    print('Filtered distance: %0.2f' % (distance(smoothed_points)))
    output_gpx(smoothed_points, 'out.gpx')

main()

