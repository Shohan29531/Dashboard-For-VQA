import pandas as pd

# Load the CSV file
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Replace 'GT_N' with 'Ground Truth' in the 'model left' column
df['model left'] = df['model left'].replace('GT_N', 'Ground Truth')

# Divide all values in the 'score' column by 10
df['score'] = df['score'] / 10

# Save the modified DataFrame back to the CSV file
df.to_csv('../Logs/trimmed_logs/all_modified.csv', index=False)
