import dash
from dash import dash_table, dcc, html, callback, register_page
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from callback_functions import *
from dash.exceptions import PreventUpdate

# Register page
register_page(__name__, name="Home_Page", path='/')

figs = list(generate_all_bar_chart())

layout = html.Div([
    html.H1("Welcome to the Lazada Sales Dashboard", style={'textAlign': 'center'}),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=figs[i]), width=6) if i < len(figs) else None  
        for i in range(0, len(figs), 2) 
    ] + [
        dbc.Col(dcc.Graph(figure=figs[i + 1]), width=6) if i + 1 < len(figs) else None  
        for i in range(0, len(figs), 2)
    ]),

    dcc.Graph(
        id='total-sales-treemap',
        figure=generate_total_sales_treemap('Laptop')  # Generate the treemap for "Laptop"
    ),
])


'''
layout = html.Div([
    html.H1("Welcome to the Lazada Sales Dashboard", style={'textAlign': 'center'}),

    dbc.Row([
        dbc.Col([dcc.Graph(figure=fig) for fig in figs], width=12)  # Adjust width if needed
    ])
])
'''