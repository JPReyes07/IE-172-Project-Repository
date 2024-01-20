import dash
import locale
import numpy as np
import webbrowser
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from datetime import datetime, date
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from dash import dcc, Patch
from dash import html
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

locale.setlocale(locale.LC_ALL, 'fil_PH')

# Example data (you may replace this with your actual data)

wellness_checkup_queue = 20
prev_med_queue = 15
prenatal_queue = 10
postnatal_queue = 5
revenue_data = {'Service A': 5000, 'Service B': 3000, 'Service C': 2000}
low_in_stock_items = {'Item X': 5, 'Item Y': 10, 'Item Z': 2}

layout = html.Div([
    # WELCOME
    dbc.Row(
        dbc.Col(
            html.H1("Welcome!",
                    style={'font-weight': 'bold',
                           'text-align': 'center'},
                    className='mt-3'
                    ),
        ),
        className='mb-4'
    ),

    # SERVICE BREAKDOWN
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Completed Service",
                            style={'background-color': '#9FC3E7'}
                        ),
                        dbc.CardBody([html.H1(id='completed-service-value',
                                              style={'font-weight': 'bold',
                                                     'text-align': 'center'}), html.P("Services completed.")]),
                    ],
                    className='h-100'
                ),
                className='mb-4',
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Women's Wellness",
                                       style={'background-color': '#9FC3E7'}),
                        dbc.CardBody([html.H4(id='wellness-checkup-value',
                                              style={'font-weight': 'bold',
                                                     'text-align': 'center'}), html.P("People in queue for wellness checkup.")]),
                    ],
                    className='h-100'
                ),
                className='mb-4',
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Preventive Medicine",
                                       style={'background-color': '#9FC3E7'}),
                        dbc.CardBody([html.H4(id='prev-med-queue-value',
                                              style={'font-weight': 'bold',
                                                     'text-align': 'center'}), html.P("People in queue for preventive medicine.")]),
                    ],
                    className='h-100'
                ),
                className='mb-4',
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Prenatal Pregnancy",
                                       style={'background-color': '#9FC3E7'}),
                        dbc.CardBody([html.H4(id='prenatal-queue-value',
                                              style={'font-weight': 'bold',
                                                     'text-align': 'center'}), html.P("People in queue for prenatal checkup.")]),
                    ],
                    className='h-100'
                ),
                className='mb-4',
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Postnatal Pregnancy",
                                       style={'background-color': '#9FC3E7'}),
                        dbc.CardBody([html.H4(id='postnatal-queue-value',
                                              style={'font-weight': 'bold',
                                                     'text-align': 'center'}), html.P("People in queue for postnatal checkup.")]),
                    ],
                    className='h-100'
                ),
                className='mb-4',
            ),
        ],
        className='align-items-stretch',  # Align cards to have equal height
    ),

    # REVENUE + LOW IN STOCK
    dbc.Row(
        [
            # REVENUE
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                "Revenue This Month",
                                style={'background-color': '#9FC3E7'}),
                            dbc.CardBody(
                                [
                                    html.H3('', id='revenue-month'),
                                    html.P("")
                                ]
                            ),
                        ]
                    ),

                    dbc.Card(
                        [
                            html.Div(id='revenue-month-breakdown-donut')
                        ]
                    ),
                ],

                className='mb-4',
                style={'font-family': 'Helvetica, sans-serif'},
            ),

            # LOW IN STOCK
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardHeader("Low in Stock",
                                           style={'background-color': '#9FC3E7'}),
                            dbc.CardBody(
                                [
                                    html.Div(id='low-in-stock')
                                ]
                            ),
                        ]
                    ),
                ],

                className='mb-4',
                style={'font-family': 'Helvetica, sans-serif'},
            ),

        ],
        className='align-items-stretch',
    ),
], style={'font-family': 'Helvetica, sans-serif'})


