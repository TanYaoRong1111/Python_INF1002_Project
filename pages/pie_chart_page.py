import dash
from dash import dcc, html, register_page, Input, Output
import dash_bootstrap_components as dbc
from dash import callback, Input, Output
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
from callback_functions import update_revenue_pie_chart



# Register the page
register_page(__name__, name="Revenue Pie Chart", path='/revenue-pie-chart')

# Dropdown options
options = ['Laptop', 'Phones']
options2 = ['Malaysia', 'Singapore', 'Thailand', 'Indonesia', 'Philippines']

# Layout for the revenue pie chart page
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Revenue Distribution by Brand", style={'textAlign': 'center', 'color': 'white'}),
                className="mb-4"
            )
        ),
        
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='product_name',
                    options=[{'label': opt, 'value': opt} for opt in options],
                    placeholder="Select Product Category",
                    className="mb-4"
                ),
                width=6
            )
        ),
        
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='country_name',
                    options=[{'label': opt, 'value': opt} for opt in options2],
                    placeholder="Select Country",
                    className="mb-4"
                ),
                width=6
            )
        ),
        
        dbc.Row(
            dbc.Col(
                dcc.Graph(id="revenue-pie-chart"),  # Pie chart component
                className="mb-4",
                id="pie_chart_col",
                style={"display": "none"},
            ),
            
        ),
    ],
    fluid=True,
    style={'padding': '20px'}
    
)


@callback(
    [Output('revenue-pie-chart', 'figure'),
     Output('pie_chart_col', 'style')],
    [Input('product_name', 'value'),
     Input('country_name', 'value')]
)
def update_content(Item, country):
    if Item is None or country is None:
        raise PreventUpdate
    else:
        return update_revenue_pie_chart(Item, country)