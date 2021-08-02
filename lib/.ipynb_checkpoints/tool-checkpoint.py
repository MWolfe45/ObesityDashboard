import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import sys
sys.path.append("..")

from app import app

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
        
        dbc.Row(
            dbc.Col(dcc.Dropdown(),style={'width':'20%'}),
        ),
        dbc.Row(
            dbc.Col(dcc.Input(style={'margin-top':'25px'}))
        ),
        dbc.Row(
            dbc.Col(dcc.Input(style={'margin-top':'25px'}))
        ),
        dbc.Row(
            dbc.Col(dcc.Input(style={'margin-top':'25px'}))
        ),
        dbc.Row(
            dbc.Col(dcc.Input(style={'margin-top':'25px'}))
        ),
        dbc.Row(
            dbc.Col(dcc.Input(style={'margin-top':'25px'}))
        )
    ])
])
