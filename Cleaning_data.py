import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
from pathlib import Path

# Define the base directory as the directory of this script
BASE_DIR = Path(__file__).parent

def clean_volume(x):
    """
    Parses 'K' and 'M' suffixes in volume strings.
    Example: '0.36K' -> 360.0
    """
    if pd.isna(x) or x == '-':
        return np.nan
    if isinstance(x, str):
        if 'K' in x:
            return float(x.replace('K', '')) * 1000
        if 'M' in x:
            return float(x.replace('M', '')) * 1000000
        return float(x)
    return x

# ---------------------------------------------------------
# 1. Load and Process Existing Files
# ---------------------------------------------------------
print("Loading existing files...")

# Load File 1: Gold Futures Historical Data
df_futures = pd.read_csv('Gold-Price-predictor\Gold Futures Historical Data.csv')
df_futures.rename(columns={'Vol.': 'Volume'}, inplace=True)
df_futures['Date'] = pd.to_datetime(df_futures['Date'], format='%d-%m-%Y')
for col in ['Price', 'Open', 'High', 'Low']:
    df_futures[col] = df_futures[col].astype(str).str.replace(',', '').astype(float)
df_futures['Volume'] = df_futures['Volume'].apply(clean_volume)
if 'Change %' in df_futures.columns:
    df_futures.drop(columns=['Change %'], inplace=True)

# Load File 2: gold_data
df_gold = pd.read_csv('Gold-Price-predictor\gold_data.csv')
df_gold['Date'] = pd.to_datetime(df_gold['Date'], format='%d/%m/%Y')
# Adjust scale: This file's volume is in thousands
df_gold['Volume'] = df_gold['Volume'] * 1000

# Combine existing data
df_combined = pd.concat([df_futures, df_gold])
df_combined.drop_duplicates(subset=['Date'], keep='first', inplace=True)
df_combined.sort_values(by='Date', inplace=True)

# ---------------------------------------------------------
# 2. Fetch New Data (2022 - 2025) using yfinance
# ---------------------------------------------------------
last_date = df_combined['Date'].max()
print(f"Data currently ends on: {last_date.date()}")

# Define the ticker for Gold Futures
ticker = "GC=F"

# Set start date to the day after the last date in your file
start_date = last_date + pd.Timedelta(days=1)
end_date = datetime.now().strftime('%Y-%m-%d') # Up to today

print(f"Downloading new data from {start_date.date()} to {end_date}...")

# Download data
df_new = yf.download(ticker, start=start_date, end=end_date, progress=False)

if not df_new.empty:
    # Reset index to make Date a column
    df_new.reset_index(inplace=True)
    
    # Ensure Date is timezone-naive to match existing data
    df_new['Date'] = df_new['Date'].dt.tz_localize(None)

    # yfinance columns: Date, Open, High, Low, Close, Adj Close, Volume
    # We map 'Close' to 'Price'
    df_new.rename(columns={'Close': 'Price'}, inplace=True)
    
    # Select only the columns we need
    df_new = df_new[['Date', 'Price', 'Open', 'High', 'Low', 'Volume']]
    
    # ---------------------------------------------------------
    # 3. Merge and Save
    # ---------------------------------------------------------
    df_final = pd.concat([df_combined, df_new])
    df_final.sort_values(by='Date', inplace=True)
    df_final.drop_duplicates(subset=['Date'], keep='last', inplace=True)
    
    print(f"Successfully added {len(df_new)} new rows.")
    print(f"New dataset range: {df_final['Date'].min().date()} to {df_final['Date'].max().date()}")
    
    # Save
    output_filename = BASE_DIR / 'gold_data_2000_2025.csv'
    df_final.to_csv(output_filename, index=False)
    print(f"Saved complete dataset to {output_filename}")
else:
    print("No new data found or download failed.")
    # Save what we have
    output_filename = BASE_DIR / 'gold_data_combined.csv'
    df_combined.to_csv(output_filename, index=False)
    print(f"Saved combined dataset to {output_filename}")

