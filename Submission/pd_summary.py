
import pandas as pd


totals = pd.read_csv('totals.csv').set_index(keys=['name'])
counts = pd.read_csv('counts.csv').set_index(keys=['name'])

min_precip = pd.Series.idxmin(totals.sum(axis = 1))

print("City with lowest total precipitation:")
print(min_precip)

total_precip_per_month = totals.sum(axis = 0)
total_counts_per_month = counts.sum(axis = 0)
avg_precip_per_month = total_precip_per_month / total_counts_per_month

print("Average precipitation in each month:")
print(avg_precip_per_month)

total_precip_per_city = totals.sum(axis = 1)
total_counts_per_city = counts.sum(axis = 1)
avg_daily_precip_per_city = total_precip_per_city / total_counts_per_city

print("Average precipitation in each city:")
print(avg_daily_precip_per_city )

