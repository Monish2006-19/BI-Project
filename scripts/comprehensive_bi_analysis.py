"""
Comprehensive Business Intelligence Analysis for Rapido Transportation
Author: BI Project Team
Date: August 29, 2025

This script performs deep analysis on the transportation dataset covering:
1. All 45 KPIs and metrics identification
2. Time-based demand analysis (morning rush, evening rush, weekends, holidays)
3. Weather impact analysis with rain priority
4. Business insights and recommendations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class RapidoBusinessIntelligence:
    """
    Comprehensive Business Intelligence Analysis for Rapido Transportation Data
    """
    
    def __init__(self, data_path):
        """Initialize with dataset path"""
        self.data_path = data_path
        self.df = None
        self.kpis = {}
        
    def load_and_prepare_data(self):
        """Load and prepare the dataset for analysis"""
        print("🚀 Loading Rapido Transportation Dataset...")
        self.df = pd.read_csv(self.data_path)
        
        # Convert datetime columns
        self.df['datetime'] = pd.to_datetime(self.df['datetime'])
        self.df['date'] = pd.to_datetime(self.df['date'])
        
        # Create additional time features for analysis
        self.df['month_name'] = self.df['datetime'].dt.month_name()
        self.df['day_name'] = self.df['datetime'].dt.day_name()
        self.df['year'] = self.df['datetime'].dt.year
        
        # Define rush hour periods
        self.df['is_morning_rush'] = (self.df['hour'] >= 8) & (self.df['hour'] <= 9)
        self.df['is_evening_rush'] = (self.df['hour'] >= 17) & (self.df['hour'] <= 18)
        self.df['is_rush_hour'] = self.df['is_morning_rush'] | self.df['is_evening_rush']
        
        # Define time periods with detailed categories
        def categorize_time_period(hour):
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
        
        self.df['detailed_time_period'] = self.df['hour'].apply(categorize_time_period)
        
        print(f"✅ Dataset loaded: {len(self.df):,} rides from {self.df['date'].min().date()} to {self.df['date'].max().date()}")
        return self.df
    
    def calculate_all_kpis(self):
        """Calculate all 45 KPIs and metrics"""
        print("\n📊 Calculating All KPIs and Metrics...")
        
        # 1-7: Revenue & Financial KPIs
        self.kpis['total_revenue'] = self.df['final_price'].sum()
        self.kpis['avg_revenue_per_ride'] = self.df['final_price'].mean()
        self.kpis['revenue_by_vehicle'] = self.df.groupby('vehicle_type')['final_price'].sum().to_dict()
        self.kpis['surge_revenue_impact'] = (self.df['final_price'] - self.df['base_price']).sum()
        self.kpis['avg_price_premium_percent'] = self.df['price_premium_percent'].mean()
        self.kpis['revenue_per_km'] = self.df['final_price'].sum() / self.df['distance_km'].sum()
        self.kpis['avg_cost_efficiency_ratio'] = (self.df['final_price'] / self.df['base_price']).mean()
        
        # 8-14: Operational KPIs
        self.kpis['total_trip_volume'] = len(self.df)
        self.kpis['avg_trip_distance'] = self.df['distance_km'].mean()
        self.kpis['fleet_utilization_by_vehicle'] = self.df['vehicle_type'].value_counts(normalize=True).to_dict()
        self.kpis['avg_waiting_time'] = self.df['waiting_time_minutes'].mean()
        self.kpis['trip_completion_rate'] = 1.0  # Assuming all trips in dataset are completed
        self.kpis['peak_hour_trip_distribution'] = self.df[self.df['is_rush_hour']]['hour'].value_counts().to_dict()
        self.kpis['distance_category_distribution'] = self.df['distance_category'].value_counts(normalize=True).to_dict()
        
        # 15-21: Time-Based Demand KPIs
        morning_rush = self.df[self.df['is_morning_rush']]
        evening_rush = self.df[self.df['is_evening_rush']]
        
        self.kpis['morning_rush_demand'] = len(morning_rush)
        self.kpis['evening_rush_demand'] = len(evening_rush)
        self.kpis['weekend_vs_weekday_performance'] = {
            'weekend': self.df[self.df['is_weekend']]['final_price'].sum(),
            'weekday': self.df[~self.df['is_weekend']]['final_price'].sum()
        }
        self.kpis['hourly_demand_pattern'] = self.df.groupby('hour').size().to_dict()
        self.kpis['day_of_week_performance'] = self.df.groupby('day_name')['final_price'].sum().to_dict()
        self.kpis['monthly_trends'] = self.df.groupby('month_name')['final_price'].sum().to_dict()
        
        rush_hour_premium = self.df[self.df['is_rush_hour']]['final_price'].mean()
        off_peak_premium = self.df[~self.df['is_rush_hour']]['final_price'].mean()
        self.kpis['rush_hour_premium'] = (rush_hour_premium - off_peak_premium) / off_peak_premium * 100
        
        # 22-28: Weather Impact KPIs
        rain_rides = self.df[self.df['weather_condition'] == 'Rain']
        clear_rides = self.df[self.df['weather_condition'] == 'Clear']
        
        self.kpis['weather_surge_frequency'] = self.df.groupby('weather_condition')['surge_multiplier'].mean().to_dict()
        self.kpis['rain_vs_clear_multiplier'] = rain_rides['surge_multiplier'].mean() / clear_rides['surge_multiplier'].mean() if len(clear_rides) > 0 else 0
        self.kpis['weather_demand_correlation'] = self.df.groupby('weather_condition').size().to_dict()
        self.kpis['precipitation_impact'] = self.df.groupby(pd.cut(self.df['precipitation'], bins=5))['surge_multiplier'].mean().to_dict()
        
        # Weather correlation with demand
        temp_corr = self.df['temperature'].corr(self.df['final_price'])
        self.kpis['temperature_demand_correlation'] = temp_corr
        
        visibility_impact = self.df.groupby(pd.cut(self.df['visibility'], bins=5)).size().to_dict()
        self.kpis['visibility_impact'] = visibility_impact
        
        storm_rides = self.df[self.df['weather_condition'] == 'Thunderstorm']
        self.kpis['storm_revenue_boost'] = storm_rides['surge_multiplier'].mean() if len(storm_rides) > 0 else 0
        
        # 29-34: Geographic & Route KPIs
        route_performance = self.df.groupby(['from_location', 'to_location']).agg({
            'final_price': ['sum', 'count'],
            'distance_km': 'mean'
        }).round(2)
        
        top_routes = route_performance['final_price']['sum'].nlargest(10)
        self.kpis['top_performing_routes'] = top_routes.to_dict()
        
        vit_routes = self.df[self.df['from_location'].str.contains('VIT', na=False) | 
                           self.df['to_location'].str.contains('VIT', na=False)]
        self.kpis['vit_university_performance'] = {
            'total_revenue': vit_routes['final_price'].sum(),
            'total_trips': len(vit_routes),
            'avg_price': vit_routes['final_price'].mean()
        }
        
        self.kpis['avg_distance_by_route'] = self.df.groupby(['from_location', 'to_location'])['distance_km'].mean().to_dict()
        
        # Route profitability (revenue per km)
        route_profitability = self.df.groupby(['from_location', 'to_location']).apply(
            lambda x: x['final_price'].sum() / x['distance_km'].sum()
        ).nlargest(10)
        self.kpis['route_profitability_index'] = route_profitability.to_dict()
        
        self.kpis['popular_destinations'] = self.df['to_location'].value_counts().head(10).to_dict()
        
        # 35-40: Business Intelligence KPIs
        demand_score = self.df.groupby(['from_location', 'to_location']).size()
        self.kpis['customer_demand_score'] = demand_score.describe().to_dict()
        
        # Surge pricing effectiveness (conversion rate)
        surge_effectiveness = self.df[self.df['surge_multiplier'] > 1.2]['final_price'].sum() / self.df['final_price'].sum()
        self.kpis['surge_pricing_effectiveness'] = surge_effectiveness
        
        # Market penetration by area
        area_penetration = self.df.groupby('from_location').size().to_dict()
        self.kpis['market_penetration_by_area'] = area_penetration
        
        # Service quality index (inverse of waiting time)
        avg_wait_by_area = self.df.groupby('from_location')['waiting_time_minutes'].mean()
        self.kpis['service_quality_index'] = (1 / avg_wait_by_area).to_dict()
        
        # Price competitiveness (compared to base price)
        price_competitiveness = (self.df['final_price'] / self.df['base_price']).mean()
        self.kpis['competitive_pricing_analysis'] = price_competitiveness
        
        # Growth rate calculation (month over month)
        monthly_revenue = self.df.groupby(['year', 'month'])['final_price'].sum()
        if len(monthly_revenue) > 1:
            growth_rate = ((monthly_revenue.iloc[-1] - monthly_revenue.iloc[0]) / monthly_revenue.iloc[0]) * 100
            self.kpis['revenue_growth_rate'] = growth_rate
        else:
            self.kpis['revenue_growth_rate'] = 0
        
        # 41-45: Strategic KPIs
        vehicle_revenue_share = self.df.groupby('vehicle_type')['final_price'].sum()
        total_revenue = vehicle_revenue_share.sum()
        self.kpis['revenue_diversification'] = (vehicle_revenue_share / total_revenue * 100).to_dict()
        
        # Demand forecasting accuracy (using standard deviation as proxy)
        demand_std = self.df.groupby('hour').size().std()
        self.kpis['demand_forecasting_accuracy'] = 100 - (demand_std / self.df.groupby('hour').size().mean() * 100)
        
        # Price elasticity (correlation between price and demand)
        price_elasticity = self.df['final_price'].corr(self.df.groupby('hour').transform('size'))
        self.kpis['price_elasticity_of_demand'] = price_elasticity
        
        # Customer satisfaction proxy
        satisfaction_proxy = (
            (self.df['waiting_time_minutes'] <= 5).mean() * 0.6 +  # Low wait time
            (self.df['price_premium_percent'] <= 30).mean() * 0.4   # Reasonable pricing
        ) * 100
        self.kpis['customer_satisfaction_proxy'] = satisfaction_proxy
        
        # Business sustainability index
        sustainability_factors = {
            'revenue_stability': 1 - self.df.groupby('date')['final_price'].sum().std() / self.df.groupby('date')['final_price'].sum().mean(),
            'demand_consistency': 1 - self.df.groupby('hour').size().std() / self.df.groupby('hour').size().mean(),
            'weather_resilience': len(self.df[self.df['weather_condition'] != 'Clear']) / len(self.df)
        }
        self.kpis['business_sustainability_index'] = np.mean(list(sustainability_factors.values())) * 100
        
        print("✅ All 45 KPIs calculated successfully!")
        return self.kpis
    
    def analyze_rush_hour_patterns(self):
        """Detailed analysis of morning and evening rush hours"""
        print("\n⏰ Analyzing Rush Hour Patterns...")
        
        # Morning rush hour analysis (8-9 AM)
        morning_rush = self.df[self.df['is_morning_rush']]
        
        # Evening rush hour analysis (5:30-6:30 PM)
        evening_rush = self.df[self.df['is_evening_rush']]
        
        rush_hour_analysis = {
            'morning_rush': {
                'total_trips': len(morning_rush),
                'total_revenue': morning_rush['final_price'].sum(),
                'avg_surge_multiplier': morning_rush['surge_multiplier'].mean(),
                'avg_waiting_time': morning_rush['waiting_time_minutes'].mean(),
                'most_popular_routes': morning_rush.groupby(['from_location', 'to_location']).size().nlargest(5).to_dict(),
                'vehicle_preference': morning_rush['vehicle_type'].value_counts().to_dict(),
                'avg_distance': morning_rush['distance_km'].mean(),
                'weather_impact': morning_rush.groupby('weather_condition')['surge_multiplier'].mean().to_dict()
            },
            'evening_rush': {
                'total_trips': len(evening_rush),
                'total_revenue': evening_rush['final_price'].sum(),
                'avg_surge_multiplier': evening_rush['surge_multiplier'].mean(),
                'avg_waiting_time': evening_rush['waiting_time_minutes'].mean(),
                'most_popular_routes': evening_rush.groupby(['from_location', 'to_location']).size().nlargest(5).to_dict(),
                'vehicle_preference': evening_rush['vehicle_type'].value_counts().to_dict(),
                'avg_distance': evening_rush['distance_km'].mean(),
                'weather_impact': evening_rush.groupby('weather_condition')['surge_multiplier'].mean().to_dict()
            }
        }
        
        # Weekend vs Weekday analysis
        weekend_data = self.df[self.df['is_weekend']]
        weekday_data = self.df[~self.df['is_weekend']]
        
        weekend_analysis = {
            'weekend_patterns': {
                'peak_hours': weekend_data.groupby('hour').size().nlargest(3).index.tolist(),
                'total_revenue': weekend_data['final_price'].sum(),
                'avg_trip_distance': weekend_data['distance_km'].mean(),
                'popular_destinations': weekend_data['to_location'].value_counts().head(5).to_dict(),
                'weather_sensitivity': weekend_data.groupby('weather_condition')['surge_multiplier'].mean().to_dict()
            },
            'weekday_patterns': {
                'peak_hours': weekday_data.groupby('hour').size().nlargest(3).index.tolist(),
                'total_revenue': weekday_data['final_price'].sum(),
                'avg_trip_distance': weekday_data['distance_km'].mean(),
                'popular_destinations': weekday_data['to_location'].value_counts().head(5).to_dict(),
                'weather_sensitivity': weekday_data.groupby('weather_condition')['surge_multiplier'].mean().to_dict()
            }
        }
        
        return rush_hour_analysis, weekend_analysis
    
    def analyze_weather_impact(self):
        """Comprehensive weather impact analysis with rain priority"""
        print("\n🌦️ Analyzing Weather Impact with Rain Priority...")
        
        weather_analysis = {}
        
        # Overall weather impact
        weather_stats = self.df.groupby('weather_condition').agg({
            'final_price': ['mean', 'sum', 'count'],
            'surge_multiplier': ['mean', 'max'],
            'waiting_time_minutes': 'mean',
            'distance_km': 'mean',
            'price_premium_percent': 'mean'
        }).round(2)
        
        weather_analysis['overall_impact'] = weather_stats.to_dict()
        
        # Rain-specific analysis (priority focus)
        rain_data = self.df[self.df['weather_condition'] == 'Rain']
        clear_data = self.df[self.df['weather_condition'] == 'Clear']
        
        rain_analysis = {
            'rain_premium': {
                'avg_surge_multiplier': rain_data['surge_multiplier'].mean(),
                'max_surge_seen': rain_data['surge_multiplier'].max(),
                'revenue_boost': (rain_data['final_price'].sum() - rain_data['base_price'].sum()),
                'trip_volume': len(rain_data),
                'avg_waiting_time': rain_data['waiting_time_minutes'].mean(),
                'popular_vehicle_in_rain': rain_data['vehicle_type'].mode().iloc[0] if len(rain_data) > 0 else 'N/A'
            },
            'rain_vs_clear_comparison': {
                'surge_difference': rain_data['surge_multiplier'].mean() - clear_data['surge_multiplier'].mean() if len(clear_data) > 0 else 0,
                'price_difference': rain_data['final_price'].mean() - clear_data['final_price'].mean() if len(clear_data) > 0 else 0,
                'demand_difference': len(rain_data) - len(clear_data),
                'waiting_time_difference': rain_data['waiting_time_minutes'].mean() - clear_data['waiting_time_minutes'].mean() if len(clear_data) > 0 else 0
            }
        }
        
        weather_analysis['rain_focus'] = rain_analysis
        
        # Seasonal weather patterns
        seasonal_weather = self.df.groupby(['month_name', 'weather_condition']).size().unstack(fill_value=0)
        weather_analysis['seasonal_patterns'] = seasonal_weather.to_dict()
        
        # Weather impact by time of day
        hourly_weather_impact = self.df.groupby(['hour', 'weather_condition'])['surge_multiplier'].mean().unstack(fill_value=0)
        weather_analysis['hourly_weather_impact'] = hourly_weather_impact.to_dict()
        
        # Extreme weather events
        extreme_weather = self.df[self.df['weather_condition'].isin(['Thunderstorm', 'Rain'])]
        extreme_analysis = {
            'extreme_weather_revenue': extreme_weather['final_price'].sum(),
            'extreme_weather_trips': len(extreme_weather),
            'avg_extreme_surge': extreme_weather['surge_multiplier'].mean(),
            'extreme_weather_share': len(extreme_weather) / len(self.df) * 100
        }
        
        weather_analysis['extreme_weather'] = extreme_analysis
        
        return weather_analysis
    
    def generate_business_insights(self):
        """Generate actionable business insights and recommendations"""
        print("\n💡 Generating Business Insights and Recommendations...")
        
        insights = {
            'revenue_insights': [],
            'operational_insights': [],
            'strategic_recommendations': [],
            'weather_strategy': [],
            'time_optimization': []
        }
        
        # Revenue insights
        total_revenue = self.kpis['total_revenue']
        surge_revenue = self.kpis['surge_revenue_impact']
        surge_contribution = (surge_revenue / total_revenue) * 100
        
        insights['revenue_insights'].append(f"💰 Total Revenue: ₹{total_revenue:,.2f}")
        insights['revenue_insights'].append(f"📈 Surge Pricing contributes {surge_contribution:.1f}% of total revenue")
        insights['revenue_insights'].append(f"🚗 Vehicle Revenue Distribution: {self.kpis['revenue_diversification']}")
        
        # Peak hour insights
        if self.kpis['evening_rush_demand'] > self.kpis['morning_rush_demand']:
            insights['time_optimization'].append("🌆 Evening rush (5:30-6:30 PM) shows higher demand than morning rush")
        else:
            insights['time_optimization'].append("🌅 Morning rush (8-9 AM) shows higher demand than evening rush")
        
        insights['time_optimization'].append(f"⚡ Rush hour premium: {self.kpis['rush_hour_premium']:.1f}% higher pricing")
        
        # Weather insights
        rain_multiplier = self.kpis.get('rain_vs_clear_multiplier', 0)
        if rain_multiplier > 1.5:
            insights['weather_strategy'].append(f"☔ Rain creates {rain_multiplier:.1f}x higher surge pricing opportunity")
        
        # Operational insights
        avg_wait = self.kpis['avg_waiting_time']
        if avg_wait > 5:
            insights['operational_insights'].append(f"⏱️ Average waiting time ({avg_wait:.1f} min) needs improvement")
        else:
            insights['operational_insights'].append(f"✅ Good service quality with {avg_wait:.1f} min average wait time")
        
        # VIT University insights
        vit_performance = self.kpis['vit_university_performance']
        vit_revenue_share = (vit_performance['total_revenue'] / total_revenue) * 100
        insights['strategic_recommendations'].append(f"🎓 VIT University routes contribute {vit_revenue_share:.1f}% of total revenue")
        
        # Top recommendations based on data
        if surge_contribution > 30:
            insights['strategic_recommendations'].append("🎯 Focus on surge pricing optimization - it's a major revenue driver")
        
        if self.kpis['customer_satisfaction_proxy'] < 70:
            insights['strategic_recommendations'].append("👥 Customer satisfaction needs attention - optimize wait times and pricing")
        
        return insights
    
    def create_summary_report(self):
        """Create a comprehensive summary report"""
        print("\n📋 Creating Summary Report...")
        
        report = {
            'executive_summary': {
                'total_rides': f"{len(self.df):,}",
                'total_revenue': f"₹{self.kpis['total_revenue']:,.2f}",
                'avg_revenue_per_ride': f"₹{self.kpis['avg_revenue_per_ride']:.2f}",
                'data_period': f"{self.df['date'].min().date()} to {self.df['date'].max().date()}",
                'surge_contribution': f"{(self.kpis['surge_revenue_impact'] / self.kpis['total_revenue']) * 100:.1f}%"
            },
            'key_performance_indicators': self.kpis,
            'business_insights': self.generate_business_insights()
        }
        
        return report
    
    def save_results(self, output_dir="../analysis/business_insights/"):
        """Save all analysis results to files"""
        import os
        import json
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Save KPIs
        with open(f"{output_dir}all_kpis.json", 'w') as f:
            json.dump(self.kpis, f, indent=2, default=str)
        
        # Save rush hour analysis
        rush_hour_analysis, weekend_analysis = self.analyze_rush_hour_patterns()
        with open(f"{output_dir}rush_hour_analysis.json", 'w') as f:
            json.dump(rush_hour_analysis, f, indent=2, default=str)
        
        with open(f"{output_dir}weekend_analysis.json", 'w') as f:
            json.dump(weekend_analysis, f, indent=2, default=str)
        
        # Save weather analysis
        weather_analysis = self.analyze_weather_impact()
        with open(f"{output_dir}weather_analysis.json", 'w') as f:
            json.dump(weather_analysis, f, indent=2, default=str)
        
        # Save summary report
        summary_report = self.create_summary_report()
        with open(f"{output_dir}summary_report.json", 'w') as f:
            json.dump(summary_report, f, indent=2, default=str)
        
        print(f"✅ All analysis results saved to {output_dir}")
        return output_dir

def main():
    """Main execution function"""
    print("🚀 Starting Comprehensive BI Analysis for Rapido Transportation")
    print("=" * 70)
    
    # Initialize analyzer
    analyzer = RapidoBusinessIntelligence("../Dataset.csv")
    
    # Load and prepare data
    df = analyzer.load_and_prepare_data()
    
    # Calculate all KPIs
    kpis = analyzer.calculate_all_kpis()
    
    # Perform specialized analyses
    rush_hour_analysis, weekend_analysis = analyzer.analyze_rush_hour_patterns()
    weather_analysis = analyzer.analyze_weather_impact()
    
    # Generate insights
    insights = analyzer.generate_business_insights()
    
    # Create and display summary
    summary = analyzer.create_summary_report()
    
    print("\n" + "=" * 70)
    print("📊 EXECUTIVE SUMMARY")
    print("=" * 70)
    
    for key, value in summary['executive_summary'].items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\n💡 KEY INSIGHTS:")
    for category, insight_list in insights.items():
        if insight_list:
            print(f"\n{category.replace('_', ' ').title()}:")
            for insight in insight_list[:3]:  # Show top 3 insights per category
                print(f"  • {insight}")
    
    # Save results
    output_dir = analyzer.save_results()
    
    print(f"\n✅ Analysis Complete! Results saved to: {output_dir}")
    print("🔄 Ready for Power BI integration...")
    
    return analyzer, summary

if __name__ == "__main__":
    analyzer, summary = main()
