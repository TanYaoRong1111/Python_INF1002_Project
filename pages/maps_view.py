import dash
from dash import dash_table, dcc, html, callback, register_page
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from callback_functions import update_table
from dash.exceptions import PreventUpdate

# Register page
register_page(__name__, name="View Map", path='/Map')

options = ['Laptop', 'Phones', 'Mouse', 'Keyboard', 'Monitor']
options2 = ['Malaysia', 'Singapore', 'Thailand', 'Indonesia']

# Example revenue data for Southeast Asian countries
revenue_data = {
    "countries": ["Thailand", "Vietnam", "Malaysia", "Indonesia", "Philippines", "Singapore", "Myanmar", "Cambodia", "Laos", "Brunei"],
    "revenue": [500, 300, 400, 600, 350, 800, 200, 150, 100, 50]  # Example revenue values
}

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
def update_map(product_name):
    if product_name is None:
        raise PreventUpdate
    
    # Example: Update revenue data based on the selected product category
    # You can replace this with your actual logic to fetch revenue data
    updated_revenue = [x * 2 if product_name == "Laptop" else x for x in revenue_data["revenue"]]
    
    # Create the choropleth map
    fig = go.Figure(go.Choropleth(
        locations=revenue_data["countries"],  # Country names
        z=updated_revenue,                   # Updated revenue values
        locationmode="country names",        # Use country names as locations
        colorscale="Viridis",                # Color scale
        colorbar_title="Revenue (in millions)",  # Color bar title
    ))

    # Update the geographic properties to focus on Southeast Asia
    fig.update_geos(
        visible=False, resolution=50, scope="asia",
        showcountries=True, countrycolor="Black",
        showsubunits=True, subunitcolor="Blue",
        center=dict(lon=105, lat=15),  # Center on Southeast Asia
        projection_scale=3,            # Zoom level

    )

    # Update the layout
    fig.update_layout(
        title=f"Revenue in Southeast Asia for {product_name}",  # Dynamic title
        height=500,
        margin={"r":0,"t":30,"l":0,"b":0}
    )

    return fig, {"display": "block"}