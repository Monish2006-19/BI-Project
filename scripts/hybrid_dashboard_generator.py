"""
Enhanced Power BI Dashboard Generator - Hybrid Approach
Combines Python-generated insights with Power BI dashboard specifications
"""

import pandas as pd
import json
import os
from datetime import datetime

def create_enhanced_power_bi_template():
    """
    Create enhanced Power BI template with Python analysis integration
    """
    
    print("🎨 Creating Enhanced Power BI Dashboard Template...")
    
    # Load Python analysis results if available
    try:
        with open('../analysis/business_insights/power_bi_insights.json', 'r') as f:
            python_insights = json.load(f)
        print("✅ Python analysis insights loaded successfully")
    except FileNotFoundError:
        print("⚠️ Python insights not found - using default template")
        python_insights = {}
    
    # Enhanced dashboard configuration with Python integration
    dashboard_config = {
        "dashboard_name": "Rapido Transportation Analytics - Hybrid Dashboard",
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        "version": "2.0 - Hybrid",
        "integration_type": "Python + Power BI",
        "python_insights": python_insights,
        "pages": [
            {
                "page_name": "Executive Dashboard",
                "page_order": 1,
                "description": "High-level KPIs, revenue trends, and business overview with Python insights",
                "python_components": [
                    "comprehensive_dashboard.html",
                    "revenue_trend.html"
                ],
                "visuals": [
                    {
                        "type": "KPI Card",
                        "title": "Total Revenue",
                        "measure": "Total Revenue",
                        "format": "₹ #,##0",
                        "python_validation": python_insights.get('key_metrics', {}).get('total_revenue', 'N/A'),
                        "position": {"x": 0, "y": 0, "width": 200, "height": 100},
                        "color_scheme": "#2E86AB"
                    },
                    {
                        "type": "KPI Card", 
                        "title": "Total Trips",
                        "measure": "Total Trips",
                        "format": "#,##0",
                        "python_validation": python_insights.get('key_metrics', {}).get('total_trips', 'N/A'),
                        "position": {"x": 220, "y": 0, "width": 200, "height": 100},
                        "color_scheme": "#4ECDC4"
                    },
                    {
                        "type": "KPI Card",
                        "title": "Average Revenue/Ride", 
                        "measure": "Average Revenue Per Ride",
                        "format": "₹ #,##0.00",
                        "python_validation": python_insights.get('key_metrics', {}).get('avg_revenue_per_ride', 'N/A'),
                        "position": {"x": 440, "y": 0, "width": 200, "height": 100},
                        "color_scheme": "#45B7D1"
                    },
                    {
                        "type": "KPI Card",
                        "title": "VIT Dependency",
                        "measure": "VIT Revenue Share",
                        "format": "0.0%",
                        "python_validation": python_insights.get('key_metrics', {}).get('vit_dependency', 'N/A'),
                        "position": {"x": 660, "y": 0, "width": 200, "height": 100},
                        "color_scheme": "#FF6B6B"
                    },
                    {
                        "type": "Line Chart",
                        "title": "Monthly Revenue Trend",
                        "x_axis": "DimTime[month_name]",
                        "y_axis": "Total Revenue",
                        "python_reference": "revenue_trend.html",
                        "position": {"x": 0, "y": 120, "width": 430, "height": 250},
                        "insights": "Python analysis shows seasonal patterns"
                    },
                    {
                        "type": "Donut Chart", 
                        "title": "Revenue by Vehicle Type",
                        "legend": "DimVehicle[vehicle_type]",
                        "values": "Total Revenue",
                        "python_reference": "vehicle_analysis.html",
                        "position": {"x": 450, "y": 120, "width": 410, "height": 250},
                        "color_palette": ["#FF6B6B", "#4ECDC4", "#45B7D1"]
                    },
                    {
                        "type": "Horizontal Bar Chart",
                        "title": "Top 10 Routes by Revenue",
                        "x_axis": "Total Revenue",
                        "y_axis": "FactRides[route]",
                        "measure": "Route Revenue Rank",
                        "python_reference": "route_analysis.html",
                        "position": {"x": 0, "y": 390, "width": 860, "height": 300},
                        "top_route": python_insights.get('route_insights', {}).get('top_route', 'N/A')
                    }
                ]
            },
            {
                "page_name": "Time Analysis",
                "page_order": 2,
                "description": "Rush hour patterns, hourly demand, and time-based insights",
                "python_components": [
                    "time_analysis.html"
                ],
                "key_insights": {
                    "peak_hour": python_insights.get('time_patterns', {}).get('peak_hour', 'N/A'),
                    "rush_hour_premium": python_insights.get('time_patterns', {}).get('rush_hour_premium', 'N/A')
                },
                "visuals": [
                    {
                        "type": "Line Chart",
                        "title": "24-Hour Demand Pattern",
                        "x_axis": "DimHour[hour]",
                        "y_axis": "Total Trips",
                        "python_reference": "time_analysis.html",
                        "position": {"x": 0, "y": 0, "width": 430, "height": 300},
                        "highlight_hours": [8, 9, 17, 18]
                    },
                    {
                        "type": "Column Chart",
                        "title": "Rush Hour vs Regular Hours Revenue",
                        "x_axis": "DimHour[is_rush_hour]",
                        "y_axis": "Rush Hour Revenue",
                        "position": {"x": 450, "y": 0, "width": 410, "height": 300},
                        "color_coding": {"Rush": "#FF6B6B", "Regular": "#4ECDC4"}
                    },
                    {
                        "type": "Stacked Bar Chart",
                        "title": "Hourly Revenue Distribution",
                        "x_axis": "DimHour[hour]",
                        "y_axis": ["Morning Rush Revenue", "Evening Rush Revenue", "Total Revenue"],
                        "position": {"x": 0, "y": 320, "width": 430, "height": 250}
                    },
                    {
                        "type": "Area Chart",
                        "title": "Weekend vs Weekday Patterns",
                        "x_axis": "DimTime[day_name]",
                        "y_axis": ["Weekend Revenue", "Weekday Revenue"],
                        "position": {"x": 450, "y": 320, "width": 410, "height": 250}
                    },
                    {
                        "type": "Matrix Table",
                        "title": "Time Performance Matrix",
                        "rows": "DimHour[hour]",
                        "columns": "DimTime[day_name]",
                        "values": "Average Revenue Per Ride",
                        "position": {"x": 0, "y": 590, "width": 860, "height": 200}
                    }
                ]
            },
            {
                "page_name": "Weather Impact",
                "page_order": 3,
                "description": "Weather condition analysis with rain priority focus",
                "python_components": [
                    "weather_analysis.html"
                ],
                "key_insights": {
                    "rain_premium": python_insights.get('weather_insights', {}).get('rain_premium', 'N/A'),
                    "best_weather": python_insights.get('weather_insights', {}).get('best_weather_for_revenue', 'N/A')
                },
                "visuals": [
                    {
                        "type": "Column Chart",
                        "title": "Revenue by Weather Condition",
                        "x_axis": "DimWeather[weather_condition]",
                        "y_axis": ["Rain Revenue", "Clear Revenue", "Thunderstorm Revenue"],
                        "python_reference": "weather_analysis.html",
                        "position": {"x": 0, "y": 0, "width": 280, "height": 300},
                        "highlight_rain": True
                    },
                    {
                        "type": "Gauge Chart",
                        "title": "Weather Premium Index",
                        "measure": "Weather Premium",
                        "min_value": 0,
                        "max_value": 3,
                        "position": {"x": 300, "y": 0, "width": 280, "height": 300},
                        "thresholds": [{"value": 1.5, "color": "yellow"}, {"value": 2.0, "color": "red"}]
                    },
                    {
                        "type": "Clustered Bar Chart",
                        "title": "Average Multiplier by Weather",
                        "x_axis": "DimWeather[weather_condition]",
                        "y_axis": "Average Multiplier",
                        "position": {"x": 600, "y": 0, "width": 260, "height": 300}
                    },
                    {
                        "type": "Scatter Plot",
                        "title": "Weather Impact on Waiting Time",
                        "x_axis": "Average Wait Time",
                        "y_axis": "Average Multiplier",
                        "legend": "DimWeather[weather_condition]",
                        "position": {"x": 0, "y": 320, "width": 420, "height": 250}
                    },
                    {
                        "type": "Line Chart",
                        "title": "Hourly Weather Premium Trends",
                        "x_axis": "DimHour[hour]",
                        "y_axis": "Weather Premium",
                        "legend": "DimWeather[weather_condition]",
                        "position": {"x": 440, "y": 320, "width": 420, "height": 250}
                    },
                    {
                        "type": "Waterfall Chart", 
                        "title": "Weather Impact on Revenue",
                        "category": "DimWeather[weather_condition]",
                        "measure": "Total Revenue",
                        "position": {"x": 0, "y": 590, "width": 860, "height": 200}
                    }
                ]
            }
        ],
        "dashboard_settings": {
            "theme": "Modern",
            "color_palette": ["#2E86AB", "#4ECDC4", "#45B7D1", "#FF6B6B", "#FFA07A"],
            "font_family": "Segoe UI",
            "background_color": "#F8F9FA",
            "python_integration": True,
            "interactive_filters": [
                "DimTime[date]",
                "DimWeather[weather_condition]",
                "DimVehicle[vehicle_type]",
                "FactRides[route]"
            ]
        }
    }
    
    return dashboard_config

