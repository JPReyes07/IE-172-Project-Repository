import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import pandas as pd
from app import app
from dash.dependencies import Input, Output, State
from apps import dbconnect as db

layout = html.Div(
    [
        dbc.Form(
            dbc.Row(
                [
                    html.H1(
                        "Patients", 
                        style={
                            'font-family': 'Helvetica, sans-serif',
                            'fontWeight': 'bold'
                        }
                    ),
                    dbc.Col(
                        dbc.Input(
                            type='text',
                            id='patientrecords_filter',
                            placeholder='Search Patients',
                            style={'borderRadius': 30}
                        ),
                        width=3,
                        style={'marginLeft': 'auto', 'textAlign': 'right', 'marginRight': '3em'}
                    )
                ],
                className='mb-3',
                style={'marginTop': '2em'}
            )
        ),
        html.Div(
            "Table with patients will go here",
            id='patientrecord_patientlist'
        )
    ],

    id = 'ptt-content'
)

@app.callback(
    [
        Output('patientrecord_patientlist', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('patientrecords_filter', 'value')
    ]
)

def patientrecord_patientlist(pathname, searchterm):
    if pathname == '/patient/records':
        sql = """ 
            SELECT 
                PTT_ID,
                (PTT_FM || ' ' ||PTT_LM) AS PTT_FULL_M, 
                PTT_BRTH, 
                PTT_CTNB, 
                PTT_ADDR_PROV,
                PTT_ID,
                PTT_ID
            FROM patient
            WHERE PTT_DEL_IND = FALSE
        """
        values = []
        cols = ['Patient ID', 'Name','Birthdate', 'Contact No.', 'Address', '    ', 'Remove']

        if searchterm:
            sql += " AND (PTT_FM ILIKE %s OR PTT_LM ILIKE %s)"
            values += [f"%{searchterm}%", f"%{searchterm}%"]

        df = db.querydatafromdatabase(sql, values, cols)

        if not df.empty:
            buttons = []
            del_buttons = []
            for ptt_id in df['Patient ID']:
                buttons += [
                    html.Div(
                        dbc.Button('View', 
                                   id='view-button',
                                   href = f"/patient/profile?from={pathname}&ptt_id={ptt_id}",
                                   size='sm', color='primary', className='mx-auto'),
                                   style={'text-align':'left'}
                    )
                ]

                del_buttons += [
                    html.Div(
                        dbc.Button(
                            '⨉',
                            n_clicks = 0,
                            id = {"type": "pttdel", "index": ptt_id},
                            color = 'danger'
                        ),
                    )
                ]

            df['    '] = buttons
            df['Remove'] = del_buttons
            df = df[['Patient ID', 'Name','Birthdate', 'Contact No.', 'Address', '    ', 'Remove']]


            table = dbc.Table.from_dataframe(
                df, 
                striped=True, 
                bordered=False,
                hover=True, 
                size='sm',
                style = {
                    'font-family': 'Helvetica, sans-serif'
                    }
            )

            return [table]
        else:
            return [html.Div(
                    "No records to display",
                    style={'text-align': 'center', 'font-style': 'italic', 'margin-top': '20px'}
                )   
            ]

    else:
        raise PreventUpdate

@app.callback(
    [
        Output('ptt-content', 'children')
    ],
    [
        Input({"type": "pttdel", "index": ALL}, 'n_clicks'),
        Input('ptt-content', 'children')
    ]
)
def del_patient(button_clicks, layout):
     if sum(button_clicks) >= 1:
        ctx = dash.callback_context
        t = list(ctx.triggered_prop_ids.values())[0]
        changed_id = t['index']

        sql = '''
            UPDATE patient
            SET PTT_DEL_IND = TRUE
            WHERE PTT_ID = %s
        '''
        values = [changed_id]

        db.modifydatabase(sql, values)

        return [layout]

