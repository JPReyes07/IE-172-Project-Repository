import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime, date
import json
import pandas as pd
import dash_table
import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from urllib.parse import urlparse, parse_qs
from apps import dbconnect as db
from app import app

layout = html.Div(
    [
        dcc.Location(id='current-page', refresh=False),
        
        # NAME, EDIT PROFILE, ADD CONSULT
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.H1('Name', 
                                    id='patient-profile-name'
                            ),
                            width={'order': '1'}
                        ),

                        dbc.Col(
                            dbc.Row(
                                dbc.Button(
                                    'Edit Profile',
                                    id='btn-edit-profile'
                                ),
                                justify='end',
                            ),
                            align='center',
                            width={'size': 3, 'order': 'last'},
                            className='me-3'
                        ),

                        dbc.Col(
                            dbc.Row(
                                dbc.Button(
                                    'Create Note',
                                    id='btn-create-note'
                                ),
                                justify='end',
                            ),
                            align='center',
                            width={'size': 3, 'order': 'last'}
                        )
                    ],
                ),
            ]
        ),

        html.Hr(),

        # PATIENT PROFILE TABLE
        html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            'Table will go here',
                            id='patient-profile-details'
                        ),

                        dbc.CardBody(
                            html.P(
                                [
                                    'In case of emergency, please contact: ',
                                    html.Ul(
                                        [
                                            html.Li(
                                                'EMC_NAME', 
                                                id='patient-profile-emc-who'
                                            ),
                                            
                                            html.Li(
                                                'EMC_CTNB', 
                                                id='patient-profile-emc-cn'
                                            ),
                                            
                                            html.Li(
                                                'EMC_REL', 
                                                id='patient-profile-emc-rel'
                                            ),
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                ),
            ]
        ),

        # CONSULT LOG TABLE
        html.Div(
            [
                dbc.Alert(id='consult-log-alert', is_open=False),
                
                html.Div(
                    'Visit history goes here!',
                    id='patient-profile-visit-history'
                )
            ]
            
        ),

        # CREATE_NOTE
        dbc.Modal(
            [
                dbc.ModalHeader(
                    [
                        html.H2(
                            'New Consultation Note',
                            style={'font-family': 'Helvetica, sans-serif'}
                        ),
                        dbc.Button('✖',
                                    id = 'exit',
                                    style = {'text-align': 'right'}
                        )
                    ],
                    close_button = False
                ),

                dbc.ModalBody(
                    html.Div(
                        [
                            dbc.Alert(id='consult-note-alert', is_open=False),
                            
                            # NAME, AGE, DATE
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.H2('Name', 
                                                id='consult-note-name'
                                        )
                                    ),

                                    dbc.Col(
                                        html.H4(f'{datetime.now().date()}')
                                    ),

                                ]
                            ),

                            # VITALS
                            dbc.Card(
                                [
                                    dbc.CardHeader('Vitals'),
                                    dbc.CardBody(
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            html.Div(
                                                                dbc.Form(
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Label(
                                                                                'Weight (kg)', 
                                                                                width=6
                                                                            ),
                                                                            dbc.Col(
                                                                                dbc.Input(
                                                                                    id='consult-note-weight',
                                                                                    type='numeric',
                                                                                    style={'width': 100,
                                                                                            'background-color': '#E0E5E9',
                                                                                            'font-family': 'Helvetica, sans-serif'
                                                                                    }
                                                                                ),
                                                                            )
                                                                        ],
                                                                        className='mb-3'
                                                                    ),
                                                                )
                                                            )
                                                        ),

                                                        dbc.Col(
                                                            html.Div(
                                                                dbc.Form(
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Label(
                                                                                'Temperature (°C)', 
                                                                                width=6
                                                                            ),
                                                                            dbc.Col(
                                                                                dbc.Input(
                                                                                    id='consult-note-temp',
                                                                                    type='numeric',
                                                                                    style={'width': 100,
                                                                                            'background-color': '#E0E5E9',
                                                                                            'font-family': 'Helvetica, sans-serif'
                                                                                    }
                                                                                ),
                                                                            )
                                                                        ],
                                                                        className='mb-3'
                                                                    ),
                                                                )
                                                            )
                                                        )
                                                    ]
                                                ),

                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            html.Div(
                                                                dbc.Form(
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Label(
                                                                                'Systolic BP', 
                                                                                width=6
                                                                            ),
                                                                            dbc.Col(
                                                                                dbc.Input(
                                                                                    id='consult-note-BP-syst',
                                                                                    type='numeric',
                                                                                    style={'width': 100,
                                                                                            'background-color': '#E0E5E9',
                                                                                            'font-family': 'Helvetica, sans-serif'
                                                                                    }
                                                                                ),
                                                                            )
                                                                        ],
                                                                        className='mb-3'
                                                                    ),
                                                                )
                                                            )
                                                        ),

                                                        dbc.Col(
                                                            html.Div(
                                                                dbc.Form(
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Label(
                                                                                'Diastolic BP', 
                                                                                width=6
                                                                            ),
                                                                            dbc.Col(
                                                                                dbc.Input(
                                                                                    id='consult-note-BP-dias',
                                                                                    type='numeric',
                                                                                    style={'width': 100,
                                                                                            'background-color': '#E0E5E9',
                                                                                            'font-family': 'Helvetica, sans-serif'
                                                                                    }
                                                                                ),
                                                                            )
                                                                        ],
                                                                        className='mb-3'
                                                                    ),
                                                                )
                                                            )
                                                        )
                                                    ]
                                                ),

                                                dbc.Row(
                                                    dbc.Col(
                                                        html.Div(
                                                            dbc.Form(
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            'Heart Rate (bpm)', 
                                                                            width=3
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                id='consult-note-hr',
                                                                                type='numeric',
                                                                                style={'width': 100,
                                                                                            'background-color': '#E0E5E9',
                                                                                            'font-family': 'Helvetica, sans-serif'
                                                                                    }
                                                                            ),
                                                                        )
                                                                    ],
                                                                    className='mb-3'
                                                                ),
                                                            )
                                                        )
                                                    ),
                                                )
                                            ]
                                        )
                                    )
                                ]
                            ),

                            # DIAGNOSIS
                            dbc.Card(
                                [
                                    dbc.CardHeader('Diagnosis'),
                                    dbc.CardBody(
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    dbc.Col(
                                                        html.Div(
                                                            dbc.Form(
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            'Service Type', 
                                                                            width=3
                                                                        ),
                                                                        dbc.Col(
                                                                            dcc.Dropdown(
                                                                                id='consult-note-service',
                                                                                options=[
                                                                                    {'label': 'Wellness Check-up', 'value': '1'},
                                                                                    {'label': 'Preventive Medicine', 'value': '2'},
                                                                                    {'label': 'Prenatal Pregnancy Care', 'value': '3'},
                                                                                    {'label': 'Postnatal Pregnancy Care', 'value': '4'},
                                                                                ],
                                                                                style={'width': 400}
                                                                            )
                                                                        )
                                                                    ],
                                                                    className='mb-3'
                                                                ),
                                                            )
                                                        )
                                                    ),
                                                ),

                                                dbc.Row(
                                                    dbc.Col(
                                                        html.Div(
                                                            dbc.Form(
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            'Note', 
                                                                            width=3
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Textarea(id='consult-note-diagnosis'),
                                                                        )
                                                                    ],
                                                                    className='mb-3'
                                                                ),
                                                            )
                                                        )
                                                    )
                                                )
                                            ]
                                        ),
                                    )
                                ]
                            )
                        ]
                    )
                ),

                dbc.ModalFooter(
                    [
                        dbc.Button(
                            'Save', id='save', className='ms-auto', n_clicks=0
                        )
                    ]

                )

            ],
            style={'font-family': 'Helvetica, sans-serif'},
            size='lg',
            id='create-note',
            is_open=False,
        ),

        # VIEW_NOTE
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle('Consultation Note')
                ),

                dbc.ModalBody(
                    html.Div(
                        [   
                            # NAME, AGE, DATE
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.H2('Name', 
                                                id='view-note-name'
                                        ),
                                    ),

                                    dbc.Col(
                                        dbc.Row(
                                            html.H4('Date',
                                                    id='view-note-date',
                                                    style={'display': 'flex', 'justify-content': 'right'}),
                                        ),
                                    ),

                                ],
                                align='end'
                            ),

                            # VITALS
                            dbc.Card(
                                [
                                    dbc.CardHeader('Vitals'),
                                    dbc.CardBody(
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            html.Div(
                                                                dbc.Form(
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Label(
                                                                                'Weight (kg)', 
                                                                                width=6
                                                                            ),
                                                                            dbc.Col(id='view-note-weight')
                                                                        ],
                                                                        className='mb-3'
                                                                    ),
                                                                )
                                                            )
                                                        ),

                                                        dbc.Col(
                                                            html.Div(
                                                                dbc.Form(
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Label(
                                                                                'Temperature (°C)', 
                                                                                width=6
                                                                            ),
                                                                            dbc.Col(id='view-note-temp')
                                                                        ],
                                                                        className='mb-3'
                                                                    ),
                                                                )
                                                            )
                                                        )
                                                    ]
                                                ),

                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            html.Div(
                                                                dbc.Form(
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Label(
                                                                                'Blood Pressure', 
                                                                                width=6
                                                                            ),
                                                                            dbc.Col(id='view-note-bp')
                                                                        ],
                                                                        className='mb-3'
                                                                    ),
                                                                )
                                                            )
                                                        ),

                                                        dbc.Col(
                                                            html.Div(
                                                                dbc.Form(
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Label(
                                                                                'Heart Rate (bpm)', 
                                                                                width=6
                                                                            ),
                                                                            dbc.Col(id='view-note-hr')
                                                                        ],
                                                                        className='mb-3'
                                                                    ),
                                                                )
                                                            )
                                                        )
                                                    ]
                                                ),
                                            ]
                                        )
                                    )
                                ]
                            ),

                            # DIAGNOSIS
                            dbc.Card(
                                [
                                    dbc.CardHeader('Diagnosis'),
                                    dbc.CardBody(
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    dbc.Col(
                                                        html.Div(
                                                            dbc.Form(
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            'Service Type', 
                                                                            width=3
                                                                        ),
                                                                        dbc.Col(id='view-note-service')
                                                                    ],
                                                                    className='mb-3'
                                                                ),
                                                            )
                                                        )
                                                    ),
                                                ),

                                                dbc.Row(
                                                    dbc.Col(
                                                        html.Div(
                                                            dbc.Form(
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            'Note', 
                                                                            width=3
                                                                        ),
                                                                        dbc.Col(id='view-note-diagnosis')
                                                                    ],
                                                                    className='mb-3'
                                                                ),
                                                            )
                                                        )
                                                    )
                                                )
                                            ]
                                        ),
                                    )
                                ]
                            )
                        ]
                    )
                ),
            ],
            style={'font-family': 'Helvetica, sans-serif'},
            size='lg',
            id='view-note',
            is_open=False
        )
    ],
    id='visit-content',
    style={'font-family': 'Helvetica, sans-serif'},

)

