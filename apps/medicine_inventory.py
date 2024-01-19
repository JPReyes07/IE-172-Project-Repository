import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from dash.dependencies import Input, Output, State, ALL
from apps import dbconnect as db
from app import app
from urllib.parse import urlparse, parse_qs

layout = html.Div(
    [
        dbc.Form(
            dbc.Row(
                [
                    html.H1("Medicine Inventory", 
                              style={'font-family': 'Helvetica, sans-serif',
                                    'fontWeight': 'bold'
                                }
                    ),

                    dbc.Col( dbc.Button("Add New Medicine",
                        id = 'addmed-button',
                        className="d-grid gap-2 col-8 mx-auto"
                        )

                    ),

                    dbc.Col( dbc.Button("Update Medicine Information",
                        id = 'updmed-button',
                        className="d-grid gap-2 col-8 mx-auto"
                        )

                    ),

                    dbc.Col(
                        dbc.Input(
                            type='text',
                            id='medinv-filter',
                            placeholder='Search Medicine',
                        ),
                        width=3,
                        style={'marginLeft': 'auto', 'textAlign': 'right', 'marginRight': '3em'}
                    ),   
                ],
                className='mb-3',
                style={'marginTop': '2em'}
            )
        ),

        # Enter new medicine
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle('New Medicine Form')
                ),

                dbc.ModalBody(
                    html.Div(
                        [
                            dbc.Card(
                                [
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
                                                                            dbc.Label('Medicine Name', width = 3),
                                                                            dbc.Col(
                                                                                dbc.Input(
                                                                                    id = 'med-new-name',
                                                                                    type = 'text',
                                                                                    style={
                                                                                            'background-color': '#E0E5E9',
                                                                                            'font-family': 'Helvetica, sans-serif',
                                                                                            'borderRadius': 12,
                                                                                            'width':'250px',
                                                                                    }
                                                                                ),
                                                                            )
                                                                        ],
                                                                        className="mb-3"
                                                                    ),
                                                                )
                                                            )
                                                        ),
                                                    ]
                                                ),

                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            html.Div(
                                                                dbc.Form(
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Label('Cost (Php)', width = 3),
                                                                            dbc.Col(
                                                                                dbc.Input(
                                                                                    id = 'med-new-cost',
                                                                                    type = 'text',
                                                                                    style={
                                                                                            'background-color': '#E0E5E9',
                                                                                            'font-family': 'Helvetica, sans-serif',
                                                                                            'borderRadius': 12,
                                                                                            'width':'250px',
                                                                                    }
                                                                                ),
                                                                            )
                                                                        ],
                                                                        className="mb-3"
                                                                    ),
                                                                )
                                                            )
                                                        ),
                                                    ]
                                                ),

                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            html.Div(
                                                                dbc.Form(
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Label('Selling Price (Php)', width = 3 ),
                                                                            dbc.Col(
                                                                                dbc.Input(
                                                                                    id = 'med-new-sp',
                                                                                    type = 'text',
                                                                                    style={
                                                                                            'background-color': '#E0E5E9',
                                                                                            'font-family': 'Helvetica, sans-serif',
                                                                                            'borderRadius': 12,
                                                                                            'width':'250px',
                                                                                    }
                                                                                ),
                                                                            )
                                                                        ],
                                                                        className="mb-3"
                                                                    ),
                                                                )
                                                            )
                                                        ),
                                                    ]
                                                ),

                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            html.Div(
                                                                dbc.Form(
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Label('Quantity', width = 3),
                                                                            dbc.Col(
                                                                                dbc.Input(
                                                                                    id = 'med-new-qty',
                                                                                    type = 'text',
                                                                                    style={
                                                                                            'background-color': '#E0E5E9',
                                                                                            'font-family': 'Helvetica, sans-serif',
                                                                                            'borderRadius': 12,
                                                                                            'width':'250px',
                                                                                    }
                                                                                ),
                                                                            )
                                                                        ],
                                                                        className="mb-3"
                                                                    ),
                                                                )
                                                            )
                                                        ),
                                                    ]
                                                ),

                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            html.Div(
                                                                dbc.Form(
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Label('Reorder Point', width = 3),
                                                                            dbc.Col(
                                                                                dbc.Input(
                                                                                    id = 'med-new-rop',
                                                                                    type = 'text',
                                                                                    style={
                                                                                            'background-color': '#E0E5E9',
                                                                                            'font-family': 'Helvetica, sans-serif',
                                                                                            'borderRadius': 12,
                                                                                            'width':'250px',
                                                                                    }
                                                                                ),
                                                                            )
                                                                        ],
                                                                        className="mb-3"
                                                                    ),
                                                                )
                                                            )
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        )
                                    )
                                ]
                            ),
                        ]
                    )
                ),                        

                dbc.ModalFooter(
                    [
                        dbc.Button(
                            "Save", id="btn-save-new-med", className="ms-auto"
                        ),

                        html.Div("Nothing's happened!", id='med-new-save-status')
                    ]

                )

            ],
            style={'font-family': 'Helvetica, sans-serif'},
            size='lg',
            id="create-medinv-form",
            is_open=False,   
        ),
        
        html.Div(
            "Table with patients will go here",
            id='medinv-table'
        ),

        # UPDATE MEDICINE INFORMATION
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle('Edit Medicine Form')
                ),

                dbc.ModalBody(
                    html.Div(
                        [
                           
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.H2('Medicine Name', id = 'med-name')
                                    ),

                                    dbc.Col(
                                        dcc.Dropdown(
                                                id = 'updmed-name',
                                                placeholder = 'Search Medication',
                                        ),
                                    ),

                                ]
                            ),
                            dbc.Card(
                                [
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
                                                                            dbc.Label('Additional Qty', width = 6),
                                                                            dbc.Col(
                                                                                dbc.Input(
                                                                                    value = 0,
                                                                                    id = 'med-addtnl-qty',
                                                                                    type = 'numeric',
                                                                                    style={
                                                                                            'background-color': '#E0E5E9',
                                                                                            'font-family': 'Helvetica, sans-serif',
                                                                                            'borderRadius': 12,
                                                                                            'width':'250px',
                                                                                    }
                                                                                ),
                                                                            )
                                                                        ],
                                                                        className="mb-3"
                                                                    ),
                                                                )
                                                            )
                                                        ),

                                                        dbc.Col(
                                                            html.Div(
                                                                dbc.Form(
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Label('Current Stock', width = 6),
                                                                            dbc.Col(
                                                                                html.Div(id = 'med-current-stock')
                                                                            )
                                                                        ],
                                                                        className="mb-3"
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
                                                                            dbc.Label('Cost Price', width = 6),
                                                                            dbc.Col(
                                                                                html.Div(id = 'med-cost')
                                                                            )
                                                                        ],
                                                                        className="mb-3"
                                                                    ),
                                                                )
                                                            )
                                                        ),
                                                        dbc.Col(
                                                            html.Div(
                                                                dbc.Form(
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Label('Total Stock', width = 6),
                                                                            dbc.Col(html.Div('',
                                                                                             id='med-total-stock'))
                                                                        ],
                                                                        className="mb-3"
                                                                    ),
                                                                )
                                                            )
                                                        ),
                                                    ]
                                                ),

                                                dbc.Row(
                                                    dbc.Col(
                                                        html.Div(
                                                            dbc.Form(
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label('Sell Price', width = 3),
                                                                        dbc.Col(
                                                                            html.Div(id = 'med-sell-price')
                                                                        )
                                                                    ],
                                                                    className="mb-3"
                                                                ),
                                                            )
                                                        )
                                                    ),
                                                )
                                            ]
                                        )
                                    )
                                ]
                            )
                        ]
                    )
                ), 
                dbc.ModalFooter(
                    [
                        dbc.Button(
                            "Save", id="btn-save-upd-med", n_clicks=0,  
                        ),

                         html.Div("Nothing's happened!", id='upd-save-status')
                    ],
                        className="mx-auto",
                )

            ],
            style={'font-family': 'Helvetica, sans-serif'},
            size='lg',
            id="upd-medinv-form",
            is_open=False,   
        ),
    ],
    style={'font-family': 'Helvetica, sans-serif'},
    id = 'medinv-content'
)

