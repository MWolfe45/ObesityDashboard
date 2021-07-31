import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import sys
sys.path.append("..")

from app import app

portrait_deck = dbc.CardDeck([
dbc.Card([
                    dbc.CardImg(src="/assets/angela.png", top=True),
                    dbc.CardBody([
                html.H4("Angela Brown", className="card-title"),
                html.P(
                    "Senior ITSM Business Analyst",
                    className="card-text",
                ),
            ])]),
dbc.Card([
                dbc.CardImg(src="/assets/anthony.png", top=True),
                dbc.CardBody([
                html.H4("Anthony Hernandez", className="card-title"),
                html.P(
                    "Financial Accountant",
                    className="card-text",
                ),
            ])]),
dbc.Card([
                dbc.CardImg(src="/assets/shevaughn.png", top=True),
                dbc.CardBody([
                html.H4("Shevaughn Holness", className="card-title"),
                html.P(
                    "Team Lead - "
                    "Student researcher, Smith College, Wright Lab",
                    className="card-text",
                ),
            ])]),
dbc.Card([
                dbc.CardImg(src="/assets/matt.png", top=True),
                dbc.CardBody([
                html.H4("Matthew Wolfe", className="card-title"),
                html.P(
                    "Researcher, Math tutor, Chess enthusiast",
                    className="card-text",
                ),
            ])])

]
)



layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("About Team 115", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row(portrait_deck)
    ])
])