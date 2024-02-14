import pandas as pd

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Define the expertise levels for each participant
expertise_levels = {
    'P1': 'High', 'P5': 'High', 'P11': 'High', 'P12': 'High',
    'P3': 'Moderate', 'P6': 'Moderate', 'P7': 'Moderate', 'P10': 'Moderate',
    'P2': 'Low', 'P4': 'Low', 'P8': 'Low', 'P9': 'Low', 'P13': 'Low',
}

# Add the 'expertise' column based on participant values
df['expertise'] = df['participant'].map(expertise_levels)

# Save the modified DataFrame to the same CSV file
df.to_csv('../Logs/trimmed_logs/all.csv', index=False)