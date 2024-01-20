import dash
import numpy as np
import webbrowser
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from datetime import datetime, date
from dash import dcc, Patch
from dash import html
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        # NAME, FILTER, ADD BUTTON
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.H1('Payment',
                                    style={'marginRight': '0.5em', }
                                    ),
                            align='center',
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='payment_filter',
                                placeholder='Search',
                                style={'borderRadius': 30}
                            ),
                            align='center',
                            width={'size': 3, 'order': '2'}
                        ),

                        dbc.Col(
                            dbc.Button(
                                'Create Invoice',
                                style={'font-family': 'Helvetica, sans-serif'},
                                id='btn-create-invoice'
                            ),
                            align='center',
                            width={'size': 2, 'order': 'last'}
                        )
                    ],
                    className='mb-3',
                    style={'marginTop': '3em', }
                ),
            ]
        ),
        
        # PAYMENT TABLE
        dbc.Card(
            [
                dbc.CardBody(
                    html.Div(id='payment_df'),
                ),

            ]
        ),
        
        # CREATE NEW INVOICE
        dbc. Modal(
            [
                dbc.ModalHeader(
                    [
                        html.H2(
                            'New Invoice',
                            style={'font-family': 'Helvetica, sans-serif'},
                        ),
                        dbc.Button('✖',
                                    id = 'exit',
                                    style = {'text-align': 'right'}
                        )
                    ],
                    close_button = False
                ),
                dbc.ModalBody(
                    [
                        dbc.Alert(id='payment-alert', is_open=False),
                        
                        # NAME
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Div('Patient Name',
                                                 style={'font-family': 'Helvetica, sans-serif'})
                                    ),
                                ],
                                style={'align-items': 'center'},

                            ),
                        ),
                        
                        # PATIENT DROPDOWN
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id='payment-patient-name',
                                            placeholder='Search Patient',
                                            style={
                                                'background-color': '#E0E5E9',
                                                'font-family': 'Helvetica, sans-serif',
                                                'borderRadius': 12,
                                                'width': '330px',
                                            }
                                        ),
                                    ),
                                ],
                            )
                        ),

                        html.Br(),

                        # SERVICE (label)
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Div('Service Availed',
                                                 style={'font-family': 'Helvetica, sans-serif',
                                                        'align-items': 'center',
                                                        })
                                    ),
                                    dbc.Col(
                                        html.Div('Fee (in Php):',
                                                 style={'font-family': 'Helvetica, sans-serif',
                                                        'marginLeft': '1em', }),
                                    ),

                                ],
                            )
                        ),
                        html.Div(
                            dbc.Row(
                                [
                                    # SERVICE (output)
                                    dbc.Col(
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    html.Div(' ', 
                                                            id='payment-service',
                                                    ),
                                                    style={'margin': '5px',
                                                        'padding': '0'}
                                                ),
                                            ],
                                            style={'margin': '2px',
                                                   'borderRadius': 12}
                                        ),
                                    ),
                                    
                                    # SERVICE FEE (input)
                                    dbc.Col(
                                        dbc.Input(
                                            id='payment-service-fee',
                                            type = 'number',
                                            style={
                                                'background-color': '#E0E5E9',
                                                'font-family': 'Helvetica, sans-serif',
                                                'borderRadius': 12,
                                                'width': '200px'
                                            }
                                        ),
                                    ),
                                ],
                            )
                        ),

                        html.Br(),

                        # MEDICINES BOUGHT
                        html.Div(
                            [
                                # LABEL
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Div('Medicines Bought',
                                                     style={'font-family': 'Helvetica, sans-serif'}
                                                     ),
                                            width=3
                                        ),

                                        dbc.Col(
                                            dbc.Button(
                                                '+',
                                                style={'width': '50px'},
                                                id='btn-add-med'
                                            )
                                        )
                                    ],

                                    style={'justify-content': 'right',
                                           'align-items': 'center'},
                                ),

                                html.Br(),
                                
                                # INPUTS
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Div(
                                                    id="payment-medicine-dropdown",
                                                    children=[]
                                                ),
                                                html.Br()
                                            ],

                                            width=8
                                        ),

                                        dbc.Col(
                                            html.Div(
                                                id="payment-medicine-qty",
                                                children=[]
                                            ),
                                            width=3
                                        )
                                    ]
                                ),
                                html.Div(id="payment-medicine-dropdown-output")
                            ]

                        ),

                        html.Br(),

                        # PAYMENT MODE
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.H6('Payment Mode',
                                                style={
                                                    'font-family': 'Helvetica, sans-serif',
                                                })
                                    ),
                                ]
                            )
                        ),
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id='payment-mode',
                                            style={
                                                'background-color': '#E0E5E9',
                                                'font-family': 'Helvetica, sans-serif',
                                                'borderRadius': 12,
                                                'width': '330px',
                                            },
                                            options=[
                                                {"label": "Cash", "value": "Cash"},
                                                {"label": "Online - GCash",
                                                    "value": "Online - GCash"},
                                                {"label": "Online - BDO",
                                                    "value": "Online - BDO"},
                                            ],
                                            placeholder='Select Payment Mode'
                                        ),
                                        width=4
                                    ),
                                ]
                            )
                        ),

                        html.Br(),

                        # SAVE
                        html.Div(
                            [
                                dbc.Button(
                                    'Save',
                                    id='btn-payment-save',
                                    style={'margin': '0 auto', 'display': 'block'}),

                                html.Div('', id='save-message',
                                         style={'text-align': 'center'})
                            ]

                        ),

                    ]

                )
            ],
            style={'font-family': 'Helvetica, sans-serif'},
            size='md',
            id="create-invoice",
            is_open=False,

        ),
    ],

    id='payment-content'
)

