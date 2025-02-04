import dash
from dash import dcc, html, register_page, Input, Output
import dash_bootstrap_components as dbc
from dash import callback, Input, Output
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate



# Register the page
register_page(__name__, name="Revenue Pie Chart", path='/revenue-pie-chart')

# Dropdown options
options = ['Laptop', 'Phones', 'Mouse', 'Keyboard', 'Monitor']
options2 = ['Malaysia', 'Singapore', 'Thailand', 'Indonesia']

# Layout for the revenue pie chart page
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Revenue Distribution by Brand", style={'textAlign': 'center'}),
                className="mb-4"
            )
        ),
        
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='product_name',
                    options=[{'label': opt, 'value': opt} for opt in options],
                    placeholder="Select Product Category",
                    className="mb-4"
                ),
                width=6
            )
        ),
        
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='country_name',
                    options=[{'label': opt, 'value': opt} for opt in options2],
                    placeholder="Select Country",
                    className="mb-4"
                ),
                width=6
            )
        ),
        
        dbc.Row(
            dbc.Col(
                dcc.Graph(id="revenue-pie-chart"),  # Pie chart component
                className="mb-4"
            )
        ),
    ],
    fluid=True,
    style={'padding': '20px'}
)


@callback(
    Output('revenue-pie-chart', 'figure'),
    [Input('product_name', 'value'),
     Input('country_name', 'value')]
)
def update_revenue_pie_chart(product_name, country_name):
    if product_name is None or country_name is None:
        # Return an empty figure with a black background
        empty_fig = px.pie()
        empty_fig.update_layout(
            paper_bgcolor="black",
            plot_bgcolor="black",
            height=500,
            width=500
        )
        return empty_fig
    
    try:
        # Load the dataset
        df = pd.read_csv(f'./Dataset/{country_name}_{product_name}.csv', index_col=0)
        
        # Calculate revenue (Price * Number of Sales)
        df['Revenue'] = df['Price'] * df['Number of Sales']
        
        # Aggregate revenue by brand and select the top 5 brands
        aggregated_data = df.groupby("Brand", as_index=False).agg({"Revenue": "sum"})
        aggregated_data = aggregated_data.sort_values(by="Revenue", ascending=False).head(5)
        
        # Create the pie chart
        pie_fig = px.pie(
            aggregated_data,
            names="Brand",
            values="Revenue",
            title=f"Top 5 Revenue Brands in {country_name} for {product_name}",
            hole=0  # 0 = full pie, increase for a donut chart
        )
        
        # Update layout for black background and better readability
        pie_fig.update_layout(
            title_font=dict(size=24, color='white'),
            height=700,  # Increase height for better visibility
            width=700,   # Increase width
            paper_bgcolor="black",
            plot_bgcolor="black",
            font=dict(color="white"),
            legend_font=dict(size=16),  # Make legend text bigger
        )
        
        return pie_fig
    
    except FileNotFoundError:
        # Return an empty figure with black background if file not found
        empty_fig = px.pie()
        empty_fig.update_layout(
            paper_bgcolor="black",
            plot_bgcolor="black",
            height=500,
            width=500
        )
        return empty_fig