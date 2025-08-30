"""
Simplified Hybrid Dashboard Generator
Creates both Python visualizations and Power BI templates
"""

import pandas as pd
import numpy as np
import os
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

def run_quick_analysis():
    """Run a quick analysis and generate key insights"""
    print("🚀 Running Quick Analysis for Hybrid Dashboard...")
    
    # Load data
    df = pd.read_csv('../Dataset.csv')
    df['route'] = df['from_location'] + ' → ' + df['to_location']
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['date'] = pd.to_datetime(df['date'])
    
    # Calculate key metrics
    metrics = {
        'total_revenue': df['final_price'].sum(),
        'total_trips': len(df),
        'avg_revenue_per_ride': df['final_price'].mean(),
        'surge_contribution': ((df['final_price'] - df['base_price']).sum() / df['final_price'].sum()) * 100,
        'vit_dependency': (len(df[df['route'].str.contains('VIT', na=False)]) / len(df)) * 100,
        'peak_hour': df.groupby('hour')['final_price'].sum().idxmax(),
        'top_route': df.groupby('route')['final_price'].sum().idxmax(),
        'rain_premium': ((df[df['weather_condition'] == 'Rain']['final_price'].mean() / 
                         df[df['weather_condition'] == 'Clear']['final_price'].mean()) - 1) * 100
    }
    
    print(f"✅ Key metrics calculated: Total Revenue ₹{metrics['total_revenue']:,.2f}")
    return df, metrics

def create_python_visualizations(df, output_dir):
    """Create essential Python visualizations"""
    print("🎨 Creating Python Visualizations...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Revenue Trend
    monthly_revenue = df.groupby(df['date'].dt.to_period('M'))['final_price'].sum()
    fig = px.line(x=monthly_revenue.index.astype(str), y=monthly_revenue.values,
                  title='Monthly Revenue Trend')
    fig.write_html(f"{output_dir}/revenue_trend.html")
    
    # 2. Hourly Demand
    hourly_data = df.groupby('hour').agg({'final_price': 'sum', 'ride_id': 'count'})
    fig = px.bar(x=hourly_data.index, y=hourly_data['ride_id'],
                 title='24-Hour Demand Pattern')
    fig.write_html(f"{output_dir}/hourly_demand.html")
    
    # 3. Weather Impact
    weather_data = df.groupby('weather_condition')['final_price'].sum()
    fig = px.bar(x=weather_data.index, y=weather_data.values,
                 title='Revenue by Weather Condition')
    fig.write_html(f"{output_dir}/weather_impact.html")
    
    # 4. Vehicle Distribution
    vehicle_data = df.groupby('vehicle_type')['final_price'].sum()
    fig = px.pie(values=vehicle_data.values, names=vehicle_data.index,
                 title='Revenue Distribution by Vehicle Type')
    fig.write_html(f"{output_dir}/vehicle_distribution.html")
    
    # 5. Top Routes
    top_routes = df.groupby('route')['final_price'].sum().sort_values(ascending=False).head(10)
    fig = px.bar(x=top_routes.values, y=top_routes.index, orientation='h',
                 title='Top 10 Routes by Revenue')
    fig.write_html(f"{output_dir}/top_routes.html")
    
    # 6. Comprehensive Dashboard
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=('Monthly Revenue', 'Hourly Demand', 'Weather Impact',
                       'Vehicle Distribution', 'Top 5 Routes', 'Rush Hour Analysis'),
        specs=[[{"type": "scatter"}, {"type": "bar"}, {"type": "bar"}],
               [{"type": "pie"}, {"type": "bar"}, {"type": "bar"}]]
    )
    
    # Add traces
    fig.add_trace(go.Scatter(x=monthly_revenue.index.astype(str), y=monthly_revenue.values,
                            mode='lines+markers', name='Revenue'), row=1, col=1)
    fig.add_trace(go.Bar(x=hourly_data.index, y=hourly_data['ride_id'], name='Trips'), row=1, col=2)
    fig.add_trace(go.Bar(x=weather_data.index, y=weather_data.values, name='Weather Revenue'), row=1, col=3)
    fig.add_trace(go.Pie(labels=vehicle_data.index, values=vehicle_data.values, name='Vehicle Revenue'), row=2, col=1)
    
    top_5_routes = top_routes.head(5)
    fig.add_trace(go.Bar(x=top_5_routes.values, y=top_5_routes.index, name='Top Routes'), row=2, col=2)
    
    rush_data = df.groupby(df['hour'].isin([8, 9, 17, 18]))['final_price'].sum()
    fig.add_trace(go.Bar(x=['Regular', 'Rush'], y=rush_data.values, name='Rush Analysis'), row=2, col=3)
    
    fig.update_layout(height=800, title_text="Rapido Transportation - Comprehensive Dashboard")
    fig.write_html(f"{output_dir}/comprehensive_dashboard.html")
    
    print(f"✅ Python visualizations created in: {output_dir}")

