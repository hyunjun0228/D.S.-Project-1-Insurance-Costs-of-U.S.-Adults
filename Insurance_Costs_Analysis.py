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
print(f'The variable that had the maximum correlation coefficient with regard to the insurance charges was "smoker", which had a correlation coefficient of 0.787251, significantly higher in comparison to that of other variables.\n')
print('The variable "region" had the minimal degree of correlation with insurance charges; it had a value of 0.006208, significantly lower in comparison to that of other variables.\n')
# End of Part 1

# Beginning of Part 2: Can the 'strongest factor' combined with other factors create a more dramatic result? Could there be a confounding variable that exists in our dataset?

# Grouping the dataset with "smoker" variable (strongest factor); there are 1064 non-smokers and 274 smokers in our dataset

smokers_charge = insurances.groupby('smoker').charges.mean().reset_index()
smokers_number = insurances.groupby('smoker').age.count().reset_index()
smokers_number.rename(columns={'age': 'num_people'}, inplace=True)
smokers_charge = pd.merge(smokers_charge, smokers_number)
percentage = round(smokers_charge.iloc[1, 1] / float(smokers_charge.iloc[0,1]), 2) * 100
print(smokers_charge)
print(f'The average amount of insurance charges of the {round(smokers_charge.iloc[0,2], 2)} non-smokers is {round(smokers_charge.iloc[0,1], 2)} dollars, and that of {smokers_charge.iloc[1,2]} smokers is {round(smokers_charge.iloc[1, 1])} dollars. On average, insurances charges of the smokers is about {percentage}% higher than that of the non-smokers.')

# Combining the "smoker" variable with another variable to find out if it creates a more dramatic result
smokers_sex = insurances.groupby(['smoker', 'sex']).charges.mean().reset_index()
print(smokers_sex)
smokers_child = insurances.groupby(['smoker', 'children']).charges.mean().reset_index()
smokers_region = insurances.groupby(['smoker', 'region']).charges.mean().reset_index()




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