'''LOAD PATIENT NAME'''
@app.callback(
    [
        Output('patient-profile-name', 'children'),
        Output('consult-note-name', 'children'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search')
    ]
)
def load_name(pathname, search):
    if pathname == '/patient/profile':
        parsed = urlparse(search)
        ptt_id = parse_qs(parsed.query)['ptt_id'][0]

        sql = '''
        SELECT 
            (pt.PTT_FM || ' ' ||pt.PTT_LM) AS PTT_FULL_M
        FROM patient pt
        WHERE PTT_ID = %s
        '''
        values = [ptt_id]
        col = ['ptt_full_m']
        df = db.querydatafromdatabase(sql, values, col)

        name = df['ptt_full_m'][0]

        return [name, name]
    else:
        raise PreventUpdate

'''LOAD PATIENT DETAILS'''
@app.callback(
    [
        Output('patient-profile-details', 'children'),
        Output('patient-profile-emc-who', 'children'),
        Output('patient-profile-emc-rel', 'children'),
        Output('patient-profile-emc-cn', 'children'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search')
    ]
)
def load_details(pathname, search):
    if pathname == '/patient/profile':
        parsed = urlparse(search)
        ptt_id = parse_qs(parsed.query)['ptt_id'][0]
        sql = ''' 
            SELECT 
                PTT_BRTH, 
                PTT_CVST, 
                PTT_CTNB, 
                (PTT_ADDR_STRT|| ', ' ||PTT_ADDR_BRGY|| ', ' ||PTT_ADDR_PROV) AS PTT_FULL_ADDR,
                PTT_EMC_M,
                PTT_EMC_RLN,
                PTT_EMC_CTNB
            FROM patient
                WHERE  PTT_ID = %s
        '''

        values = [ptt_id]
        cols = ['Birthdate', 'Civil Status', 'Contact Number',
                'Address', 'EMC_who', 'EMC_relation', 'EMC_ctnb']
        df = db.querydatafromdatabase(sql, values, cols)
        df_basic = df[['Birthdate', 'Civil Status',
                       'Contact Number', 'Address']].T
        df_basic.reset_index(inplace=True)
        df_basic.columns = [' ', ' ']
        df_emc = df[['EMC_who', 'EMC_relation', 'EMC_ctnb']]

        table = dbc.Table.from_dataframe(df_basic, striped=True, bordered=False,
                                         hover=True, size='sm')

        return [table, df_emc['EMC_who'], df_emc['EMC_relation'], df_emc['EMC_ctnb']]

    else:
        raise PreventUpdate

'''EDIT PATIENT DETAILS'''
@app.callback(
    [
        Output('url', 'href')
    ],
    [
        Input('btn-edit-profile', 'n_clicks')
    ],
    [
        State('url', 'search')
    ]
)
def load_edit_mode(editbtn, search):
    ctx = dash.callback_context
    if ctx.triggered:
        event_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if event_id == 'btn-edit-profile' and editbtn:
            parsed = urlparse(search)
            ptt_id = parse_qs(parsed.query)['ptt_id'][0]

            href = f'/patient/registration?mode=edit&ptt_id={ptt_id}'
            return [href]

'''LOAD BLANK CONSULT_NOTE FORM'''
@app.callback(
    [
        Output('create-note', 'is_open', allow_duplicate=True),
    ],
    [
        Input('btn-create-note', 'n_clicks'),
    ],
    prevent_initial_call=True
)
def load_consult_note(modalbtn):
    ctx = dash.callback_context
    if ctx.triggered:
        event_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if event_id == 'btn-create-note' and modalbtn:
            modal_open = False
            modal_open = True
            return [modal_open]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

'''SAVE INPUTS'''
@app.callback(
    [
        Output('consult-note-alert', 'is_open'),
        Output('consult-note-alert', 'color'),
        Output('consult-note-alert', 'children'),
        
    ],
    [
        Input('save', 'n_clicks'),
        Input('consult-note-weight', 'value'),
        Input('consult-note-temp', 'value'),
        Input('consult-note-BP-syst', 'value'),
        Input('consult-note-BP-dias', 'value'),
        Input('consult-note-hr', 'value'),
        Input('consult-note-service', 'value'),
        Input('consult-note-diagnosis', 'value'),
    ],
    [
        State('url', 'search')
    ]
)
def save_consult_note(modalbtn,
                      Weight, Temperature, Systolic_Blood_Pressure, Diastolic_Blood_Pressure, Heart_Rate,
                      Service, Diagnosis,
                      search):
    ctx = dash.callback_context
    if ctx.triggered:
        event_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if event_id == 'save' and modalbtn:
            alert_open = True
            alert_color = 'success'
            alert_text = 'Consult note saved!'

            parsed = urlparse(search)
            prev = parse_qs(parsed.query)['from'][0]
            ptt_id = parse_qs(parsed.query)['ptt_id'][0]
            
            required_fields = ['Weight', 'Temperature', 'Systolic_Blood_Pressure', 'Diastolic_Blood_Pressure', 'Heart_Rate', 
                               'Service', 'Diagnosis']
            
            for field in required_fields:
                if not locals().get(field):
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = f"{field.replace('_', ' ')} is required!"
                    return [alert_open, alert_color, alert_text]
            
            else:
                    
                if prev == '/queue':
                    sql = '''
                    WITH get_visit_id AS(
                        SELECT 
                            MAX(VISIT_ID) AS VISIT_ID
                        FROM patient_visit 
                        WHERE PTT_ID = %s AND VISIT_DEL_IND = FALSE
                    )

                    UPDATE patient_visit
                    SET 
                        VISIT_D_NOW = %s, 
                        VISIT_WGHT = %s,
                        VISIT_TMP = %s,
                        VISIT_BP_sys = %s,
                        VISIT_BP_dia = %s,
                        VISIT_HR = %s,
                        SRVC_ID = %s,
                        VISIT_DGNS = %s
                    WHERE VISIT_ID = (SELECT VISIT_ID FROM get_visit_id) AND PTT_ID = %s
                    '''
                    values = [ptt_id, datetime.date().now(), Weight, Temperature, 
                            Systolic_Blood_Pressure, Diastolic_Blood_Pressure, 
                            Heart_Rate, Service, Diagnosis, ptt_id]
                    db.modifydatabase(sql, values)

                if prev == '/patient/records':
                    sql = '''
                    INSERT INTO patient_visit (VISIT_D_NOW, VISIT_HR, VISIT_BP_SYS, VISIT_BP_DIA, VISIT_WGHT, VISIT_TMP, VISIT_DGNS, SRVC_ID, PTT_ID, MDSC_ID)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1);
                    '''
                    values = [datetime.now().date(), Heart_Rate, Systolic_Blood_Pressure, Diastolic_Blood_Pressure,
                            Weight, Temperature,  Diagnosis, Service, ptt_id]
                    db.modifydatabase(sql, values)

                return [alert_open, alert_color, alert_text]

'''REFRESH TO SHOW SAVE SUCCESS'''
@app.callback(
    [
        Output('visit-content', 'children', allow_duplicate=True),
        Output('create-note', 'is_open')
    ],
    [
        Input('exit', 'n_clicks'),
        Input('visit-content', 'children')
    ],
    prevent_initial_call=True
)
def save_profile_status(modalbtn, layout):
    ctx = dash.callback_context
    if ctx.triggered:
        event_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if event_id == 'exit' and modalbtn:
            return [layout, False]
            
'''LOAD VISIT HISTORY'''
@app.callback(
    [
        Output('patient-profile-visit-history', 'children')
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search')
    ]
)
def load_visit_history(pathname, search):
    if pathname == '/patient/profile':
        parsed = urlparse(search)
        ptt_id = parse_qs(parsed.query)['ptt_id'][0]
        sql = '''
            SELECT
                pv.VISIT_D_NOW,
                s.SRVC_M,
                pv.VISIT_DGNS,
                pv.VISIT_ID,
                pv.VISIT_ID,
                pv.VISIT_ID
            FROM patient_visit pv
            JOIN service s
            ON s.SRVC_ID = pv.SRVC_ID
            WHERE (PTT_ID = %s AND pv.VISIT_D_NOW <= %s) AND pv.VISIT_DEL_IND = FALSE
        '''
        values = [ptt_id, datetime.now().date()]
        cols = ['Date', 'Service', 'Diagnosis', 'Visit_ID', '    ', 'Remove']
        df = db.querydatafromdatabase(sql, values, cols)

        df['Diagnosis'] = df['Diagnosis'].str.slice(0, 30) + '...'

        if not df.empty:
            view_buttons = []
            del_buttons = []
            for visit_id in df['Visit_ID']:
                view_buttons += [
                    html.Div(
                        dbc.Button('View Note',
                                   n_clicks=0,
                                   id={'type': 'view-note', 'index': visit_id},
                                   size='sm', color='primary', className='mx-auto'),
                        style={'text-align': 'left'}
                    )
                ]

                del_buttons += [
                    html.Div(
                        html.Div(
                            dbc.Button(
                                '⨉',
                                n_clicks=0,
                                id={'type': 'visitdel', 'index': visit_id},
                                color='danger'
                            ),
                        )
                    )
                ]

            df['    '] = view_buttons
            df['Remove'] = del_buttons
            df = df[['Date', 'Service', 'Diagnosis', '    ', 'Remove']]

            table = dbc.Table.from_dataframe(
                df,
                striped=True,
                bordered=True,
                hover=True,
                size='sm',
                style={
                    'font-family': 'Helvetica, sans-serif',
                    'text-align': 'center'
                }
            )

            return [table]
    else:
        raise PreventUpdate

'''VIEW EACH VISIT LOG'''
@app.callback(
    [
        Output('view-note', 'is_open'),
        Output('view-note-name', 'children'),
        Output('view-note-date', 'children'),
        Output('view-note-weight', 'children'),
        Output('view-note-temp', 'children'),
        Output('view-note-bp', 'children'),
        Output('view-note-hr', 'children'),
        Output('view-note-service', 'children'),
        Output('view-note-diagnosis', 'children'),
    ],
    [
        Input({'type': 'view-note', 'index': ALL}, 'n_clicks'),
    ],
    [
        State('url', 'search')
    ]
)
def view_note(button_clicks, search):
    parsed = urlparse(search)
    ptt_id = parse_qs(parsed.query)['ptt_id'][0]

    ctx = dash.callback_context
    t = list(ctx.triggered_prop_ids.values())[0]
    changed_id = t['index']

    if sum(button_clicks) >= 1:
        modal_open = False

        sql = '''
            SELECT
                (pt.PTT_FM || ' ' ||pt.PTT_LM) AS PTT_FULL_M,
                pv.VISIT_D_NOW,
                pv.VISIT_WGHT,
                pv.VISIT_TMP,
                (pv.VISIT_BP_SYS || '/' || pv.VISIT_BP_DIA) AS VISIT_BP,
                pv.VISIT_HR,
                s.SRVC_M,
                pv.VISIT_DGNS
            FROM patient_visit pv
            JOIN patient pt
            ON pt.PTT_ID = pv.PTT_ID
            JOIN service s
            ON s.SRVC_ID = pv.SRVC_ID
            WHERE pt.PTT_ID = %s AND pv.VISIT_ID = %s
        '''
        values = [ptt_id, changed_id]
        cols = ['ptt_full_m', 'visit_date', 'weight',
                'temp', 'bp', 'hr', 'service', 'diagnosis']

        df = db.querydatafromdatabase(sql, values, cols)

        modal_open = True

        return [modal_open, df['ptt_full_m'], df['visit_date'], df['weight'], df['temp'], df['bp'], df['hr'],
                df['service'], df['diagnosis']]
    else:
        raise PreventUpdate

'''DELETE VISIT LOG'''
@app.callback(
    [
        Output('visit-content', 'children')
    ],
    [
        Input({'type': 'visitdel', 'index': ALL}, 'n_clicks'),
        Input('visit-content', 'children')
    ]
)
def del_visit(button_clicks, layout):
    if sum(button_clicks) >= 1:
        ctx = dash.callback_context
        t = list(ctx.triggered_prop_ids.values())[0]
        changed_id = t['index']

        sql = '''
            UPDATE patient_visit
            SET VISIT_DEL_IND = TRUE
            WHERE VISIT_ID = %s
        '''
        values = [changed_id]

        db.modifydatabase(sql, values)

        return [layout]
