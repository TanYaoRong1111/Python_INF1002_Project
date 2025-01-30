import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
from dataFilter import data_processing

def update_bar_chart(value, country):
    if value is None:
        raise PreventUpdate

    #Convert inputs into strings
    value, country = str(value), str(country)

    df = pd.read_csv(f'./Dataset/{country}_{value}.csv', index_col=0)

    # Create a histogram figure
    sorted_df = (
        df.groupby("Brand", as_index=False)
        .agg({"Number of Sales": "sum"})  # Calculate the sum of sales per brand
        .sort_values("Number of Sales", ascending=False).head(5)  # Sort by average sales in descending order
    )
    figure = px.histogram(sorted_df, x="Brand", y="Number of Sales", histfunc="sum", color='Brand',template='plotly_white', title='Top 5 Brands by Sales')

    figure.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white")
    )
    
    
    return figure, {"display": "block"}

def update_pie_chart(value, country):
    #Convert inputs into strings
    value, country = str(value), str(country)

    df = pd.read_csv(f'./Dataset/{country}_{value}.csv', index_col=0)

    # Create a histogram figure
    sorted_df = (
        df.groupby("Brand", as_index=False)
        .agg({"Number of Sales": "sum"})  # Calculate the sum of sales per brand
        .sort_values("Number of Sales", ascending=False).head(5)  # Sort by average sales in descending order
    )


    pie_fig = px.pie(sorted_df, values="Number of Sales", names="Brand", hole=.3, title=f'{country} Top 5 Brands by Sales')
    

    pie_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white")
    )

    return pie_fig, {"display": "block"}

def update_table(value, country):
    if value is None:
        raise PreventUpdate
    
    value, country = str(value), str(country)

    df = pd.read_csv(f'./Dataset/{country}_{value}.csv', index_col=0)
    # Update DataTable
    new_data = df.to_dict("records")

    # Create a histogram figure
    sorted_df = (
        df.groupby("Brand", as_index=False)
        .agg({"Number of Sales": "sum"})  # Calculate the sum of sales per brand
        .sort_values("Number of Sales", ascending=False).head(5)  # Sort by average sales in descending order
    )
    figure = px.histogram(sorted_df, x="Brand", y="Number of Sales", histfunc="sum", color='Brand',template='plotly_white', title='Top 5 Brands by Sales')

    figure.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )
    
    
    return new_data

def generate_all_bar_chart():

    figs = []
    countries = ['Malaysia', 'Singapore', 'Thailand','Indonesia']

    for country in countries:

        df = pd.read_csv(f'./Dataset/{country}_Laptop.csv', index_col=0)

        sorted_df = (
            df.groupby("Brand", as_index=False)
            .agg({"Number of Sales": "sum"})  # Calculate the sum of sales per brand
            .sort_values("Number of Sales", ascending=False).head(5)  # Sort by average sales in descending order
        )

        figure = px.histogram(sorted_df, x="Brand", y="Number of Sales", histfunc="sum", color='Brand',template='plotly_white', title=f'{country} Top 5 Laptop by Sales')

        figure.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white")
        )

        pie_fig = px.pie(sorted_df, values="Number of Sales", names="Brand", hole=.3, title=f'{country} Top 5 Brands by Sales')

        pie_fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white")
        )

        figs.append(figure)
        figs.append(pie_fig)

    return figs


