
import numpy as np
import matplotlib.pyplot as plt


data = np.load('monthdata.npz')

totals = data['totals']
counts = data['counts']

plt.plot(totals, counts)
plt.show()

min_precip = np.argmin(totals.sum(axis = 1))

print("Row with the lowest precipitation:")
print(min_precip)

total_precip_per_month = totals.sum(axis = 0)
total_counts_per_month = counts.sum(axis = 0)
avg_precip_per_month = total_precip_per_month / total_counts_per_month

print("Average precipitation in each month:")
print(avg_precip_per_month )

total_precip_per_city = totals.sum(axis = 1)
total_counts_per_city = counts.sum(axis = 1)
avg_daily_precip_per_city = total_precip_per_city / total_counts_per_city

print("Average precipitation in each city:")
print(avg_daily_precip_per_city )

totals_reshaped = totals.reshape(totals.size // 12, 4, 3)
totals_reshaped2 = totals_reshaped.sum(axis = 2)

print("Quarterly precipitation totals:")
print(totals_reshaped2 )

