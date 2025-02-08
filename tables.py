import dash
from dash import dash_table, dcc, html, callback, register_page
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from callback_functions import update_table
from dash.exceptions import PreventUpdate
import dash_ag_grid as dag

# Register page
register_page(__name__, name="Tables", path='/tables')

options = ['Laptop', 'Phones', 'Mouse', 'Keyboard', 'Monitor']
options2 = ['Malaysia', 'Singapore', 'Thailand', 'Indonesia']

# Define the AG Grid column definitions
columnDefs = [
    {"field": "Name", "filter": "agTextColumnFilter"},
    {"field": "Price", "filter": "agNumberColumnFilter"},
    {"field": "Brand", "filter": "agTextColumnFilter"},
    {"field": "Rating", "filter": "agNumberColumnFilter"},
    {"field": "Seller Name", "filter": "agTextColumnFilter"},
    {"field": "Number of Sales", "filter": "agNumberColumnFilter"},
    {"field": "Number of Reviews", "filter": "agNumberColumnFilter"}
]

df = pd.DataFrame({
    "Name": [],
    "Price": [],
    "Brand": [],
    "Rating": [],
    "Seller Name": [],
    "Number of Sales": [],
    "Number of Reviews": []
})

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

                dag.AgGrid(
                    id="data-table2",
                    columnDefs=columnDefs,
                    rowData=df.to_dict("records"),
                    defaultColDef={
                        "filter": True,  # Enable filtering for all columns
                        "sortable": True,  # Enable sorting for all columns
                        "resizable": True,  # Allow resizing columns
                        "floatingFilter": True  # Add floating filters above the grid
                    },
                    dashGridOptions={"pagination": True, "paginationPageSize": 10},  # Enable pagination
                    style={"height": 550, "width": "100%"}  # Set grid height and width
                ),
            )
        ),


    ],
    fluid=True,
    style={'padding': '20px'}
    
)

@callback(
    Output('data-table2', 'rowData'),
    [Input('input1', 'value'), Input('input2', 'value')]
)
def update_content(input1, input2):
    if input1 is None or input2 is None:
        raise PreventUpdate
    else:
        return update_table(str(input1), str(input2))