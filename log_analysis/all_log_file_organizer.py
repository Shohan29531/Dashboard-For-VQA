import pandas as pd

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Define a function to strip +, -, or * from the beginning of items
def strip_characters(cell):
    # Split the string into items based on comma
    items = cell.split(',')
    # Strip leading +, -, or * from each item
    stripped_items = [item.lstrip('+-*') for item in items]
    # Join the modified items back into a comma-separated string
    return ','.join(stripped_items)

# Apply the function to the 'see' column
df['see'] = df['see'].apply(strip_characters)

# Save the modified DataFrame to a new CSV file
df.to_csv('../Logs/trimmed_logs/all_mod.csv', index=False)
