import pandas as pd

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Define a function for Z normalization using range in the denominator
def z_normalize(series):
    return (series - series.mean()) / (series.std())

# Apply Z normalization for each participant separately
df['normalized_score'] = df.groupby('participant')['score'].transform(z_normalize)

# Save the modified dataframe to a new CSV file
df.to_csv('../Logs/trimmed_logs/all.csv', index=False)