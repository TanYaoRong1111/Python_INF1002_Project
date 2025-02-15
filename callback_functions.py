import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from dataFilter import data_processing

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import re

# Helper Functions
def load_data(country, product_name):
    """Load dataset for a specific country and product."""
    file_path = f'./Dataset/{country}_{product_name}.csv'
    return pd.read_csv(file_path, index_col=0)

def calculate_revenue(df):
    """Calculate revenue by multiplying 'Price' and 'Number of Sales'."""
    df['Revenue'] = df['Price'] * df['Number of Sales']
    return df

def create_sorted_df(df, group_by_col, agg_col, sort_col, ascending=False, head=5):
    """Group data, aggregate, and sort."""
    sorted_df = (
        df.groupby(group_by_col, as_index=False)
        .agg({agg_col: "sum"})
        .sort_values(sort_col, ascending=ascending)
        .head(head)
    )
    return sorted_df

def create_bar_chart(sorted_df, x_col, y_col, title, color_col):
    """Create a bar chart."""
    figure = px.histogram(
        sorted_df,
        x=x_col,
        y=y_col,
        histfunc="sum",
        color=color_col,
        template='plotly_white',
        title=title
    )
    figure.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white")
    )
    return figure

def create_pie_chart(sorted_df, values_col, names_col, title):
    """Create a pie chart."""
    pie_fig = px.pie(
        sorted_df,
        values=values_col,
        names=names_col,
        hole=0.3,
        title=title
    )
    pie_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white")
    )
    return pie_fig

def create_empty_figure():
    """Return an empty Plotly figure with a black background."""
    empty_fig = px.pie()
    empty_fig.update_layout(
        paper_bgcolor="black",
        plot_bgcolor="black",
        height=500,
        width=500
    )
    return empty_fig

# Main Functions
def generate_total_sales_treemap(value):
    """Generate a treemap showing total sales by summing 'Price' column for each country."""
    countries = ['Malaysia', 'Singapore', 'Thailand', 'Indonesia', 'Philippines']
    total_sales = []

    for country in countries:
        df = load_data(country, value)
        revenue = (df['Price'] * df['Number of Sales']).sum()
        total_sales.append(round(revenue, 2))

    sales_df = pd.DataFrame({
        'Country': countries,
        'Total Sales': total_sales
    })
    sales_df['HoverText'] = sales_df.apply(lambda row: f"{row['Country']} = ${row['Total Sales']:.2f}", axis=1)

    flag_colors = {
    'Malaysia': 'rgb(0, 40, 104)',
    'Singapore': 'rgb(255, 0, 0)',     
    'Thailand': 'rgb(0, 32, 91)',      
    'Indonesia': 'rgb(217, 0, 0)',      
    'Philippines': 'rgb(0, 56, 168)'   
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
    treemap_fig.update_traces(hovertemplate='%{customdata[0]}')
    treemap_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white")
    )
    return treemap_fig

def update_bar_chart(value, country):
    if value is None:
        raise PreventUpdate

    df = load_data(country, value)
    sorted_df = create_sorted_df(df, "Brand", "Number of Sales", "Number of Sales", ascending=False, head=5)
    title = 'Top 5 Brands by Sales'
    figure = create_bar_chart(sorted_df, "Brand", "Number of Sales", title, "Brand")
    return figure, {"display": "block"}

def update_pie_chart(value, country):
    df = load_data(country, value)
    sorted_df = create_sorted_df(df, "Brand", "Number of Sales", "Number of Sales", ascending=False, head=5)
    title = f'{country} Top 5 Brands by Sales'
    pie_fig = create_pie_chart(sorted_df, "Number of Sales", "Brand", title)
    return pie_fig, {"display": "block"}

def update_table(value, country):
    if value is None:
        raise PreventUpdate

    df = load_data(country, value)
    new_data = df.to_dict("records")
    return new_data

def generate_all_bar_chart():
    figs = []
    countries = ['Malaysia', 'Singapore', 'Thailand', 'Indonesia']

    for country in countries:
        df = load_data(country, "Laptop")
        sorted_df = create_sorted_df(df, "Brand", "Number of Sales", "Number of Sales", ascending=False, head=5)

        # Bar Chart
        bar_title = f'{country} Top 5 Laptop by Sales'
        bar_fig = create_bar_chart(sorted_df, "Brand", "Number of Sales", bar_title, "Brand")
        figs.append(bar_fig)

        # Pie Chart
        pie_title = f'{country} Top 5 Brands by Sales'
        pie_fig = create_pie_chart(sorted_df, "Number of Sales", "Brand", pie_title)
        figs.append(pie_fig)

    return figs