@app.callback(
    [
        Output('completed-service-value', 'children'),
    ],
    [
        Input('url', 'pathname')
    ]
)
def summarize_completed_service_today(pathname):
    sql = '''
     SELECT 
        COUNT(*) 
    FROM patient_visit
    WHERE DATE(visit_d_now) = CURRENT_DATE AND visit_q = 'COMPLETED' AND VISIT_DEL_IND = FALSE;
    '''

    values = []
    cols = ['service_count_all']

    df = db.querydatafromdatabase(sql, values, cols)

    return [df['service_count_all']]


@app.callback(
    [
        Output('wellness-checkup-value', 'children'),
    ],
    [
        Input('url', 'pathname')
    ]
)
def summarize_wellness_checkup_today(pathname):
    sql = '''
    SELECT 
        COUNT(*) 
    FROM patient_visit
    WHERE DATE(visit_d_now) = CURRENT_DATE
        AND srvc_id = 1
        AND visit_q <> 'COMPLETED'
        AND VISIT_DEL_IND = FALSE;
    '''

    values = []
    cols = ['wellness_checkup_count']

    df = db.querydatafromdatabase(sql, values, cols)

    return [df['wellness_checkup_count']]


@app.callback(
    [
        Output('prev-med-queue-value', 'children'),
    ],
    [
        Input('url', 'pathname')
    ]
)
def summarize_prev_med_queue_today(pathname):
    sql = '''
    SELECT 
        COUNT(*) 
    FROM patient_visit
    WHERE DATE(visit_d_now) = CURRENT_DATE
	AND srvc_id = 2
	AND visit_q <> 'COMPLETED'
        AND VISIT_DEL_IND = FALSE;
    '''

    values = []
    cols = ['prev_med_queue_count']

    df = db.querydatafromdatabase(sql, values, cols)

    return [df['prev_med_queue_count']]


@app.callback(
    [
        Output('prenatal-queue-value', 'children'),
    ],
    [
        Input('url', 'pathname')
    ]
)
def summarize_prenatal_queue_today(pathname):
    sql = '''
    SELECT 
        COUNT(*) 
    FROM patient_visit
    WHERE DATE(visit_d_now) = CURRENT_DATE
	AND srvc_id = 3
	AND visit_q <> 'COMPLETED'
        AND VISIT_DEL_IND = FALSE;
    '''

    values = []
    cols = ['prenatal_queue_count']

    df = db.querydatafromdatabase(sql, values, cols)

    return [df['prenatal_queue_count']]


@app.callback(
    [
        Output('postnatal-queue-value', 'children'),
    ],
    [
        Input('url', 'pathname')
    ]
)
def summarize_postnatal_queue_today(pathname):
    sql = '''
    SELECT 
        COUNT(*) 
    FROM patient_visit
    WHERE DATE(visit_d_now) = CURRENT_DATE
	AND srvc_id = 4
	AND visit_q <> 'COMPLETED'
        AND VISIT_DEL_IND = FALSE;
    '''

    values = []
    cols = ['postnatal_queue_count']

    df = db.querydatafromdatabase(sql, values, cols)

    return [df['postnatal_queue_count']]


@app.callback(
    [
        Output('revenue-month', 'children'),
    ],
    [
        Input('url', 'pathname')
    ]
)
def summarize_monthly_revenue(pathname):
    sql = '''
    WITH patient_service_history AS(
        SELECT
            pv.VISIT_ID,
            (pt.PTT_FM || ' ' ||pt.PTT_LM) AS PTT_FULL_M,
            sv.SRVC_M AS service,
            pym.PYM_MDE,
            pym.PYM_SP,
            pym.PYM_ID
        FROM patient_visit pv
        JOIN patient pt
        ON pt.PTT_ID = pv.PTT_ID
        JOIN service sv
        ON sv.SRVC_ID = pv.SRVC_ID
        JOIN payment pym
        ON pym.VISIT_ID = pv.VISIT_ID
        WHERE EXTRACT(MONTH FROM pv.visit_d_now) = EXTRACT(MONTH FROM CURRENT_DATE)
    ),

    med_solve AS(
        SELECT
            pym.PYM_ID,
            STRING_AGG(med.MED_M, ', ') AS medicine_availed,
            SUM(med.MED_MP * med_pym.MED_PYM_Q) AS total_medicine_payment
        FROM payment pym
        JOIN medicine_payment med_pym 
        ON med_pym.PYM_ID = pym.PYM_ID
        JOIN medicine med 
        ON med.MED_ID = med_pym.MED_ID
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
        JOIN med_solve ms
        ON ms.PYM_ID = psh.PYM_ID
    )

    SELECT SUM(ft.TOTAL_FEE )
    FROM final_table ft
    '''

    values = []
    cols = ['total_revenue_this_month']

    df = db.querydatafromdatabase(sql, values, cols)

    amt = locale.currency(int(df['total_revenue_this_month']), grouping=True)
    return [amt]


