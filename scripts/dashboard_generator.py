"""
Power BI Dashboard Generator for Rapido Transportation Analytics
Creates a comprehensive 3-page dashboard with professional visualizations
"""

import pandas as pd
import json
from datetime import datetime
import os

def create_power_bi_template():
    """
    Create Power BI template structure and configuration
    """
    
    print("🎨 Creating Power BI Dashboard Template...")
    
    # Dashboard configuration
    dashboard_config = {
        "dashboard_name": "Rapido Transportation Analytics Dashboard",
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        "version": "1.0",
        "pages": [
            {
                "page_name": "Executive Dashboard",
                "page_order": 1,
                "description": "High-level KPIs, revenue trends, and business overview",
                "visuals": [
                    {
                        "type": "KPI Card",
                        "title": "Total Revenue",
                        "measure": "Total Revenue",
                        "format": "₹ #,##0",
                        "position": {"x": 0, "y": 0, "width": 200, "height": 100}
                    },
                    {
                        "type": "KPI Card", 
                        "title": "Total Trips",
                        "measure": "Total Trips",
                        "format": "#,##0",
                        "position": {"x": 220, "y": 0, "width": 200, "height": 100}
                    },
                    {
                        "type": "KPI Card",
                        "title": "Average Revenue/Ride", 
                        "measure": "Average Revenue Per Ride",
                        "format": "₹ #,##0.00",
                        "position": {"x": 440, "y": 0, "width": 200, "height": 100}
                    },
                    {
                        "type": "KPI Card",
                        "title": "Surge Contribution %",
                        "measure": "Surge Percentage", 
                        "format": "0.0%",
                        "position": {"x": 660, "y": 0, "width": 200, "height": 100}
                    },
                    {
                        "type": "Line Chart",
                        "title": "Revenue Trend by Month",
                        "x_axis": "DimTime[month_name]",
                        "y_axis": "Total Revenue",
                        "position": {"x": 0, "y": 120, "width": 400, "height": 250}
                    },
                    {
                        "type": "Donut Chart", 
                        "title": "Revenue by Vehicle Type",
                        "legend": "DimVehicle[vehicle_type]",
                        "values": ["Bike Revenue", "Auto Revenue", "Cab Revenue"],
                        "position": {"x": 420, "y": 120, "width": 300, "height": 250}
                    },
                    {
                        "type": "Horizontal Bar Chart",
                        "title": "Top 10 Routes by Revenue", 
                        "y_axis": "FactRides[route]",
                        "x_axis": "Total Revenue",
                        "position": {"x": 740, "y": 120, "width": 400, "height": 250}
                    },
                    {
                        "type": "Table",
                        "title": "Vehicle Performance Summary",
                        "columns": [
                            "DimVehicle[vehicle_type]",
                            "Total Trips", 
                            "Total Revenue",
                            "Average Revenue Per Ride"
                        ],
                        "position": {"x": 0, "y": 390, "width": 500, "height": 200}
                    }
                ]
            },
            {
                "page_name": "Time & Demand Analysis",
                "page_order": 2, 
                "description": "Rush hour patterns, time-based demand, and scheduling insights",
                "visuals": [
                    {
                        "type": "Line Chart",
                        "title": "Hourly Demand Pattern (24 Hours)",
                        "x_axis": "DimHour[hour]",
                        "y_axis": "Total Trips",
                        "secondary_y": "Average Surge Multiplier",
                        "position": {"x": 0, "y": 0, "width": 600, "height": 250}
                    },
                    {
                        "type": "Column Chart",
                        "title": "Rush Hour vs Regular Hours",
                        "x_axis": "DimHour[is_rush_hour]", 
                        "y_axis": ["Rush Hour Revenue", "Total Revenue"],
                        "position": {"x": 620, "y": 0, "width": 400, "height": 250}
                    },
                    {
                        "type": "Stacked Bar Chart",
                        "title": "Day of Week Performance",
                        "x_axis": "DimTime[day_name]",
                        "y_axis": "Total Revenue",
                        "legend": "DimVehicle[vehicle_type]",
                        "position": {"x": 0, "y": 270, "width": 500, "height": 250}
                    },
                    {
                        "type": "Area Chart",
                        "title": "Weekend vs Weekday Revenue",
                        "x_axis": "DimTime[date]",
                        "y_axis": ["Weekend Revenue", "Weekday Revenue"],
                        "position": {"x": 520, "y": 270, "width": 500, "height": 250}
                    },
                    {
                        "type": "Heat Map",
                        "title": "Hour vs Day of Week Revenue Matrix",
                        "x_axis": "DimHour[hour]",
                        "y_axis": "DimTime[day_name]", 
                        "values": "Total Revenue",
                        "position": {"x": 0, "y": 540, "width": 600, "height": 200}
                    },
                    {
                        "type": "KPI Cards Row",
                        "cards": [
                            {"title": "Morning Rush Revenue", "measure": "Rush Hour Revenue (8-9 AM)"},
                            {"title": "Evening Rush Revenue", "measure": "Rush Hour Revenue (5:30-6:30 PM)"}, 
                            {"title": "Peak Hour", "measure": "Highest Traffic Hour"}
                        ],
                        "position": {"x": 620, "y": 540, "width": 400, "height": 200}
                    }
                ]
            },
            {
                "page_name": "Weather Impact Analysis", 
                "page_order": 3,
                "description": "Weather-based surge analysis, rain impact, and seasonal patterns",
                "visuals": [
                    {
                        "type": "Column Chart",
                        "title": "Weather Conditions Impact on Revenue",
                        "x_axis": "DimWeather[weather_condition]",
                        "y_axis": "Total Revenue",
                        "secondary_y": "Average Surge Multiplier",
                        "position": {"x": 0, "y": 0, "width": 500, "height": 250}
                    },
                    {
                        "type": "Gauge Chart",
                        "title": "Rain Premium vs Clear Weather",
                        "measure": "Weather Premium",
                        "min_value": 0,
                        "max_value": 1,
                        "target": 0.38,
                        "position": {"x": 520, "y": 0, "width": 250, "height": 250}
                    },
                    {
                        "type": "Clustered Bar Chart",
                        "title": "Rain vs Clear Weather Comparison",
                        "categories": ["Total Trips", "Average Price", "Average Surge"],
                        "series": ["Rain Revenue", "Clear Revenue"],
                        "position": {"x": 790, "y": 0, "width": 350, "height": 250}
                    },
                    {
                        "type": "Scatter Plot",
                        "title": "Temperature vs Revenue Correlation",
                        "x_axis": "FactRides[temperature]",
                        "y_axis": "FactRides[final_price]", 
                        "size": "FactRides[surge_multiplier]",
                        "position": {"x": 0, "y": 270, "width": 400, "height": 250}
                    },
                    {
                        "type": "Line Chart",
                        "title": "Monthly Weather Impact Trends",
                        "x_axis": "DimTime[month_name]",
                        "y_axis": "Total Revenue",
                        "legend": "DimWeather[weather_condition]",
                        "position": {"x": 420, "y": 270, "width": 500, "height": 250}
                    },
                    {
                        "type": "Waterfall Chart", 
                        "title": "Revenue Impact by Weather Conditions",
                        "categories": ["Clear", "Clouds", "Haze", "Rain", "Thunderstorm"],
                        "values": "Weather Revenue Impact",
                        "position": {"x": 940, "y": 270, "width": 300, "height": 250}
                    },
                    {
                        "type": "Table",
                        "title": "Weather Impact Summary",
                        "columns": [
                            "DimWeather[weather_condition]",
                            "Total Trips",
                            "Total Revenue", 
                            "Average Surge Multiplier",
                            "Weather Premium %"
                        ],
                        "position": {"x": 0, "y": 540, "width": 700, "height": 200}
                    },
                    {
                        "type": "Card Visual",
                        "title": "Extreme Weather Revenue",
                        "measure": "Storm Revenue Boost",
                        "description": "Revenue from Thunderstorm conditions",
                        "position": {"x": 720, "y": 540, "width": 200, "height": 100}
                    }
                ]
            }
        ],
        "filters": [
            {
                "type": "Date Range Slicer",
                "field": "DimTime[date]",
                "position": "top"
            },
            {
                "type": "Dropdown Slicer", 
                "field": "DimVehicle[vehicle_type]",
                "position": "top"
            },
            {
                "type": "Multi-select Slicer",
                "field": "DimWeather[weather_condition]", 
                "position": "top"
            }
        ],
        "theme": {
            "primary_color": "#1f77b4",
            "secondary_color": "#ff7f0e", 
            "accent_color": "#2ca02c",
            "background_color": "#ffffff",
            "text_color": "#333333",
            "font_family": "Segoe UI"
        }
    }
    
    # Save dashboard configuration
    os.makedirs("../power_bi/templates", exist_ok=True)
    config_file = "../power_bi/templates/dashboard_config.json"
    
    with open(config_file, 'w') as f:
        json.dump(dashboard_config, f, indent=2)
    
    print(f"✅ Dashboard template saved: {config_file}")
    return dashboard_config

