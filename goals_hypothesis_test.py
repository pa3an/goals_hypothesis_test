
# This project was first completed on DataCamp (Hypothesis Testing with Men's and Women's Soccer Matches)
# the datases are available to download on DataCamp.com
# the purpose of the project is to verify whether there is a statistically significant
# difference between goals scored in women's and men's games
# the test is run on a subset of the data, to include games from 2002 onward, and World Cup game only (no qualifiers)


# import the libraries
import pandas as pd
import scipy.stats as stats

### import the datasets
men_results = pd.read_csv('men_results.csv')
women_results = pd.read_csv('women_results.csv')

### let's have a look at the data types
men_results.dtypes

### convert the date column to datetime
men_results['date'] = pd.to_datetime(men_results['date'])
women_results['date'] = pd.to_datetime(women_results['date'])

### create a new column, with the total goals per game
men_results['total_goals'] = men_results['home_score'] + men_results['away_score']
women_results['total_goals'] = women_results['home_score'] + women_results['away_score']

# subset by date and tournament
men_goals = men_results.loc[(men_results['date']>= '2002-01-01') & (men_results['tournament']=='FIFA World Cup')]
women_goals = women_results.loc[(women_results['date']>= '2002-01-01') & (women_results['tournament']=='FIFA World Cup')]

print(men_goals.head())

### let's plot the distributions of total_goals

import matplotlib.pyplot as plt

# bin range is given by the above stats (min and max)
men_bins = range(9)
women_bins = range(14)

plt.hist(men_goals['total_goals'], bins=men_bins, alpha=0.5, label='Men')
plt.hist(women_goals['total_goals'], bins=women_bins, alpha=0.5, label='Women')

xticks = range(0,15, 2) #x ticks is whole numbers only
plt.xlabel('Total Goals')
plt.ylabel('Frequency')
plt.title('Distribution of total goals per game')

plt.xlim(0,15)
plt.legend()
plt.show()

# let's also do a Shapiro-Wilk test to check normality

from scipy.stats import shapiro
_, men_p_value = shapiro(men_goals['total_goals'])
_, women_p_value = shapiro(women_goals['total_goals'])

# if pvalues are lower than 0.01, then the data is not normally distributed
# can also be set to 0.05

if men_p_value > 0.01:
    print('men normally distributed')
else:
    print('men not normally distributed')

if women_p_value > 0.01:
    print('women normally distributed')
else:
    print('women not normally distributed')

### let's check the variance with boxplots

plt.boxplot([men_goals['total_goals'], women_goals['total_goals']])
plt.xticks([1,2], ['Men', 'Women'])
plt.xlabel('Gender')
plt.ylabel('Total Goals/Game')
plt.title('Comparison of goals/game between men and women')
plt.show()

print(men_goals['total_goals'].describe())
print(women_goals['total_goals'].describe())

# data is not normally distributed
# we'll do a Wilcoxon-Mann-Whitney Test

from scipy.stats import mannwhitneyu

p_value_women = mannwhitneyu(women_goals['total_goals'], men_goals['total_goals'], alternative='greater')
p_value_men = mannwhitneyu(women_goals['total_goals'], men_goals['total_goals'], alternative='less')

### check p-value against a significance level of 10%
### and just to be sure, we run two tests, one each way

if p_value_women.pvalue < 0.01:
    result_women = "reject - women score more"
else:
    result_women = "Fail to reject - women don't score more."

result_dict_women = {'p_val_women':p_value_women.pvalue, 'result':result_women}


if p_value_men.pvalue < 0.01:
    result_men = "reject - men score more"
else:
    result_men = "Fail to reject - men don't score more."
    
result_dict_men = {'p_val_men':p_value_men.pvalue, 'result': result_men}


print(result_dict_women)
print(result_dict_men)
