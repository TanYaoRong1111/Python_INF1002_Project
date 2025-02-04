import dash
from dash import dash_table, dcc, html, callback, register_page
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from callback_functions import update_top5, get_brands_and_country
from dash.exceptions import PreventUpdate

# Register page
register_page(__name__, name="Chatbot", path='/top5_filter')

# Custom navbar with dropdown
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    # Instructions for input
                    children=[
                        html.H2("Top 5 Laptops based on Ratings", style={'color': 'white'}),
                        html.P("(followed by Number of Sales if ratings are the same)"),
                        html.Br(),
                        html.H4("Criterias:", style={'color': 'white'}),
                        html.P("A country name must be stated", style={'color': 'grey'}),
                        html.P("If you want to include price range, input in this format:", style={'color': 'grey'}),
                        html.P('"price range (minimum price),(Maximum price)"'),
                        html.P('[If either one price is not needed, replace with a "0"]', style={'color': 'white'}),
                    ],
                    className="mb-4"
                ),
                width=12
            )
        ),
        
        dbc.Row(
            dbc.Col(
                dcc.Input(
                    id='input_filter',
                    type='text',
                    placeholder="Enter query...",
                    className="mb-4",
                    style={'width': '100%'}
                ),
                width=12
            )
        ),
        
        dbc.Row(
            dbc.Col(
                html.Div(
                    id="criteria_not_met",  # Alert if country not present in input and/or price range format is wrong
                    children="Please specify a country in the filter input and/or use the correct format for price range!",
                    style={'display': 'none'}  # Initially hidden
                ),
                className="mb-4"
            )
        ),
        
        dbc.Row(
            dbc.Col(
                dash_table.DataTable(
                    id="data-table3",
                    page_size=10,  # Number of rows per page        
                    sort_action="native",  # Enable native sorting
                    sort_mode="single",  # Allow single-column sorting
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

# Callback function to update the table based on the user's input
@callback(
    [Output('data-table3', 'data'), Output('criteria_not_met', 'style')],
    [Input('input_filter', 'value')]
)
def update_content(input_filter):
    if not input_filter:
        raise PreventUpdate
    
    # Checking to see if a ValueError is raised
    try:
        # Return the data for the table and ensure the popup is not displayed
        return update_top5(input_filter), {'display': 'none'}
    
    except (ValueError):
        # If no country is found or price range format is wrong, trigger the popup (ValueError is raised)
        return [], {'display': 'block'}