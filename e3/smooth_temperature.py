
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pykalman import KalmanFilter
import numpy as np
lowess = sm.nonparametric.lowess
cpu_data = pd.read_csv('sysinfo.csv')

## Part 1 Lowess

cpu_data['timestamp'] = pd.to_datetime(cpu_data['timestamp'])
cpu_data['timestamp'] = cpu_data['timestamp'].apply(lambda x: x.timestamp())
plt.figure(figsize=(12, 4))
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5, label='cpu_data')
loess_smoothed = lowess(cpu_data['temperature'].values,cpu_data['timestamp'],frac=0.02)
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-', label='Loess')

## Part 2 Kalman

kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1']]
initial_state = kalman_data.iloc[0]
observation_covariance = np.diag([0.9, 0.9, 0.9]) ** 2 # TODO: shouldn't be zero
transition_covariance = np.diag([0.1, 0.1, 0.1]) ** 2 # TODO: shouldn't be zero
transition = [[1, 0, -0.27], [0, 0.85, -1.14], [0, 0.06, 0.37]] # TODO: shouldn't (all) be zero
kf = KalmanFilter(initial_state_mean=initial_state,
                    initial_state_covariance=observation_covariance,
                    observation_covariance=observation_covariance,
                    transition_covariance=transition_covariance,
                    transition_matrices=transition  )
kalman_smoothed, _ = kf.smooth(kalman_data)
plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'g-', label='Kalman')
plt.legend()
# plt.show() # easier for testing
plt.savefig('cpu.svg') # for final submission

