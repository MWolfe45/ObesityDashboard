import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import sys
sys.path.append("..")
from constants import *
from app import app

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Citations", className="text-center"), className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(
                dbc.CardBody([
                html.H4("Literature:", className="card-title"),
                html.Ul([
                    dcc.Link(children=html.Li(ref1),href="https://www.who.int/health-topics/obesity#tab=tab_1", refresh=True),
                    dcc.Link(html.Li(ref2), href="https://news.usc.edu/135112/where-you-live-may-influence-whether-you-are-overweight-study-finds/", refresh=True),
                    dcc.Link(html.Li(ref3), href="https://www.cdc.gov/obesity/adult/causes.html", refresh=True),
                    dcc.Link(html.Li(ref4), href="https://www.cdc.gov/obesity/data/obesity-and-covid-19.html", refresh=True),
                    dcc.Link(html.Li(ref5), href="https://stop.publichealth.gwu.edu/sites/stop.publichealth.gwu.edu/files/documents/Fast%20Facts%20Cost%20of%20Obesity.pdf", refresh=True),
                    dcc.Link(html.Li(ref6), href="https://www.nejm.org/doi/full/10.1056/NEJMsa1909301", refresh=True),
                    dcc.Link(html.Li(ref7),href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6052856/", refresh=True)
                ]               
                        ),
                            ])
                            )
                    )
                ]),
        dbc.Row([
            dbc.Col(dbc.Card(
                dbc.CardBody([
                html.H4("Libraries Used:", className="card-title"),
                html.Ul(
                    [html.Li(lib1),
                    html.Li(lib2),
                    html.Li(lib3),
                    html.Li(lib4),
                    html.Li(lib5),
                    ],
                    className="card-text",
                        )
                            ])
                    ))
        ])
                    ])
                    ])
html.Link()