import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import sys
sys.path.append("..")

from app import app

layout = html.Div([
    html.H3('App 4'),
    dcc.Dropdown(
        id='app-4-dropdown',
        options=[
            {'label': 'App 4 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-4-display-value'),
    dcc.Link('Go to App 2', href='/apps/app2')
])


@app.callback(
    Output('app-4-display-value', 'children'),
    Input('app-4-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)