def create_power_bi_project_file():
    """
    Create Power BI project file with data model relationships
    """
    
    print("📊 Creating Power BI Project Structure...")
    
    # Power BI project structure
    pbi_project = {
        "name": "Rapido Transportation Analytics",
        "version": "1.0.0",
        "dataModel": {
            "tables": [
                {
                    "name": "FactRides",
                    "type": "fact",
                    "source": "rapido_dashboard_data.xlsx",
                    "sheet": "FactRides",
                    "key_columns": ["ride_id"],
                    "measures": [
                        "distance_km", "base_price", "final_price", 
                        "surge_multiplier", "waiting_time_minutes",
                        "price_premium_percent", "surge_amount", "price_per_km"
                    ]
                },
                {
                    "name": "DimTime", 
                    "type": "dimension",
                    "source": "rapido_dashboard_data.xlsx",
                    "sheet": "DimTime",
                    "key_columns": ["date"],
                    "attributes": [
                        "year", "month", "quarter", "month_name", 
                        "day_name", "is_weekend"
                    ]
                },
                {
                    "name": "DimHour",
                    "type": "dimension", 
                    "source": "rapido_dashboard_data.xlsx",
                    "sheet": "DimHour",
                    "key_columns": ["hour"],
                    "attributes": ["time_period", "is_rush_hour"]
                },
                {
                    "name": "DimVehicle",
                    "type": "dimension",
                    "source": "rapido_dashboard_data.xlsx", 
                    "sheet": "DimVehicle",
                    "key_columns": ["vehicle_type"],
                    "attributes": ["capacity", "category"]
                },
                {
                    "name": "DimWeather",
                    "type": "dimension",
                    "source": "rapido_dashboard_data.xlsx",
                    "sheet": "DimWeather", 
                    "key_columns": ["weather_condition"],
                    "attributes": ["weather_main", "weather_description", "impact_level"]
                }
            ],
            "relationships": [
                {
                    "from_table": "FactRides",
                    "from_column": "date", 
                    "to_table": "DimTime",
                    "to_column": "date",
                    "cardinality": "many_to_one",
                    "cross_filter": "single"
                },
                {
                    "from_table": "FactRides", 
                    "from_column": "hour",
                    "to_table": "DimHour",
                    "to_column": "hour",
                    "cardinality": "many_to_one",
                    "cross_filter": "single"
                },
                {
                    "from_table": "FactRides",
                    "from_column": "vehicle_type",
                    "to_table": "DimVehicle", 
                    "to_column": "vehicle_type",
                    "cardinality": "many_to_one",
                    "cross_filter": "single"
                },
                {
                    "from_table": "FactRides",
                    "from_column": "weather_condition",
                    "to_table": "DimWeather",
                    "to_column": "weather_condition", 
                    "cardinality": "many_to_one",
                    "cross_filter": "single"
                }
            ]
        }
    }
    
    # Save project file
    project_file = "../power_bi/rapido_transportation.pbip"
    with open(project_file, 'w') as f:
        json.dump(pbi_project, f, indent=2)
    
    print(f"✅ Power BI project file created: {project_file}")
    return pbi_project

