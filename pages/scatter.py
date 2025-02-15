import dash
from dash import dcc, html, register_page, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
import os

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
                dcc.RadioItems(
                    id='top_brands_selector',
                    options=[
                        {'label': 'Top 5 Brands', 'value': 5},
                        {'label': 'Top 10 Brands', 'value': 10}
                    ],
                    value=5,
                    labelStyle={'display': 'inline-block', 'margin-right': '10px', 'color': 'white'}
                ),
                width=6,
                className="mb-4"
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
)

@callback(
    Output('scatter-chart', 'figure'),
    Output('scatter_col', 'style'),
    Input('country_name', 'value'),
    Input('product_name', 'value'),
    Input('top_brands_selector', 'value')
)
def update_scatter(selected_country, selected_product, top_n):
    if not selected_country or not selected_product:
        raise PreventUpdate

    file_path = f"Dataset/{selected_country}_{selected_product}.csv"

    if not os.path.exists(file_path):
        fig = px.scatter(title="Dataset not found")
        return fig, {"display": "block"}  # Show error message

    try:
        df = pd.read_csv(file_path)
        df.rename(columns={"Number of Sales": "Sales"}, inplace=True)  # Ensure column name consistency

        required_columns = {"Price", "Rating", "Brand", "Sales"}
        if not required_columns.issubset(df.columns):
            fig = px.scatter(title="Invalid dataset format")
            return fig, {"display": "block"}

        if df.empty:
            fig = px.scatter(title="No data available")
            return fig, {"display": "block"}

        # Normalize column names
        df.columns = df.columns.str.strip()
        
        top_brands = df.groupby("Brand")["Sales"].sum().nlargest(top_n).index
        df_filtered = df[df["Brand"].isin(top_brands)]
        
        fig = px.scatter(df_filtered, x="Price", y="Rating", 
                         title=f"Price vs Rating for {selected_product} in {selected_country} (Top {top_n} Brands)",
                         color="Brand", 
                         size_max=10,
                         template="plotly_dark",
                         trendline="ols")

        return fig, {"display": "block"}

    except Exception:
        fig = px.scatter(title="Error loading data")
        return fig, {"display": "block"}
