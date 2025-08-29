"""
Power BI Data Model Preparation Script
Author: BI Project Team
Date: August 29, 2025

This script prepares optimized datasets for Power BI dashboard:
1. Creates fact and dimension tables following star schema
2. Generates DAX measures and calculations
3. Optimizes data types for Power BI performance
4. Creates data model documentation
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import json

class PowerBIDataPreparation:
    """
    Prepare and optimize data for Power BI dashboard
    """
    
    def __init__(self, source_data_path, output_dir="../power_bi/data_model/"):
        self.source_data_path = source_data_path
        self.output_dir = output_dir
        self.df = None
        self.fact_table = None
        self.dimension_tables = {}
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
    
    def load_and_prepare_source_data(self):
        """Load source data and prepare for star schema design"""
        print("📊 Loading source data for Power BI preparation...")
        
        self.df = pd.read_csv(self.source_data_path)
        
        # Convert datetime columns
        self.df['datetime'] = pd.to_datetime(self.df['datetime'])
        self.df['date'] = pd.to_datetime(self.df['date'])
        
        # Add additional calculated columns for Power BI
        self.df['revenue_category'] = pd.cut(self.df['final_price'], 
                                           bins=[0, 50, 100, 200, float('inf')],
                                           labels=['Low', 'Medium', 'High', 'Premium'])
        
        self.df['surge_category'] = pd.cut(self.df['surge_multiplier'],
                                         bins=[0, 1.2, 1.5, 2.0, float('inf')],
                                         labels=['Normal', 'Low Surge', 'High Surge', 'Peak Surge'])
        
        # Create unique identifiers for dimensions
        self.df['location_route_id'] = self.df['from_location'] + " → " + self.df['to_location']
        self.df['weather_condition_id'] = self.df['weather_condition'] + "_" + self.df['weather_description']
        
        print(f"✅ Source data prepared: {len(self.df):,} records")
        return self.df
    
    def create_fact_table(self):
        """Create the main fact table for rides"""
        print("🏗️ Creating Fact Table: Rides...")
        
        fact_columns = [
            # Primary Key
            'ride_id',
            
            # Foreign Keys (will link to dimension tables)
            'datetime',
            'date',
            'vehicle_type',
            'location_route_id',
            'weather_condition',
            
            # Measures (numerical facts)
            'distance_km',
            'base_price',
            'final_price',
            'surge_multiplier',
            'waiting_time_minutes',
            'price_premium_percent',
            'temperature',
            'humidity',
            'precipitation',
            'wind_speed',
            'visibility',
            
            # Additional calculated measures
            'surge_amount',  # final_price - base_price
            'price_per_km',
            'revenue_per_minute',  # final_price / (waiting_time + estimated_trip_time)
        ]
        
        self.fact_table = self.df[fact_columns].copy()
        
        # Calculate additional measures
        self.fact_table['surge_amount'] = self.fact_table['final_price'] - self.fact_table['base_price']
        self.fact_table['price_per_km'] = self.fact_table['final_price'] / self.fact_table['distance_km']
        
        # Estimate trip time and calculate revenue per minute
        estimated_trip_time = self.fact_table['distance_km'] * 3  # Assume 3 minutes per km
        total_time = self.fact_table['waiting_time_minutes'] + estimated_trip_time
        self.fact_table['revenue_per_minute'] = self.fact_table['final_price'] / total_time
        
        # Optimize data types for Power BI performance
        self.fact_table['ride_id'] = self.fact_table['ride_id'].astype('string')
        self.fact_table['vehicle_type'] = self.fact_table['vehicle_type'].astype('category')
        self.fact_table['weather_condition'] = self.fact_table['weather_condition'].astype('category')
        
        # Round numerical columns for better performance
        numeric_columns = ['distance_km', 'base_price', 'final_price', 'surge_multiplier', 
                          'price_premium_percent', 'surge_amount', 'price_per_km', 'revenue_per_minute']
        for col in numeric_columns:
            self.fact_table[col] = self.fact_table[col].round(2)
        
        print(f"✅ Fact table created with {len(self.fact_table)} rows and {len(self.fact_table.columns)} columns")
        return self.fact_table
    
    def create_time_dimension(self):
        """Create comprehensive time dimension table"""
        print("📅 Creating Dimension Table: Time...")
        
        # Get unique dates from the dataset
        unique_dates = pd.date_range(start=self.df['date'].min(), 
                                   end=self.df['date'].max(), 
                                   freq='D')
        
        time_dim = pd.DataFrame({'date': unique_dates})
        
        # Add comprehensive time attributes
        time_dim['year'] = time_dim['date'].dt.year
        time_dim['quarter'] = time_dim['date'].dt.quarter
        time_dim['month'] = time_dim['date'].dt.month
        time_dim['month_name'] = time_dim['date'].dt.month_name()
        time_dim['week_of_year'] = time_dim['date'].dt.isocalendar().week
        time_dim['day_of_year'] = time_dim['date'].dt.dayofyear
        time_dim['day_of_month'] = time_dim['date'].dt.day
        time_dim['day_of_week'] = time_dim['date'].dt.dayofweek
        time_dim['day_name'] = time_dim['date'].dt.day_name()
        time_dim['is_weekend'] = time_dim['day_of_week'].isin([5, 6])
        time_dim['is_month_start'] = time_dim['date'].dt.is_month_start
        time_dim['is_month_end'] = time_dim['date'].dt.is_month_end
        time_dim['is_quarter_start'] = time_dim['date'].dt.is_quarter_start
        time_dim['is_quarter_end'] = time_dim['date'].dt.is_quarter_end
        
        # Add business calendar attributes
        time_dim['fiscal_year'] = time_dim['year']  # Assuming calendar year = fiscal year
        time_dim['fiscal_quarter'] = time_dim['quarter']
        
        # Add season information
        def get_season(month):
            if month in [12, 1, 2]:
                return 'Winter'
            elif month in [3, 4, 5]:
                return 'Spring'
            elif month in [6, 7, 8]:
                return 'Summer'
            else:
                return 'Autumn'
        
        time_dim['season'] = time_dim['month'].apply(get_season)
        
        # Add Indian holidays (simplified)
        indian_holidays = [
            '2024-01-26',  # Republic Day
            '2024-03-08',  # Holi
            '2024-04-14',  # Ram Navami
            '2024-08-15',  # Independence Day
            '2024-10-02',  # Gandhi Jayanti
            '2024-10-31',  # Diwali
            '2024-12-25'   # Christmas
        ]
        
        time_dim['is_holiday'] = time_dim['date'].dt.strftime('%Y-%m-%d').isin(indian_holidays)
        
        # Create date key for relationships
        time_dim['date_key'] = time_dim['date'].dt.strftime('%Y%m%d').astype(int)
        
        self.dimension_tables['time_dimension'] = time_dim
        print(f"✅ Time dimension created with {len(time_dim)} rows")
        return time_dim
    
    def create_hour_dimension(self):
        """Create hour dimension for detailed time analysis"""
        print("🕐 Creating Dimension Table: Hour...")
        
        hours = list(range(24))
        hour_dim = pd.DataFrame({'hour': hours})
        
        # Add time period classifications
        def get_time_period(hour):
            if 0 <= hour < 6:
                return 'Late Night'
            elif 6 <= hour < 8:
                return 'Early Morning'
            elif 8 <= hour < 10:
                return 'Morning Rush'
            elif 10 <= hour < 12:
                return 'Late Morning'
            elif 12 <= hour < 14:
                return 'Lunch Time'
            elif 14 <= hour < 17:
                return 'Afternoon'
            elif 17 <= hour < 19:
                return 'Evening Rush'
            elif 19 <= hour < 22:
                return 'Evening'
            else:
                return 'Night'
        
        hour_dim['time_period'] = hour_dim['hour'].apply(get_time_period)
        hour_dim['is_business_hour'] = hour_dim['hour'].between(9, 18)
        hour_dim['is_rush_hour'] = hour_dim['hour'].isin([8, 9, 17, 18])
        hour_dim['is_peak_demand'] = hour_dim['hour'].isin([8, 9, 17, 18, 19])
        
        # Add hour categories for grouping
        hour_dim['hour_category'] = pd.cut(hour_dim['hour'],
                                         bins=[-1, 6, 12, 18, 24],
                                         labels=['Night', 'Morning', 'Afternoon', 'Evening'])
        
        self.dimension_tables['hour_dimension'] = hour_dim
        print(f"✅ Hour dimension created with {len(hour_dim)} rows")
        return hour_dim
    
    def create_location_dimension(self):
        """Create location and route dimension"""
        print("📍 Creating Dimension Table: Locations & Routes...")
        
        # Create unique locations
        all_locations = pd.concat([
            self.df['from_location'],
            self.df['to_location']
        ]).unique()
        
        location_dim = pd.DataFrame({'location_name': all_locations})
        location_dim['location_id'] = location_dim.index + 1
        
        # Categorize locations
        def categorize_location(location):
            if 'VIT' in location:
                return 'University'
            elif any(keyword in location.lower() for keyword in ['hospital', 'medical']):
                return 'Healthcare'
            elif any(keyword in location.lower() for keyword in ['station', 'railway']):
                return 'Transportation Hub'
            elif any(keyword in location.lower() for keyword in ['road', 'street']):
                return 'Residential/Commercial'
            elif any(keyword in location.lower() for keyword in ['bus', 'stand']):
                return 'Bus Terminal'
            else:
                return 'General'
        
        location_dim['location_category'] = location_dim['location_name'].apply(categorize_location)
        
        # Create route dimension
        route_combinations = self.df[['from_location', 'to_location', 'location_route_id']].drop_duplicates()
        route_dim = route_combinations.copy()
        route_dim['route_id'] = route_dim.index + 1
        
        # Add route characteristics
        route_stats = self.df.groupby('location_route_id').agg({
            'distance_km': ['mean', 'min', 'max'],
            'final_price': 'mean',
            'ride_id': 'count'
        }).round(2)
        
        route_stats.columns = ['avg_distance', 'min_distance', 'max_distance', 'avg_price', 'total_trips']
        route_dim = route_dim.merge(route_stats, left_on='location_route_id', right_index=True)
        
        # Categorize routes by distance
        route_dim['distance_category'] = pd.cut(route_dim['avg_distance'],
                                              bins=[0, 5, 10, 15, float('inf')],
                                              labels=['Short', 'Medium', 'Long', 'Extra Long'])
        
        # Categorize routes by popularity
        route_dim['popularity_category'] = pd.cut(route_dim['total_trips'],
                                                bins=[0, 50, 200, 500, float('inf')],
                                                labels=['Low', 'Medium', 'High', 'Very High'])
        
        self.dimension_tables['location_dimension'] = location_dim
        self.dimension_tables['route_dimension'] = route_dim
        
        print(f"✅ Location dimension created with {len(location_dim)} locations")
        print(f"✅ Route dimension created with {len(route_dim)} routes")
        return location_dim, route_dim
    
    def create_weather_dimension(self):
        """Create weather dimension table"""
        print("🌦️ Creating Dimension Table: Weather...")
        
        # Get unique weather conditions
        weather_combinations = self.df[['weather_condition', 'weather_main', 'weather_description']].drop_duplicates()
        weather_dim = weather_combinations.copy()
        weather_dim['weather_id'] = weather_dim.index + 1
        
        # Add weather impact categories
        def categorize_weather_impact(condition):
            if condition in ['Rain', 'Thunderstorm']:
                return 'High Impact'
            elif condition in ['Clouds', 'Haze']:
                return 'Medium Impact'
            elif condition in ['Clear']:
                return 'Low Impact'
            else:
                return 'Unknown'
        
        weather_dim['impact_category'] = weather_dim['weather_condition'].apply(categorize_weather_impact)
        
        # Add weather severity
        def get_weather_severity(condition):
            severity_map = {
                'Clear': 1,
                'Clouds': 2,
                'Haze': 3,
                'Rain': 4,
                'Thunderstorm': 5
            }
            return severity_map.get(condition, 0)
        
        weather_dim['severity_score'] = weather_dim['weather_condition'].apply(get_weather_severity)
        
        # Add expected surge impact
        def get_expected_surge(condition):
            surge_map = {
                'Clear': 1.1,
                'Clouds': 1.3,
                'Haze': 1.4,
                'Rain': 1.8,
                'Thunderstorm': 2.2
            }
            return surge_map.get(condition, 1.0)
        
        weather_dim['expected_surge_multiplier'] = weather_dim['weather_condition'].apply(get_expected_surge)
        
        self.dimension_tables['weather_dimension'] = weather_dim
        print(f"✅ Weather dimension created with {len(weather_dim)} weather conditions")
        return weather_dim
    
    def create_vehicle_dimension(self):
        """Create vehicle type dimension"""
        print("🚗 Creating Dimension Table: Vehicle Types...")
        
        vehicle_types = self.df['vehicle_type'].unique()
        vehicle_dim = pd.DataFrame({'vehicle_type': vehicle_types})
        vehicle_dim['vehicle_id'] = vehicle_dim.index + 1
        
        # Add vehicle characteristics
        vehicle_characteristics = {
            'bike': {
                'capacity': 1,
                'base_fare_per_km': 12,
                'surge_sensitivity': 'High',
                'weather_impact': 'High',
                'category': 'Two Wheeler'
            },
            'auto': {
                'capacity': 3,
                'base_fare_per_km': 18,
                'surge_sensitivity': 'Medium',
                'weather_impact': 'Medium',
                'category': 'Three Wheeler'
            },
            'cab': {
                'capacity': 4,
                'base_fare_per_km': 25,
                'surge_sensitivity': 'Low',
                'weather_impact': 'Low',
                'category': 'Four Wheeler'
            }
        }
        
        for vehicle in vehicle_types:
            if vehicle in vehicle_characteristics:
                chars = vehicle_characteristics[vehicle]
                for key, value in chars.items():
                    vehicle_dim.loc[vehicle_dim['vehicle_type'] == vehicle, key] = value
        
        self.dimension_tables['vehicle_dimension'] = vehicle_dim
        print(f"✅ Vehicle dimension created with {len(vehicle_dim)} vehicle types")
        return vehicle_dim
    
    def create_dax_measures(self):
        """Create DAX measures for Power BI"""
        print("📐 Creating DAX Measures...")
        
        dax_measures = {
            # Basic Revenue Measures
            "Total Revenue": "SUM(FactRides[final_price])",
            "Total Base Revenue": "SUM(FactRides[base_price])",
            "Surge Revenue": "SUM(FactRides[surge_amount])",
            "Average Ticket Size": "AVERAGE(FactRides[final_price])",
            
            # Trip Volume Measures
            "Total Trips": "COUNTROWS(FactRides)",
            "Average Distance": "AVERAGE(FactRides[distance_km])",
            "Total Distance": "SUM(FactRides[distance_km])",
            
            # Time Intelligence Measures
            "Revenue MTD": "TOTALMTD(SUM(FactRides[final_price]), DimTime[date])",
            "Revenue QTD": "TOTALQTD(SUM(FactRides[final_price]), DimTime[date])",
            "Revenue YTD": "TOTALYTD(SUM(FactRides[final_price]), DimTime[date])",
            "Revenue Previous Month": "CALCULATE(SUM(FactRides[final_price]), PREVIOUSMONTH(DimTime[date]))",
            "Revenue Growth MoM": "DIVIDE([Total Revenue] - [Revenue Previous Month], [Revenue Previous Month])",
            
            # Surge Analysis Measures
            "Average Surge Multiplier": "AVERAGE(FactRides[surge_multiplier])",
            "Surge Revenue %": "DIVIDE([Surge Revenue], [Total Revenue])",
            "Trips with Surge": "CALCULATE(COUNTROWS(FactRides), FactRides[surge_multiplier] > 1.2)",
            "Surge Trip %": "DIVIDE([Trips with Surge], [Total Trips])",
            
            # Weather Impact Measures
            "Rain Trips": "CALCULATE(COUNTROWS(FactRides), DimWeather[weather_condition] = \"Rain\")",
            "Rain Revenue": "CALCULATE(SUM(FactRides[final_price]), DimWeather[weather_condition] = \"Rain\")",
            "Clear Weather Revenue": "CALCULATE(SUM(FactRides[final_price]), DimWeather[weather_condition] = \"Clear\")",
            "Weather Premium": "DIVIDE([Rain Revenue], [Clear Weather Revenue]) - 1",
            
            # Time-based Measures
            "Rush Hour Revenue": "CALCULATE(SUM(FactRides[final_price]), DimHour[is_rush_hour] = TRUE)",
            "Weekend Revenue": "CALCULATE(SUM(FactRides[final_price]), DimTime[is_weekend] = TRUE)",
            "Weekday Revenue": "CALCULATE(SUM(FactRides[final_price]), DimTime[is_weekend] = FALSE)",
            
            # Service Quality Measures
            "Average Wait Time": "AVERAGE(FactRides[waiting_time_minutes])",
            "Service Quality Score": "1 / ([Average Wait Time] + 1) * 100",
            "Trips Under 5 Min Wait": "CALCULATE(COUNTROWS(FactRides), FactRides[waiting_time_minutes] <= 5)",
            "Service Quality %": "DIVIDE([Trips Under 5 Min Wait], [Total Trips])",
            
            # Vehicle Performance
            "Bike Revenue": "CALCULATE(SUM(FactRides[final_price]), DimVehicle[vehicle_type] = \"bike\")",
            "Auto Revenue": "CALCULATE(SUM(FactRides[final_price]), DimVehicle[vehicle_type] = \"auto\")",
            "Cab Revenue": "CALCULATE(SUM(FactRides[final_price]), DimVehicle[vehicle_type] = \"cab\")",
            
            # KPI Measures
            "Revenue per KM": "DIVIDE([Total Revenue], [Total Distance])",
            "Revenue per Trip": "[Average Ticket Size]",
            "Utilization Rate": "DIVIDE([Total Trips], 24 * DISTINCTCOUNT(DimTime[date]))",
            
            # Advanced Analytics
            "Revenue Trend": "VAR CurrentRevenue = [Total Revenue] VAR PreviousPeriodRevenue = CALCULATE([Total Revenue], PREVIOUSMONTH(DimTime[date])) RETURN IF(CurrentRevenue > PreviousPeriodRevenue, \"↗️ Increasing\", \"↘️ Decreasing\")",
            "Peak Hour Indicator": "IF(SELECTEDVALUE(DimHour[is_rush_hour]) = TRUE, \"🔥 Peak Hours\", \"📊 Regular Hours\")",
            "Weather Impact Indicator": "SWITCH(SELECTEDVALUE(DimWeather[impact_category]), \"High Impact\", \"⛈️ High Impact\", \"Medium Impact\", \"☁️ Medium Impact\", \"Low Impact\", \"☀️ Low Impact\", \"➖ Unknown\")"
        }
        
        # Save DAX measures to file
        measures_file = os.path.join(self.output_dir, "../measures/dax_measures.txt")
        os.makedirs(os.path.dirname(measures_file), exist_ok=True)
        
        with open(measures_file, 'w') as f:
            f.write("# DAX Measures for Rapido Transportation BI Dashboard\n")
            f.write("# Copy and paste these measures into Power BI\n\n")
            
            for measure_name, dax_formula in dax_measures.items():
                f.write(f"## {measure_name}\n")
                f.write(f"{dax_formula}\n\n")
        
        print(f"✅ {len(dax_measures)} DAX measures created and saved")
        return dax_measures
    
    def export_to_excel(self):
        """Export all tables to Excel for Power BI import"""
        print("📤 Exporting tables to Excel...")
        
        excel_file = os.path.join(self.output_dir, "rapido_data_model.xlsx")
        
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # Export fact table
            self.fact_table.to_excel(writer, sheet_name='FactRides', index=False)
            
            # Export dimension tables
            for table_name, table_data in self.dimension_tables.items():
                sheet_name = table_name.replace('_dimension', '').title()
                if sheet_name.startswith('Dim'):
                    sheet_name = sheet_name
                else:
                    sheet_name = f"Dim{sheet_name}"
                table_data.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"✅ Data model exported to: {excel_file}")
        return excel_file
    
    def create_data_model_documentation(self):
        """Create comprehensive documentation for the data model"""
        print("📚 Creating Data Model Documentation...")
        
        documentation = {
            "data_model_overview": {
                "schema_type": "Star Schema",
                "fact_table": "FactRides",
                "dimension_tables": list(self.dimension_tables.keys()),
                "total_records": len(self.fact_table),
                "date_range": f"{self.df['date'].min().date()} to {self.df['date'].max().date()}",
                "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "fact_table_details": {
                "table_name": "FactRides",
                "primary_key": "ride_id",
                "record_count": len(self.fact_table),
                "columns": list(self.fact_table.columns),
                "measures": [col for col in self.fact_table.columns if col in 
                           ['distance_km', 'base_price', 'final_price', 'surge_multiplier', 
                            'waiting_time_minutes', 'price_premium_percent', 'surge_amount']],
                "foreign_keys": ['datetime', 'vehicle_type', 'weather_condition', 'location_route_id']
            },
            "dimension_tables_details": {},
            "relationships": [
                {
                    "from_table": "FactRides",
                    "from_column": "date",
                    "to_table": "DimTime",
                    "to_column": "date",
                    "relationship_type": "Many-to-One"
                },
                {
                    "from_table": "FactRides",
                    "from_column": "hour",
                    "to_table": "DimHour",
                    "to_column": "hour",
                    "relationship_type": "Many-to-One"
                },
                {
                    "from_table": "FactRides",
                    "from_column": "vehicle_type",
                    "to_table": "DimVehicle",
                    "to_column": "vehicle_type",
                    "relationship_type": "Many-to-One"
                },
                {
                    "from_table": "FactRides",
                    "from_column": "weather_condition",
                    "to_table": "DimWeather",
                    "to_column": "weather_condition",
                    "relationship_type": "Many-to-One"
                },
                {
                    "from_table": "FactRides",
                    "from_column": "location_route_id",
                    "to_table": "DimRoute",
                    "to_column": "location_route_id",
                    "relationship_type": "Many-to-One"
                }
            ]
        }
        
        # Add dimension table details
        for table_name, table_data in self.dimension_tables.items():
            documentation["dimension_tables_details"][table_name] = {
                "record_count": len(table_data),
                "columns": list(table_data.columns),
                "primary_key": table_data.columns[0] if len(table_data.columns) > 0 else None
            }
        
        # Save documentation
        doc_file = os.path.join(self.output_dir, "data_model_documentation.json")
        with open(doc_file, 'w') as f:
            json.dump(documentation, f, indent=2, default=str)
        
        print(f"✅ Data model documentation saved to: {doc_file}")
        return documentation
    
    def generate_power_bi_setup_guide(self):
        """Generate step-by-step Power BI setup guide"""
        print("📋 Creating Power BI Setup Guide...")
        
        setup_guide = """
