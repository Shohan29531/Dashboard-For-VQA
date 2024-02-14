import os
import pandas as pd

# Specify the folder path containing trimmed CSV files
output_path = '../Logs/trimmed_logs/'

# Initialize an empty DataFrame to store concatenated data
concatenated_df = pd.DataFrame()

# Iterate through all CSV files in the folder
for file_name in os.listdir(output_path):
    if file_name.endswith('.csv'):
        # Construct the full path to the CSV file
        file_path = os.path.join(output_path, file_name)

        # Read the CSV file
        df = pd.read_csv(file_path)

        # Concatenate the current DataFrame to the overall DataFrame
        concatenated_df = pd.concat([concatenated_df, df], ignore_index=True)

# Convert 'participant' column to categorical with a custom order
participant_order = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12', 'P13']
concatenated_df['participant'] = pd.Categorical(concatenated_df['participant'], categories=participant_order, ordered=True)

# Sort the DataFrame by the 'participant' column
concatenated_df.sort_values('participant', inplace=True)

# Specify the path for the new CSV file containing all rows
all_rows_file_path = os.path.join(output_path, 'all.csv')

# Save the sorted DataFrame to a new CSV file
concatenated_df.to_csv(all_rows_file_path, index=False)