def generate_power_bi_instructions():
    """
    Generate step-by-step Power BI implementation instructions
    """
    
    instructions = {
        "setup_phase": {
            "title": "Phase 1: Power BI Setup & Data Import",
            "steps": [
                "1. Open Power BI Desktop",
                "2. Import data from 'power_bi/data_model/rapido_dashboard_data.xlsx'",
                "3. Verify all 5 tables are imported: FactRides, DimTime, DimHour, DimVehicle, DimWeather",
                "4. Create relationships in Model view",
                "5. Import all DAX measures from 'power_bi/measures/advanced_dax_measures.txt'"
            ]
        },
        "page_creation": {
            "title": "Phase 2: Dashboard Page Creation",
            "executive_dashboard": [
                "Create new page 'Executive Dashboard'",
                "Add 4 KPI cards for: Total Revenue, Total Trips, Avg Revenue/Ride, VIT Dependency",
                "Add monthly revenue trend line chart",
                "Add vehicle revenue donut chart",
                "Add top 10 routes horizontal bar chart",
                "Apply executive color scheme: #2E86AB primary"
            ],
            "time_analysis": [
                "Create new page 'Time Analysis'",
                "Add 24-hour demand pattern line chart",
                "Add rush hour vs regular column chart",
                "Add hourly revenue stacked bar chart",
                "Add weekend vs weekday area chart",
                "Add time performance matrix table"
            ],
            "weather_impact": [
                "Create new page 'Weather Impact'",
                "Add weather revenue column chart",
                "Add weather premium gauge chart",
                "Add multiplier by weather bar chart",
                "Add weather-wait time scatter plot",
                "Add hourly weather trends line chart",
                "Add weather revenue waterfall chart"
            ]
        },
        "python_integration": {
            "title": "Phase 3: Python Analysis Integration",
            "validation_steps": [
                "Cross-reference KPI values with Python analysis outputs",
                "Validate Total Revenue matches: Expected ₹13,170,756.08",
                "Confirm rush hour patterns align with Python insights",
                "Verify weather premium calculations",
                "Check route rankings against Python analysis"
            ],
            "enhancement_options": [
                "Embed Python HTML charts as web content (if supported)",
                "Use Python insights for dynamic text boxes",
                "Cross-validate all measures with Python outputs",
                "Create Python-derived calculated columns if needed"
            ]
        },
        "advanced_features": {
            "title": "Phase 4: Advanced Dashboard Features",
            "interactive_elements": [
                "Add date range slicer",
                "Add weather condition filter",
                "Add vehicle type buttons",
                "Add route search box",
                "Configure cross-filtering between visuals"
            ],
            "formatting": [
                "Apply consistent color scheme",
                "Set up conditional formatting for KPIs",
                "Add visual-level filters",
                "Configure tooltip customizations",
                "Set up mobile layout"
            ]
        }
    }
    
    return instructions

