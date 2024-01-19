import dash
import webbrowser
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from datetime import datetime, date
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from urllib.parse import urlparse, parse_qs

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        dcc.Store(
            id = 'ptt-profile-toload',
            storage_type = 'memory',
            data = 0
        ),

        html.H1('Patient Registration',
                style={
                    'font-family': 'Helvetica, sans-serif',
                    'fontWeight': 'bold'
                }
        ),

        html.Hr(),

        # Personal Information
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H3('Personal Information',
                                style={
                                    'font-family': 'Helvetica, sans-serif',
                                    'fontWeight': 'bold'
                                }
                        )
                    ]
                ),

                dbc.CardBody(
                    [
                        ## Name
                        html.Div(
                            [
                                dbc.Row(
                                    [dbc.Col(
                                        html.Div(
                                            dbc.Row(
                                                dbc.Label(
                                                    "Name", 
                                                    width = 'auto',
                                                    style = {'font-family': 'Helvetica, sans-serif'}
                                                )
                                            )
                                        ),
                                        width = 2
                                    ),
                                     
                                     dbc.Col(
                                         html.Div(
                                            dbc.Form(
                                                dbc.Row(
                                                    [
                                                        dbc.Label(
                                                            'Last Name:', 
                                                            width = 'auto',
                                                            style = {'font-family': 'Helvetica, sans-serif'}
                                                        ),
                                                        dbc.Col(
                                                            dbc.Input(
                                                                id = 'personalinfo-name-LN',
                                                                type = 'text',
                                                                style = {
                                                                        'background-color': '#E0E5E9',
                                                                        'font-family': 'Helvetica, sans-serif'},

                                                            ),
                                                        )
                                                    ],
                                                    className="me-3"
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
                                                            'First Name:', 
                                                            width = 'auto',
                                                            style = {
                                                                'font-family': 'Helvetica, sans-serif'}
                                                        ),

                                                        dbc.Col(
                                                            dbc.Input(
                                                                id = 'personalinfo-name-FN',
                                                                type = 'text',
                                                                style = {
                                                                        'background-color': '#E0E5E9',
                                                                        'font-family': 'Helvetica, sans-serif'
                                                                }
                                                            ),
                                                        )
                                                    ],
                                                    className="me-3"
                                                ),
                                            )
                                        )
                                     )
                                    ]
                                )
                            ]
                        ),

                        html.Hr(),

                        ## Birthday
                        html.Div(
                            [
                                dbc.Row(
                                    [dbc.Col(
                                        html.Div(
                                            dbc.Row(
                                                dbc.Label(
                                                    "Birthday", 
                                                    width = 'auto',
                                                    style = {
                                                            'font-family': 'Helvetica, sans-serif'
                                                    }
                                                ),
                                            )
                                        ),
                                        width = 2
                                    ),
                                     
                                     dbc.Col(
                                         html.Div(
                                            dbc.Form(
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            dmc.DatePickerInput(
                                                                id = "personalinfo-bday",
                                                                valueFormat="YYYY-MM-DD",
                                                                minDate = date(1950, 1, 1),
                                                                style={"width": 200,
                                                                       'background-color': '#E0E5E9'
                                                                },
                                                            ),
                                                        )
                                                    ],
                                                    className="me-3"
                                                ),
                                            )
                                        )
                                     )
                                    ]
                                )
                            ]
                        ),

                        html.Hr(),

                        ## Civil Status
                        html.Div(
                            [
                                dbc.Row(
                                    [dbc.Col(
                                        html.Div(
                                            dbc.Row(
                                                dbc.Label("Civil Status", 
                                                          width = 'auto',
                                                          style = {'font-family': 'Helvetica, sans-serif'}),
                                            )
                                        ),
                                        width = 2
                                    ),
                                     
                                     dbc.Col(
                                         html.Div(
                                            dbc.Row(
                                                [
                                                    dbc.Select(
                                                        id="personalinfo-civilstatus",
                                                        options=[
                                                            {"label": "Single", "value": "Single"},
                                                            {"label": "Married", "value": "Married"},
                                                            {"label": "Divorced", "value": "Divorced"},
                                                            {"label": "Widowed", "value": "Widowed"},
                                                        ],
                                                        style={"width": 200,
                                                               'font-family': 'Helvetica, sans-serif',
                                                               'background-color': '#E0E5E9'
                                                        }
                                                    )
                                                ],
                                                className="me-3"
                                            ),
                                            style = {'margin-left': 15}
                                        ),
                                     )
                                    ]
                                )
                            ]
                        ),

                        html.Hr(),

                        ## Address
                        html.Div(
                            [
                                dbc.Row(
                                    [dbc.Col(
                                        html.Div(
                                            dbc.Row(
                                                dbc.Label("Address", 
                                                          width = 'auto',
                                                          style = {'font-family': 'Helvetica, sans-serif'}),
                                                className = "my-3"
                                            )
                                        ),
                                        width = 2
                                    ),
                                     
                                     dbc.Col(
                                         html.Div(
                                             [
                                                dbc.Row(
                                                    dbc.Form(
                                                        dbc.Row(
                                                            [
                                                                dbc.Label('Street Address:', 
                                                                          width = 4,
                                                                          style = {'font-family': 'Helvetica, sans-serif'}),
                                                                dbc.Col(
                                                                    dbc.Input(
                                                                        id = 'personalinfo-addr-st',
                                                                        type = 'text',
                                                                        style = {
                                                                            'font-family': 'Helvetica, sans-serif',
                                                                            'background-color': '#E0E5E9'
                                                                        }
                                                                    ),
                                                                )
                                                            ],
                                                            className = "me-3 my-3"
                                                        ),
                                                    )
                                                ),

                                                dbc.Row(
                                                    dbc.Form(
                                                        dbc.Row(
                                                            [
                                                                dbc.Label('Municipality/Barangay:', 
                                                                          width = 4,
                                                                          style = {'font-family': 'Helvetica, sans-serif'}),
                                                                dbc.Col(
                                                                    dbc.Input(
                                                                        id = 'personalinfo-addr-brgy',
                                                                        type = 'text',
                                                                        style = {
                                                                            'font-family': 'Helvetica, sans-serif',
                                                                            'background-color': '#E0E5E9'
                                                                        }
                                                                    ),
                                                                )
                                                            ],
                                                            className = "me-3 my-3"
                                                        ),
                                                    )
                                                ),

                                                dbc.Row(
                                                    dbc.Form(
                                                        dbc.Row(
                                                            [
                                                                dbc.Label('Province/Chartered City:', 
                                                                          width = 4,
                                                                          style = {'font-family': 'Helvetica, sans-serif'}),
                                                                dbc.Col(
                                                                    dbc.Input(
                                                                        id = 'personalinfo-addr-prov',
                                                                        type = 'text',
                                                                        style = {
                                                                            'font-family': 'Helvetica, sans-serif',
                                                                            'background-color': '#E0E5E9'
                                                                        }
                                                                    ),
                                                                )
                                                            ],
                                                            className = "me-3 my-3"
                                                        ),
                                                    )
                                                ),

                                            ]
                                         )
                                     ),
                                    ]
                                )
                            ]
                        ),
                    ]
                )
            ]
        ),

        html.Br(),
        html.Br(),

        # Contact Information
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H3('Contact Information',
                                style={
                                    'font-family': 'Helvetica, sans-serif',
                                    'fontWeight': 'bold'
                                }
                        )
                    ]
                ),

                dbc.CardBody(
                    [
                        ## Personal Contact Number
                        html.Div(
                            [
                                dbc.Row(
                                    [dbc.Col(
                                        html.Div(
                                            dbc.Row(
                                                dbc.Label("Personal Contact Number", 
                                                          width = 'auto',
                                                          style = {'font-family': 'Helvetica, sans-serif'}
                                                )
                                            )
                                        ),
                                        width = 4
                                    ),
                                     
                                     dbc.Col(
                                         html.Div(
                                            dbc.Form(
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            dbc.Input(
                                                                placeholder = 'e.g., 09123456789',
                                                                id = 'personalinfo-cn',
                                                                type = 'number',
                                                                maxLength = 11,
                                                                style={
                                                                    "width": 500,
                                                                    'font-family': 'Helvetica, sans-serif',
                                                                    'background-color': '#E0E5E9'
                                                                }
                                                            ),
                                                        )
                                                    ],
                                                    className="me-3"
                                                ),
                                            )
                                        )
                                     ),
                                    ]
                                )
                            ]
                        ),

                        html.Hr(),

                        ## Emergency Contact Number
                        html.Div(
                            [
                                dbc.Row(
                                    [dbc.Col(
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    dbc.Label("Person to Contact In Case of Emergency", 
                                                            width = 'auto',
                                                            style = {'font-family': 'Helvetica, sans-serif'},
                                                            className="me-3 my-3")
                                                ),
                                                dbc.Row(
                                                    dbc.Label("Relationship", 
                                                            width = 'auto',
                                                            style = {'font-family': 'Helvetica, sans-serif'},
                                                            className="me-3 my-3")
                                                ),
                                                dbc.Row(
                                                    dbc.Label("Contact Number", 
                                                            width = 'auto',
                                                            style = {'font-family': 'Helvetica, sans-serif'},
                                                            className="me-3 my-3")
                                                ),
                                            ]
                                        ),
                                        width = 4
                                    ),
                                     
                                     dbc.Col(
                                         html.Div(
                                            [
                                                dbc.Form(
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                dbc.Input(
                                                                    id = 'personalinfo-emc-who',
                                                                    type = 'text',
                                                                    style={
                                                                        "width": 500,
                                                                        'font-family': 'Helvetica, sans-serif',
                                                                        'background-color': '#E0E5E9'
                                                                    },
                                                                    className="me-3 my-3"
                                                                ),
                                                            ),
                                                        ],
                                                    ),
                                                ),

                                                dbc.Form(
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                dbc.Input(
                                                                    id = 'personalinfo-emc-rel',
                                                                    type = 'text',
                                                                    style={
                                                                        "width": 500,
                                                                        'font-family': 'Helvetica, sans-serif',
                                                                        'background-color': '#E0E5E9'
                                                                    },
                                                                    className="me-3 my-3"
                                                                ),
                                                            ),
                                                        ],
                                                    ),
                                                ),

                                                dbc.Form(
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                dbc.Input(
                                                                    placeholder = 'e.g., 09123456789',
                                                                    id = 'personalinfo-emc-cn',
                                                                    type = 'number',
                                                                    style={
                                                                        "width": 500,
                                                                        'font-family': 'Helvetica, sans-serif',
                                                                        'background-color': '#E0E5E9'
                                                                    },
                                                                    className="me-3 my-3"
                                                                ),
                                                            ),
                                                        ],
                                                    ),
                                                ),

                                            ]
                                        )
                                     ),
                                    ]
                                )
                            ]
                        ),

                    ]
                )
            ]
        ),

        html.Br(),
        html.Br(),

        # Medical History
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H3('Medical History',
                                style={
                                    'font-family': 'Helvetica, sans-serif',
                                    'fontWeight': 'bold'
                                }
                        )
                    ]
                ),

                dbc.CardBody(
                    html.Div(
                            [
                                dbc.Row(
                                    [dbc.Col(
                                        html.Div(
                                            dbc.Row(
                                                dbc.Label("Medical History", 
                                                          width = 'auto',
                                                          style={
                                                                'font-family': 'Helvetica, sans-serif',
                                                                'fontWeight': 'bold'
                                                            }
                                                )
                                            )
                                        ),
                                        width = 4
                                    ),
                                     
                                     dbc.Col(
                                         html.Div(
                                            dbc.Form(
                                                dbc.Row(
                                                    [
                                                       dbc.Textarea(
                                                            id = 'personalinfo-mh'
                                                        ),
                                                    ],
                                                    className="me-3"
                                                ),
                                            )
                                        )
                                     ),
                                    ]
                                )
                            ]
                        ),
                )
            ]
        ),
   
        html.Br(),
        html.Br(),
        
        dbc.Alert(id='personalinfo-alert', is_open=False),

        dbc.Button(
            'Add to Patient Database',
            id = 'personalinfo-add-btn',
            n_clicks = 0
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                
                dbc.ModalBody(
                    'Text',
                    id = 'personalinfo-feedback_message'
                )
            ],

            centered = True,
            id = 'personalinfo-successmodal',
            backdrop = 'static',
            is_open = False
        )

    ]
)

