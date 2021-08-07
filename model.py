# loading in necessary packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as sm
import statsmodels.api as sma
import sklearn
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn import model_selection
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, cross_validate, KFold, GridSearchCV, ShuffleSplit
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline


# loading in obesity data from our EDA and dropping columns that have too many null values. Additonally, hawaii and alaska
# had no inputs for obesity rates which are necessary for our model. Thus, they were dropped. 
# furthermore, obesity proxies that went into creating healthy score access was also dropped.
obesity_df = pd.read_csv("data/obesity_eda.csv")
obesity_df[~obesity_df.region.str.contains('O')]
obesity_df = obesity_df.drop(columns = ['primary_minority', 'supercenter_access_score', 'grocery_access_score', 'fullservice_access_score', 'farmersmarket_access_score', 'wic_available_per1000', 'snap_bens_per1000'])
obesity_df['percent_other'] = obesity_df['percent_nhpi'] + obesity_df['percent_multi']

# Loading in car access data
car_access_df = pd.read_csv("data/car_access_2017.csv")
unemployment_df = pd.read_csv("data/unemployment _2017.csv")
unemployment_df = unemployment_df[["fips","total_unemployment_rate_over_16", "total_educated_some_college_or_associates_25_64", "pop_est_over_16"]]
unemployment_df["some_college_rate"] = unemployment_df["total_educated_some_college_or_associates_25_64"]/unemployment_df["pop_est_over_16"]
unemployment_df = unemployment_df[["fips","total_unemployment_rate_over_16", "some_college_rate"]]

# Merged the two data sets
obesity_df = pd.merge(obesity_df, car_access_df, how = 'left', on = 'fips')
obesity_df = pd.merge(obesity_df, unemployment_df, how = 'left', on = 'fips')
obesity_df = obesity_df.drop(columns = ['percent_asian_low_access_15','percent_pop_low_access_15', 'percent_low_income_low_access_15',
       'percent_snap_low_access_15', 'percent_child_low_access_15',
       'percent_white_low_access_15', 'percent_nhna_low_access_15','nhpi_low_access_15', 'percent_no_car_low_access_15', 'percent_senior_low_access_15',
       'percent_black_low_access_15', 'percent_hispanic_low_access_15',
       'percent_nhpi_low_access_15', 'percent_multiracial_low_access_15'])


# made some numerical variables easier to read 
obesity_df['percent_no_car'] = obesity_df['percent_no_car'] * 100
obesity_df['pop_estimate'] = obesity_df['pop_estimate']/1000


# Making our food dessert categorical variable. 
conditions = [(obesity_df["fi_rate"] > 15) & (obesity_df["healthy_access_category"] != 'high'), 
              (obesity_df["fi_rate"] <= 15)]
values = [1, 0]

obesity_df["food_dessert"] = np.select(conditions, values)

# dropping any remaining null values so our model can work
obesity_df = obesity_df.dropna()

# creating dummy variables; the VIF test does not take in categorical variables
obesity_df['region'] = obesity_df['region'].map({'N':1, 'M':2, 'S':3, 'W':4})
obesity_df['healthy_access_category'] = obesity_df['healthy_access_category'].map({'low':1, 'medium':2, 'high':3})
obesity_df['class_category'] = obesity_df['class_category'].map({'low_income':1, 'lower_mid_class':2, 'mid_class':3, 'highest_income': 4})



pot_vars = obesity_df[['grocery_per1000', 'super_per1000',
       'convenience_per1000', 'specialty_per1000', 
       'fast_food_per1000', 'full_service_per1000', 'school_lunch_prog_17',
       'percent_no_car', 'total_unemployment_rate_over_16','pct_fm_accept_wic', 'pct_fm_credit', 
       'pct_fm_sell_frveg']]


# code was modeled and influenced by DS4A (Correlation One) material. 
formula= 'obesity_rate ~ super_per1000 + convenience_per1000 + specialty_per1000 + pct_fm_accepting_snap + pct_fm_credit + fast_food_per1000 + full_service_per1000 + pop_estimate + percent_no_car + total_unemployment_rate_over_16'
model_final = sm.ols(formula = formula, data = obesity_df)
lin_reg = model_final.fit()
# print(lin_reg.summary())


# obtain user input to put into a new dataframe that we will then use to predict obesity rates
# fips = float(input())
# super_input = float(input())
# convenience_store = float(input())
# specialty_store = float(input())
# fm_snap = float(input())
# fm_credit = float(input())
# fast_food = float(input())
# restaurant = float(input())
# no_car = float(input())
# unemployment = float(input())

# population = obesity_df.loc[obesity_df['fips'] == fips, 'pop_estimate'].iloc[0]


# we then create a new dataframe with the variables above so we can input it into the model prediction
# new_vals = pd.DataFrame({'super_per1000': [super_input], 'convenience_per1000': [convenience_store],'specialty_per1000': [specialty_store], 'pct_fm_accepting_snap': [fm_snap],'pct_fm_credit': [fm_credit], 'fast_food_per1000': [fast_food], 'full_service_per1000': [restaurant], 'pop_estimate': [population],'percent_no_car': [no_car], 'total_unemployment_rate_over_16': [unemployment]})


# the new variables are put into the new model and then the second value is the predicted obesity in the county based upon changes
# xnew = sma.add_constant(new_vals)
# ynewpred =  lin_reg.predict(xnew)
# ynewpred