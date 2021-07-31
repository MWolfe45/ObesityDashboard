  
import plotly.graph_objects as go

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import sys
from app import app
import plotly.express as px
import json
from urllib.request import urlopen

sys.path.append("..")

from constants import obesity_subset, label_dict
from app import app

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

#Importing and preparing dataframes for each visualization
df = pd.read_csv('data/eda_dataframe.csv')

#Define histogram figure
figdis = px.histogram(df, x=df['obesity_rate'],marginal='rug', hover_data=df.columns,color_discrete_sequence=['Plum'])
figdis.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      template = "seaborn",
                      margin=dict(t=0))

#Define stacked bar graph figure

figstacked = px.bar(obesity_subset,x=['pop_white','pop_black', 'pop_native_american', 'pop_asian', 'pop_nhpi', 'pop_multi', 'pop_nonwhite_hispanic'], y='rank', orientation='h')
figstacked.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      template = "seaborn",
                      margin=dict(t=0))


#EXPLORATORY DATA ANALYSIS PAGE LAYOUT
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children='American Obesity: Exploratory Data Analysis'), className="mb-2")]),
        
        dbc.Row([
            dbc.Col(html.H6(children='Visualising national trends'), className="mb-4")
                ]),
        
        dbc.Row([
            dbc.Col(dcc.RadioItems(id='obesity_or_health_index',
                options=[
                    {'label':'Obesity', 'value':'obesity_rate'},
                    {'label':'Health Index', 'value':'healthy_access_score'}
                ],
                value= 'obesity_rate',
                labelStyle={'display':'block'}
            ))]),
        
        dbc.Row(dbc.Card(children=dbc.Col(dcc.Graph(id='map_obesity_or_health_index')), style={'width':'66rem'})),
        
        dbc.Row(
            [dbc.Card(children=dbc.Col(dcc.Graph(figure=figdis)), style={'width':'33rem'}),
            dbc.Card(children=dbc.Col(dcc.Graph(id='region_bplot')), style={'width':'33rem'})]),
        
        dbc.Row([
        dbc.Col(dbc.Card(html.H3(children='Variable Correlation Analysis: Food Access and Income',
                                 className="text-center text-light bg-primary"), body=True, color="primary")
        , className="mt-4 mb-4")]),
        
        dbc.Row(
            [dbc.Col(dcc.Dropdown(id='access_dropdown',
                                options=[{'label':'Grocery', 'value':'grocery_per1000'},
                                 {'label':'Superstore', 'value':'super_per1000'},
                                 {'label':'Convenience', 'value':'convenience_per1000'},
                                 {'label':'Specialty Stores', 'value':'specialty_per1000'}
], value='grocery_per1000', style={'width':'15rem'})),
            
             dbc.Col(dcc.Dropdown(id='income_dropdown',
                                options=[{'label':'Obesity', 'value':'obesity_rate'},
                                 {'label':'Healthy Access Index', 'value':'healthy_access_score'}
], value='obesity_rate', style={'width':'15rem'})  
                                 )]),
        
        dbc.Row(
            [dbc.Card(
     children=dbc.Col(dcc.Graph(id='access_scatter')), style={'width':'35rem'}),
        dbc.Card(children=dbc.Col(dcc.Graph(id='income_plots')), style={'width':'35rem'})]),
        
        dbc.Row(dbc.Card(html.H3(children='Impact Across Racial Demographics',
                                 className="text-center text-light bg-primary"), body=True, color="primary")),
        
        dbc.Row(dbc.Card(dcc.Graph(figure=figstacked), style={'width':'100rem'})),
        
        dbc.Row(dbc.Col(dcc.Dropdown(id='race_dropdown', options=[
            {'label':label_dict['percent_white'],'value':'percent_white'},{'label':label_dict['percent_black'],'value':'percent_black'},{'label':label_dict['percent_native_american'],'value':'percent_native_american'},{'label':label_dict['percent_asian'],'value':'percent_asian'},{'label':label_dict['percent_multi'],'value':'percent_multi'},{'label':label_dict['percent_nonwhite_hispanic'],'value':'percent_nonwhite_hispanic'}
        ],value='percent_white', style={'width':'15rem'}) )),
        
        dbc.Row(dbc.Col(dbc.Card(dcc.Graph(id='race_scatter'), style={'width':'33rem'})))
                 ])
                 ])



