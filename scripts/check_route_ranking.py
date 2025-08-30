import pandas as pd
import numpy as np

# Load the data
df = pd.read_excel('d:/Data/Github/SheldonC2005/BI-Project/power_bi/data_model/rapido_dashboard_data.xlsx', sheet_name='FactRides')

# Calculate revenue by route and rank them
route_revenue = df.groupby('route').agg({
    'final_price': ['sum', 'count'],
    'base_price': 'sum'
}).round(2)

route_revenue.columns = ['Total_Revenue', 'Total_Trips', 'Base_Revenue']
route_revenue['Revenue_Rank'] = route_revenue['Total_Revenue'].rank(ascending=False, method='min').astype(int)

# Sort by revenue to see the ranking
route_revenue_sorted = route_revenue.sort_values('Total_Revenue', ascending=False)

print('=== TOP 10 ROUTES BY REVENUE ===')
print(route_revenue_sorted.head(10)[['Total_Revenue', 'Total_Trips', 'Revenue_Rank']])
print(f'\nTotal routes: {len(route_revenue_sorted)}')
print(f'Total revenue across all routes: ₹{route_revenue_sorted["Total_Revenue"].sum():,.2f}')

# Check if all rank 1 routes have the same revenue
top_routes = route_revenue_sorted[route_revenue_sorted['Revenue_Rank'] == 1]
print(f'\n=== ROUTES WITH RANK 1 ===')
print(f'Number of routes with rank 1: {len(top_routes)}')
print(top_routes[['Total_Revenue', 'Total_Trips', 'Revenue_Rank']])

# Show some examples of different ranks
print(f'\n=== SAMPLE OF DIFFERENT RANKS ===')
sample_ranks = route_revenue_sorted.head(15)[['Total_Revenue', 'Revenue_Rank']]
print(sample_ranks)
