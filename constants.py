import pandas as pd



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


# HEre we are creating a graphic that showcases the proportion of races that live within each obesity category. 

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