#APP CALLBACK FUNCTIONS


#Callback function for cloropleth map
@app.callback(Output('map_obesity_or_health_index','figure'),
             [Input('obesity_or_health_index', 'value')])

def update_map(choice):
    
    
    if choice == 'obesity_rate':
        scale_a, scale_b = 0, 50 
        title_m = 'US Obesity Rate Distribution (2017)'
    elif choice == 'healthy_access_score':
        scale_a, scale_b = 0, 12
        title_m = 'US Healthy Food Access Index (2017)'
        
    merged_df = df.copy()
    merged_df['fips'] = merged_df['fips'].astype(str).str.zfill(5)
    obesity_map = px.choropleth_mapbox(merged_df, geojson=counties, locations=merged_df.fips, color=merged_df[choice], hover_name=merged_df.county, hover_data = {'obesity_rate':True, 'percent_white':True,'percent_black':True,'percent_asian':True,'percent_nhpi':True,'percent_multi':True,'percent_native_american':True,'percent_nonwhite_hispanic':True,}, color_continuous_scale="Viridis_r", range_color=(scale_a,scale_b), mapbox_style = "carto-positron", zoom=3, opacity=0.65, center = {"lat": 39.0902, "lon": -101.7129},labels={'obesity_rate':'Obesity Rate', 'healthy_access_score':'Healthy Food Access'})

    obesity_map.update_layout(margin={"r":30,"t":30,"l":30,"b":30})
    obesity_map.update_layout(title_text = title_m, title_font_family="Arial", title_font_color="black",font_family="Arial",font_color="black",legend_title_font_color="green")
    #https://stackoverflow.com/questions/58166002/how-to-add-caption-subtitle-using-plotly-method-in-python
  
    obesity_map.update_layout(annotations=[
           go.layout.Annotation(
                showarrow=False,
                text='Note: 2017 data was used as it is the most recent year that contains robust food related data',
                xanchor='right',
                x=1,
                xshift= 100,
                yanchor='top',
                y=0.00,
                font=dict(
                    family="Courier New, monospace",
                    size=13,
                    color="#000000"
                )
            )])
    obesity_map['layout']['xaxis'].update(side='top')
    return obesity_map

#Callback function for regional boxplots
@app.callback(Output('region_bplot', 'figure'),
              [Input('obesity_or_health_index', 'value')])

def update_box(choice):
    df4 = df.copy()
    fig = px.box(x=df4['region'], y=df4[choice],labels={
                     "x": "Region",
                     "y": str(label_dict[choice]),
                 },color_discrete_sequence=['Teal'])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      template = "seaborn",
                      margin=dict(t=5))
    return fig


#Callback function for food access scatterplots
@app.callback(Output('access_scatter','figure'),
             [Input('access_dropdown', 'value')])

def update_scatter(choice):
    df2 = df.copy()
    fig = px.scatter(x=df2[choice], y=df2['obesity_rate'],
                     labels={
                     "x": str(label_dict[choice]),
                     "y": "Obesity Rate"})

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      template = "seaborn",
                      margin=dict(t=0))
    return fig

#Callback function for income visualization
@app.callback(Output('income_plots','figure'),
             [Input('income_dropdown', 'value')])
    
def update_box2(choice):
    df3 = df.copy()
    fig = px.box(x=df3['class_category'], y=df3[choice], labels={
                     "x": 'Income Classifcation',
                     "y": str(label_dict[choice])},
                     color_discrete_sequence=['Teal']
                 )
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      template = "seaborn",
                      margin=dict(t=5))
    return fig


@app.callback(Output('race_scatter','figure'),
             [Input('race_dropdown','value')])

def update_scatter2(choice):
    df5 = df.copy()
    fig = px.scatter(x=df5[choice], y=df5['obesity_rate'], labels={
                     "x": str(label_dict[choice]),
                     "y": "Obesity Rate"})
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  template = "seaborn",
                  margin=dict(t=0))
    return fig