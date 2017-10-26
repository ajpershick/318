import time
from implementations import all_implementations
import numpy as np
import pandas as pd

def main():
    data = pd.DataFrame()
    for sort in all_implementations:
        sort_array = np.zeros(40)
        for i in range(40):
            random_array = np.random.randint(10000, 100 * 20000 + 10000, size=(24000,))
            st = time.time()
            sort(random_array)
            en = time.time()
            sort_array[i] = (en-st)
        data[sort.__name__] = sort_array

    data.to_csv('data.csv', index=False)

if __name__ == '__main__':
    main()