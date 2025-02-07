import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from dataFilter import data_processing

def generate_total_sales_treemap(value):
    """Generate a treemap showing the total sales by summing the 'Price' column for each country."""
    countries = ['Malaysia', 'Singapore', 'Thailand', 'Indonesia', 'Philippines']
    total_sales = []

    
    for country in countries:
        df = pd.read_csv(f'./Dataset/{country}_{value}.csv', index_col=0)
        revenue = 0
        # Loop through each row
        for index, row in df.iterrows():
            revenue += int(row['Price']) * int(row['Number of Sales'])
        
        total_sales.append(round(revenue, 2))
    
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
    # Update DataTable
    new_data = df.to_dict("records")  
    
    return new_data

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
    countries = ['malaysia', 'singapore', 'thailand', 'indonesia', 'philippines']

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
    price_max = 0

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

    # If price_max is 0, set it to infinity (no upper limit)
    if price_max == 0:
        price_max = float('inf')

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


import pandas as pd
import plotly.graph_objects as go

def create_boxplot_layout(item_name):
    """
    Creates a grouped boxplot layout for laptop prices across multiple countries,
    including only prices where "Number of sales" is more than 100.
    
    Returns:
        go.Figure: A Plotly figure containing the boxplots.
    """
    # Define dataset paths
    countries = ["Indonesia", "Malaysia", "Singapore", "Thailand", "Philippines"]
    file_paths = [f"./Dataset/{country}_{item_name}.csv" for country in countries]
    
    # Load data and create boxplots
    boxplots = []
    for country, path in zip(countries, file_paths):
        # Load the data for the current country
        data = pd.read_csv(path)
        
        # Filter the data to include only rows where "Number of sales" > 200
        filtered_data = data[data['Number of Sales'] > 200]
        
        # Create a boxplot using the filtered 'Price' values
        if not filtered_data.empty:  # Ensure there's data left after filtering
            boxplots.append(go.Box(y=filtered_data['Price'], name=f"{country} {item_name}"))
        else:
            print(f"No data available for {country} after filtering.")
    
    # Create figure with boxplots
    figure = go.Figure(data=boxplots)
    figure.update_layout(
        title=f'Boxplots for Prices of {item_name} (Filtered by Sales > 200)',
        xaxis=dict(title='Countries', color='white', gridcolor='rgba(255, 255, 255, 0.2)'),
        yaxis=dict(title='Price Values', color='white', gridcolor='rgba(255, 255, 255, 0.2)'),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
        font=dict(color='white'),  # White text color
        boxmode='group'  # Grouped boxplots
    )
    
    return figure

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
        
        return pie_fig, {"display": "block"}
    
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

def update_map(product_name):
    if product_name is None:
        raise PreventUpdate
    
    # Example: Update revenue data based on the selected product category
    # You can replace this with your actual logic to fetch revenue data


    countries = ['Malaysia', 'Singapore', 'Thailand', 'Indonesia', 'Philippines']
    total_sales = []

    
    for country in countries:
        df = pd.read_csv(f'./Dataset/{country}_{product_name}.csv', index_col=0)
        revenue = 0
        # Loop through each row
        for index, row in df.iterrows():
            revenue += int(row['Price']) * int(row['Number of Sales'])
        
        total_sales.append(round(revenue, 2))

    
    sales = {
        "countries": countries,
        'Total Sales': total_sales
    }

    
    updated_revenue = [x for x in sales["Total Sales"]]
    
    # Create the choropleth map
    fig = go.Figure(go.Choropleth(
        locations=sales["countries"],          # Country names
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