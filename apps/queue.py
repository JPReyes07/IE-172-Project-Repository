import ast
import dash
import webbrowser
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
from datetime import datetime, timedelta
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        dcc.Location(id = 'current-url', refresh=True),
        html.H1('Queue',
                style={
                    'font-family': 'Helvetica, sans-serif',
                    'fontWeight': 'bold'
                }
        ),
        html.Hr(),

        dbc.Card(
            [
                dbc.CardBody(
                    [
                        # Header-Options
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col('Date',
                                                style={
                                                    'font-family': 'Helvetica, sans-serif',
                                                    'fontWeight': 'bold'
                                                }
                                        ),
                                        dbc.Col('Service',
                                                style={
                                                    'font-family': 'Helvetica, sans-serif',
                                                    'fontWeight': 'bold'
                                                }
                                        )
                                    ]
                                ),

                                dbc.Row(
                                    [
                                        # DATE FILTER
                                        dbc.Col(
                                            html.Div(
                                                dmc.DatePickerInput(
                                                    id = "queue-date-filter",
                                                    valueFormat="YYYY-MM-DD",
                                                    value = datetime.now().date(),
                                                    style={"width": 200},
                                                ),
                                            )
                                        ),

                                        # SERVICE FILTER    
                                        dbc.Col(
                                            html.Div(
                                                dbc.Row(
                                                    [
                                                        dcc.Dropdown(
                                                            id="queue-service-filter",
                                                            options=[
                                                                {"label": "Wellness Check-up", "value": "1"},
                                                                {"label": "Preventive Medicine", "value": "2"},
                                                                {"label": "Prenatal Pregnancy Care", "value": "3"},
                                                                {"label": "Postnatal Pregnancy Care", "value": "4"},
                                                            ],
                                                            style={"width": 400}
                                                        )
                                                    ],
                                                    className="me-3"
                                                ),
                                                style = {'margin-left': 15}
                                            )    
                                        )
                                    ]
                                ),
                            ]
                        ),

                        html.Hr(),
                        
                        html.Div(
                            [
                                dbc.Row(
                                    dbc.Col('Select Patient and Service to Add to the Queue',
                                            style={
                                                'font-family': 'Helvetica, sans-serif',
                                                'fontWeight': 'bold'
                                            }
                                    )
                                ),

                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'queue-patient-add',
                                                placeholder = 'Search Patient',
                                            ),
                                            width = 5
                                        ),

                                        dbc.Col(
                                            dcc.Dropdown(
                                                id = 'queue-service-add',
                                                options=[
                                                    {"label": "Wellness Check-up", "value": "1"},
                                                    {"label": "Preventive Medicine", "value": "2"},
                                                    {"label": "Prenatal Pregnancy Care", "value": "3"},
                                                    {"label": "Postnatal Pregnancy Care", "value": "4"},
                                                ],
                                                placeholder = 'Select Service'
                                            ),
                                            width = 5
                                        ),

                                        dbc.Col(
                                            dbc.Button(
                                                'Add',
                                                id = 'queue-add'
                                            )
                                        )

                                    ]
                                )
                            ]
                        ),

                        html.Hr(),

                        html.Div(id = 'queue-df'),

                        html.Div(id = 'test'),
                        html.Div(id = 'test2')

                    ]
                )
                
            ]
        )

    ],

    id = 'queue-content'
)

'''LOAD PATIENT INTO DROPDOWN'''
@app.callback(
    [
        Output('queue-patient-add', 'options'),
    ],
    [
        Input('url', 'pathname')
    ]
)
def ptt_loaddropdown(pathname):
    if pathname == '/queue':
        sql = '''
            SELECT
                (PTT_FM || ' ' ||PTT_LM) AS PTT_FULL_M,
                PTT_ID
            FROM patient      
        '''

        values = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, values, cols)

        ptt_list = df.to_dict(orient = 'records')

    else:
        raise PreventUpdate
    
    return [ptt_list]

'''ADDING AND REMOVING A PERSON INTO QUEUE'''
@app.callback(
    [
        Output('queue-content', 'children'),
    ],
    [
        Input('queue-add', 'n_clicks'),
        Input('queue-date-filter', 'value'),
        Input({"type": "queuedel", "index": ALL}, 'n_clicks'),
        Input('queue-content', 'children'),
    ],
    [
        State('queue-patient-add', 'value'),
        State('queue-service-add', 'value')
    ]
)
def add_queue(addbtn, datevalue, button_clicks, layout, ptt_id, service):
    ctx = dash.callback_context
    date_now = datetime.now().date()
    ctx = dash.callback_context
    t = list(ctx.triggered_prop_ids.values())[0]

    if ctx.triggered:
        event_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if event_id == 'queue-add' and addbtn:

            # Medical Secretary Side
            if datevalue == date_now:
                sql = '''
                INSERT INTO patient_visit (VISIT_D_NOW, VISIT_D_PREV,
                                            VISIT_HR, VISIT_BP_SYS, VISIT_BP_DIA, VISIT_WGHT, VISIT_TMP, VISIT_Q, VISIT_DGNS, 
                                            SRVC_ID, PTT_ID, MDSC_ID)
                VALUES
                    (%s, NULL,
                    NULL, NULL, NULL, NULL, NULL, 'NO SHOW', NULL,
                    %s, %s, NULL);
                '''

                values = [datevalue, service, ptt_id]
                db.modifydatabase(sql, values)
            # Physician Side
            else:
                sql = '''
                WITH get_visit_d_prev AS(
                    SELECT MAX(VISIT_D_NOW) AS PREV_D
                    FROM patient_visit
                    WHERE PTT_ID = %s

                )

                INSERT INTO patient_visit (VISIT_D_NOW, VISIT_D_PREV,
                                            VISIT_HR, VISIT_BP_SYS, VISIT_BP_DIA, VISIT_WGHT, VISIT_TMP, VISIT_Q, VISIT_DGNS, 
                                            SRVC_ID, PTT_ID, MDSC_ID)
                VALUES
                    (%s, (SELECT PREV_D FROM get_visit_d_prev), 
                    NULL, NULL, NULL, NULL, NULL, 'NO SHOW', NULL, 
                    %s, %s, NULL);
                '''

                values = [ptt_id, datevalue, service, ptt_id]
                db.modifydatabase(sql, values)

        if sum(button_clicks) >= 1:
            changed_id = t['index']

            sql = '''
                UPDATE patient_visit
                SET VISIT_DEL_IND = TRUE
                WHERE VISIT_ID = %s
            '''
            values = [changed_id]

            db.modifydatabase(sql, values)

        return [layout]
    
    else:
        raise PreventUpdate

