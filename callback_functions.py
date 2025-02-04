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

# Function to get unique brands and countries from the dataset
def get_brands_and_country(input_str):
    # Extract country from the input
    input_parts = input_str.lower().split()
    
    # List of possible country names to match from the input
    countries = ['malaysia', 'singapore', 'thailand', 'indonesia']

    # Find the country from the input
    country = None
    for word in input_parts:
        if word in countries:
            country = word.capitalize()
            break
    
    # If no country is found, raise an error and it will cause update_content(input_filter) to show a popup
    if not country:
        raise ValueError
    
    # Now, load the dataset based on the extracted country
    df = pd.read_csv(f'./Dataset/{country}_Laptop.csv', index_col=0)

    # Get one instance of each unique brand
    brands = df['Brand'].unique().tolist()
    
    return brands, country

def update_top5(input_str):
    input_parts = input_str.lower().split()

    # Get the unique brands and country from the input string
    brands, country = get_brands_and_country(input_str)
    
    brand_filter = None
    price_min = 0
    price_max = float('inf')

    # Extract the brand from the input if mentioned
    for word in input_parts:
        if word in [brand.lower() for brand in brands]:
            brand_filter = word.capitalize()

    # Extract price range if available
    if "price range" in input_str.lower():
        # Get the string input that comes after "price range" and remove any extra spaces
        price_parts = input_str.lower().split("price range")[1].strip()
        # Split the extracted string into two variables and change their data type to int
        price_min, price_max = map(int, price_parts.split(","))

    # Read the dataset for the specific country and product category
    df = pd.read_csv(f'./Dataset/{country}_Laptop.csv', index_col=0)
    
    # Filter laptops based on the extracted data
    filtered_laptops = []
    for _, laptop in df.iterrows():
        if brand_filter and laptop["Brand"].lower() != brand_filter.lower():
            continue
        if laptop["Price"] < price_min or laptop["Price"] > price_max:
            continue
        filtered_laptops.append(laptop)

    # Sort laptops by rating and if the rating is the same its sorted by number of sales.
    filtered_laptops = sorted(filtered_laptops, key=lambda x: (x["Rating"], x["Number of Sales"]), reverse=True)

    # Convert the top 5 filtered laptops to dictionary format
    new_data = [laptop.to_dict() for laptop in filtered_laptops[:5]]

    return new_data
