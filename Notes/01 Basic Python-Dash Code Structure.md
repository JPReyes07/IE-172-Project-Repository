# Basic Dash Code Template
This page details the most **basic** code structure in building a Dash App

## STEP 1: Import Dependencies

```
import dash
import webbrowser
import dash_bootstrap_components as dbc

from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
```

## STEP 2: Instantiate your App 
Create a dash object named "app" and give it a title. This will be reflected in your browser tab.

```
app = dash.Dash(__name__, external_stylesheets = ['assets/bootstrap.css'])
app.title = ' '
```

## STEP 3: Layout your App
Be mindful of the following:
* **CHILDREN PROPERTY**: Enclose multiple child components in a list. Properties such as color, ids, and hrefs should NOT be inside the list.
* **HIERARCHY**: html.Div > dbc.Card > dbc.CardHeader = dbc.CardBody
* **DOCS**: Consult with the online dbc docs for more info on dbc components

```
app.layout = html.Div(
    [
        dbc.Card(
            [
                dbc.Button(children=["Primary"],
                           color="primary",
                           className="me-1"),
            ]
        )
    ]
)
```

## STEP 3: Callbacks
A callback enables user interactivity within the dashboard app. 
It connects the Dash components to each other so that performing one action causes something else to happen.
It has 2 parts: a callback decorator and the callback function

### Callback Decorator
The callback decorator should be placed right above the callback function, and there must be no space between the decorator and the function. 
The decorator takes three main arguments: Output, Input, and State
* Each argument should direct to some component_id - the *id* attached to the element
* Each argument should change/take in a component_property - any property attached to an element

For demo: [Callback Structure in a dcc.Dropdown](https://dash.plotly.com/dash-core-components/dropdown)

```
@app.callback(
    [
        Output(component_id = '', component_property = '' )
    ],
    [
        Input(component_id = '', component_property = '' )
    ]    
)
```

### Callback Function 
A function is created to "make something happen" using the variables in the decorator
It is **required** for this specific function to have an argument

```
def function(argument):
    pass
```

## STEP 4: Running the App
Use this code to run the program

```
if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', autoraise=True)
    app.run_server(debug=False)
```

# What it looks like:

```python
import dash
import webbrowser
import dash_bootstrap_components as dbc

from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__, external_stylesheets = ['assets/bootstrap.css'])
app.title = ' '

app.layout = html.Div(
    [
        dbc.Card(
            [
                dbc.Button(children=["Primary"],
                           color="primary",
                           className="me-1"),
            ]
        )
    ]
)

@app.callback(
    [
        Output(component_id = '', component_property = '' )
    ],
    [
        Input(component_id = '', component_property = '' )
    ]    
)
def function(argument):
    pass

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', autoraise=True)
    app.run_server(debug=False)
```



---JPReyes07---
