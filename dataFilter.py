import pandas as pd
from webScraping import *
import numpy as np


def data_to_dataframe(res):
    # Change the data to JSON format
    df = pd.json_normalize(res)

    # Change Integers/Floats to numeric
    df = convert_to_numeric(df)

    return df


# Convert Numeric Columns to Numeric
def convert_to_numeric(df):
    # Ensure 'rating' is numeric
    df["ratingScore"] = pd.to_numeric(df["ratingScore"], errors="coerce")

    # Ensure 'Price' is numeric
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Ensure 'review' is numeric
    df['review'] = pd.to_numeric(df['review'], errors="coerce")

    # Round to 2 decimal places for raiting
    df["ratingScore"] = df["ratingScore"].round(2)

    return df


def convert_sold_to_number(sold_value):
    # Handle NaN or empty values
    if pd.isna(sold_value) or sold_value == "":
        return np.nan  # Return NaN for invalid or missing values

    # Converting 5 sold or 5,4k sold to 5 and 5400 respectively
    if "Terjual" in str(sold_value):
        if "K" in str(sold_value):
            return float(sold_value.replace("K", "").replace(" Terjual", "")) * 1000
        return int(str(sold_value).replace(" Terjual", ""))
    else:
        if "K" in str(sold_value):
            return float(sold_value.replace("K", "").replace(" sold", "")) * 1000
        return int(str(sold_value).replace(" sold", ""))


def data_frame_filtering(df):
    # Remove Title Heads with 【.*?】
    df["name"] = df["name"].str.replace(r"【.*?】", "", regex=True).str.strip()
    # Remove Title Heads with [.*?]
    df["name"] = df["name"].str.replace(r"[.*?]", "", regex=True).str.strip()

    df["name"] = df["name"].str.replace(r"^(?:\[.*?\]\s*)?", "", regex=True).str.strip()

    # Remove DataSet Column Brand if it has "No brand inside"
    df = df[~df["brandName"].str.contains("No Brand", case=False, na=False)]
    df = df[~df["brandName"].str.contains("NoBrand", case=True, na=False)]
    df = df[~df["brandName"].str.contains("No Brad", case=True, na=False)]
    # Reset the index (optional)
    df.reset_index(drop=True, inplace=True)

    return df


def data_processing(df):
    # Filter the dataframe to get required fields
    filtered_df = df[['name', 'price', 'brandName',
                      'ratingScore', 'sellerName', 'itemSoldCntShow', 'review']]

    # Rename columns for better readability
    filtered_df = filtered_df.rename(columns={
        'name': 'Name',
        'price': 'Price',
        'brandName': 'Brand',
        'ratingScore': 'Rating',
        'sellerName': 'Seller Name',
        'itemSoldCntShow': 'Number of Sales',
        'review': 'Number of Reviews'
    })

    filtered_df["Number of Sales"] = filtered_df["Number of Sales"].apply(
        convert_sold_to_number)

    filtered_df.replace(["NaN", ""], pd.NA, inplace=True)
    filtered_df = filtered_df.dropna()

    # Round to 0 decimal places for rating
    filtered_df["Number of Sales"] = filtered_df["Number of Sales"].round(0)

    return filtered_df


def create_csv():
    input_country = input("Enter Country to Web Scrape: [Malaysia, Singapore, Thailand, Indonesia]")
    input_item = input("Enter item to scrape from lazada: ")
    input_pages = int(input("Enter number of pages to scrape: "))


    res = webScrapingLazadaPhilippines(str(input_item), page=input_pages)


    df = data_to_dataframe(res)

    df = data_frame_filtering(df)

    df = data_processing(df)

    df.to_csv(f"{input_country}_Laptop.csv")