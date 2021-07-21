import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import sys
sys.path.append("..")

from app import app


layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Hi! Welcome to the VICTOR Dashboard", className="text-center"), className="mb-5 mt-5")
        ]),
        
        dbc.Row([
            dbc.Col(html.H5(children='Our group has assembled a tool which provides evidence-based recommendations for policy makers regarding the obesity   epidemic. '), className="mb-4")
        ]),
        
        dbc.Row([
            dbc.Col(html.H5(children='It consists of two main pages: EDA, which shows the insights gained through our exploratory analysis, and '
                                     "Tool, which uses these insights to develop a predictive model and allows users to explore recommendations for their specific population."), className="mb-5")
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(children=[html.H3(children='Get the original datasets used in this dashboard',
                                               className="text-center"),
                dbc.Row([dbc.Col(dbc.Button("Food Environment Atlas", href="https://www.ers.usda.gov/data-products/food-environment-atlas/data-access-and-documentation-downloads/", color="primary", block=True), className="mt-3"), 
                     dbc.Col(dbc.Button("Map the Meal Gap", href="https://www.feedingamerica.org/research/map-the-meal-gap/how-we-got-the-map-data", color="primary", block=True), className="mt-3")], justify="center")], body=True, color="dark", outline=True), width={'size':6, 'offset':12}, className="mb-4"), 
        
        dbc.Col(dbc.Card(children=[html.H3(children='Access the code used to build this dashboard', className="text-center"), dbc.Button("GitHub", href="https://github.com/Shevaughnth/team_115", color="primary", className="mt-3"),
                                       ], body=True, color="dark", outline=True), width={'size':6, 'offset':12}, className="mb-4"),
        ], className="mb-5")
    ])
])