# Power BI Dashboard Setup Guide
## Rapido Transportation Analytics

### Step 1: Import Data
1. Open Power BI Desktop
2. Click "Get Data" > "Excel"
3. Browse and select: `rapido_data_model.xlsx`
4. Select all sheets and click "Load"

### Step 2: Create Relationships
Navigate to Model view and create these relationships:
- FactRides[date] → DimTime[date] (Many-to-One)
- FactRides[hour] → DimHour[hour] (Many-to-One)  
- FactRides[vehicle_type] → DimVehicle[vehicle_type] (Many-to-One)
- FactRides[weather_condition] → DimWeather[weather_condition] (Many-to-One)
- FactRides[location_route_id] → DimRoute[location_route_id] (Many-to-One)

### Step 3: Add DAX Measures
1. Create a new table called "Measures"
2. Copy DAX measures from `dax_measures.txt`
3. Add each measure using "New Measure" button

### Step 4: Dashboard Pages Structure

#### Page 1: Executive Dashboard
- Total Revenue KPI Card
- Total Trips KPI Card
- Average Revenue per Ride KPI Card
- Revenue Trend Line Chart
- Vehicle Type Revenue Donut Chart
- Top Routes by Revenue Table

#### Page 2: Time & Demand Analysis
- Hourly Demand Pattern Line Chart
- Rush Hour vs Regular Hours Column Chart
- Weekend vs Weekday Performance
- Monthly Revenue Trend
- Day of Week Revenue Heatmap

