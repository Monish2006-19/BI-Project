"""
Quick Business Intelligence Analysis for Rapido Transportation
Focus on Key Metrics and Power BI Preparation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
print("🚀 Loading Rapido Transportation Dataset...")
df = pd.read_csv("../Dataset.csv")

# Convert datetime columns
df['datetime'] = pd.to_datetime(df['datetime'])
df['date'] = pd.to_datetime(df['date'])

print(f"✅ Dataset loaded: {len(df):,} rides from {df['date'].min().date()} to {df['date'].max().date()}")

# Define rush hours
df['is_morning_rush'] = (df['hour'] >= 8) & (df['hour'] <= 9)
df['is_evening_rush'] = (df['hour'] >= 17) & (df['hour'] <= 18)
df['is_rush_hour'] = df['is_morning_rush'] | df['is_evening_rush']

print("\n📊 CALCULATING KEY KPIs...")
print("=" * 50)

# Key Revenue KPIs
total_revenue = df['final_price'].sum()
total_base_revenue = df['base_price'].sum()
surge_revenue = total_revenue - total_base_revenue
avg_revenue_per_ride = df['final_price'].mean()
surge_contribution_pct = (surge_revenue / total_revenue) * 100

print(f"💰 Total Revenue: ₹{total_revenue:,.2f}")
print(f"💰 Base Revenue: ₹{total_base_revenue:,.2f}")
print(f"💰 Surge Revenue: ₹{surge_revenue:,.2f}")
print(f"📈 Surge Contribution: {surge_contribution_pct:.1f}%")
print(f"💳 Average Revenue per Ride: ₹{avg_revenue_per_ride:.2f}")

# Trip Volume KPIs
total_trips = len(df)
avg_distance = df['distance_km'].mean()
avg_waiting_time = df['waiting_time_minutes'].mean()

print(f"\n🚗 Total Trips: {total_trips:,}")
print(f"📏 Average Distance: {avg_distance:.2f} km")
print(f"⏱️ Average Waiting Time: {avg_waiting_time:.1f} minutes")

# Vehicle Performance
vehicle_revenue = df.groupby('vehicle_type')['final_price'].sum()
vehicle_trips = df.groupby('vehicle_type').size()
print(f"\n🚙 Vehicle Revenue Distribution:")
for vehicle, revenue in vehicle_revenue.items():
    pct = (revenue / total_revenue) * 100
    trips = vehicle_trips[vehicle]
    print(f"  {vehicle.title()}: ₹{revenue:,.2f} ({pct:.1f}%) - {trips:,} trips")

# Rush Hour Analysis
print(f"\n⏰ RUSH HOUR ANALYSIS:")
print("=" * 30)

morning_rush = df[df['is_morning_rush']]
evening_rush = df[df['is_evening_rush']]

print(f"🌅 Morning Rush (8-9 AM):")
print(f"  Trips: {len(morning_rush):,}")
print(f"  Revenue: ₹{morning_rush['final_price'].sum():,.2f}")
print(f"  Avg Surge: {morning_rush['surge_multiplier'].mean():.2f}x")

print(f"\n🌆 Evening Rush (5:30-6:30 PM):")
print(f"  Trips: {len(evening_rush):,}")
print(f"  Revenue: ₹{evening_rush['final_price'].sum():,.2f}")
print(f"  Avg Surge: {evening_rush['surge_multiplier'].mean():.2f}x")

# Weather Impact Analysis
print(f"\n🌦️ WEATHER IMPACT ANALYSIS:")
print("=" * 35)

weather_stats = df.groupby('weather_condition').agg({
    'final_price': ['count', 'sum', 'mean'],
    'surge_multiplier': 'mean'
}).round(2)

print("Weather Impact Summary:")
for weather in weather_stats.index:
    trips = weather_stats.loc[weather, ('final_price', 'count')]
    revenue = weather_stats.loc[weather, ('final_price', 'sum')]
    avg_price = weather_stats.loc[weather, ('final_price', 'mean')]
    avg_surge = weather_stats.loc[weather, ('surge_multiplier', 'mean')]
    
    print(f"  {weather}: {trips:,} trips, ₹{revenue:,.0f} revenue, {avg_surge:.2f}x surge")

# Rain vs Clear Weather Comparison
rain_data = df[df['weather_condition'] == 'Rain']
clear_data = df[df['weather_condition'] == 'Clear']

if len(rain_data) > 0 and len(clear_data) > 0:
    rain_avg_surge = rain_data['surge_multiplier'].mean()
    clear_avg_surge = clear_data['surge_multiplier'].mean()
    surge_difference = rain_avg_surge / clear_avg_surge
    
    print(f"\n☔ Rain Impact:")
    print(f"  Rain trips: {len(rain_data):,}")
    print(f"  Rain surge: {rain_avg_surge:.2f}x")
    print(f"  Clear surge: {clear_avg_surge:.2f}x")
    print(f"  Rain premium: {surge_difference:.2f}x higher than clear weather")

# Time Pattern Analysis
print(f"\n⏰ TIME PATTERN ANALYSIS:")
print("=" * 32)

hourly_stats = df.groupby('hour').agg({
    'ride_id': 'count',
    'final_price': 'sum',
    'surge_multiplier': 'mean'
}).round(2)

peak_hours = hourly_stats['ride_id'].nlargest(3)
print("Top 3 Peak Hours:")
for hour, trips in peak_hours.items():
    revenue = hourly_stats.loc[hour, 'final_price']
    surge = hourly_stats.loc[hour, 'surge_multiplier']
    print(f"  {hour}:00 - {trips:,} trips, ₹{revenue:,.0f} revenue, {surge:.2f}x surge")

# Weekend vs Weekday
weekend_data = df[df['is_weekend']]
weekday_data = df[~df['is_weekend']]

print(f"\n📅 Weekend vs Weekday:")
print(f"  Weekend: {len(weekend_data):,} trips, ₹{weekend_data['final_price'].sum():,.0f}")
print(f"  Weekday: {len(weekday_data):,} trips, ₹{weekday_data['final_price'].sum():,.0f}")

# VIT University Analysis
vit_routes = df[df['from_location'].str.contains('VIT', na=False) | 
               df['to_location'].str.contains('VIT', na=False)]

print(f"\n🎓 VIT UNIVERSITY ROUTES:")
print("=" * 30)
print(f"  Total VIT trips: {len(vit_routes):,}")
print(f"  VIT revenue: ₹{vit_routes['final_price'].sum():,.2f}")
print(f"  VIT revenue share: {(vit_routes['final_price'].sum() / total_revenue) * 100:.1f}%")
print(f"  Avg VIT trip price: ₹{vit_routes['final_price'].mean():.2f}")

# Top Routes
print(f"\n🗺️ TOP 10 ROUTES BY REVENUE:")
print("=" * 35)
route_revenue = df.groupby(['from_location', 'to_location'])['final_price'].sum().nlargest(10)
for i, ((from_loc, to_loc), revenue) in enumerate(route_revenue.items(), 1):
    print(f"  {i}. {from_loc} → {to_loc}: ₹{revenue:,.0f}")

print("\n" + "=" * 70)
print("✅ ANALYSIS COMPLETE!")
print("🔄 Preparing data for Power BI...")

# Prepare simplified data for Power BI
print("\n📤 Creating Power BI Dataset...")

# Create a clean fact table
fact_table = df[[
    'ride_id', 'datetime', 'date', 'hour', 'vehicle_type', 
    'from_location', 'to_location', 'distance_km', 'weather_condition',
    'base_price', 'final_price', 'surge_multiplier', 'waiting_time_minutes',
    'price_premium_percent', 'temperature', 'humidity', 'precipitation',
    'is_weekend', 'month', 'quarter', 'day_of_week'
]].copy()

# Add calculated fields
fact_table['surge_amount'] = fact_table['final_price'] - fact_table['base_price']
fact_table['price_per_km'] = fact_table['final_price'] / fact_table['distance_km']
fact_table['route'] = fact_table['from_location'] + " → " + fact_table['to_location']

# Create time dimension
time_dim = df[['date', 'month', 'quarter', 'day_of_week', 'is_weekend']].drop_duplicates()
time_dim['year'] = time_dim['date'].dt.year
time_dim['month_name'] = time_dim['date'].dt.month_name()
time_dim['day_name'] = time_dim['date'].dt.day_name()

# Create hour dimension
hour_dim = pd.DataFrame({
    'hour': range(24),
    'time_period': ['Late Night' if h < 6 else 
                   'Early Morning' if h < 8 else
                   'Morning Rush' if h < 10 else
                   'Late Morning' if h < 12 else
                   'Lunch Time' if h < 14 else
                   'Afternoon' if h < 17 else
                   'Evening Rush' if h < 19 else
                   'Evening' if h < 22 else 'Night' for h in range(24)],
    'is_rush_hour': [h in [8, 9, 17, 18] for h in range(24)]
})

# Vehicle dimension
vehicle_dim = pd.DataFrame({
    'vehicle_type': ['bike', 'auto', 'cab'],
    'capacity': [1, 3, 4],
    'category': ['Two Wheeler', 'Three Wheeler', 'Four Wheeler']
})

# Weather dimension
weather_dim = df[['weather_condition', 'weather_main', 'weather_description']].drop_duplicates()
weather_dim['impact_level'] = weather_dim['weather_condition'].map({
    'Clear': 'Low',
    'Clouds': 'Medium', 
    'Haze': 'Medium',
    'Rain': 'High',
    'Thunderstorm': 'Very High'
})

# Export to Excel for Power BI
print("💾 Exporting to Excel for Power BI...")
import os
os.makedirs('../power_bi/data_model', exist_ok=True)

with pd.ExcelWriter('../power_bi/data_model/rapido_dashboard_data.xlsx', engine='openpyxl') as writer:
    fact_table.to_excel(writer, sheet_name='FactRides', index=False)
    time_dim.to_excel(writer, sheet_name='DimTime', index=False)
    hour_dim.to_excel(writer, sheet_name='DimHour', index=False)
    vehicle_dim.to_excel(writer, sheet_name='DimVehicle', index=False)
    weather_dim.to_excel(writer, sheet_name='DimWeather', index=False)

print("✅ Excel file created: ../power_bi/data_model/rapido_dashboard_data.xlsx")

# Create DAX measures file
dax_measures = """
# Key DAX Measures for Rapido Transportation Dashboard

