import dash
from dash import dash_table, dcc, html, callback, register_page
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from callback_functions import update_bar_chart
from dash.exceptions import PreventUpdate

# Register page
register_page(__name__, name="Bar chart", path='/')

options = ['Laptop', 'Phones', 'Mouse', 'Keyboard', 'Monitor']
options2 = ['Malaysia', 'Singapore', 'Thailand','Indonesia']

# Custom navbar with dropdown

layout = dbc.Container(
    [
        # Dropdown for Product Category selection
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='input1',
                    options=[{'label': opt, 'value': opt} for opt in options],
                    placeholder="Select Product Category",
                    className="mb-4"
                ),
                width=6
            )
        ),

        # Dropdown for Country selection
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='input2',
                    options=[{'label': opt, 'value': opt} for opt in options2],
                    placeholder="Select Country",
                    className="mb-4"
                ),
                width=6
            )
        ),

        # Output message
        dbc.Row(
            dbc.Col(
                html.Div(id="output", className="alert alert-info", role="alert"),
                className="mb-4"
            )
        ),

        # Row for side-by-side bar graphs
        dbc.Row(
            [
                # First bar graph
                dbc.Col(
                    dcc.Graph(
                        id="sales-histogram",
                        style={
                            'borderRadius': '15px',
                            'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)'
                        },
                        config={'displayModeBar': False}
                    ),
                    width=6,
                    style={"display": "none"},
                    id="graph-container",
                ),

                # Second bar graph
                dbc.Col(
                    dcc.Graph(
                        id="malaysia-sales-histogram",
                        style={
                            'borderRadius': '15px',
                            'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)'
                        },
                        config={'displayModeBar': False}
                    ),
                    width=6,
                    style={"display": "none"},
                    id="2nd-graph-container",
                ),
            ],
            className="mb-4"
        ),
    ],
    fluid=True,
    style={'padding': '20px'}
)



@callback(
    [
     Output('sales-histogram', 'figure'),
     Output("graph-container", "style")],
    [Input('input1', 'value'), Input('input2', 'value')]
)
def update_content(Item, country):
    if Item is None or country is None:
        raise PreventUpdate
    else:
        return update_bar_chart(Item, country)

@callback(
    [
     Output('malaysia-sales-histogram', 'figure'),
     Output("2nd-graph-container", "style")],
    [Input('input1', 'value'), Input('input2', 'value')]
)
def update_content(Item, country):
    if Item is None or country is None:
        raise PreventUpdate
    else:
        return update_bar_chart(Item, country)
