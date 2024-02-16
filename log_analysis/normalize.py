import pandas as pd

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Define a function for min-max normalization
def min_max_normalize(series):
    return (series - series.min()) / (series.max() - series.min())

# Apply min-max normalization for each participant separately
df['normalized_score'] = df.groupby('participant')['score'].transform(min_max_normalize)

# Save the modified dataframe to a new CSV file
df.to_csv('../Logs/trimmed_logs/all_normalized.csv', index=False)