def create_integration_guide():
    """
    Create comprehensive integration guide for Python + Power BI workflow
    """
    
    guide = {
        "workflow_overview": {
            "description": "Hybrid approach combining Python analytics with Power BI visualization",
            "benefits": [
                "Python provides deep statistical analysis and validation",
                "Power BI offers professional dashboard interface",
                "Cross-validation ensures data accuracy",
                "Flexible analysis with powerful visualization"
            ]
        },
        "data_flow": [
            "1. Raw data (Dataset.csv) → Python analysis",
            "2. Python generates: KPIs, insights, validation data, interactive charts",
            "3. Clean data exported to Excel for Power BI",
            "4. Power BI imports clean data + DAX measures",
            "5. Power BI dashboard built with Python validation",
            "6. Final dashboard combines both capabilities"
        ],
        "validation_checkpoints": {
            "data_consistency": [
                "Total Revenue: Python vs Power BI must match exactly",
                "Trip counts: Verify consistency across platforms",
                "Route rankings: Cross-check top 10 routes",
                "Time patterns: Validate rush hour calculations"
            ],
            "measure_validation": [
                "Each DAX measure should have Python equivalent",
                "Weather premium calculations must align",
                "VIT dependency percentages must match",
                "Surge pricing impact should be consistent"
            ]
        },
        "troubleshooting": {
            "common_issues": [
                "Data type mismatches: Ensure consistent formatting",
                "Relationship errors: Verify key column matches",
                "Measure conflicts: Check for circular dependencies",
                "Performance issues: Optimize large datasets"
            ],
            "validation_failures": [
                "If totals don't match: Check data import process",
                "If trends differ: Verify date/time handling",
                "If categories vary: Check text formatting consistency"
            ]
        }
    }
    
    return guide