'''GENERATE PAYMENT TABLE'''
@app.callback(
    [
        Output('payment_df', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('payment_filter', 'value'),
    ],
)
def payment_df(pathname, searchterm):
    if pathname == '/payment':
        sql = '''
        WITH patient_service_history AS (
            SELECT
                pv.VISIT_ID,
                (pt.PTT_FM || ' ' || pt.PTT_LM) AS PTT_FULL_M,
                sv.SRVC_M AS service,
                pym.PYM_MDE,
                pym.PYM_SP,
                pym.PYM_ID
            FROM patient_visit pv
            JOIN patient pt ON pt.PTT_ID = pv.PTT_ID
            JOIN service sv ON sv.SRVC_ID = pv.SRVC_ID
            JOIN payment pym ON pym.VISIT_ID = pv.VISIT_ID
            WHERE pym.PYM_DEL_IND = FALSE
        ),

        med_solve AS (
            SELECT
                pym.PYM_ID,
                COALESCE(STRING_AGG(med.MED_M, ', '), 'No Medicine Sold') AS medicine_availed,
                COALESCE(SUM(med.MED_MP * med_pym.MED_PYM_Q), 0) AS total_medicine_payment
            FROM payment pym
            LEFT JOIN medicine_payment med_pym ON med_pym.PYM_ID = pym.PYM_ID
            LEFT JOIN medicine med ON med.MED_ID = med_pym.MED_ID
            GROUP BY pym.VISIT_ID, pym.PYM_ID
        ),
        
        final_table AS(
            SELECT
                psh.PYM_ID,
                psh.PTT_FULL_M,
                psh.SERVICE,
                ms.MEDICINE_AVAILED,
                psh.PYM_SP,
                ms.TOTAL_MEDICINE_PAYMENT,
                psh.PYM_MDE,
                (psh.PYM_SP + ms.TOTAL_MEDICINE_PAYMENT) AS TOTAL_FEE,
                psh.PYM_ID
            FROM patient_service_history psh
            JOIN med_solve ms ON ms.PYM_ID = psh.PYM_ID
            ORDER BY psh.PYM_ID DESC
        )
        
        SELECT * FROM final_table
        '''
        values = []
        cols = ['Ref No.', 'Name', 'Service', 'Medicine/s Availed',
                'Service Fee', 'Medicine Fee', 'Payment Mode', 'Total Fee', 'ID']

        if searchterm:
            sql += " WHERE PTT_FULL_M ILIKE %s"
            values += [f"%{searchterm}%"]

        df = db.querydatafromdatabase(sql, values, cols)

        if not df.empty:
            buttons = []
            for pym_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button(
                            '⨉',
                            n_clicks=0,
                            id={"type": "pymdel", "index": pym_id},
                            color = 'danger'
                        ),
                    )
                ]

            df['Action'] = buttons
            df = df[['Ref No.', 'Name', 'Service', 'Medicine/s Availed',
                     'Service Fee', 'Medicine Fee', 'Payment Mode', 'Total Fee', 'Action']]

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
            return [html.P("No data found.")]
    else:
        raise PreventUpdate

'''LOAD BLANK PAYMENT FORM'''
@app.callback(
    [
        Output('create-invoice', 'is_open', allow_duplicate=True)
    ],
    [
        Input('btn-create-invoice', 'n_clicks')
    ],
    prevent_initial_call=True
)
def load_payment_form(modalbtn):
    ctx = dash.callback_context
    if ctx.triggered:
        event_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if event_id == 'btn-create-invoice' and modalbtn:
            modal_open = False
            modal_open = True
            return [modal_open]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

