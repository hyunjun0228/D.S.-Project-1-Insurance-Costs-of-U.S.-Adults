import pandas as pd
import numpy as np


# In this project, I intend to analyze a sample of insurance costs of individuals across the United States, classified by age, sex, bmi, number of children, and inhabiting region. I would like to find out 1) the largest contributor to the cost of health insurance charges, 2) whether the region in which people inhabit affects the overall health insurance charges, and 3) as a 24-year old male with no children how much I would be charged for the insurance based on the given sample. 

# My hypothesis is that 1) the largest contributor is bmi, because it is a good indicator of one's health condition, which plays a huge role in determining the insurance costs in general. 2) I do not think that there would be a meaningful difference in insurance charges depending on where people live, and 3) I would probably pay less than 10000 for insurance.


# Here we go: 

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

# In search for the answer to Q1, I will calculate the correlation coefficient of each variable with the insurance charges

age_charges = insurances['age'].corr(insurances['charges'])
sex_charges = insurances['sex'].corr(insurances['charges'])
bmi_charges = insurances['bmi'].corr(insurances['charges'])
child_charges = insurances['children'].corr(insurances['charges'])
smoker_charges = insurances['smoker'].corr(insurances['charges'])
region_charges = insurances['region'].corr(insurances['charges'])

# Creating a table of variables against the correlation coefficients to easily compare the values
charges_corr_df = pd.DataFrame({'variables': ['age', 'sex', 'bmi', 'child', 'smoker', 'region'], 'corr_coeff': [age_charges, sex_charges, bmi_charges, child_charges, smoker_charges, region_charges]})
max_var = charges_corr_df[charges_corr_df.corr_coeff == charges_corr_df.corr_coeff.max()]
max_var_name = max_var['variables']
max_var_co = max_var['corr_coeff']
print(charges_corr_df, '\n')

print(f'The variable that had the maximum correlation coefficient with regard to the insurance charges was "smoker", which had a correlation coefficient of 0.787251, significantly higher than that of others')