def create_advanced_dax_measures():
    """
    Create advanced DAX measures for the dashboard
    """
    
    print("📐 Creating Advanced DAX Measures...")
    
    advanced_measures = """
# Advanced DAX Measures for Rapido Transportation Dashboard
# Copy these measures into Power BI Desktop

## Core Revenue Measures
Total Revenue = SUM(FactRides[final_price])
Total Base Revenue = SUM(FactRides[base_price])
Surge Revenue = [Total Revenue] - [Total Base Revenue]
Average Revenue Per Ride = AVERAGE(FactRides[final_price])
Revenue Per KM = DIVIDE([Total Revenue], SUM(FactRides[distance_km]))

## Trip Volume Measures  
Total Trips = COUNTROWS(FactRides)
Average Distance = AVERAGE(FactRides[distance_km])
Total Distance = SUM(FactRides[distance_km])

## Surge Analysis Measures
Average Surge Multiplier = AVERAGE(FactRides[surge_multiplier])
Surge Percentage = DIVIDE([Surge Revenue], [Total Revenue]) * 100
Trips with Surge = CALCULATE([Total Trips], FactRides[surge_multiplier] > 1.2)
Surge Trip Percentage = DIVIDE([Trips with Surge], [Total Trips]) * 100

## Time Intelligence Measures
Revenue MTD = TOTALMTD([Total Revenue], DimTime[date])
Revenue QTD = TOTALQTD([Total Revenue], DimTime[date])
Revenue YTD = TOTALYTD([Total Revenue], DimTime[date])

Revenue Previous Month = 
CALCULATE(
    [Total Revenue],
    PREVIOUSMONTH(DimTime[date])
)

Revenue Growth MoM = 
VAR CurrentMonth = [Total Revenue]
VAR PreviousMonth = [Revenue Previous Month]
RETURN 
IF(
    NOT ISBLANK(PreviousMonth),
    DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth) * 100,
    BLANK()
)

## Weather Impact Measures
Rain Revenue = 
CALCULATE(
    [Total Revenue],
    DimWeather[weather_condition] = "Rain"
)

Clear Revenue = 
CALCULATE(
    [Total Revenue], 
    DimWeather[weather_condition] = "Clear"
)

Weather Premium = 
VAR RainAvg = CALCULATE(AVERAGE(FactRides[final_price]), DimWeather[weather_condition] = "Rain")
VAR ClearAvg = CALCULATE(AVERAGE(FactRides[final_price]), DimWeather[weather_condition] = "Clear")
RETURN DIVIDE(RainAvg, ClearAvg) - 1

Thunderstorm Revenue = 
CALCULATE(
    [Total Revenue],
    DimWeather[weather_condition] = "Thunderstorm"  
)

Storm Revenue Boost = 
VAR StormAvgPrice = CALCULATE(AVERAGE(FactRides[final_price]), DimWeather[weather_condition] = "Thunderstorm")
VAR OverallAvgPrice = AVERAGE(FactRides[final_price])
RETURN DIVIDE(StormAvgPrice, OverallAvgPrice) - 1

## Rush Hour Analysis
Rush Hour Revenue = 
CALCULATE(
    [Total Revenue],
    DimHour[is_rush_hour] = TRUE
)

Rush Hour Trips = 
CALCULATE(
    [Total Trips], 
    DimHour[is_rush_hour] = TRUE
)

Morning Rush Revenue = 
CALCULATE(
    [Total Revenue],
    DimHour[hour] IN {8, 9}
)

Evening Rush Revenue = 
CALCULATE(
    [Total Revenue],
    DimHour[hour] IN {17, 18}
)

Peak Hour Indicator = 
VAR CurrentHour = SELECTEDVALUE(DimHour[hour])
VAR HourTrips = CALCULATE([Total Trips], DimHour[hour] = CurrentHour)
VAR MaxTrips = MAXX(ALL(DimHour), CALCULATE([Total Trips], DimHour[hour] = EARLIER(DimHour[hour])))
RETURN 
IF(
    HourTrips = MaxTrips,
    "🔥 Peak Hour",
    IF(
        SELECTEDVALUE(DimHour[is_rush_hour]),
        "⚡ Rush Hour", 
        "📊 Regular Hour"
    )
)

## Vehicle Performance Measures
Bike Revenue = 
CALCULATE(
    [Total Revenue],
    DimVehicle[vehicle_type] = "bike"
)

Auto Revenue = 
CALCULATE(
    [Total Revenue],
    DimVehicle[vehicle_type] = "auto" 
)

Cab Revenue = 
CALCULATE(
    [Total Revenue],
    DimVehicle[vehicle_type] = "cab"
)

Vehicle Revenue Share = 
VAR SelectedVehicleRevenue = 
CALCULATE(
    [Total Revenue],
    VALUES(DimVehicle[vehicle_type])
)
RETURN DIVIDE(SelectedVehicleRevenue, [Total Revenue]) * 100

## Service Quality Measures
Average Wait Time = AVERAGE(FactRides[waiting_time_minutes])

Service Quality Score = 
VAR AvgWait = [Average Wait Time]
RETURN 
SWITCH(
    TRUE(),
    AvgWait <= 2, 100,
    AvgWait <= 3, 90,
    AvgWait <= 4, 80, 
    AvgWait <= 5, 70,
    AvgWait <= 7, 60,
    50
)

Trips Under 5 Min Wait = 
CALCULATE(
    [Total Trips],
    FactRides[waiting_time_minutes] <= 5
)

Service Quality Percentage = 
DIVIDE([Trips Under 5 Min Wait], [Total Trips]) * 100

## VIT University Analysis
VIT Revenue = 
CALCULATE(
    [Total Revenue],
    OR(
        CONTAINSSTRING(FactRides[from_location], "VIT"),
        CONTAINSSTRING(FactRides[to_location], "VIT")
    )
)

VIT Trips = 
CALCULATE(
    [Total Trips],
    OR(
        CONTAINSSTRING(FactRides[from_location], "VIT"),
        CONTAINSSTRING(FactRides[to_location], "VIT")
    )
)

VIT Revenue Share = DIVIDE([VIT Revenue], [Total Revenue]) * 100

Non-VIT Revenue = [Total Revenue] - [VIT Revenue]

VIT vs Non-VIT Ratio = DIVIDE([VIT Revenue], [Non-VIT Revenue])

## Weekend Analysis
Weekend Revenue = 
CALCULATE(
    [Total Revenue],
    DimTime[is_weekend] = TRUE
)

Weekday Revenue = 
CALCULATE(
    [Total Revenue],
    DimTime[is_weekend] = FALSE  
)

Weekend vs Weekday Premium = 
VAR WeekendAvg = DIVIDE([Weekend Revenue], CALCULATE([Total Trips], DimTime[is_weekend] = TRUE))
VAR WeekdayAvg = DIVIDE([Weekday Revenue], CALCULATE([Total Trips], DimTime[is_weekend] = FALSE))
RETURN DIVIDE(WeekendAvg, WeekdayAvg) - 1

## Dynamic Text Measures
Revenue Trend Indicator = 
VAR CurrentRevenue = [Total Revenue]
VAR PreviousRevenue = [Revenue Previous Month]
RETURN 
SWITCH(
    TRUE(),
    ISBLANK(PreviousRevenue), "📊 New Period",
    CurrentRevenue > PreviousRevenue * 1.1, "📈 Strong Growth",
    CurrentRevenue > PreviousRevenue * 1.05, "↗️ Growing", 
    CurrentRevenue > PreviousRevenue * 0.95, "➡️ Stable",
    CurrentRevenue > PreviousRevenue * 0.9, "↘️ Declining",
    "📉 Significant Decline"
)

Weather Impact Summary = 
VAR SelectedWeather = SELECTEDVALUE(DimWeather[weather_condition])
VAR WeatherSurge = CALCULATE(AVERAGE(FactRides[surge_multiplier]), DimWeather[weather_condition] = SelectedWeather)
RETURN 
SelectedWeather & " - " & FORMAT(WeatherSurge, "0.00") & "x surge"

## Ranking Measures  
Route Revenue Rank = 
RANKX(
    ALL(FactRides[route]),
    CALCULATE([Total Revenue], VALUES(FactRides[route])),
    , DESC
)

Hour Revenue Rank = 
RANKX(
    ALL(DimHour[hour]),
    CALCULATE([Total Revenue], VALUES(DimHour[hour])),
    , DESC
)

## Color Coding Measures
Surge Level Color = 
VAR SurgeValue = AVERAGE(FactRides[surge_multiplier])
RETURN 
SWITCH(
    TRUE(),
    SurgeValue >= 2, "#FF0000",      // Red for high surge
    SurgeValue >= 1.5, "#FF8C00",   // Orange for medium surge  
    SurgeValue >= 1.2, "#FFD700",   // Yellow for low surge
    "#00FF00"                       // Green for normal pricing
)

Revenue Performance Color = 
VAR Growth = [Revenue Growth MoM]
RETURN 
SWITCH(
    TRUE(),
    Growth > 10, "#00AA00",     // Dark green for strong growth
    Growth > 5, "#90EE90",      // Light green for good growth
    Growth > -5, "#FFFF00",     // Yellow for stable
    Growth > -10, "#FFA500",    // Orange for decline
    "#FF0000"                   // Red for significant decline
)
"""
    
    # Save advanced measures
    measures_file = "../power_bi/measures/advanced_dax_measures.txt"
    with open(measures_file, 'w') as f:
        f.write(advanced_measures)
    
    print(f"✅ Advanced DAX measures saved: {measures_file}")
    return advanced_measures