@app.callback(
        [
            Output('ptt-profile-toload', 'data')
        ],
        [
            Input('url', 'pathname')
        ],
        [
            State('url', 'search')
        ]
)
def ptt_profile_upd_store(pathname, search):
    if pathname == '/patient/registration':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        data = 1 if create_mode == 'edit' else 0

    else:
        raise PreventUpdate
    
    return [data]

@app.callback(
        [
            Output('personalinfo-name-LN', 'value'),
            Output('personalinfo-name-FN', 'value'),
            Output('personalinfo-bday', 'value'),
            Output('personalinfo-civilstatus', 'value'),
            Output('personalinfo-addr-st', 'value'),
            Output('personalinfo-addr-brgy', 'value'),
            Output('personalinfo-addr-prov', 'value'),

            Output('personalinfo-cn', 'value'),
            Output('personalinfo-emc-who', 'value'),
            Output('personalinfo-emc-rel', 'value'),
            Output('personalinfo-emc-cn', 'value'),

            Output('personalinfo-mh', 'value')
        ],
        [
            Input('ptt-profile-toload', 'modified_timestamp')
        ],
        [
            State('ptt-profile-toload', 'data'),
            State('url', 'search')
        ]
)
def ptt_profile_upd_store(timestamp, data, search):
    if data:
        parsed = urlparse(search)
        ptt_id = parse_qs(parsed.query)['ptt_id'][0]
        
        sql = '''
            SELECT
                *
            FROM patient
            WHERE PTT_ID = %s
        '''
        values = [ptt_id]
        cols = ['ID', 'First_Name', 'Last_Name', 'Birthdate', 
                'Street_Address', 'Barangay_Address', 'Province',
                'Contact_Number', 'Civil_Status',
                'Emergency_Contact', 'Emergency_Contact_Relationship', 'Emergency_Contact_Number',
                'Medical_History', 'DEL_IND']

        df = db.querydatafromdatabase(sql, values, cols)

        fm = df['First_Name'][0]
        lm = df['Last_Name'][0]
        bday = df['Birthdate'][0]
        street_address = df['Street_Address'][0]
        barangay_address = df['Barangay_Address'][0]
        province = df['Province'][0]
        contact_number = df['Contact_Number'][0]
        civil_status = df['Civil_Status'][0]
        emergency_contact = df['Emergency_Contact'][0]
        emergency_contact_relationship = df['Emergency_Contact_Relationship'][0]
        emergency_contact_number = df['Emergency_Contact_Number'][0]
        medical_history = df['Medical_History'][0]


        return [lm, fm, bday, civil_status,
                street_address, barangay_address, province,
                contact_number, emergency_contact, emergency_contact_relationship, emergency_contact_number,
                medical_history]

    else:
        raise PreventUpdate

