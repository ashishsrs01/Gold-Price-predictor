import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from datetime import datetime
from pathlib import Path

from Cleaning_data import BASE_DIR
# Load the cleaned and combined data
data_path = BASE_DIR / 'gold_data_2000_2025.csv'
data = pd.read_csv(data_path)
data['Date'] = pd.to_datetime(data['Date'])
data.sort_values(by='Date', inplace=True)
data.reset_index(drop=True, inplace=True)
print(f"Loaded data from {data_path} with {len(data)} records.")
# Ensure 'Price' column exists
if 'Price' not in data.columns:
    raise ValueError("The dataset must contain a 'Price' column.")

# Display basic statistics
print("Basic Statistics:")
print(data['Price'].describe())
# Check for missing values
missing_values = data.isnull().sum()
print("\nMissing Values:")
print(missing_values)
# Visualize the price trend
plt.figure(figsize=(14, 7))
plt.plot(data['Date'], data['Price'], label='Gold Price', color='gold')
plt.title('Gold Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()