def create_power_bi_template(metrics):
    """Create Power BI dashboard template"""
    print("📊 Creating Power BI Template...")
    
    template = {
        "dashboard_name": "Rapido Transportation Analytics - Hybrid Dashboard",
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        "version": "2.0 - Hybrid",
        "key_metrics": {
            "total_revenue": f"₹{metrics['total_revenue']:,.2f}",
            "total_trips": f"{metrics['total_trips']:,}",
            "avg_revenue_per_ride": f"₹{metrics['avg_revenue_per_ride']:.2f}",
            "surge_contribution": f"{metrics['surge_contribution']:.1f}%",
            "vit_dependency": f"{metrics['vit_dependency']:.1f}%",
            "peak_hour": str(metrics['peak_hour']),
            "top_route": metrics['top_route'],
            "rain_premium": f"{metrics['rain_premium']:.1f}%"
        },
        "pages": [
            {
                "name": "Executive Dashboard",
                "visuals": [
                    {"type": "KPI Card", "title": "Total Revenue", "measure": "Total Revenue"},
                    {"type": "KPI Card", "title": "Total Trips", "measure": "Total Trips"},
                    {"type": "KPI Card", "title": "Avg Revenue/Ride", "measure": "Average Revenue Per Ride"},
                    {"type": "KPI Card", "title": "VIT Dependency", "measure": "VIT Revenue Share"},
                    {"type": "Line Chart", "title": "Revenue Trend", "x": "DimTime[date]", "y": "Total Revenue"},
                    {"type": "Donut Chart", "title": "Vehicle Revenue", "legend": "DimVehicle[vehicle_type]", "values": "Total Revenue"},
                    {"type": "Bar Chart", "title": "Top Routes", "x": "Total Revenue", "y": "FactRides[route]"}
                ]
            },
            {
                "name": "Time Analysis", 
                "visuals": [
                    {"type": "Line Chart", "title": "24-Hour Demand", "x": "DimHour[hour]", "y": "Total Trips"},
                    {"type": "Column Chart", "title": "Rush Hour Revenue", "x": "DimHour[is_rush_hour]", "y": "Rush Hour Revenue"},
                    {"type": "Area Chart", "title": "Weekend vs Weekday", "x": "DimTime[day_name]", "y": "Weekend Revenue"}
                ]
            },
            {
                "name": "Weather Impact",
                "visuals": [
                    {"type": "Column Chart", "title": "Weather Revenue", "x": "DimWeather[weather_condition]", "y": "Total Revenue"},
                    {"type": "Gauge Chart", "title": "Rain Premium", "measure": "Weather Premium"},
                    {"type": "Scatter Plot", "title": "Weather vs Wait Time", "x": "Average Wait Time", "y": "Average Multiplier"}
                ]
            }
        ],
        "implementation_steps": [
            "1. Import data from power_bi/data_model/rapido_dashboard_data.xlsx",
            "2. Create relationships between tables",
            "3. Import DAX measures from power_bi/measures/advanced_dax_measures.txt",
            "4. Create dashboard pages as specified",
            "5. Validate metrics against Python analysis",
            "6. Apply formatting and interactivity"
        ]
    }
    
    return template