'''LOAD BLANK MED FORM'''
@app.callback(
    [
        Output('create-medinv-form', 'is_open'),
    ],
    [
        Input('addmed-button', 'n_clicks'),
    ],
    [
        State('url', 'search')
    ]
)
def load_new_med_form (modalbtn, search):
    ctx = dash.callback_context
    if ctx.triggered:
        event_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if event_id == 'addmed-button' and modalbtn:
            modal_open = False
            modal_open = True                   
            return [modal_open]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

'''SAVE NEW MEDICINE'''
@app.callback(
    [
        Output('med-new-save-status', 'children'),
    ],
    [
        Input('btn-save-new-med', 'n_clicks'),
        Input('med-new-name', 'value'),
        Input('med-new-cost', 'value'),
        Input('med-new-sp', 'value'),
        Input('med-new-qty', 'value'),
        Input('med-new-rop', 'value')
    ]
)
def save_med_new(savebtn, med_name, med_cost, med_sp, med_qty, med_rop):
    ctx = dash.callback_context
    if ctx.triggered:
        event_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if event_id == 'btn-save-new-med' and savebtn:
            sql = '''
                INSERT INTO medicine(MED_M, MED_COST, MED_MP, MED_COUNT, MED_ROP)
                VALUES(%s, %s, %s, %s, %s)
            '''
            values = [med_name, med_cost, med_sp, med_qty, med_rop]

            db.modifydatabase(sql, values)

            return['Saved!']

