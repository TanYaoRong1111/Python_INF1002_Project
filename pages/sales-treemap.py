import dash
from dash import dcc, html, register_page, Input, Output
import dash_bootstrap_components as dbc
from dash import callback, Input, Output
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
from callback_functions import update_revenue_pie_chart
import os

register_page(__name__, name="Total Sales Treemap", path='/sales-treemap')

category_options = ['Laptop', 'Phones']
country_options = ['Malaysia', 'Singapore', 'Thailand', 'Philippines']

flag_colors = {
    'Malaysia': 'rgb(0, 40, 104)',
    'Singapore': 'rgb(255, 0, 0)',     
    'Thailand': 'rgb(0, 32, 91)',      
    'Indonesia': 'rgb(217, 0, 0)',      
    'Philippines': 'rgb(0, 56, 168)'   
    }

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Total Sales Treemap", 
                        style={'textAlign': 'center', 'color': 'white'}),
                className="mb-4"
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='category_name',
                    options=[{'label': category, 'value': category} for category in category_options],
                    placeholder="Select Product Category",
                    className="mb-4",
                    style={'backgroundColor': 'white', 'color': 'black'}
                ),
                width=6
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id="treemap-chart-phones"),  
                id="treemap_col_phones",
                className="mb-4",
                style={"display": "none"},
            )
        ),
    ],
    fluid=True,
)

def load_data(country, category):
    """Loads data from CSV files based on country and category."""
    filename = f"Dataset/{country}_{category}.csv"
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return pd.DataFrame(columns=['Brand', 'Number of Sales'])

@dash.callback(
    [Output('treemap-chart-phones', 'figure'),
     Output('treemap_col_phones', 'style')],
    [Input('category_name', 'value')]
)
def update_treemap(selected_category):
    if not selected_category:
        raise PreventUpdate
    
    sales_data = []
    country_totals = {}
    for country in country_options:
        df = load_data(country, selected_category)
        if not df.empty:
            country_sales = df.groupby('Brand', as_index=False)['Number of Sales'].sum()
            country_sales['Country'] = country
            sales_data.append(country_sales)
            country_totals[country] = df['Number of Sales'].sum()
    
    if not sales_data:
        return px.treemap(title="No data available"), {"display": "none"}
    
    sales_df = pd.concat(sales_data, ignore_index=True)
    
    sales_df = sales_df[sales_df['Country'].isin(flag_colors.keys())]
    
    if sales_df.empty:
        return px.treemap(title="No data available"), {"display": "none"}
    
    sales_df['Total Sales'] = sales_df['Country'].map(country_totals)
    
    treemap_fig = px.treemap(
        sales_df,
        path=['Country', 'Brand'],
        values='Number of Sales',
        title=f'Total Sales by Brand for {selected_category}',
        template='plotly_dark',
        color='Country',
        color_discrete_map=flag_colors,
        custom_data=['Brand', 'Number of Sales', 'Country', 'Total Sales']
    )
    
    treemap_fig.update_traces(
        hovertemplate=
        "<b>%{customdata[2]}</b>: %{customdata[0]} - %{customdata[1]} sales"
    )
    
    return treemap_fig, {"display": "block"}
