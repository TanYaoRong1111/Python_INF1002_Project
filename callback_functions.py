import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
from dataFilter import data_processing

def generate_total_sales_treemap(value):
    """Generate a treemap showing the total sales by summing the 'Price' column for each country."""
    countries = ['Malaysia', 'Singapore', 'Thailand', 'Indonesia']
    total_sales = []

    
    for country in countries:
        df = pd.read_csv(f'./Dataset/{country}_{value}.csv', index_col=0)
        
        
        total_sales.append(round(df['Price'].sum(), 2))

    
    sales_df = pd.DataFrame({
        'Country': countries,
        'Total Sales': total_sales
    })

    
    sales_df['HoverText'] = sales_df.apply(lambda row: f"{row['Country']} = ${row['Total Sales']:.2f}", axis=1)

    
    flag_colors = {
        'Malaysia': 'rgb(0, 0, 139)',       
        'Singapore': 'rgb(255, 0, 0)',       
        'Thailand': 'rgb(30, 144, 255)',     
        'Indonesia': 'rgb(220, 20, 60)'      
    }

    
    treemap_fig = px.treemap(
        sales_df, 
        path=['Country'], 
        values='Total Sales',
        title=f'Total Sales by Country for {value}', 
        color='Country',  
        color_discrete_map=flag_colors,  
        template='plotly_white',
        custom_data=['HoverText']  
    )

    
    treemap_fig.update_traces(
        hovertemplate='%{customdata[0]}'  
    )

    
    treemap_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white")
    )

    return treemap_fig




def update_bar_chart(value, country):
    if value is None:
        raise PreventUpdate

    
    value, country = str(value), str(country)

    df = pd.read_csv(f'./Dataset/{country}_{value}.csv', index_col=0)

    
    sorted_df = (
        df.groupby("Brand", as_index=False)
        .agg({"Number of Sales": "sum"})  
        .sort_values("Number of Sales", ascending=False).head(5)  
    )
    figure = px.histogram(sorted_df, x="Brand", y="Number of Sales", histfunc="sum", color='Brand',template='plotly_white', title='Top 5 Brands by Sales')

    figure.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white")
    )
    
    
    return figure, {"display": "block"}

def update_pie_chart(value, country):
    
    value, country = str(value), str(country)

    df = pd.read_csv(f'./Dataset/{country}_{value}.csv', index_col=0)

    
    sorted_df = (
        df.groupby("Brand", as_index=False)
        .agg({"Number of Sales": "sum"})  
        .sort_values("Number of Sales", ascending=False).head(5)  
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
    
    new_data = df.to_dict("records")

    
    sorted_df = (
        df.groupby("Brand", as_index=False)
        .agg({"Number of Sales": "sum"})  
        .sort_values("Number of Sales", ascending=False).head(5)  
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
            .agg({"Number of Sales": "sum"})  
            .sort_values("Number of Sales", ascending=False).head(5)  
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


