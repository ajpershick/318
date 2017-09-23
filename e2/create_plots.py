import sys
import pandas as pd
import matplotlib.pyplot as plt

filename1 = sys.argv[1]
filename2 = sys.argv[2]

data1 = pd.read_table(filename1, sep=' ', header=None, index_col=1, names=['lang', 'page', 'views', 'bytes'])
data2 = pd.read_table(filename2, sep=' ', header=None, index_col=1, names=['lang', 'page', 'views', 'bytes'])

data1 = data1.sort_values(by='views', ascending=False, kind='quicksort', na_position='last')
data2 = data2.sort_values(by='views', ascending=False, kind='quicksort', na_position='last')

### Part 2:

data2['data1_views'] = data1['views']

# Plotting

plt.figure(figsize=(10, 5)) # change the size to something sensible
plt.subplot(1, 2, 1) # subplots in 1 row, 2 columns, select the first
plt.plot(data1['views'].values) # build plot 1
plt.title('Popularity Distribution')
plt.xlabel('Rank')
plt.ylabel('Views')
plt.subplot(1, 2, 2) # ... and then select the second
plt.title('Daily Correlation')
plt.xlabel('Data 1 views')
plt.ylabel('Data 2 Views')
plt.scatter(data2['data1_views'].values, data2['views'].values, s=7) # build plot 2
plt.xscale('log')
plt.yscale('log')
plt.savefig('wikipedia.png')
















