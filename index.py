import ast
import dash
import webbrowser
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app

from apps import commonmodules as cm

from apps.patient import patient_records
from apps.patient import patient_registration
from apps.patient import patient_profile

from apps import queue
from apps import payment
from apps import medicine_inventory
from apps import dashboard

CONTENT_STYLE = {
    'margin-top': '2em',
    'margin-left': '1em',
    'margin-right': '1em',
    'padding': '1em 1em'
}

image_path = "assets/GyneCare.png"

login_layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(dbc.CardImg(src=image_path, alt="Header Image",top=True, style={'width': '100%', 'object-fit': 'contain'})
                                       ),
                        dbc.CardBody(
                            [
                                dbc.Form(
                                    [
                                        html.Label("Username", style={'marginLeft':'1.2em'}),
                                        html.Div(
                                            dbc.Input(
                                                id='username-input',
                                                type='text',
                                                placeholder='Username',
                                                style={
                                                    'background-color': '#E0E5E9',
                                                    'font-family': 'Verdana, sans-serif',
                                                    'borderRadius': 12,
                                                    'width': '330px',
                                                    'marginLeft':'1.2em',
                                                },
                                            ),
                                            className='text-center' 
                                        ),
                                    ]
                                ),

                                html.Br(),

                                dbc.Form(
                                    [
                                        html.Label("Password", style={'marginLeft':'1.2em'}),
                                        html.Div(
                                            dbc.Input(
                                                id='password-input',
                                                type='password',
                                                placeholder='Password',
                                                style={
                                                    'background-color': '#E0E5E9',
                                                    'font-family': 'Verdana, sans-serif',
                                                    'borderRadius': 12,
                                                    'width': '330px',
                                                    'marginLeft':'1.2em',
                                                },
                                            ),
                                            className='text-center' 
                                        ),
                                    ]
                                ),

                                html.Br(),
                                
                                dbc.Button('Login', id='login-button', style={'width': '100px',
                                                    'marginLeft':'8em'}),
                                html.Div(id='login-status')
                            ]
                        )
                    ],
                    style={'width': '400px'},
                    className='mx-auto'  
                ),
                width={'size': 6, 'offset': 3},  
                style={'marginTop': '15vh'}  
            )
        )
    ],
    style={'height': '100vh'}  
)



main_layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),
        dbc.Row(
            [
                dbc.Row(
                    [
                        html.Div(
                            html.Img(
                                src = 'assets/GyneCare.png',
                                style = {
                                    'width': 'auto', 
                                    'height': '110px'
                                }
                            ),
                            style={
                                'position': 'absolute',
                                'top': 0,
                                'left': 0,
                                'zIndex': 1,
                            }
                        ),
                       
                        html.Div(
                            html.H1(
                                'GynCare',
                                style={
                                    'font-family': 'Helvetica, sans-serif',
                                    'fontWeight': 'bold'
                                }
                            ),
                            style={
                                'background': 'linear-gradient(0deg, rgba(0,81,161,1) 0%, rgba(159,195,231,1) 49%, rgba(255,255,255,1) 100%)',
                                'height': '75px',
                                'padding': '5px 120px 5px',
                                'position': 'relative',
                                'zIndex': 0, 
                            }
                        ),

                        html.Div(
                            html.H6(
                                'Martinez Memorial Hospital',
                                style = {
                                    'font-family': 'Helvetica, sans-serif',
                                }
                                ),
                            style={
                                'color': 'white',
                                'background-color': '#0051A1',
                                'height': '35px',
                                'padding': '5px 120px 5px',
                                'position': 'relative', 
                                'zIndex': 0,  
                            }
                        ),
                    ]
                    
                ),

                html.Br (), 
                dbc.Row(
                    [
                        dbc.Col(cm.sidebar, width=2), 
                        dbc.Col(
                            html.Div(id='page-content', style={'width': '100%'})
                        )
                    ]
                ),

            ]
        )
    ]
)

app.layout = login_layout

@app.callback(
    Output('url', 'pathname'),  
    [Input('login-button', 'n_clicks')],
    [State('username-input', 'value'),
     State('password-input', 'value')]
)
def check_login(n_clicks, username, password):
    if n_clicks:
        absolute_username = 'username'
        absolute_password = 'admin'

        if username == absolute_username and password == absolute_password:
             app.layout = main_layout
             return '/dashboard'
        raise PreventUpdate

@app.callback(
    [
        Output('page-content', 'children'),
    ],
    [
        Input('url', 'pathname')
    ]
)
def display_page(pathname):
    ctx = dash.callback_context
    if ctx.triggered:
        event_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if event_id == 'url':
            if pathname == '/dashboard' or pathname == '/':
                return_layout = dashboard.layout
            elif pathname == '/patient/records':
                return_layout = patient_records.layout
            elif pathname == '/patient/registration':
                return_layout = patient_registration.layout
            elif pathname == '/patient/profile':
                return_layout = patient_profile.layout
            elif pathname == '/queue':
                return_layout = queue.layout
            elif pathname == '/payment':
                return_layout = payment.layout
            elif pathname == '/medicine':
                return_layout = medicine_inventory.layout
            else:
                return_layout = 'error404'
            
            return [return_layout]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', autoraise=True)
    app.run_server(debug=False)