def create_dashboard_documentation():
    """
    Create comprehensive dashboard documentation
    """
    
    print("📚 Creating Dashboard Documentation...")
    
    documentation = """
# Rapido Transportation Analytics Dashboard
## Complete Power BI Implementation Guide

### Dashboard Overview
This dashboard provides comprehensive analytics for Rapido transportation operations in Vellore, covering:
- Executive KPIs and business performance
- Time-based demand patterns and rush hour analysis  
- Weather impact on pricing and demand
- Vehicle performance and route optimization

### Data Model Structure

#### Fact Table: FactRides
- **Primary Key**: ride_id
- **Measures**: 88,938 rides with financial and operational metrics
- **Date Range**: January 1, 2024 - December 31, 2024
- **Key Metrics**: Revenue, distance, surge pricing, wait times

#### Dimension Tables:
1. **DimTime**: Date hierarchy with business calendar
2. **DimHour**: 24-hour analysis with rush hour classification
3. **DimVehicle**: Vehicle types with characteristics
4. **DimWeather**: Weather conditions with impact levels

### Page 1: Executive Dashboard

#### Key Performance Indicators
- **Total Revenue**: ₹13,170,756.08
- **Total Trips**: 88,938 rides
- **Average Revenue per Ride**: ₹148.09  
- **Surge Contribution**: 35.6% of total revenue

#### Main Visualizations
1. **Revenue Trend Line Chart**: Monthly revenue progression
2. **Vehicle Revenue Donut Chart**: Distribution by bike/auto/cab
3. **Top Routes Bar Chart**: Highest revenue generating routes
4. **Performance Summary Table**: Vehicle type comparison

#### Business Insights
- Auto rickshaws lead revenue share (40.0%)
- VIT University routes dominate (59.9% of revenue)
- Surge pricing highly effective (35.6% contribution)

### Page 2: Time & Demand Analysis

#### Rush Hour Performance
- **Morning Rush (8-9 AM)**: 11,712 trips, ₹1,946,854 revenue
- **Evening Rush (5:30-6:30 PM)**: 12,444 trips, ₹1,870,512 revenue
- **Peak Hour**: 6:00 PM with 6,954 trips

#### Visualizations
1. **24-Hour Demand Pattern**: Line chart showing hourly trip volume
2. **Rush vs Regular Hours**: Column chart comparison
3. **Day of Week Heatmap**: Revenue by day and hour
4. **Weekend vs Weekday**: Performance comparison

#### Time Optimization Insights
- Evening peak generates highest revenue density
- Rush hour premium averages 9.5% higher pricing
- Weekend patterns differ significantly from weekday

### Page 3: Weather Impact Analysis

#### Weather Revenue Impact
- **Clear Weather**: 35,833 trips, 1.37x average surge
- **Rain Conditions**: 17,802 trips, 1.90x average surge  
- **Thunderstorms**: 4,451 trips, 2.28x average surge
- **Rain Premium**: 38% higher pricing than clear weather

#### Key Visualizations
1. **Weather Conditions Bar Chart**: Revenue and surge by weather
2. **Rain vs Clear Comparison**: Side-by-side performance
3. **Temperature Correlation**: Scatter plot analysis
4. **Seasonal Weather Trends**: Monthly weather impact

#### Weather Strategy Insights
- Rain events create significant revenue opportunities
- Thunderstorms generate highest surge multipliers
- Weather forecasting can optimize fleet positioning

### Implementation Steps

#### Step 1: Data Import
1. Open Power BI Desktop
2. Import `rapido_dashboard_data.xlsx`
3. Load all 5 sheets (FactRides + 4 dimension tables)

#### Step 2: Create Relationships
- FactRides[date] → DimTime[date]
- FactRides[hour] → DimHour[hour]  
- FactRides[vehicle_type] → DimVehicle[vehicle_type]
- FactRides[weather_condition] → DimWeather[weather_condition]

#### Step 3: Add DAX Measures
Copy and paste measures from `advanced_dax_measures.txt`

#### Step 4: Build Visualizations
Follow the visual specifications for each page

#### Step 5: Apply Formatting
- Use corporate color scheme
- Add consistent fonts and spacing
- Enable drill-through capabilities

### Filter Configuration

#### Global Filters (All Pages)
- **Date Range Slicer**: DimTime[date]
- **Vehicle Type**: DimVehicle[vehicle_type]
- **Weather Condition**: DimWeather[weather_condition]

#### Page-Specific Filters
- **Page 2**: Hour range slider
- **Page 3**: Temperature range, precipitation level

### Performance Optimization

#### Data Model Tips
- Use DirectQuery only if needed
- Minimize high-cardinality columns in visuals
- Pre-aggregate measures where possible
- Use CALCULATE efficiently in DAX

#### Visual Performance  
- Limit table rows to top N results
- Use summary tables for detailed data
- Optimize slicers to affect only relevant visuals

### Color Scheme and Branding

#### Primary Colors
- **Primary Blue**: #1f77b4 (headers, primary data)
- **Secondary Orange**: #ff7f0e (highlights, secondary data)  
- **Success Green**: #2ca02c (positive indicators)
- **Warning Red**: #d62728 (alerts, negative indicators)

#### Conditional Formatting
- Revenue growth: Green (positive) to Red (negative)
- Surge levels: Green (normal) to Red (high surge)
- Service quality: Green (good) to Red (poor)

### Business Recommendations

#### Immediate Actions (1-30 days)
1. Optimize fleet positioning during 6-7 PM peak
2. Increase auto rickshaw availability (highest margins)
3. Develop weather-based surge algorithms

#### Short Term (1-3 months)  
1. Diversify beyond VIT University routes
2. Implement predictive pricing for weather events
3. Launch targeted promotions for off-peak hours

#### Long Term (3-12 months)
1. Expand to other educational institutions
2. Develop subscription services for regular commuters
3. Integrate with weather forecasting APIs

### Dashboard Maintenance

#### Daily Monitoring
- Check revenue KPIs vs targets
- Monitor service quality metrics
- Review surge pricing effectiveness

#### Weekly Analysis
- Analyze route performance trends
- Review vehicle utilization rates  
- Assess weather impact patterns

#### Monthly Reviews
- Update business forecasts
- Review strategic KPIs
- Plan operational adjustments

### Troubleshooting

#### Common Issues
1. **Slow Performance**: Check relationship directions, optimize DAX
2. **Incorrect Totals**: Verify measure context and filters
3. **Missing Data**: Check data refresh and source connections

#### Data Quality Checks
- Verify date ranges are complete
- Check for duplicate ride IDs
- Validate surge multiplier ranges (1.0 - 3.0)
- Confirm revenue calculations match source

---

**Dashboard Version**: 1.0  
**Last Updated**: August 29, 2025  
**Data Coverage**: January 1, 2024 - December 31, 2024  
**Total Records**: 88,938 rides
"""
    
    # Save documentation
    doc_file = "../power_bi/templates/dashboard_documentation.md"
    with open(doc_file, 'w') as f:
        f.write(documentation)
    
    print(f"✅ Dashboard documentation saved: {doc_file}")
    return documentation