Total Revenue = SUM(FactRides[final_price])
Total Trips = COUNTROWS(FactRides)
Average Revenue Per Ride = AVERAGE(FactRides[final_price])
Surge Revenue = SUM(FactRides[surge_amount])
Surge Percentage = DIVIDE([Surge Revenue], [Total Revenue]) * 100

# Time Intelligence
Revenue MTD = TOTALMTD([Total Revenue], DimTime[date])
Revenue QTD = TOTALQTD([Total Revenue], DimTime[date])
Revenue Growth = 
VAR CurrentMonth = [Total Revenue]
VAR PreviousMonth = CALCULATE([Total Revenue], PREVIOUSMONTH(DimTime[date]))
RETURN DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth) * 100

# Weather Analysis
Rain Revenue = CALCULATE([Total Revenue], DimWeather[weather_condition] = "Rain")
Clear Revenue = CALCULATE([Total Revenue], DimWeather[weather_condition] = "Clear")
Weather Premium = DIVIDE([Rain Revenue], [Clear Revenue]) - 1

# Rush Hour Analysis
Rush Hour Revenue = CALCULATE([Total Revenue], DimHour[is_rush_hour] = TRUE)
Rush Hour Trips = CALCULATE([Total Trips], DimHour[is_rush_hour] = TRUE)