def update_revenue_pie_chart(product_name, country_name):
    if product_name is None or country_name is None:
        return create_empty_figure()

    try:
        df = load_data(country_name, product_name)
        df = calculate_revenue(df)
        aggregated_data = create_sorted_df(df, "Brand", "Revenue", "Revenue", ascending=False, head=5)

        pie_fig = create_pie_chart(aggregated_data, "Revenue", "Brand", f"Top 5 Revenue Brands in {country_name} for {product_name}")
        pie_fig.update_layout(
            title_font=dict(size=24, color='white'),
            height=700,
            width=700,
            legend_font=dict(size=16)
        )
        return pie_fig, {"display": "block"}
    except FileNotFoundError:
        return create_empty_figure()

def update_map(product_name):
    if product_name is None:
        raise PreventUpdate

    countries = ['Malaysia', 'Singapore', 'Thailand', 'Indonesia', 'Philippines']
    total_sales = []

    for country in countries:
        df = load_data(country, product_name)
        revenue = (df['Price'] * df['Number of Sales']).sum()
        total_sales.append(round(revenue, 2))

    sales = {
        "countries": countries,
        "Total Sales": total_sales
    }

    fig = go.Figure(go.Choropleth(
        locations=sales["countries"],
        z=sales["Total Sales"],
        locationmode="country names",
        colorscale="Viridis",
        colorbar_title="Revenue (in millions)"
    ))
    fig.update_geos(
        visible=False,
        resolution=50,
        scope="asia",
        showcountries=True,
        countrycolor="Black",
        showsubunits=True,
        subunitcolor="Blue",
        center=dict(lon=105, lat=15),
        projection_scale=3
    )
    fig.update_layout(
        title=f"Revenue in Southeast Asia for {product_name}",
        height=500,
        margin={"r": 0, "t": 30, "l": 0, "b": 0}
    )
    return fig, {"display": "block"}

def create_boxplot_layout(item_name):
    """
    Creates a grouped boxplot layout for laptop prices across multiple countries,
    including only prices where "Number of sales" is more than 200.
    
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

def update_top5(input_str):
    input_parts = input_str.lower().split()

    # Get the unique brands and country from the input string
    brands, country, product = get_brands_country_product(input_str)
    
    brand_filter = None
    price_min = 0
    price_max = 0

    # Extract the brand from the input if mentioned
    for word in input_parts:
        if word.lower() in [brand.lower() for brand in brands]:
            brand_filter = word

    # Extract price range if available
    # Get the string input that comes after "price range" and remove any extra spaces
    # \s* --> one or more spaces            \d+ --> one or more digits
    price_range_match = re.search(r"price range\s*(\d+)\s*,\s*(\d+)", input_str.lower())
    if price_range_match:
        # Split the extracted string into two variables and change their data type to int
        price_min, price_max = map(int, price_range_match.groups())

    # If price_max is 0, set it to infinity (no upper limit)
    if price_max == 0:
        price_max = float('inf')

    # Read the dataset for the specific country and product category
    df = pd.read_csv(f'./Dataset/{country}_{product}.csv', index_col=0)
    
    # Filter laptops based on the extracted data
    filtered_product = []
    for _, product in df.iterrows():
        if brand_filter and product["Brand"].lower() != brand_filter.lower():
            continue
        if product["Price"] < price_min or product["Price"] > price_max:
            continue
        filtered_product.append(product)

    # Sort laptops by rating and if the rating is the same its sorted by number of sales.
    filtered_product = sorted(filtered_product, key=lambda x: (x["Rating"], x["Number of Sales"]), reverse=True)

    # Convert the top 5 filtered laptops to dictionary format
    new_data = [product.to_dict() for product in filtered_product[:5]]

    return new_data

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

# Function to get unique brands and countries from the dataset
def get_brands_country_product(input_str):
    # Extract country from the input
    input_parts = input_str.lower().split()
    
    # List of possible country names to match from the input
    countries = ['malaysia', 'singapore', 'thailand', 'indonesia', 'philippines']
    products = ['laptop', 'phones']

    # Find the country and product from the input
    country = None
    product = None
    for word in input_parts:
        if word in countries:
            country = word.capitalize()
        if word in products:
            product = word.capitalize()
        if country and product:  
            break
    
    # If no country and/or product is found, raise an error and it will cause update_content(input_filter) to show a popup
    if not country or not product:
        raise ValueError
    
    # Now, load the dataset based on the extracted country
    df = pd.read_csv(f'./Dataset/{country}_{product}.csv', index_col=0)

    # Get one instance of each unique brand
    brands = df['Brand'].unique().tolist()
    
    return brands, country, product


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

