import dash
from dash import dash_table, dcc, html, callback, register_page
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from callback_functions import *
from dash.exceptions import PreventUpdate
from callback_functions import generate_total_sales_treemap, create_boxplot_layout

# Register page
register_page(__name__, name="Home_Page", path='/')

options = ['Laptop', 'Phones']

# Get the boxplot figure
boxplot_figure = create_boxplot_layout("Laptop")

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H1(
                "Welcome to the Lazada Sales Dashboard",
                className="text-center my-4"
            ),
            width=12
        )
    ]),

    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='product_name',
                options=[{'label': opt, 'value': opt} for opt in options],
                placeholder="Select Product Category",
                className="mb-3"
            ),
            width=6
        )
    ], justify="center"),

    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='total-sales-treemap',
                figure=generate_total_sales_treemap('Laptop'),
                style={'height': '500px'}
            ),
            width=12
        )
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='boxplot',
                figure=boxplot_figure,
                style={'height': '500px'}
            ),
            width=12
        )
    ], className="mb-4")
], fluid=True)


@callback(
    
    [Output('total-sales-treemap', 'figure'),
     Output('boxplot', 'figure')],
    [Input('product_name', 'value')]
)
def update_content(Item):
    if Item is None:
        raise PreventUpdate
    else:
        return generate_total_sales_treemap(Item), create_boxplot_layout(Item)