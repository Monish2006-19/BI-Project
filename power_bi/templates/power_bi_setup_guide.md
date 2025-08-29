# Power BI Dashboard Setup Guide

## Rapido Transportation Analytics

### 📁 Files Created for Power BI

- `rapido_dashboard_data.xlsx` - Main dataset with fact and dimension tables
- `dax_measures.txt` - Pre-built DAX measures for copy-paste
- This setup guide

### 🎯 Dashboard Structure (3 Pages)

#### Page 1: Executive Dashboard

**Key Visuals:**

- Total Revenue KPI Card (₹13.17M)
- Total Trips KPI Card (88,938)
- Surge Contribution KPI Card (35.6%)
- Revenue by Vehicle Type Donut Chart
- Monthly Revenue Trend Line Chart
- Top 5 Routes by Revenue Table

#### Page 2: Time & Demand Analysis

**Key Visuals:**

- Hourly Demand Pattern Line Chart
- Rush Hour vs Regular Hours Comparison
- Weekend vs Weekday Revenue
- Day of Week Heatmap
- Time Period Revenue Distribution

#### Page 3: Weather Impact Analysis

**Key Visuals:**

- Weather Condition Revenue Bar Chart
- Rain vs Clear Weather Comparison
- Weather Surge Multiplier Chart
- Seasonal Weather Patterns
- Temperature vs Revenue Scatter Plot

### 🔧 Step-by-Step Setup

#### Step 1: Import Data

1. Open Power BI Desktop
2. Click **"Get Data"** > **"Excel"**
3. Browse to: `power_bi/data_model/rapido_dashboard_data.xlsx`
4. Select **ALL** worksheets:
   - FactRides (main transaction data)
   - DimTime (date dimensions)
   - DimHour (hour classifications)
   - DimVehicle (vehicle types)
   - DimWeather (weather conditions)
5. Click **"Load"**

#### Step 2: Create Relationships

Go to **Model View** and create these relationships:

**Required Relationships:**

- `FactRides[date]` → `DimTime[date]` (Many-to-One)
- `FactRides[hour]` → `DimHour[hour]` (Many-to-One)
- `FactRides[vehicle_type]` → `DimVehicle[vehicle_type]` (Many-to-One)
- `FactRides[weather_condition]` → `DimWeather[weather_condition]` (Many-to-One)

**How to Create:**

1. Drag from FactRides field to corresponding Dimension field
2. Ensure relationship direction is Many-to-One
3. Set cross-filter direction to "Single" (default)

#### Step 3: Add DAX Measures

1. Create a new table called **"Measures"**
2. Open `dax_measures.txt` file
3. Copy each measure formula:

**Essential Measures:**

```dax
Total Revenue = SUM(FactRides[final_price])
Total Trips = COUNTROWS(FactRides)
Surge Revenue = SUM(FactRides[surge_amount])
Rush Hour Revenue = CALCULATE([Total Revenue], DimHour[is_rush_hour] = TRUE)
Rain Revenue = CALCULATE([Total Revenue], DimWeather[weather_condition] = "Rain")
```

### 📊 Recommended Visuals by Page

#### Executive Dashboard Visuals:

1. **KPI Cards** (Top Row):

   - Total Revenue: `[Total Revenue]`
   - Total Trips: `[Total Trips]`
   - Avg Revenue/Ride: `[Average Revenue Per Ride]`
   - Surge %: `[Surge Percentage]`

2. **Revenue Trend** (Line Chart):

   - Axis: `DimTime[month_name]`
   - Values: `[Total Revenue]`

3. **Vehicle Revenue** (Donut):

   - Legend: `DimVehicle[vehicle_type]`
   - Values: `[Total Revenue]`

4. **Top Routes** (Table):
   - Columns: `FactRides[route]`, `[Total Revenue]`, `[Total Trips]`

#### Time Analysis Visuals:

1. **Hourly Pattern** (Line Chart):

   - Axis: `DimHour[hour]`
   - Values: `[Total Revenue]`, `[Total Trips]`

2. **Rush Hour Comparison** (Column Chart):

   - Axis: `DimHour[time_period]`
   - Values: `[Total Revenue]`

3. **Day of Week** (Matrix/Heatmap):
   - Rows: `DimTime[day_name]`
   - Values: `[Total Revenue]` (with conditional formatting)

#### Weather Analysis Visuals:

1. **Weather Revenue** (Bar Chart):

   - Axis: `DimWeather[weather_condition]`
   - Values: `[Total Revenue]`

2. **Surge by Weather** (Column Chart):

   - Axis: `DimWeather[weather_condition]`
   - Values: `[Average Surge Multiplier]`

3. **Rain Premium** (Card):
   - Value: `[Weather Premium]`

### 🎨 Formatting Tips

#### Color Scheme:

- **Primary**: #1f4e79 (Dark Blue)
- **Secondary**: #70ad47 (Green)
- **Accent**: #ffc000 (Orange)
- **Warning**: #c5504b (Red)

#### Number Formatting:

- Revenue: ₹ #,##0 (Indian Rupees)
- Percentages: 0.0%
- Multipliers: 0.00"x"

#### Visual Enhancements:

- Enable data labels on charts
- Add trend lines where appropriate
- Use conditional formatting for KPIs
- Set up drill-through for detailed analysis

### 🔍 Interactive Features

#### Slicers to Add:

1. **Date Range Slicer**: `DimTime[date]`
2. **Vehicle Type**: `DimVehicle[vehicle_type]`
3. **Weather Condition**: `DimWeather[weather_condition]`
4. **Time Period**: `DimHour[time_period]`

#### Drill-Through Pages:

Create a detailed route analysis page with drill-through from route visuals

### 📈 Advanced Analytics

#### Time Intelligence:

```dax
Revenue Growth MoM =
VAR CurrentMonth = [Total Revenue]
VAR PreviousMonth = CALCULATE([Total Revenue], PREVIOUSMONTH(DimTime[date]))
RETURN DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth) * 100
```

#### Weather Impact:

```dax
Weather Impact Score =
SWITCH(
    TRUE(),
    SELECTEDVALUE(DimWeather[weather_condition]) = "Rain", 1.9,
    SELECTEDVALUE(DimWeather[weather_condition]) = "Thunderstorm", 2.3,
    SELECTEDVALUE(DimWeather[weather_condition]) = "Clear", 1.4,
    1.5
)
```

### 🚀 Performance Optimization

1. **Import Mode**: Use for best performance with this dataset size
2. **Aggregations**: Pre-calculate common metrics in DAX
3. **Relationships**: Keep as simple Many-to-One relationships
4. **Visuals**: Limit to 6-8 visuals per page for optimal load times

### 📱 Mobile Layout

Configure mobile-friendly layouts for each page:

- Stack KPI cards vertically
- Simplify charts for smaller screens
- Prioritize most important visuals

### 🔄 Data Refresh

Since this is historical data:

- Set refresh schedule if data updates
- Consider incremental refresh for large datasets
- Test refresh performance regularly

---

### 📞 Support

For questions about the dashboard setup or data model, refer to:

- `business_analysis_report.md` for insights
- `dax_measures.txt` for complete measure definitions
- Data model documentation in the same directory

**Created**: August 29, 2025  
**Version**: 1.0  
**Data Source**: Rapido Transportation Dataset (88,938 rides)