def save_enhanced_dashboard_config():
    """
    Save all enhanced dashboard components
    """
    
    # Create output directory
    output_dir = "../power_bi/templates/"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate all components
    dashboard_config = create_enhanced_power_bi_template()
    instructions = generate_power_bi_instructions()
    integration_guide = create_integration_guide()
    
    # Save dashboard configuration
    with open(f"{output_dir}enhanced_dashboard_config.json", 'w') as f:
        json.dump(dashboard_config, f, indent=2, default=str)
    
    # Save instructions
    with open(f"{output_dir}power_bi_instructions.json", 'w') as f:
        json.dump(instructions, f, indent=2, default=str)
    
    # Save integration guide
    with open(f"{output_dir}integration_guide.json", 'w') as f:
        json.dump(integration_guide, f, indent=2, default=str)
    
    # Create markdown documentation
    create_markdown_documentation(output_dir, dashboard_config, instructions, integration_guide)
    
    print(f"✅ Enhanced dashboard templates saved to: {output_dir}")
    return output_dir

def create_markdown_documentation(output_dir, config, instructions, guide):
    """
    Create comprehensive markdown documentation
    """
    
    # Main documentation file
    doc_content = f"""# Rapido Transportation Analytics - Hybrid Dashboard Guide

## Overview
This is a hybrid analytics solution combining Python-powered analysis with Power BI visualization capabilities.

### Dashboard Structure
- **Page 1**: Executive Dashboard (KPIs, trends, overview)
- **Page 2**: Time Analysis (rush hours, patterns, demand)
- **Page 3**: Weather Impact (rain priority, premium analysis)

### Key Features
- Cross-validated metrics between Python and Power BI
- Interactive visualizations with professional design
- Real-time insights integration
- Mobile-responsive layout

## Implementation Phases

### Phase 1: Setup & Data Import
{chr(10).join([f"- {step}" for step in instructions['setup_phase']['steps']])}

### Phase 2: Page Creation

#### Executive Dashboard
{chr(10).join([f"- {step}" for step in instructions['page_creation']['executive_dashboard']])}

#### Time Analysis
{chr(10).join([f"- {step}" for step in instructions['page_creation']['time_analysis']])}

#### Weather Impact
{chr(10).join([f"- {step}" for step in instructions['page_creation']['weather_impact']])}

### Phase 3: Python Integration
{chr(10).join([f"- {step}" for step in instructions['python_integration']['validation_steps']])}

### Phase 4: Advanced Features
{chr(10).join([f"- {step}" for step in instructions['advanced_features']['interactive_elements']])}

## Data Validation
- **Total Revenue**: Must match ₹13,170,756.08
- **Total Trips**: Must match 88,938
- **VIT Dependency**: Cross-check percentage calculations
- **Weather Premium**: Validate rain vs clear pricing

## Files Structure
- `enhanced_dashboard_config.json`: Complete dashboard specification
- `power_bi_instructions.json`: Step-by-step implementation guide
- `integration_guide.json`: Python-Power BI integration workflow
- `hybrid_dashboard_guide.md`: This documentation

## Support Files
- Python analysis: `../scripts/comprehensive_bi_analysis.py`
- DAX measures: `../measures/advanced_dax_measures.txt`
- Clean data: `../data_model/rapido_dashboard_data.xlsx`

## Color Scheme
- Primary: #2E86AB (Blue)
- Secondary: #4ECDC4 (Teal) 
- Accent 1: #45B7D1 (Light Blue)
- Accent 2: #FF6B6B (Red)
- Accent 3: #FFA07A (Orange)

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    with open(f"{output_dir}hybrid_dashboard_guide.md", 'w') as f:
        f.write(doc_content)
    
    print("  ✓ Markdown documentation created")

def main():
    """
    Main function to generate enhanced dashboard components
    """
    print("🚀 Generating Enhanced Power BI Dashboard Components")
    print("=" * 60)
    
    # Save all components
    output_dir = save_enhanced_dashboard_config()
    
    print("\n✅ Enhanced Dashboard Generation Complete!")
    print(f"📁 Output directory: {output_dir}")
    print("\n📋 Generated Files:")
    print("  • enhanced_dashboard_config.json")
    print("  • power_bi_instructions.json") 
    print("  • integration_guide.json")
    print("  • hybrid_dashboard_guide.md")
    
    print("\n🔄 Next Steps:")
    print("  1. Run Python analysis: comprehensive_bi_analysis.py")
    print("  2. Open Power BI Desktop")
    print("  3. Follow hybrid_dashboard_guide.md")
    print("  4. Cross-validate all metrics")
    
    return output_dir

if __name__ == "__main__":
    main()
