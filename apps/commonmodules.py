from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from app import app

navlink_style = {
    'color': '#E0E5E9',
    'font-family': 'Helvetica, sans-serif',
    'font-weight': 'bold',
}

primarynav = dbc.Nav(
    [
        dbc.NavLink('Dashboard',
                    href='/dashboard',
                    style=navlink_style
        ),

        dbc.NavLink('Patient Records',
                    href='/patient/records',
                    style=navlink_style
        ),

        dbc.NavLink('Patient Registration',
                    href='/patient/registration?mode=add',
                    style=navlink_style
        ),

        dbc.NavLink('Queue', 
                    href='/queue', 
                    style=navlink_style
        ),

        dbc.NavLink('Medicine Inventory',
                    href='/medicine',
                    style=navlink_style
        ),

        dbc.NavLink('Payment',
                    href='/payment',
                    style=navlink_style
        )
    ],
    vertical=True,
    pills=True,
    style={'background-color': '#0051A1', 'padding': '10px', 'flex': 1}
)

sidebar = html.Div(
    [
        html.Div([primarynav], 
                 style={
                     'display': 'flex', 
                     'flexDirection': 'column', 
                     'background-color': '#f8f9fa', 
                     'height': '200vh'
                }
        ),
    ]
)
