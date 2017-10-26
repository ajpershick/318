import sys
import pandas as pd
from scipy import stats as st
from statsmodels.stats.multicomp import pairwise_tukeyhsd

data = pd.read_csv('data.csv')
qs1 = data['qs1']
qs2 = data['qs2']
qs3 = data['qs3']
qs4 = data['qs4']
qs5 = data['qs5']
merge = data['merge1']
partition_sort = data['partition_sort']

#ANOVA test
ANOVA = st.f_oneway(qs1, qs2, qs3, qs4, qs5, merge, partition_sort)
print('ANOVA: ' + str(ANOVA.pvalue))

#Tukey Test
data_melt = pd.melt(data)
posthoc = pairwise_tukeyhsd(
        data_melt['value'], data_melt['variable'],
        alpha=0.05)
print('posthoc: ', posthoc)
posthoc_means = pd.DataFrame(posthoc._multicomp.groupstats.groupmean, index=posthoc.groupsunique)
print(posthoc_means.sort_values(by=0))

#Means
print(str(qs1.mean()) + '\n', str(qs2.mean()) + '\n', str(qs3.mean()) + '\n', str(qs4.mean()) + '\n', str(qs5.mean()) + '\n', str(merge.mean()) + '\n', str(partition_sort.mean()) + '\n')
print('end')