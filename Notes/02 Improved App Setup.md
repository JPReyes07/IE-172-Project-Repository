# Improved App Setup

There is another way to instantiate our app object so it can be reused multiple times on different app elements

## Create ONE ```app.py``` file and import it instead 

```python
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import logging

app = dash.Dash(__name__, external_stylesheets=['assets/bootstrap.css'])

app.title = 'IE 172 Case'

# To make sure that callbacks are not activated when input elements enter the layout
app.config.suppress_callback_exceptions = True

# To acquire CSS locally (i.e., bootstrap.css in assets folder)
app.css.config.serve_locally = True

# To run the app offline
app.scripts.config.serve_locally = True

# To reduce logging 
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
```

Now, when trying to create an app page, just import app with:

```python
from app import app
# from <<.py file>> import <<declared_variable>>
```

in the .py file of the app page