'''GENERATE QUEUE TABLE'''
@app.callback(
    [
        Output('queue-df', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('queue-date-filter', 'value'),
        Input('queue-service-filter', 'value'),
    ]
)
def load_queue(pathname, datevalue, srvc_id):
    if pathname == '/queue':
        if srvc_id is None:
            sql = '''
            SELECT
                (pt.PTT_FM || ' ' ||pt.PTT_LM) AS PTT_FULL_M,
                sv.SRVC_M AS service,
                sv.SRVC_ID,
                pv.VISIT_Q,
                pv.VISIT_ID,
                pv.VISIT_ID,
                pt.PTT_ID,
                pt.PTT_ID
            FROM patient_visit pv
            JOIN patient pt
            ON pt.PTT_ID = pv.PTT_ID
            JOIN service sv
            ON sv.SRVC_ID = pv.SRVC_ID
            WHERE (pv.VISIT_D_NOW = %s OR pv.VISIT_Q = 'NO-SHOW') AND VISIT_DEL_IND = FALSE
            '''
            values = [datevalue] 

            cols = ['NAME', 'SERVICE', 'SRVC_ID', 'CONSULT STATUS', '    ', 'VISIT_ID', 'PTT_ID', 'REMOVE']

            df = db.querydatafromdatabase(sql, values, cols)
        else: 
            sql = '''
            SELECT
                (pt.PTT_FM || ' ' ||pt.PTT_LM) AS PTT_FULL_M,
                sv.SRVC_M AS service,
                sv.SRVC_ID,
                pv.VISIT_Q,
                pv.VISIT_ID,
                pv.VISIT_ID,
                pt.PTT_ID,
                pt.PTT_ID
            FROM patient_visit pv
            JOIN patient pt
            ON pt.PTT_ID = pv.PTT_ID
            JOIN service sv
            ON sv.SRVC_ID = pv.SRVC_ID
            WHERE ((pv.VISIT_D_NOW = %s OR pv.VISIT_Q = 'NO-SHOW') AND sv.SRVC_ID = %s) AND VISIT_DEL_IND = FALSE
            '''
            values = [datevalue, srvc_id] 

            cols = ['NAME', 'SERVICE', 'SRVC_ID', 'CONSULT STATUS', '    ', 'VISIT_ID', 'PTT_ID', 'REMOVE']

            df = db.querydatafromdatabase(sql, values, cols)
        

        if not df.empty: 
            dropdown = []
            view_buttons = []
            del_buttons = []
            for visit_id in df['VISIT_ID']:
                dropdown += [
                    html.Div(
                        dcc.Dropdown(
                            id={"type": "queuedropdown", "index": visit_id},
                            options=[
                                {"label": "NO-SHOW", "value": "NO-SHOW"},
                                {"label": "IN QUEUE", "value": "IN QUEUE"},
                                {"label": "IN PROGRESS", "value": "IN PROGRESS"},
                                {"label": "COMPLETED", "value": "COMPLETED"},
                            ],
                            value=df.loc[df['VISIT_ID'] == visit_id, 'CONSULT STATUS'].values[0]
                        ),
                    )
                ]

                view_buttons += [
                    html.Div(
                        dbc.Button(
                            'View Profile',
                            href = f"/patient/profile?from={pathname}&ptt_id={df.loc[df['VISIT_ID'] == visit_id, 'PTT_ID'].iloc[0]}"
                        ),
                    )
                ]

                del_buttons += [
                    html.Div(
                        dbc.Button(
                            '⨉',
                            n_clicks = 0,
                            id = {"type": "queuedel", "index": visit_id},
                            color = 'danger'
                        ),
                    )
                ]
            
            df['CONSULT STATUS'] = dropdown
            df['    '] = view_buttons
            df['REMOVE'] = del_buttons
            df = df[['NAME', 'SERVICE','CONSULT STATUS', '    ', 'REMOVE']]
            
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
            return [html.P("No data for the selected date.")]
    else:
        raise PreventUpdate

'''UPDATE QUEUE STATUS'''
@app.callback(
    Output('test', 'children'),
    [Input({"type": "queuedropdown", "index": ALL}, 'value'),
     Input({"type": "queueupdate", "index": ALL}, 'n_clicks')],
)
def update_queue_status(dropdown_values, button_clicks):
    ctx = dash.callback_context
    t = list(ctx.triggered_prop_ids.values())[0]
    changed_id = t['index']

    y = ctx.triggered[0]["value"]

    sql = '''
        UPDATE patient_visit 
        SET VISIT_Q = %s
        WHERE VISIT_ID = %s
    '''
    values = [y, changed_id]
    db.modifydatabase(sql, values)

    return ['']