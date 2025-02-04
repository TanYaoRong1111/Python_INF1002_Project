import pandas as pd

EXCHANGE_RATES = {
    "PHP": 0.024,    
    "USD": 1.35,     
    "MYR": 0.29,     
    "IDR": 0.000089,
    "THB": 0.040
}


def convert_price_to_sgd(price_column, currency):
    if currency not in EXCHANGE_RATES:
        raise ValueError(f"Error: Exchange rate for '{currency}' not found.")

    exchange_rate = EXCHANGE_RATES[currency]
    converted_prices = pd.to_numeric(price_column, errors="coerce") * exchange_rate

    return converted_prices.round(2)  


def convert_csv_prices_to_sgd(input_csv: str, currency: str, price_column="Price"):
    try:
        # Read the input CSV file
        df = pd.read_csv(input_csv)

        # Check if the specified price column exists in the CSV
        if price_column not in df.columns:
            raise ValueError(f"Error: Column '{price_column}' not found in CSV.")

        # Convert prices to SGD and overwrite the 'Price' column
        df[price_column] = convert_price_to_sgd(df[price_column], currency)

        # Save the updated DataFrame back to the same input CSV file (overwrite)
        df.to_csv(input_csv, index=False)
        print(f"✅ Conversion complete! File overwritten with new 'Price' values in SGD.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Get user input for file path and currency
    input_csv = input('Enter the full path of the input CSV file: ').strip().replace('"', '').replace("\\", "/")
    currency = input('Enter the currency of the price column (e.g., PHP, USD, MYR, IDR, THB): ').strip().upper()

    # Perform the conversion and overwrite the file
    convert_csv_prices_to_sgd(input_csv, currency)