'''LOAD PATIENT DROPDOWN'''
@app.callback(
    [
        Output('payment-patient-name', 'options'),
    ],
    [
        Input('url', 'pathname')
    ]
)
def load_ptt_dropdown(pathname):
    if pathname == '/payment':
        sql = '''
            SELECT
                (PTT_FM || ' ' ||PTT_LM) AS PTT_FULL_M,
                PTT_ID
            FROM patient
            WHERE PTT_DEL_IND = FALSE    
        '''

        values = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, values, cols)

        ptt_list = df.to_dict(orient='records')

    else:
        raise PreventUpdate

    return [ptt_list]

'''LOAD SERVICE'''
@app.callback(
    [
        Output('payment-service', 'children'),
    ],
    [
        Input('payment-patient-name', 'value'),
        Input('url', 'pathname')
    ]
)
def load_service(ptt_id, pathname):
    if pathname == '/payment':
        sql = '''
            WITH get_visit_id AS(
                    SELECT 
                        MAX(VISIT_ID) AS VISIT_ID
                    FROM patient_visit 
                    WHERE PTT_ID = %s
            )

            SELECT
                s.SRVC_M AS SERVICE
            FROM service s
            JOIN patient_visit pv
            ON pv.SRVC_id = s.SRVC_ID
            WHERE (pv.VISIT_ID = (SELECT VISIT_ID FROM get_visit_id)) AND pv.VISIT_Q = 'IN PROGRESS' AND pv.VISIT_DEL_IND = FALSE; 
        '''

        values = [ptt_id]
        cols = ['service']

        df = db.querydatafromdatabase(sql, values, cols)

        if df.empty:
            return [html.Div('Check Queue Status!', style={'fs': '16px'})]
        else:
            return [df['service']]
    else:
        raise PreventUpdate

'''ADDING MEDICINE'''
@app.callback(
    [
        Output("payment-medicine-dropdown", "children"),
        Output("payment-medicine-qty", "children")
    ],
    [
        Input("btn-add-med", "n_clicks"),
        Input('url', 'pathname')
    ]
)
def display_dropdowns(n_clicks, pathname):
    if pathname == '/payment':
        patched_med = Patch()
        patched_med_qty = Patch()

        sql = '''
            WITH most_recent_refill AS (
                SELECT
                    MED_ID,
                    MED_COUNT,
                    MAX(MED_COUNT_LAST_UPD) AS MOST_RECENT_REFILL
                FROM medicine
                GROUP BY MED_ID, MED_COUNT
            ),

            solving_current_stock AS (
                SELECT
                    m.MED_ID,
                    mr.MED_COUNT,
                    CASE
                        WHEN (mr.MED_COUNT - COALESCE(SUM(mp.MED_PYM_Q), 0)) < 0 THEN 0
                        ELSE (mr.MED_COUNT - COALESCE(SUM(mp.MED_PYM_Q), 0))
                    END AS UPD_STOCK
                FROM medicine m
                LEFT JOIN medicine_payment mp
                    ON m.MED_ID = mp.MED_ID AND mp.MED_PYM_TIME > (
                        SELECT MOST_RECENT_REFILL
                        FROM most_recent_refill
                        WHERE MED_ID = m.MED_ID
                    )
                JOIN most_recent_refill mr
                    ON m.MED_ID = mr.MED_ID
                GROUP BY m.MED_ID, mr.MED_COUNT
            ),

            final_table AS (
                SELECT
                    med.MED_ID,
                    med.MED_M,
                    med.MED_COST,
                    med.MED_MP,
                    COALESCE(solved.UPD_STOCK, med.MED_COUNT) AS UPD_STOCK,
                    med.MED_ROP
                FROM medicine med
                LEFT JOIN solving_current_stock solved
                    ON med.MED_ID = solved.MED_ID
                WHERE med.med_del_ind = false
            )

                        
            SELECT
                (MED_M || ' ' || '(Stock: ' || UPD_STOCK || ')') as MED_INFO,
                MED_ID
            FROM final_table
        '''

        values = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, values, cols)

        med_list = df.to_dict(orient='records')

        new_med_dropdown = dcc.Dropdown(
            med_list,
            id={"type": "payment-med-brand", "index": n_clicks},
            style={
                'background-color': '#E0E5E9',
                'font-family': 'Helvetica, sans-serif'
            },
            className = 'mb-3'
        )

        new_med_qty = dbc.Input(
            value=0,
            id={"type": "payment-med-qty", "index": n_clicks},
            style={
                'background-color': '#E0E5E9',
                'font-family': 'Helvetica, sans-serif', 
                'line-height': '16px'
            },
            className = 'mb-3'
        )
        patched_med.append(new_med_dropdown)
        patched_med_qty.append(new_med_qty)
        return [patched_med, patched_med_qty]
    else:
        raise PreventUpdate

