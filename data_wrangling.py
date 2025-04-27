import pandas as pd

file_path = 'data/cdi.csv' 
df = pd.read_csv(file_path)

print(df.columns)


# Load the data


# 1. Standardize column names (remove spaces and lower case)
df.columns = df.columns.str.strip().str.lower()

# 2. Handle missing values
# Replace blank strings with NaN
df.replace('', pd.NA, inplace=True)

# 3. Convert numeric columns to proper types
numeric_cols = [
    'datavalue', 'datavaluealt', 'lowconfidencelimit', 'highconfidencelimit',
    'locationid'
]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
#parsing geolocation column to be a lat and long not just one string
def location(geo):
    if pd.isna(geo):
        return pd.Series({'latitude': None, 'longitude': None})
    try:
        geo = geo.replace('POINT (', '').replace(')', '')
        lon, lat = map(float, geo.split())
        return pd.Series({'latitude': lat, 'longitude': lon})
    except(ValueError, TypeError): # exception to handle issues (unused)
        return pd.Series({'latitude': None, 'longitude': None})

geo_split = df['geolocation'].apply(location)
df = pd.concat([df, geo_split], axis=1)

df.drop(columns=['geolocation'], inplace=True)

# 6. Optional: Fill missing values for statification with general population. 
strat_cols = ['stratification1', 'stratification2', 'stratification3']
df[strat_cols] = df[strat_cols].fillna('General Population')

df.reset_index(drop=True, inplace=True)

print(df.head())
df.to_csv('data/clean_cdi.csv', index=False)
