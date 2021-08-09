#######################################################
# Main APP definition.
#
# Dash Bootstrap Components used for main theme and better
# organization.
#######################################################

import dash
import dash_bootstrap_components as dbc

import os

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.SANDSTONE], update_title='Loading...')
server = app.server

request_path_prefix = None
workspace_user = os.getenv('JUPYTERHUB_USER')  # Get DS4A Workspace user name
if workspace_user:
    request_path_prefix = '/user/' + workspace_user + '/proxy/8050/'

# app = dash.Dash(__name__,
#                 requests_pathname_prefix=request_path_prefix,
#                 external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# We need this for function callbacks not present in the app.layout
app.config.suppress_callback_exceptions = True