import dash
from dash import dcc, html, register_page, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate


register_page(__name__, name="Rating Box Plot", path='/rating-box-plot')


product_options = ['Laptop', 'Phones']
country_options = ['Indonesia', 'Malaysia', 'Philippines', 'Singapore', 'Thailand']


layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Rating Spread Across Brands", 
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
                dcc.Graph(id="boxplot-chart"),  
                id="boxplot_col",
                className="mb-4",
                style={"display": "none"},
            )
        ),
    ],
    fluid=True,
     
)


@dash.callback(
    [Output('boxplot-chart', 'figure'),
     Output('boxplot_col', 'style')],
    [Input('country_name', 'value'),
     Input('product_name', 'value')]
)
def update_boxplot(selected_country, selected_product):
    if not selected_country or not selected_product:
        raise PreventUpdate

    
    file_path = f"Dataset/{selected_country}_{selected_product}.csv"

    try:
        df = pd.read_csv(file_path)

        
        if "Brand" not in df.columns or "Rating" not in df.columns:
            return px.box(title="Invalid dataset format"), {"display": "none"}

        
        brand_counts = df["Brand"].value_counts()
        valid_brands = brand_counts[brand_counts >= 5].index
        filtered_df = df[df["Brand"].isin(valid_brands)]

        if filtered_df.empty:
            return px.box(title="No brands meet the minimum rating count (5)"), {"display": "none"}

        
        fig = px.box(filtered_df, x="Brand", y="Rating",
                     title=f"Rating Variability Across {selected_product} Brands in {selected_country}",
                     points="all",  
                     color="Brand",
                     template="plotly_dark")  

        return fig, {"display": "block"}

    except FileNotFoundError:
        return px.box(title="Dataset not found"), {"display": "none"}
