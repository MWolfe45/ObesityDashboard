import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import sys
sys.path.append("..")

from app import app
from model import lin_reg
from constants import states_dicts, county_dicts, county_select, obesity_df

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Predictive Modeling", className="text-center"), className="mb-5 mt-5")
        ]),
        
        dbc.Row([
            dbc.Col(html.H5(children='Our model is based on the variables described below. Here, you can choose a specific county from the dropdown menu to populate the fields corresponding to relevant variables.'), className="mb-4")
        ]),
        
        dbc.Row([
            dbc.Col(html.H5(children="To operate, please choose your specific US county from the dropdown menu. The variable fields will be populated with your county's specifc figures, which you can then alter to predict the effects of implemented changes."), className="mb-5")
        ]),
        
        dbc.Row([
            dbc.Col(dcc.Dropdown(id='county_selection', options=county_dicts, placeholder='Select your county'),style={'width':'20%'}),
            dbc.Col(dcc.Dropdown(id='state_selection', options=states_dicts, placeholder= 'Select your state'),style={'width':'20%'})],
        ),
        dbc.Row(
            [dbc.Col(html.Label('Fips code: ')),
             dbc.Col(html.Div(id='fips-output-container'))]
        ),
        
        dbc.Row([dbc.Col(dbc.Card([
        dbc.Row(
            [dbc.Col(html.Label('Superstores per 1000: ')),
            dbc.Col(html.Div(id='superstore_var'))]
        ),
        dbc.Row(
            [dbc.Col(html.Label('Grocery Stores per 1000: ')),
            dbc.Col(html.Div(id='grocery_var'))]
        ),
        dbc.Row(
            [dbc.Col(html.Label('Convenience Stores per 1000: ')),
            dbc.Col(html.Div(id='convenience_var'))]
        ),
        dbc.Row(
            [dbc.Col(html.Label('Specialty Stores per 1000: ')),
            dbc.Col(html.Div(id='specialty_var'))]
        ),
        dbc.Row(
            [dbc.Col(html.Label('Fast Food Restaurants per 1000: ')),
            dbc.Col(html.Div(id='fast_var'))]
        ),
        dbc.Row(
            [dbc.Col(html.Label('Full Service Restaurants per 1000: ')),
            dbc.Col(html.Div(id='full_var'))]
        ),
        dbc.Row(
            [dbc.Col(html.Label('School Lunch Programs: ')),
            dbc.Col(html.Div(id='lunch_var'))]
        ),
        dbc.Row(
            [dbc.Col(html.Label('Percent Without Car Access: ')),
            dbc.Col(html.Div(id='no_car_var'))]
        ),
        dbc.Row(
            [dbc.Col(html.Label('Percent of Farmers Markets that Accept WIC: ')),
            dbc.Col(html.Div(id='farm_wic_var'))]
        ),
        dbc.Row(
            [dbc.Col(html.Label('Percent of Farmers Market that Accept Credit: ')),
            dbc.Col(html.Div(id='farm_cred_var'))]
        ),
        dbc.Row(
            [dbc.Col(html.Label('Percent of Farmers Markets that Sell Fresh Vegetables: ')),
            dbc.Col(html.Div(id='farm_veg_var'))]
        ),
            
        dbc.Row(
            [dbc.Col(html.Label('Total Unemployment: ')),
            dbc.Col(html.Div(id='unem_var'))]
        )
        ], style={'margin-top':'25px'})),
        dbc.Col(
            [dbc.Row(dbc.Card([html.Label('Actual Obesity Rate: '),html.Div(id='obesity_actual')], style={'margin-top':'25px', 'width':'600px'})),
            dbc.Row(dbc.Card())
            ])
                
                ])
    ])
])

# Callback for county selections based on state
@app.callback(Output('county_selection','options'),
             [Input('state_selection', 'value')])

