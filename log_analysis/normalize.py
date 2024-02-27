import pandas as pd

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Define a function for Z normalization using range in the denominator
def z_normalize(series):
    return (series - series.mean())

def min_max_normalize(series):
    return (series - series.min()) / (series.max() - series.min())
 
# Apply Z normalization for each participant separately
df['normalized_score_mc'] = df.groupby('participant')['score'].transform(z_normalize)


df['normalized_score'] = df['normalized_score_mc'].transform(min_max_normalize)

# df['normalized_score'] = df.groupby('participant')['score'].transform(min_max_normalize)

# Save the modified dataframe to a new CSV file
df.to_csv('../Logs/trimmed_logs/all.csv', index=False)