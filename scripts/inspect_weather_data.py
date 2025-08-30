"""
Check Weather Dimension Structure and Fix Duplicates
"""

import pandas as pd
import os

print("🔍 Inspecting current Excel file structure...")

# Load the Excel file
file_path = '../power_bi/data_model/rapido_dashboard_data.xlsx'

# Read DimWeather sheet
dim_weather = pd.read_excel(file_path, 'DimWeather')

print(f"DimWeather shape: {dim_weather.shape}")
print(f"Column names: {list(dim_weather.columns)}")
print("\nFirst few rows:")
print(dim_weather.head())

print(f"\nUnique values in first column ({dim_weather.columns[0]}):")
first_col_counts = dim_weather[dim_weather.columns[0]].value_counts()
print(first_col_counts)

print(f"\nDuplicates in {dim_weather.columns[0]}:")
duplicates = first_col_counts[first_col_counts > 1]
if len(duplicates) > 0:
    print(duplicates)
else:
    print("No duplicates found!")

# Let's also check all the data
print("\nAll data in DimWeather:")
print(dim_weather.to_string())
