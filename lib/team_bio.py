import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import sys
sys.path.append("..")

from app import app

layout = html.Div([
    html.H3('App 3'),
    dcc.Dropdown(
        id='app-3-dropdown',
        options=[
            {'label': 'App 3 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-3-display-value'),
    dcc.Link('Go to App 2', href='/apps/app2')
])


@app.callback(
    Output('app-3-display-value', 'children'),
    Input('app-3-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)