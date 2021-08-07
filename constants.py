import pandas as pd
import numpy as np


# Constants for References Page
ref1 = "World Health Organization, Obesity."

ref2 = "Gersema, Emily. 'Where you live may influence whether you are overweight, study finds.'"

ref3 = "Center for Disease Control, Adult Obesity Causes and Consequences. "

ref4 = "Center for Disease Control, Obesity, Race/Ethnicity, and COVID-19. "

ref5 = "Strategies to Overcome and Prevent (STOP) Obesity Alliance. “Fast Facts: The Cost of Obesity”"

ref6 = "Ward, Zachary M.P.H., et al. “Projected U.S. State Level Prevalence of Adult Obesity and Severe Obesity."

ref7='Polonsky, Heather M. and Sarwer, David B.”The Psychosocial Burden of Obesity.”'

lib1 = "pandas"
lib2 = "plotly"
lib3 = "dash"
lib4 = "sci-kit learn"
lib5 = "numpy"

# Constant Labels for EDA Page
label_dict={'grocery_per1000':'Grocery Access','super_per1000':'Superstore Access','convenience_per1000':'Convience Store Access','specialty_per1000':'Specialty Store Access', 'obesity_rate':'Obesity Rate','healthy_access_score':'Healthy Food Access Score','percent_white':'Percent White', 'percent_black':'Percent Black','percent_native_american':'Percent Native American','percent_asian':'Percent Asian','percent_multi':'Percent Multi-racial','percent_nonwhite_hispanic':'Percent Nonwhite Hispanic'
           }


# Here we are creating a graphic that showcases the proportion of races that live within each obesity category. 

demo = pd.read_csv("data/demo_pop_data_2017.csv")
merged_df = pd.read_csv("data/eda_dataframe.csv")
ob_df = pd.merge(merged_df, demo, how='left', on='fips')
obesity_subset = ob_df[['obesity_category', 'pop_white', 'pop_black', 'pop_native_american', 'pop_asian', 'pop_nhpi', 'pop_multi', 'pop_nonwhite_hispanic']]
obesity_subset = obesity_subset.groupby('obesity_category').sum()

obesity_subset = obesity_subset.T

obesity_subset['low'] = obesity_subset['low'] / obesity_subset['low'].sum()
obesity_subset['med'] = obesity_subset['med'] / obesity_subset['med'].sum()
obesity_subset['high'] = obesity_subset['high'] / obesity_subset['high'].sum()

obesity_subset = obesity_subset.drop(columns='0')
obesity_subset = obesity_subset.T
obesity_subset =  obesity_subset.reset_index()
obesity_subset = obesity_subset.sort_values(by = 'obesity_category')
new_list = ['3', '1','2']
obesity_subset['rank']  = new_list * 1
obesity_subset = obesity_subset.sort_values(by = 'rank', ascending = False)
obesity_subset['rank'].replace({"1":"low","2":"med","3":"high"}, inplace = True)
#https://matplotlib.org/stable/api/colors_api.html?highlight=color#module-matplotlib.colors
colors = ["#BF6380", "#E3914D","#E3E14D","#22908C","#4B0082","#0277C9","#7463BF"] 
# osp = obesity_subset.plot(
#     x='rank',
#     color=colors,
#     kind = 'barh',
#     stacked = True,
#     title = 'Proportion of Race Demographic Within Obesity Categories',
#     mark_right = True,
#     figsize=(20,10)
#     )

# osp.set_xlabel("Proportion of Race Demographic")
# osp.set_ylabel("Obesity Category")
# plt.tight_layout()


# Making Dataframe for the selection of the right fips for county/state combinations
county_select = pd.DataFrame()
county_select['county_names'] = merged_df['county']
county_select['state'] = merged_df['state']
county_select['fips'] = merged_df['fips']

county_list = merged_df['county'].to_list()
states_list = merged_df['state'].to_list()
states_list = list(dict.fromkeys(states_list))


county_dicts = [{'label':'--Reset Selection--', 'value':'--Reset Selection--'}]
states_dicts = [{'label':'--Reset Selection--', 'value':'--Reset Selection--'}]
for county in county_list:
    county_options = {'label':county, 'value':county}
    county_dicts.append(county_options)

for state in states_list:
    states_options = {'label':state, 'value':state}
    states_dicts.append(states_options)

    
    
    
    
########################################################################################################################################    
# Setting up Dataframe for modeling page

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