def main():
    """
    Execute Phase 4: Complete Power BI Dashboard Creation
    """
    
    print("🚀 PHASE 4: POWER BI DASHBOARD CREATION")
    print("=" * 55)
    
    # Create dashboard template
    dashboard_config = create_power_bi_template()
    
    # Create Power BI project structure
    pbi_project = create_power_bi_project_file()
    
    # Create advanced DAX measures
    advanced_measures = create_advanced_dax_measures()
    
    # Create comprehensive documentation
    documentation = create_dashboard_documentation()
    
    print("\n" + "=" * 55)
    print("✅ PHASE 4 COMPLETE: POWER BI DASHBOARD READY!")
    print("=" * 55)
    
    print("\n📊 DELIVERABLES CREATED:")
    print("✅ Dashboard template with 3-page structure")
    print("✅ Advanced DAX measures (50+ calculations)")  
    print("✅ Complete implementation documentation")
    print("✅ Power BI project configuration")
    
    print("\n🎯 DASHBOARD FEATURES:")
    print("📈 Executive Dashboard: KPIs, trends, vehicle performance")
    print("⏰ Time Analysis: Rush hours, demand patterns, scheduling")
    print("🌦️ Weather Impact: Surge optimization, rain premium analysis")
    
    print("\n🔧 IMPLEMENTATION READY:")
    print("📂 rapido_dashboard_data.xlsx - Import into Power BI")
    print("📐 advanced_dax_measures.txt - Copy/paste measures")
    print("📋 dashboard_documentation.md - Complete guide")
    
    print("\n💡 KEY INSIGHTS HIGHLIGHTED:")
    print("• VIT University dependency (59.9% revenue)")
    print("• Surge pricing effectiveness (35.6% contribution)")  
    print("• Rain revenue premium (38% higher than clear)")
    print("• Evening peak optimization (6 PM highest demand)")
    print("• Auto rickshaw focus (40% revenue share)")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Open Power BI Desktop")
    print("2. Import rapido_dashboard_data.xlsx")
    print("3. Copy DAX measures from advanced_dax_measures.txt")
    print("4. Follow dashboard_documentation.md guide")
    print("5. Apply branding and final styling")
    
    return {
        'dashboard_config': dashboard_config,
        'pbi_project': pbi_project,
        'documentation': documentation,
        'status': 'ready_for_implementation'
    }

if __name__ == "__main__":
    results = main()