#### Page 3: Weather Impact Analysis
- Weather Condition Impact Bar Chart
- Rain vs Clear Weather Comparison
- Weather-based Surge Multiplier
- Seasonal Weather Patterns
- Temperature vs Revenue Scatter Plot

### Step 5: Add Filters and Slicers
- Date Range Slicer
- Vehicle Type Slicer
- Weather Condition Slicer
- Location Slicer

### Step 6: Format and Style
- Apply consistent color scheme
- Add title and logo
- Format numbers with Indian currency (₹)
- Enable drill-through capabilities

### Recommended Visuals:
- KPI Cards for key metrics
- Line charts for trends
- Bar charts for comparisons
- Heat maps for patterns
- Scatter plots for correlations
- Tables for detailed data

### Performance Tips:
- Use DirectQuery only if needed
- Optimize DAX measures
- Limit high-cardinality filters
- Use aggregated data where possible
        """
        
        guide_file = os.path.join(self.output_dir, "../templates/power_bi_setup_guide.md")
        os.makedirs(os.path.dirname(guide_file), exist_ok=True)
        
        with open(guide_file, 'w') as f:
            f.write(setup_guide)
        
        print(f"✅ Power BI setup guide saved to: {guide_file}")
        return setup_guide
    
    def run_full_preparation(self):
        """Execute the complete data preparation pipeline"""
        print("🚀 Starting Power BI Data Preparation Pipeline...")
        print("=" * 60)
        
        # Load source data
        self.load_and_prepare_source_data()
        
        # Create fact table
        self.create_fact_table()
        
        # Create all dimension tables
        self.create_time_dimension()
        self.create_hour_dimension()
        self.create_location_dimension()
        self.create_weather_dimension()
        self.create_vehicle_dimension()
        
        # Create DAX measures
        self.create_dax_measures()
        
        # Export to Excel
        excel_file = self.export_to_excel()
        
        # Create documentation
        self.create_data_model_documentation()
        
        # Generate setup guide
        self.generate_power_bi_setup_guide()
        
        print("=" * 60)
        print("✅ Power BI Data Preparation Complete!")
        print(f"📊 Fact Table: {len(self.fact_table):,} rides")
        print(f"📋 Dimension Tables: {len(self.dimension_tables)}")
        print(f"📤 Excel File: {excel_file}")
        print("🔄 Ready for Power BI Dashboard Creation!")
        
        return {
            'fact_table': self.fact_table,
            'dimension_tables': self.dimension_tables,
            'excel_file': excel_file,
            'output_directory': self.output_dir
        }

def main():
    """Main execution function"""
    print("🚀 Power BI Data Model Preparation")
    print("=" * 50)
    
    # Initialize data preparation
    prep = PowerBIDataPreparation("../Dataset.csv")
    
    # Run full preparation pipeline
    results = prep.run_full_preparation()
    
    return prep, results

if __name__ == "__main__":
    prep, results = main()
