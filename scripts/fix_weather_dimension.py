"""
Fix Weather Dimension - Remove Duplicates for Power BI
Ensures clean Many-to-One relationships
"""

import pandas as pd
import os

print("🔧 Fixing Weather Dimension Duplicates...")

# Load the current Excel file
file_path = '../power_bi/data_model/rapido_dashboard_data.xlsx'

# Read all sheets
with pd.ExcelFile(file_path) as xls:
    fact_rides = pd.read_excel(xls, 'FactRides')
    dim_time = pd.read_excel(xls, 'DimTime')
    dim_hour = pd.read_excel(xls, 'DimHour')
    dim_vehicle = pd.read_excel(xls, 'DimVehicle')
    dim_weather = pd.read_excel(xls, 'DimWeather')

print(f"Current DimWeather rows: {len(dim_weather)}")
print("Duplicate weather conditions detected:")
duplicates = dim_weather.groupby('Column1').size()
for weather, count in duplicates[duplicates > 1].items():
    print(f"  {weather}: {count} rows")

# Fix: Remove duplicates and keep first occurrence
print("\n🧹 Removing duplicates...")
dim_weather_clean = dim_weather.drop_duplicates(subset=['Column1'], keep='first')

print(f"✅ Clean DimWeather rows: {len(dim_weather_clean)}")
print("Unique weather conditions:")
for weather in sorted(dim_weather_clean['Column1'].unique()):
    impact = dim_weather_clean[dim_weather_clean['Column1'] == weather]['Column4'].iloc[0]
    print(f"  ✓ {weather} ({impact} Impact)")

# Create backup of original file
backup_path = file_path.replace('.xlsx', '_backup.xlsx')
os.rename(file_path, backup_path)
print(f"📁 Backup created: {backup_path}")

# Write clean data back to Excel
print("💾 Writing clean data...")
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    fact_rides.to_excel(writer, sheet_name='FactRides', index=False)
    dim_time.to_excel(writer, sheet_name='DimTime', index=False)
    dim_hour.to_excel(writer, sheet_name='DimHour', index=False)
    dim_vehicle.to_excel(writer, sheet_name='DimVehicle', index=False)
    dim_weather_clean.to_excel(writer, sheet_name='DimWeather', index=False)

print("✅ Fixed Excel file created!")
print("\n🎯 Next Steps:")
print("1. Close Power BI Desktop")
print("2. Reopen and import the fixed Excel file")
print("3. Create relationships - they should work now!")
print("4. DimWeather will have unique weather conditions only")
