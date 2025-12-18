import numpy as np
import pandas as pd

data1 = pd.read_csv('C:\\Project\\Gold-Price-predictor\\Gold Futures Historical Data.csv')
data2 = pd.read_csv('C:\\Project\\Gold-Price-predictor\\gold_data.csv')

Data = pd.concat([data1, data2], ignore_index=True)
Data = Data.drop_duplicates().reset_index(drop=True)

Data['Date'] = pd.to_datetime(Data['Date'], format='%b %d, %Y')
Data = Data.sort_values(by='Date').reset_index(drop=True)
Data['Price'] = Data['Price'].str.replace(',', '').astype(float)
Data['Open'] = Data['Open'].str.replace(',', '').astype(float)
Data['High'] = Data['High'].str.replace(',', '').astype(float)
Data['Low'] = Data['Low'].str.replace(',', '').astype(float)
Data['Vol.'] = Data['Vol.'].str.replace(',', '').replace('-', '0').astype(float)
Data['Change %'] = Data['Change %'].str.replace('%', '').astype(float)
Data = Data.dropna().reset_index(drop=True)

Data.to_csv('C:\\Project\\Gold-Price-predictor\\cleaned_gold_data.csv', index=False)

print("Data cleaning complete. Cleaned data saved to 'cleaned_gold_data.csv'.")

