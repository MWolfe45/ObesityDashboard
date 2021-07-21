import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import sys

sys.path.append("..")

from app import app

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col()]
        dbc.Row([
            dbc.Col()
                ]),
        dbc.Row([
            dbc.Col()
                ]),
        dbc.Row([
            dbc.Col()],
            className="mb-5"))