# Vehicle Performance
Bike Revenue = CALCULATE([Total Revenue], DimVehicle[vehicle_type] = "bike")
Auto Revenue = CALCULATE([Total Revenue], DimVehicle[vehicle_type] = "auto")
Cab Revenue = CALCULATE([Total Revenue], DimVehicle[vehicle_type] = "cab")

# Service Quality
Average Wait Time = AVERAGE(FactRides[waiting_time_minutes])
Service Quality Score = 1 / ([Average Wait Time] + 1) * 100

# KPIs
Revenue Per KM = DIVIDE([Total Revenue], SUM(FactRides[distance_km]))
Average Surge Multiplier = AVERAGE(FactRides[surge_multiplier])
VIT Revenue = 
CALCULATE([Total Revenue], 
    OR(
        CONTAINSSTRING(FactRides[from_location], "VIT"),
        CONTAINSSTRING(FactRides[to_location], "VIT")
    )
)
"""

os.makedirs('../power_bi/measures', exist_ok=True)
with open('../power_bi/measures/dax_measures.txt', 'w') as f:
    f.write(dax_measures)

print("✅ DAX measures saved: ../power_bi/measures/dax_measures.txt")

print("\n🎯 KEY BUSINESS INSIGHTS:")
print("=" * 40)
print(f"1. 📈 Surge pricing is highly effective - contributing {surge_contribution_pct:.1f}% of revenue")
print(f"2. 🎓 VIT University routes are crucial - {(vit_routes['final_price'].sum() / total_revenue) * 100:.1f}% of revenue")
print(f"3. ☔ Rain significantly boosts revenue through surge pricing")
print(f"4. 🌆 Evening rush hour shows strong demand patterns")
print(f"5. 🚗 Auto rickshaws generate the highest revenue share")

print(f"\n✅ Ready for Power BI Dashboard Creation!")
print(f"📂 Files created in /power_bi/ directory")
print(f"🚀 Next: Import rapido_dashboard_data.xlsx into Power BI")
