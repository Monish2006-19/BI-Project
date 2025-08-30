import pandas as pd

# Load and check dataset
df = pd.read_csv('../Dataset.csv')

print('Dataset columns:')
print(df.columns.tolist())
print('\nFirst few rows:')
print(df.head())
print(f'\nDataset shape: {df.shape}')

# Check for route-related columns
route_cols = [col for col in df.columns if 'route' in col.lower() or 'from' in col.lower() or 'to' in col.lower()]
print(f'\nRoute-related columns: {route_cols}')