@app.callback(
    [
        Output('personalinfo-alert', 'color'),
        Output('personalinfo-alert', 'children'),
        Output('personalinfo-alert', 'is_open'),
        Output('personalinfo-successmodal', 'is_open'),
        Output('personalinfo-feedback_message', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('personalinfo-name-LN', 'value'),
        Input('personalinfo-name-FN', 'value'),
        Input('personalinfo-bday', 'value'),
        Input('personalinfo-civilstatus', 'value'),
        Input('personalinfo-addr-st', 'value'),
        Input('personalinfo-addr-brgy', 'value'),
        Input('personalinfo-addr-prov', 'value'),

        Input('personalinfo-cn', 'value'),
        Input('personalinfo-emc-who', 'value'),
        Input('personalinfo-emc-rel', 'value'),
        Input('personalinfo-emc-cn', 'value'),

        Input('personalinfo-mh', 'value'),

        Input('personalinfo-add-btn', 'n_clicks')
    ],
    [
         State('url', 'search')
    ]
)
def ptt_saveprofile(pathname, 
                    Last_Name, First_Name, Birthdate, Civil_Status,
                    Street_Address, Barangay_Address, Province,
                    Contact_Number, Emergency_Contact, Emergency_Contact_Relationship, Emergency_Contact_Number,
                    Medical_History,
                    addbtn, search):
    ctx = dash.callback_context
    if ctx.triggered:
        event_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if event_id == 'personalinfo-add-btn' and addbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            feedback_message = ''

            required_fields = ['Last_Name', 'First_Name', 'Birthdate', 'Civil_Status',
                               'Street_Address', 'Barangay_Address', 'Province',
                               'Contact_Number', 'Emergency_Contact', 'Emergency_Contact_Relationship', 'Emergency_Contact_Number',
                               'Medical_History']
            
            for field in required_fields:
                if not locals().get(field):
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = f"{field.replace('_', ' ')} is required!"
                    break
            

            else:
                parsed = urlparse(search)
                mode = parse_qs(parsed.query)['mode'][0]
                if mode == 'edit':
                    ptt_id = parse_qs(parsed.query)['ptt_id'][0]
                    sql = '''
                        UPDATE patient
                        SET 
                            PTT_FM = %s,
                            PTT_LM = %s,
                            PTT_BRTH = %s,
                            PTT_ADDR_STRT = %s,
                            PTT_ADDR_BRGY = %s,
                            PTT_ADDR_PROV = %s,
                            PTT_CTNB = %s,
                            PTT_CVST = %s,
                            PTT_EMC_M = %s,
                            PTT_EMC_RLN = %s,
                            PTT_EMC_CTNB = %s,
                            PTT_MED_HIST = %s
                        WHERE PTT_ID = %s
                    '''
                    values = [First_Name, Last_Name, Birthdate,
                                Street_Address, Barangay_Address, Province,
                                Contact_Number,  Civil_Status,
                                Emergency_Contact, Emergency_Contact_Relationship, Emergency_Contact_Number,
                                Medical_History, ptt_id]
                    db.modifydatabase(sql, values)
                    modal_open = True
                    feedback_message = 'A patient has been updated!'
                
                else:
                    sql = '''
                        INSERT INTO patient (
                            PTT_FM, 
                            PTT_LM, 
                            PTT_BRTH,
                            PTT_ADDR_STRT,
                            PTT_ADDR_BRGY,
                            PTT_ADDR_PROV,
                            PTT_CTNB,
                            PTT_CVST,
                            PTT_EMC_M,
                            PTT_EMC_RLN,
                            PTT_EMC_CTNB,
                            PTT_MED_HIST
                        ) 
                        VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    '''

                    values = [First_Name, Last_Name, Birthdate,
                            Street_Address, Barangay_Address, Province,
                            Contact_Number,  Civil_Status,
                            Emergency_Contact, Emergency_Contact_Relationship, Emergency_Contact_Number,
                            Medical_History]
                    db.modifydatabase(sql, values)

                    modal_open = True
                    feedback_message = 'A new patient has been added!'
                    

            return [alert_color, alert_text, alert_open, 
                    modal_open, feedback_message]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate