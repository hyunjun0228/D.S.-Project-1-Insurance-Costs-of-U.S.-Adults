import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

#Beginning of Part 1 of the project: Determine the strongest and the weakest contributing factor to the insurance charges

# Function that changes the region into an integer
def region_index(x):
	if x == 'southwest':
		return 1
	elif x == 'southeast':
		return 2
	elif x == 'northwest':
		return 3
	else:
		return 4

# Read in the given sample 
insurances = pd.read_csv('insurance.csv')
insurances['sex'] = insurances.sex.apply(lambda x: 1 if x =="male" else 2)
insurances['smoker'] = insurances.smoker.apply(lambda x: 1 if x =='yes' else 0)
insurances['region'] = insurances.region.apply(lambda x: region_index(x))

#Calculating the correlation coefficient of each variable with the insurance charges
age_charges = insurances['age'].corr(insurances['charges'])
sex_charges = insurances['sex'].corr(insurances['charges'])
bmi_charges = insurances['bmi'].corr(insurances['charges'])
child_charges = insurances['children'].corr(insurances['charges'])
smoker_charges = insurances['smoker'].corr(insurances['charges'])
region_charges = insurances['region'].corr(insurances['charges'])

# Creating a table of variables against the correlation coefficients to easily compare the values
charges_corr_df = pd.DataFrame({'variables': ['age', 'sex', 'bmi', 'child', 'smoker', 'region'], 'corr_coeff': [age_charges, sex_charges, bmi_charges, child_charges, smoker_charges, region_charges]})
max_var = charges_corr_df[charges_corr_df.corr_coeff == charges_corr_df.corr_coeff.max()]
min_var = charges_corr_df[charges_corr_df.corr_coeff == charges_corr_df.corr_coeff.min()]
print(charges_corr_df)

# Printing my conclusion
print(f'The variable that had the maximum correlation coefficient with regard to the insurance charges was "smoker", which had a correlation coefficient of 0.787251, significantly higher in comparison to that of other variables.')
print('The variable "region" had the minimal degree of correlation with insurance charges; it had a value of 0.006208, significantly lower in comparison to that of other variables.\n')
# End of Part 1

# Beginning of Part 2: How does the "smoker" variable when grouped with the "sex" variable provide affect the insurance charges? In other words, how does the smoking habits in each sex affect the insurance charges? Is it larger for male, or is it larger for female?

# Grouping the dataset with "smoker" variable (strongest factor); there are 1064 non-smokers and 274 smokers in our dataset

smokers_charge = insurances.groupby('smoker').charges.mean().reset_index()
smokers_number = insurances.groupby('smoker').age.count().reset_index()
smokers_number.rename(columns={'age': 'num_people'}, inplace=True)
smokers_charge = pd.merge(smokers_charge, smokers_number)
percentage = round(smokers_charge.iloc[1, 1] / float(smokers_charge.iloc[0,1]), 2) * 100
print(smokers_charge)
print(f'The average amount of insurance charges of the {round(smokers_charge.iloc[0,2], 2)} non-smokers is {round(smokers_charge.iloc[0,1], 2)} dollars, and that of {smokers_charge.iloc[1,2]} smokers is {round(smokers_charge.iloc[1, 1])} dollars. On average, insurance charges of the smokers is about {percentage}% higher than that of the non-smokers.\n')

# Combining the "smoker" variable with another variable to find out if it creates a more dramatic result
smokers_sex = insurances.groupby(['smoker', 'sex']).charges.mean().reset_index()
print(smokers_sex)
print(f'The average insurance charges of a female non-smoker ($8762.29) was {round(8762.2973 / float(8087.204731) * 100 - 100, 2)}% higher than that of a male non-smoker ($8087.20). On the other hand, the average insurance charges of a male smoker ($33042.01) was {round(33042.005975 / float(30678.996276) * 100 - 100, 2)}% higher than that of a female smoker ($30679.0).\n')

# Beginning of Part 3: How do the insurance charges differ in different age groups? Is there wider spread among certain age groups? If there is, what could be the explanation of the wider spread? (ex. more smokers in certain age groups)
my_bins=[10, 19, 29, 39, 49,59, 69]
my_labels = ['10s', '20s', '30s', '40s', '50s', '60s']
insurances['age_group'] = pd.cut(insurances['age'], bins=my_bins, labels=my_labels)

age_group_charges_median = insurances.groupby('age_group').charges.median().reset_index()
age_group_charges_median.rename(columns={'charges': 'median_charges'},inplace=True)
age_group_charges_diff = insurances.groupby('age_group').charges.apply(lambda x: x.max() - x.min()).reset_index()
age_group_charges_diff.rename(columns={'charges': 'max_min_diff'}, inplace=True)
age_group_charges = pd.merge(age_group_charges_median, age_group_charges_diff)
print(age_group_charges)
print(f'The median of the insurances charges of different age groups increases as the age group moves from a younger group to an older group. Also, the biggest difference between max and min insurance charges exist in the 40s age group ($57177.21), which is {round(float(57177.21)/(38600.87) * 100 - 100,2)}% higher than that of the 10s age group ($38600.87). I suspect that this is due to the different proportion of smokers in each age group.\n')
age_group_smokers = insurances.groupby(['age_group', 'smoker']).charges.count().reset_index()
age_group_smokers_pivot = age_group_smokers.pivot(columns='smoker', index='age_group', values='charges').reset_index()
age_group_smokers_pivot.rename(columns={0: 'non_smoker', 1:'smoker'}, inplace=True)
age_group_smokers_pivot['smoker_proportion'] = round(age_group_smokers_pivot['smoker'] / (age_group_smokers_pivot['non_smoker'] + age_group_smokers_pivot['smoker']), 2)
print(age_group_smokers_pivot)
print(f'The smoker porportion turned out to be equally high among all age groups, and this evidently contradicts my claim that there exists a wider spread in insurance charges in certain age groups due to higher smoker proportion in the age group. Thus, not only should we make conclusions based on the "smoker" variable alone, but we should also take the "age" variable into account, since it plays a significant role in determining the insurance charges')



# Mean and median of the charges (two candidates for measuring the center of the distribution), without grouping with any other variables

# Charges_mean is approximately $13270 and charges_median is approximately $9382. This difference indicates that the distribution of the charges is possibly skewed to the right. We could examine this through the graphs
# charges_mean = insurances.charges.mean()
# charges_median = insurances.charges.median()

# insurance_cost_graph = plt.figure(1)
# plt.hist(insurances.charges, range=(0, 70000), bins=14, edgecolor='k', alpha=0.65)
# plt.title('Insurance Costs of U.S. Adult Population')
# plt.xlabel('Insurance Costs ($)')
# plt.ylabel('Number of people')

# plt.axvline(charges_mean, color='k', linestyle='dashed', linewidth=0.5)
# plt.axvline(charges_median, color='k', linestyle='dashed', linewidth=0.5)
# min_ylim, max_ylim = plt.ylim()
# plt.text(charges_mean*1.1, max_ylim * 0.9, f'Mean: {round(charges_mean, 2)}')
# plt.text(charges_median*1.1, max_ylim * 0.8, f'Median: {round(charges_median,2)}')

# plt.show()

# From this graph, we can understand that the distribution of the insurance cost is skewed to the right, and median makes a better indicator of showing the center of the distribution than does the mean.





