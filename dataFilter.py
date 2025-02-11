import re
import pandas as pd
import numpy as np
from webScraping import *  # Assuming this function exists in `webScraping`

def data_to_dataframe(res):
    """
    Convert JSON data to a DataFrame and ensure numeric columns are properly formatted.
    """
    df = pd.json_normalize(res)  # Normalize JSON data into a DataFrame
    numeric_columns = ["ratingScore", "price", "review"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")  # Convert to numeric, coercing errors to NaN
    df["ratingScore"] = df["ratingScore"].round(2)  # Round ratingScore to 2 decimal places
    return df

def convert_sold_to_number(sold_value):
    """
    Convert 'sold' values like '5 sold', '5K sold', or 'Terjual 5' to numeric values.
    """
    if pd.isna(sold_value) or sold_value == "":
        return np.nan  # Handle missing or invalid values
    
    sold_value = str(sold_value).replace("K", "").replace(" sold", "").replace(" Terjual", "")
    try:
        value = float(sold_value)
        return value * 1000 if "K" in str(sold_value) else value
    except ValueError:
        return np.nan  # Return NaN if conversion fails

def clean_title(title):
    """
    Clean product titles by removing patterns like 【.*?】 or [.*?].
    """
    if not isinstance(title, str):  # Ensure title is a string
        return title
    # Remove patterns like 【.*?】, [.*?], or any leading/trailing whitespace
    return re.sub(r"(【.*?】|\[.*?\])", "", title).strip()

def data_frame_filtering(df):
    """
    Filter and clean the DataFrame by removing unwanted rows and cleaning column values.
    """
    # Clean product names
    df["name"] = df["name"].apply(clean_title)
    
    # Remove rows with specific brand names
    exclude_brands = ["No Brand", "NoBrand", "No Brad"]
    df = df[~df["brandName"].str.contains("|".join(exclude_brands), case=False, na=False)]
    
    # Reset index after filtering
    df.reset_index(drop=True, inplace=True)
    return df

def data_processing(df):
    """
    Process the DataFrame to include only relevant columns, rename them, and clean their values.
    """
    # Select and rename relevant columns
    filtered_df = df.rename(
        columns={
            "name": "Name",
            "price": "Price",
            "brandName": "Brand",
            "ratingScore": "Rating",
            "sellerName": "Seller Name",
            "itemSoldCntShow": "Number of Sales",
            "review": "Number of Reviews"
        }
    )[["Name", "Price", "Brand", "Rating", "Seller Name", "Number of Sales", "Number of Reviews"]]
    
    # Convert 'Number of Sales' to numeric
    filtered_df["Number of Sales"] = filtered_df["Number of Sales"].apply(convert_sold_to_number)
    
    # Replace empty strings or "NaN" with NaN and drop rows with missing values
    filtered_df.replace(["", "NaN"], pd.NA, inplace=True)
    filtered_df.dropna(inplace=True)
    
    # Round 'Number of Sales' to 0 decimal places
    filtered_df["Number of Sales"] = filtered_df["Number of Sales"].round(0)
    return filtered_df

def validate_country(input_country):
    """
    Validate the country input.
    """
    valid_countries = ["Malaysia", "Singapore", "Thailand", "Indonesia"]
    if input_country not in valid_countries:
        raise ValueError(f"Invalid country: {input_country}. Valid options are: {', '.join(valid_countries)}.")
    return input_country

def validate_item(input_item):
    """
    Validate the item input.
    """
    if not input_item.strip():
        raise ValueError("Item name cannot be empty.")
    return input_item.strip()

def validate_pages(input_pages):
    """
    Validate the number of pages input.
    """
    try:
        pages = int(input_pages)
        if pages <= 0:
            raise ValueError("Number of pages must be a positive integer.")
        return pages
    except ValueError:
        raise ValueError("Invalid input for number of pages. Please enter a positive integer.")

def scrape_data(country, item, pages):
    """
    Scrape data based on the selected country.
    """
    scraping_functions = {
        "Malaysia": webScrapingLazadaMalaysia,
        "Singapore": webScrapingLazadaSingapore,
        "Thailand": webScrapingLazadaThailand,
        "Indonesia": webScrapingLazadaIndonesia,
        "Philippines": webScrapingLazadaPhilippines,
    }
    if country not in scraping_functions:
        raise ValueError(f"No scraping function available for country: {country}")
    
    # Call the appropriate scraping function
    return scraping_functions[country](item, page=pages)

def create_csv():
    """
    Scrape data from Lazada, process it, and save it as a CSV file.
    """
    try:
        # Input validation
        input_country = validate_country(
            input("Enter Country to Web Scrape: [Malaysia, Singapore, Thailand, Indonesia]: ").strip()
        )
        input_item = validate_item(
            input("Enter item to scrape from Lazada: ").strip()
        )
        input_pages = validate_pages(
            input("Enter number of pages to scrape: ").strip()
        )

        # Scrape data
        res = scrape_data(input_country, input_item, input_pages)

        # Process data
        df = data_to_dataframe(res)
        df = data_frame_filtering(df)
        df = data_processing(df)

        # Save to CSV
        output_file = f"{input_country}_{input_item.replace(' ', '_')}.csv"
        df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")