'''SOLVING FOR THE TOTAL'''
@app.callback(
    [
        Output("payment-medicine-dropdown-output", "children")
    ],
    [
        Input('payment-service-fee', 'value'),
        Input({"type": "payment-med-brand", "index": ALL}, "value"),
        Input({"type": "payment-med-qty", "index": ALL}, "value"),
    ]
)
def display_total(srvc_sp, meds, qtys):
    selected_med_price = []
    sql = '''
        SELECT 
            MED_ID, 
            MED_M, 
            MED_MP
        FROM medicine
    '''
    values = []
    cols = ['med_id', 'med_name', 'med_price']

    df = db.querydatafromdatabase(sql, values, cols)
    for i in meds:
        selected_med_price += [df.loc[df['med_id'] == i, 'med_price'].iloc[0]]

    total = sum(float(x) * float(y)
                for x, y in zip(selected_med_price, qtys)) + float(srvc_sp)

    return [total]

'''SAVE IN DB'''
@app.callback(
    [
        Output('payment-alert', 'is_open'),
        Output('payment-alert', 'color'),
        Output('payment-alert', 'children'),
    ],
    [
        Input('btn-payment-save', 'n_clicks'),
        Input('payment-patient-name', 'value'),
        Input('payment-mode', 'value'),
        Input('payment-service-fee', 'value'),
        Input({"type": "payment-med-brand", "index": ALL}, "value"),
        Input({"type": "payment-med-qty", "index": ALL}, "value"),

    ]
)
def save_payment(savebtn, Patient, Payment_Mode, Service_Fee, meds, qtys):
    ctx = dash.callback_context
    if ctx.triggered:
        event_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if event_id == 'btn-payment-save' and savebtn:
            alert_open = True
            alert_color = 'success'
            alert_text = 'Payment saved!'
            
            required_fields = ['Patient', 'Payment_Mode', 'Service_Fee']
            
            '''EMPTY ERROR VALIDATION'''
            for field in required_fields:
                if not locals().get(field):
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = f"{field.replace('_', ' ')} is required!"
                    return [alert_open, alert_color, alert_text]
            
            else:  
                sql = '''
                    WITH get_visit_id AS(
                        SELECT 
                            MAX(VISIT_ID) AS VISIT_ID
                        FROM patient_visit 
                        WHERE PTT_ID = %s
                    )

                    INSERT INTO payment(PYM_MDE, PYM_SP, VISIT_ID)
                    VALUES(%s, %s, (SELECT VISIT_ID FROM get_visit_id));
                    
                    
                    WITH get_visit_id AS(
                        SELECT 
                            MAX(VISIT_ID) AS VISIT_ID
                        FROM patient_visit 
                        WHERE PTT_ID = %s
                    )
                    UPDATE patient_visit
                    SET VISIT_Q = 'COMPLETED'
                    WHERE VISIT_ID = (SELECT VISIT_ID FROM get_visit_id);
                '''
                values = [Patient, Payment_Mode, Service_Fee, Patient]

                db.modifydatabase(sql, values)

                for x, y in zip(meds, qtys):
                    sql = '''
                        WITH get_pym_id AS(
                            SELECT 
                                MAX(PYM_ID) AS PYM_ID
                            FROM payment
                        )
                        INSERT INTO medicine_payment(MED_ID, MED_PYM_Q, PYM_ID, MED_PYM_TIME)
                        VALUES(%s, %s, (SELECT PYM_ID FROM get_pym_id), NOW())
                    '''
                    values = [x, y]
                    db.modifydatabase(sql, values)

                return [alert_open, alert_color, alert_text]

'''REFRESH TO SHOW SAVE SUCCESS'''
@app.callback(
    [
        Output('payment-content', 'children', allow_duplicate=True),
        Output('create-invoice', 'is_open')
    ],
    [
        Input('exit', 'n_clicks'),
        Input('payment-content', 'children')
    ],
    prevent_initial_call=True
)
def save_payment_status(modalbtn, layout):
    ctx = dash.callback_context
    if ctx.triggered:
        event_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if event_id == 'exit' and modalbtn:
            return [layout, False]

'''DELETE MEDICINE'''
@app.callback(
    [
        Output('payment-content', 'children')
    ],
    [
        Input({"type": "pymdel", "index": ALL}, 'n_clicks'),
        Input('payment-content', 'children')
    ]
)
def del_medicine(button_clicks, layout):
    if sum(button_clicks) >= 1:
        ctx = dash.callback_context
        t = list(ctx.triggered_prop_ids.values())[0]
        changed_id = t['index']

        sql = '''
            UPDATE payment
            SET PYM_DEL_IND = TRUE
            WHERE PYM_ID = %s
        '''
        values = [changed_id]

        db.modifydatabase(sql, values)

        return [layout]
