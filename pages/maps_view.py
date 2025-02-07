import dash
from dash import dash_table, dcc, html, callback, register_page
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from callback_functions import update_table, update_map
from dash.exceptions import PreventUpdate

# Register page
register_page(__name__, name="View Map", path='/Map')

options = ['Laptop', 'Phones']
options2 = ['Malaysia', 'Singapore', 'Thailand', 'Indonesia','Philippines']



# Custom navbar with dropdown
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='product_name',
                    options=options,
                    placeholder="Select Product Category",
                    className="mb-4"
                ),
                width=6
            )
        ),
        
        dbc.Row(
            dbc.Col(
                html.Div(id="output", className="alert alert-info", role="alert"),
                className="mb-4"
            )
        ),
        
        dbc.Row(
            dbc.Col(
                dcc.Graph(id="choropleth-map"),  # Choropleth map component
                className="mb-4"
            ),
            style={"display": "none"},
            id="3rd-graph-container",
        ),
        
    ],
    fluid=True,
    style={'padding': '20px'}
)

# Callback to update the choropleth map
@callback(
    [Output('choropleth-map', 'figure'), Output("3rd-graph-container", "style")],
    [Input('product_name', 'value')]
)

def update_content(Item):
    if Item is None:
        raise PreventUpdate
    else:
        return update_map(Item)
