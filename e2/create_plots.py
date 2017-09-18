import sys
import pandas as pd
import matplotlib.pyplot as plt

filename1 = sys.argv[1]
filename2 = sys.argv[2]

pd.read_table(filename, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])

plt.figure(figsize=(10, 5)) # change the size to something sensible
plt.subplot(1, 2, 1) # subplots in 1 row, 2 columns, select the first
plt.plot(…) # build plot 1
plt.subplot(1, 2, 2) # ... and then select the second
plt.plot(…) # build plot 2
plt.show()