@app.callback(
    [
        Output('revenue-month-breakdown-donut', 'children'),
    ],
    [
        Input('url', 'pathname')
    ]
)
def break_monthly_revenue(pathname):
    sql = '''
        WITH patient_service_history AS(
            SELECT
                pv.VISIT_ID,
                (pt.PTT_FM || ' ' ||pt.PTT_LM) AS PTT_FULL_M,
                sv.SRVC_M AS service,
                pym.PYM_MDE,
                pym.PYM_SP,
                pym.PYM_ID
            FROM patient_visit pv
            JOIN patient pt
            ON pt.PTT_ID = pv.PTT_ID
            JOIN service sv
            ON sv.SRVC_ID = pv.SRVC_ID
            JOIN payment pym
            ON pym.VISIT_ID = pv.VISIT_ID
            WHERE EXTRACT(MONTH FROM pv.visit_d_now) = EXTRACT(MONTH FROM CURRENT_DATE)
        ),

        med_solve AS(
            SELECT
                pym.PYM_ID,
                STRING_AGG(med.MED_M, ', ') AS medicine_availed,
                SUM(med.MED_MP * med_pym.MED_PYM_Q) AS total_medicine_payment
            FROM payment pym
            JOIN medicine_payment med_pym 
            ON med_pym.PYM_ID = pym.PYM_ID
            JOIN medicine med 
            ON med.MED_ID = med_pym.MED_ID
            GROUP BY pym.VISIT_ID, pym.PYM_ID
        ),

    final_table AS (
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
        FROM
            patient_service_history psh
            JOIN med_solve ms ON ms.PYM_ID = psh.PYM_ID
    )

    SELECT
        ft.SERVICE,
        SUM(ft.TOTAL_FEE) AS TOTAL_SALES
    FROM
        final_table ft
    GROUP BY
        ft.SERVICE;
    '''

    values = []
    cols = ['service', 'total_sales']

    df = db.querydatafromdatabase(sql, values, cols)

    labels = df["service"].values.tolist()
    sizes = df['total_sales'].values.tolist()
    colors = ['#FF0000', '#0000FF', '#FFFF00', '#ADFF2F']
    explode = (0.05, 0.05, 0.05, 0.05)

    # Create a Pie chart using plotly.graph_objs
    pie_chart = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=0.3, marker=dict(
        colors=colors, line=dict(color='#000000', width=2)), textinfo='label+percent', pull=explode)])

    # Return the Pie chart as a Dash component
    return [dcc.Graph(figure=pie_chart)]


@app.callback(
    [
        Output('low-in-stock', 'children'),
    ],
    [
        Input('url', 'pathname')
    ]
)
def summarize_stock(pathname):
    sql = '''
    WITH most_recent_refill AS (
        SELECT
            MED_ID,
            MED_COUNT,
            MAX(MED_COUNT_LAST_UPD) AS MOST_RECENT_REFILL
        FROM medicine
        WHERE MED_DEL_IND = FALSE
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
        WHERE MED_DEL_IND = FALSE
    )

    SELECT med_m, upd_stock, med_rop 
	FROM final_table
	WHERE upd_stock <= med_rop;
    '''

    values = []
    cols = ['Medication', 'Current Stock', 'ROP']

    df = db.querydatafromdatabase(sql, values, cols)
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
