"""
Fix Weather Dimension - Create Proper Unique Dimension
Ensures clean Many-to-One relationships for Power BI
"""

import pandas as pd
import os

print("🔧 Creating Clean Weather Dimension...")

# Load all sheets from Excel file
file_path = '../power_bi/data_model/rapido_dashboard_data.xlsx'

with pd.ExcelFile(file_path) as xls:
    fact_rides = pd.read_excel(xls, 'FactRides')
    dim_time = pd.read_excel(xls, 'DimTime')
    dim_hour = pd.read_excel(xls, 'DimHour')
    dim_vehicle = pd.read_excel(xls, 'DimVehicle')
    dim_weather_old = pd.read_excel(xls, 'DimWeather')

print(f"Original DimWeather rows: {len(dim_weather_old)}")
print("Current weather conditions with duplicates:")
print(dim_weather_old['weather_condition'].value_counts())

# Create clean dimension with one row per weather condition
weather_summary = {
    'Clear': {'main_category': 'Clear Sky', 'description': 'Clear weather conditions', 'impact_level': 'Low', 'typical_surge': '1.37x'},
    'Clouds': {'main_category': 'Cloudy', 'description': 'Partly to mostly cloudy', 'impact_level': 'Medium', 'typical_surge': '1.50x'},
    'Haze': {'main_category': 'Atmospheric Haze', 'description': 'Reduced visibility due to haze', 'impact_level': 'Medium', 'typical_surge': '1.60x'},
    'Rain': {'main_category': 'Precipitation', 'description': 'Light to moderate rainfall', 'impact_level': 'High', 'typical_surge': '1.90x'},
    'Thunderstorm': {'main_category': 'Severe Weather', 'description': 'Thunderstorms with heavy rain', 'impact_level': 'Very High', 'typical_surge': '2.28x'}
}

# Create new clean dimension table
dim_weather_clean = pd.DataFrame([
    {
        'weather_condition': condition,
        'main_category': details['main_category'],
        'description': details['description'],
        'impact_level': details['impact_level'],
        'typical_surge_multiplier': details['typical_surge'],
        'severity_score': {'Low': 1, 'Medium': 2, 'High': 3, 'Very High': 4}[details['impact_level']],
        'weather_emoji': {'Clear': '☀️', 'Clouds': '☁️', 'Haze': '🌫️', 'Rain': '☔', 'Thunderstorm': '⛈️'}[condition]
    }
    for condition, details in weather_summary.items()
])

print(f"\n✅ Clean DimWeather rows: {len(dim_weather_clean)}")
print("New unique weather conditions:")
for _, row in dim_weather_clean.iterrows():
    print(f"  {row['weather_emoji']} {row['weather_condition']}: {row['impact_level']} Impact ({row['typical_surge_multiplier']})")

# Verify no duplicates in fact table relationships
print(f"\nFact table weather conditions check:")
fact_weather_counts = fact_rides['weather_condition'].value_counts()
print(fact_weather_counts)

# Check if all fact table weather conditions exist in dimension
missing_conditions = set(fact_rides['weather_condition'].unique()) - set(dim_weather_clean['weather_condition'].unique())
if missing_conditions:
    print(f"⚠️  Missing conditions in dimension: {missing_conditions}")
else:
    print("✅ All fact table weather conditions exist in dimension")

# Create backup
backup_path = file_path.replace('.xlsx', '_backup.xlsx')
if not os.path.exists(backup_path):
    os.rename(file_path, backup_path)
    print(f"📁 Backup created: {backup_path}")

# Write clean data
print("💾 Writing clean data with unique weather dimension...")
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    fact_rides.to_excel(writer, sheet_name='FactRides', index=False)
    dim_time.to_excel(writer, sheet_name='DimTime', index=False)
    dim_hour.to_excel(writer, sheet_name='DimHour', index=False)
    dim_vehicle.to_excel(writer, sheet_name='DimVehicle', index=False)
    dim_weather_clean.to_excel(writer, sheet_name='DimWeather', index=False)

print("✅ Fixed Excel file created!")

print("\n🎯 POWER BI STEPS:")
print("1. ❌ Cancel the current relationship dialog")
print("2. 🔄 Close Power BI and reopen")
print("3. 📊 Import the updated Excel file")
print("4. 🔗 Create relationship: FactRides[weather_condition] → DimWeather[weather_condition]")
print("5. ✅ Set cardinality: Many to One (*:1)")
print("6. 🎉 Relationship should work perfectly now!")

print("\n📋 New DimWeather Structure:")
print(dim_weather_clean.to_string(index=False))