def update_options(choice):
    
    if choice == '--Reset Selection--':
        if not choice:
            raise PreventUpdate
        return county_dicts
    
    else:
        if not choice:
            raise PreventUpdate
        new_df = county_select.copy()
        new_df = new_df[new_df['state']==choice]

        new_county_list = new_df['county_names'].to_list()
        new_county_dicts = [{'label':'--Reset Selection--', 'value':'--Reset Selection--'}]
        for county in new_county_list:
            new_county_options = {'label':county, 'value':county}
            new_county_dicts.append(new_county_options)

        return new_county_dicts

# Callback for state selections based on county
@app.callback(Output('state_selection','options'),
             [Input('county_selection', 'value')])

def update_options(choice):
    
    if choice== '--Reset Selection--':
        if not choice:
            raise PreventUpdate
        return states_dicts
    
    else:
        if not choice:
            raise PreventUpdate

        new_df = county_select.copy()
        new_df = new_df[new_df['county_names']==choice]

        new_state_list = new_df['state'].to_list()
        new_state_dicts = [{'label':'--Reset Selection--', 'value':'--Reset Selection--'}]
        for state in new_state_list:
            new_state_options = {'label':state, 'value':state}
            new_state_dicts.append(new_state_options)



        return new_state_dicts
    
# Callback for state selections based on county
@app.callback(Output('fips-output-container','children'),
             Input('county_selection', 'value'),
             Input('state_selection', 'value'),
)

def show_fips(county, state):
    
    
    new_df = county_select.copy()
    new_df = new_df[new_df['state']==state]
    new_df = new_df[new_df['county_names']==county]
    if new_df.empty:
        return 'No county selected'
    else:
        code = new_df['fips'].iloc[0]
    return code


@app.callback(Output('obesity_actual', 'children'),
              Output('superstore_var', 'children'),
              Output('grocery_var', 'children'),
              Output('convenience_var', 'children'),
              Output('specialty_var', 'children'),
              Output('fast_var', 'children'),
              Output('full_var', 'children'),
              Output('lunch_var', 'children'),
              Output('no_car_var', 'children'),
              Output('farm_wic_var', 'children'),
              Output('farm_cred_var', 'children'),
              Output('farm_veg_var', 'children'),
              Output('unem_var', 'children'),
             Input('fips-output-container', 'children'))

def update_superstore(fips):
    new_df = obesity_df.copy()
    new_df = new_df[new_df['fips']==fips]
    superstore_df = new_df['super_per1000']
    if new_df.empty:
        return '','','','','','','','','','','','',''

    superstore_var = superstore_df.iloc[0]
    grocery_df = new_df['grocery_per1000']
    grocery_var = grocery_df.iloc[0]
   
    convenience_df = new_df['convenience_per1000']
    convenience_var = convenience_df.iloc[0]
    
    specialty_df = new_df['specialty_per1000']
    specialty_var = specialty_df.iloc[0]
    
    fast_df = new_df['fast_food_per1000']
    fast_var = fast_df.iloc[0]
    
    full_df = new_df['full_service_per1000']
    full_var = full_df.iloc[0]
    
    lunch_df = new_df['school_lunch_prog_17']
    lunch_var = lunch_df.iloc[0]
    
    no_car_df = new_df['percent_no_car']
    no_car_var = no_car_df.iloc[0]
    
    farm_wic_df = new_df['pct_fm_accept_wic']
    farm_wic_var = farm_wic_df.iloc[0]
    
    farm_cred_df = new_df['pct_fm_credit']
    farm_cred_var = farm_cred_df.iloc[0]
   
    farm_veg_df = new_df['pct_fm_sell_frveg']
    farm_veg_var = farm_veg_df.iloc[0]
    
    unem_df = new_df['total_unemployment_rate_over_16']
    unem_var = unem_df.iloc[0]
    
    ob_df = new_df['obesity_rate']
    ob_var = ob_df.iloc[0]
    return ob_var, superstore_var, grocery_var, convenience_var, specialty_var, fast_var, full_var, lunch_var, no_car_var, farm_wic_var, farm_cred_var, farm_veg_var, unem_var


        