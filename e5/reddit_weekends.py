import pandas as pd
import sys
import gzip
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_TEMPLATE = (
    "Initial (invalid) T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann–Whitney U-test p-value: {utest_p:.3g}"
)

def main():

    # Prepping data
    counts = sys.argv[1]
    reddit_counts = gzip.open(counts, 'rt', encoding='utf-8')
    data = pd.read_json(reddit_counts, lines=True)

    # Filtering
    data['weekday'] = data['date'].apply(lambda x: x.weekday())
    data['date'] = pd.to_datetime(data['date'])
    data = data[(data['date'] < '2014-01-01') & (data['date'] > '2011-12-31') & (data['subreddit'] == 'canada')]
    weekdays_only = data[data['weekday'] < 5 ]
    weekends_only = data[data['weekday'] > 4 ]

    # Running initial tests
    initial_ttest_p = scipy.stats.ttest_ind(weekdays_only['comment_count'], weekends_only['comment_count']).pvalue
    initial_weekday_normality_p = scipy.stats.normaltest(weekdays_only['comment_count']).pvalue
    initial_weekend_normality_p = scipy.stats.normaltest(weekends_only['comment_count']).pvalue
    initial_levene_p = scipy.stats.levene(weekdays_only['comment_count'], weekends_only['comment_count']).pvalue

    # Fix 1: Transforming
    transformed_weekday_normality_p = scipy.stats.normaltest(np.sqrt(weekdays_only['comment_count'])).pvalue
    transformed_weekend_normality_p = scipy.stats.normaltest(np.sqrt(weekends_only['comment_count'])).pvalue
    transformed_levene_p = scipy.stats.levene(np.sqrt(weekdays_only['comment_count']), np.sqrt(weekends_only['comment_count'])).pvalue

    # Fix 2: CLT

    weekends_only['year_week'] = weekends_only['date'].apply(lambda x: str(x.isocalendar()[0]) + str(x.isocalendar()[1]))
    weekdays_only['year_week'] = weekdays_only['date'].apply(lambda x: str(x.isocalendar()[0]) + str(x.isocalendar()[1]))
    weekdays_grouped = weekdays_only.groupby('year_week').agg({'comment_count': 'mean'})
    weekends_grouped = weekends_only.groupby('year_week').agg({'comment_count': 'mean'})

    weekly_ttest_p = scipy.stats.ttest_ind(weekdays_grouped['comment_count'], weekends_grouped['comment_count']).pvalue
    weekly_weekday_normality_p = scipy.stats.normaltest(weekdays_grouped['comment_count']).pvalue
    weekly_weekend_normality_p = scipy.stats.normaltest(weekends_grouped['comment_count']).pvalue
    weekly_levene_p = scipy.stats.levene(weekdays_grouped['comment_count'], weekends_grouped['comment_count']).pvalue

    # Fix 3: U-Test
    utest_p = scipy.stats.mannwhitneyu(weekdays_only['comment_count'], weekends_only['comment_count']).pvalue

    print(OUTPUT_TEMPLATE.format(
            initial_ttest_p=initial_ttest_p,
            initial_weekday_normality_p=initial_weekday_normality_p,
            initial_weekend_normality_p=initial_weekend_normality_p,
            initial_levene_p=initial_levene_p,
            transformed_weekday_normality_p=transformed_weekday_normality_p,
            transformed_weekend_normality_p=transformed_weekend_normality_p,
            transformed_levene_p=transformed_levene_p,
            weekly_weekday_normality_p=weekly_weekday_normality_p,
            weekly_weekend_normality_p=weekly_weekend_normality_p,
            weekly_levene_p=weekly_levene_p,
            weekly_ttest_p=weekly_ttest_p,
            utest_p=utest_p,
        ))


if __name__ == "__main__":
    main()