'''LOAD MEDICINE TABLE'''
@app.callback(
    [
        Output('medinv-table', 'children'),
    ],
    [
        Input('url', 'pathname'),
    ],
)
def load_med_inv (pathname):
    if pathname == '/medicine':
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
                    (mr.MED_COUNT - COALESCE(SUM(mp.MED_PYM_Q), 0)) AS UPD_STOCK
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
            )

            SELECT
                med.MED_ID,
                med.MED_M,
                med.MED_COST,
                med.MED_MP,
                COALESCE(solved.UPD_STOCK, med.MED_COUNT) AS UPD_STOCK,
                med.MED_ROP,
                med.MED_ID
            FROM medicine med
            LEFT JOIN solving_current_stock solved
                ON med.MED_ID = solved.MED_ID
            WHERE med.med_del_ind = false;
        '''
        values = []
        cols = ['MedID', 'Medication', 'Cost (Php)', 'Selling Price (Php)', 'Current Stock', 'Reorder Point', 'Remove']

        df = db.querydatafromdatabase(sql, values, cols)

        if not df.empty: 
            del_buttons = []

            for med_id in df['MedID']:
                del_buttons += [
                    html.Div(
                        dbc.Button(
                            '⨉',
                            n_clicks = 0,
                            id = {"type": "meddel", "index": med_id},
                            color = 'danger'
                        ),
                    )
                ]
        df['Remove'] = del_buttons

        df = df[['MedID', 'Medication', 'Cost (Php)', 'Selling Price (Php)', 'Current Stock', 'Reorder Point', 'Remove']]

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

'''LOAD UPDATE MEDICINE FORM'''
@app.callback(
    [
        Output('upd-medinv-form', 'is_open'),
    ],
    [
        Input('updmed-button', 'n_clicks'),
    ],
)
def load_upd_med_form (modalbtn):
    ctx = dash.callback_context
    if ctx.triggered:
        event_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if event_id == 'updmed-button' and modalbtn:
            modal_open = False
            modal_open = True                   
            return [modal_open]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

'''LOAD MEDICINE DROPDOWN'''
@app.callback(
    [
        Output('updmed-name', 'options'),
    ],
    [
        Input('url', 'pathname')
    ]
)
def load_med_dropdown(pathname):
    if pathname == '/medicine':
        sql = '''
            SELECT
                MED_M,
                MED_ID
            FROM medicine     
        '''

        values = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, values, cols)

        med_list = df.to_dict(orient = 'records')

    else:
        raise PreventUpdate
    
    return [med_list]

'''LOAD MEDICINE INFORMATION'''
@app.callback(
    [
        Output('med-current-stock', 'children'),
        Output('med-cost', 'children'),
        Output('med-sell-price', 'children'),
    ],
    [
        Input('updmed-name', 'value'),
    ],
)
def load_med_info(med_id):
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
                (mr.MED_COUNT - COALESCE(SUM(mp.MED_PYM_Q), 0)) AS UPD_STOCK
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

        final_table AS(
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
        )

        SELECT
            MED_M,
            UPD_STOCK,
            MED_COST,
            MED_MP
        FROM final_table
        WHERE MED_ID = %s
    '''
    values = [med_id]
    cols = ['med_name', 'current_stock', 'cost', 'sp']

    df = db.querydatafromdatabase(sql, values, cols)
    return [df['current_stock'], df['cost'], df['sp']]

'''SUM VALUES'''
@app.callback(
    [
        Output('med-total-stock', 'children')
    ],
    [
        Input('updmed-name', 'value'),
        Input('med-addtnl-qty', 'value')
    ]
)
def sum_new_stock(med_id, addtnl):
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
                (mr.MED_COUNT - COALESCE(SUM(mp.MED_PYM_Q), 0)) AS UPD_STOCK
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

        final_table AS(
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
        )

        SELECT
            UPD_STOCK
        FROM final_table
        WHERE MED_ID = %s
    '''
    values = [med_id]
    cols = ['current_stock']

    df = db.querydatafromdatabase(sql, values, cols)

    total = float(addtnl) + float(df['current_stock'])
    return[total]

'''SAVE UPDATES'''
@app.callback(
    [
        Output('upd-save-status', 'children')
    ],
    [
        Input('btn-save-upd-med', 'n_clicks'),
        Input('updmed-name', 'value'),
        Input('med-total-stock', 'children'),
    ]
)
def save_updates(savebtn, med_id, upd_stock):
    ctx = dash.callback_context
    if ctx.triggered:
        event_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if event_id == 'btn-save-upd-med' and savebtn:
            sql = '''
            UPDATE medicine
            SET 
                MED_COUNT = %s,
                MED_COUNT_LAST_UPD = NOW()
            WHERE MED_ID = %s
            '''
            values = [upd_stock, med_id]

            db.modifydatabase(sql, values)

            return ['Saved!']


'''DELETE MEDICINE'''
@app.callback(
    [
        Output('medinv-content', 'children')
    ],
    [
        Input({"type": "meddel", "index": ALL}, 'n_clicks'),
        Input('medinv-content', 'children')
    ]
)
def del_medicine(button_clicks, layout):
     if sum(button_clicks) >= 1:
        ctx = dash.callback_context
        t = list(ctx.triggered_prop_ids.values())[0]
        changed_id = t['index']

        sql = '''
            UPDATE medicine
            SET MED_DEL_IND = TRUE
            WHERE MED_ID = %s
        '''
        values = [changed_id]

        db.modifydatabase(sql, values)

        return [layout]

