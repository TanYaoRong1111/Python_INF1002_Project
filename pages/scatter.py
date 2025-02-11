import dash
from dash import dcc, html, register_page, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate

register_page(__name__, name="Price vs Rating Scatter Plot", path='/price-rating-scatter')

product_options = ['Laptop', 'Phones']
country_options = ['Indonesia', 'Malaysia', 'Philippines', 'Singapore', 'Thailand']

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Price vs Rating Across Countries", 
                        style={'textAlign': 'center', 'color': 'white'}),
                className="mb-4"
            )
        ),

        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='country_name',
                    options=[{'label': country, 'value': country} for country in country_options],
                    placeholder="Select Country",
                    className="mb-4",
                    style={'backgroundColor': 'white', 'color': 'black'}
                ),
                width=6
            )
        ),

        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='product_name',
                    options=[{'label': opt, 'value': opt} for opt in product_options],
                    placeholder="Select Product Category",
                    className="mb-4",
                    style={'backgroundColor': 'white', 'color': 'black'}
                ),
                width=6
            )
        ),

        dbc.Row(
            dbc.Col(
                dcc.Graph(id="scatter-chart"),  
                id="scatter_col",
                className="mb-4",
                style={"display": "none"},
            )
        ),
    ],
    fluid=True,
    style={'padding': '20px', 'backgroundColor': 'black'}  
)

@dash.callback(
    [Output('scatter-chart', 'figure'),
     Output('scatter_col', 'style')],
    [Input('country_name', 'value'),
     Input('product_name', 'value')]
)
def update_scatter(selected_country, selected_product):
    if not selected_country or not selected_product:
        raise PreventUpdate

    file_path = f"Dataset/{selected_country}_{selected_product}.csv"

    try:
        df = pd.read_csv(file_path)

        if "Price" not in df.columns or "Rating" not in df.columns:
            return px.scatter(title="Invalid dataset format"), {"display": "none"}

        if df.empty:
            return px.scatter(title="No data available"), {"display": "none"}

        fig = px.scatter(df, x="Price", y="Rating", 
                         title=f"Price vs Rating for {selected_product} in {selected_country}",
                         color="Brand", 
                         size_max=10,
                         template="plotly_dark",
                         trendline="ols")

        return fig, {"display": "block"}

    except FileNotFoundError:
        return px.scatter(title="Dataset not found"), {"display": "none"}
