import dash
from dash import dash_table, dcc, html, callback, register_page
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from callback_functions import update_table
from dash.exceptions import PreventUpdate

# Register page
register_page(__name__, name="Tables", path='/tables')

options = ['Laptop', 'Phones', 'Mouse', 'Keyboard', 'Monitor']
options2 = ['Malaysia', 'Singapore', 'Thailand', 'Indonesia']

# Custom navbar with dropdown

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='input1',
                    options=options,
                    placeholder="Select Product Category",
                    className="mb-4"
                ),
                width=6
            )
        ),

        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='input2',
                    options=options2,
                    placeholder="Select Country",
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
                dash_table.DataTable(
                    id="data-table2",
                    page_size=10,  # Number of rows per page        
                    sort_action="native",  # Enable native sorting
                    sort_mode="single",  # Allow single-column sorting
                    # filter_action='native',
                    style_cell_conditional=[
                        {'if': {'column_id': 'Name'},
                        'width': '50%'},
                        {'if': {'column_id': 'Seller Name'},
                        'width': '20%'},
                    ],
                    style_data={
                        'whiteSpace': 'normal',  # Allow text wrapping
                        'height': '50px',  # Fixed height for rows
                        'lineHeight': '50px',  # Ensures text stays vertically aligned
                    },
                    style_data_conditional=[
                        {
                            'if': {'state': 'active'},  # Highlighting rows won't affect height
                            'height': '50px',
                        },
                    ],
                    # Style adjustments
                    style_cell={
                        "textAlign": "center",
                        "padding": "0",  # Remove padding for consistent height
                        "width": "100px",
                        "fontSize": "12px",
                    },
                )
            )
        ),


    ],
    fluid=True,
    style={'padding': '20px'}
    
)

@callback(
    Output('data-table2', 'data'),
    [Input('input1', 'value'), Input('input2', 'value')]
)
def update_content(input1, input2):
    if input1 is None or input2 is None:
        raise PreventUpdate
    else:
        return update_table(str(input1), str(input2))