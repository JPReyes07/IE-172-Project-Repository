import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import logging

app = dash.Dash(__name__, external_stylesheets=['assets/bootstrap.css'])

app.title = 'IE 172 Case'

# Make sure that callbacks are not activated when input elements enter the layout
app.config.suppress_callback_exceptions = True

# Acquire CSS locally
app.css.config.serve_locally = True

# To run the app offline
app.scripts.config.serve_locally = True

# To reduce logging 
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


