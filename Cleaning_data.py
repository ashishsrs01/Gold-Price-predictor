import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
input_file1 = BASE_DIR / 'Gold Futures Historical Data.csv'
input_file2 = BASE_DIR / 'gold_data.csv'
output_file = BASE_DIR / 'cleaned_gold_data.csv'

# Read and combine data
data1 = pd.read_csv(input_file1)
data2 = pd.read_csv(input_file2)
Data = pd.concat([data1, data2], ignore_index=True)

# Remove duplicates
Data = Data.drop_duplicates().reset_index(drop=True)

# Clean and format columns
Data['Date'] = pd.to_datetime(Data['Date'], format='mixed', dayfirst=True)
Data = Data.sort_values(by='Date').reset_index(drop=True)

Data['Price'] = Data['Price'].astype(str).str.replace(',', '').astype(float)
Data['Open'] = Data['Open'].astype(str).str.replace(',', '').astype(float)
Data['High'] = Data['High'].astype(str).str.replace(',', '').astype(float)
Data['Low'] = Data['Low'].astype(str).str.replace(',', '').astype(float)
Data['Vol.'] = Data['Vol.'].astype(str).str.replace(',', '').str.replace('-', '0').astype(float, errors='ignore')
Data['Change %'] = Data['Change %'].astype(str).str.replace('%', '').astype(float)

# Remove rows with missing values
Data = Data.dropna().reset_index(drop=True)

# Save cleaned data
Data.to_csv(output_file, index=False)
print("Data cleaning complete. Cleaned data saved to 'cleaned_gold_data.csv'.")