def save_hybrid_components(metrics, template):
    """Save all hybrid components"""
    
    # Create directories
    os.makedirs("../power_bi/templates/", exist_ok=True)
    os.makedirs("../analysis/business_insights/", exist_ok=True)
    
    # Save Power BI template
    with open("../power_bi/templates/hybrid_dashboard_template.json", 'w') as f:
        json.dump(template, f, indent=2)
    
    # Save metrics for validation
    with open("../analysis/business_insights/power_bi_insights.json", 'w') as f:
        json.dump(metrics, f, indent=2, default=str)
    
    # Create implementation guide
    guide = f"""# Hybrid Dashboard Implementation Guide

## Overview
This hybrid solution combines Python analytics with Power BI visualization.

## Key Metrics (Python Validated)
- Total Revenue: ₹{metrics['total_revenue']:,.2f}
- Total Trips: {metrics['total_trips']:,}
- Average Revenue per Ride: ₹{metrics['avg_revenue_per_ride']:.2f}
- Surge Contribution: {metrics['surge_contribution']:.1f}%
- VIT Dependency: {metrics['vit_dependency']:.1f}%
- Peak Hour: {metrics['peak_hour']}:00
- Top Route: {metrics['top_route']}
- Rain Premium: {metrics['rain_premium']:.1f}%

## Implementation Steps

### 1. Python Visualizations
- Created interactive HTML charts in visualizations/charts/
- Cross-validate these with Power BI visuals

### 2. Power BI Setup
- Import data from power_bi/data_model/rapido_dashboard_data.xlsx
- Import DAX measures from power_bi/measures/advanced_dax_measures.txt
- Fix Route Revenue Rank measure (remove VALUES())

### 3. Dashboard Creation
- Page 1: Executive Dashboard (KPIs, trends, overview)
- Page 2: Time Analysis (rush hours, patterns)
- Page 3: Weather Impact (rain priority, premiums)

### 4. Validation
- Total Revenue must match: ₹{metrics['total_revenue']:,.2f}
- Route rankings should match Python analysis
- Weather premiums should align

## Files Created
- Python visualizations: visualizations/charts/
- Power BI template: power_bi/templates/hybrid_dashboard_template.json
- Validation data: analysis/business_insights/power_bi_insights.json
- This guide: power_bi/templates/hybrid_implementation_guide.md

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    with open("../power_bi/templates/hybrid_implementation_guide.md", 'w') as f:
        f.write(guide)
    
    print("✅ All hybrid components saved!")

def main():
    """Main execution"""
    print("🚀 Creating Hybrid Dashboard Solution")
    print("=" * 50)
    
    # Run analysis
    df, metrics = run_quick_analysis()
    
    # Create Python visualizations
    create_python_visualizations(df, "../visualizations/charts")
    
    # Create Power BI template
    template = create_power_bi_template(metrics)
    
    # Save everything
    save_hybrid_components(metrics, template)
    
    print("\n✅ Hybrid Dashboard Generation Complete!")
    print("\n📁 Generated Components:")
    print("  • Python Visualizations: visualizations/charts/")
    print("  • Power BI Template: power_bi/templates/")
    print("  • Implementation Guide: power_bi/templates/hybrid_implementation_guide.md")
    
    print("\n🔄 Next Steps:")
    print("  1. Open visualizations/charts/comprehensive_dashboard.html")
    print("  2. Open Power BI Desktop")
    print("  3. Follow hybrid_implementation_guide.md")
    print("  4. Cross-validate all metrics")
    
    return df, metrics, template

if __name__ == "__main__":
    df, metrics, template = main()
