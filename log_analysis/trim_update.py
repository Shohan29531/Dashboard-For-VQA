import os
import pandas as pd

# Specify the folder path containing CSV files
folder_path = '../Logs/all_user_log/'

output_path = '../Logs/trimmed_logs/'

# Define the mapping of participant names to expertise levels
expertise_mapping = {
    'P1': 'Expert', 'P4': 'Expert', 'P5': 'Expert', 'P11': 'Expert', 'P12': 'Expert', 'P14': 'Expert', 'P15': 'Expert',
    'P2': 'Non-Expert', 'P3': 'Non-Expert', 'P6': 'Non-Expert',
    'P7': 'Non-Expert', 'P8': 'Non-Expert', 'P9': 'Non-Expert', 'P10': 'Non-Expert', 'P13': 'Non-Expert'
}

# Iterate through all CSV files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        # Construct the full path to the CSV file
        file_path = os.path.join(folder_path, file_name)

        # Read the CSV file
        df = pd.read_csv(file_path)

        # Convert timestamp column to datetime format
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d::%H:%M:%S', errors='coerce')

        # Calculate the timing as the difference between consecutive timestamps
        df['timing'] = (df['timestamp'] - df['timestamp'].shift(1)).dt.total_seconds().fillna(0)

        # Set the first row of 'timing' to the second-row value plus 60
        df.at[0, 'timing'] = df.at[1, 'timing'] + 60

        # Count the number of items in the 'see' column
        df['see_count'] = df['see'].apply(lambda x: len(str(x).split(',')))

        # Drop specified columns
        columns_to_drop = ['winner model', 'not_see', 'comments', 'mode', 'model right']
        df = df.drop(columns=columns_to_drop, errors='ignore')

        # Move the 'see' column to the last position
        df = df[[col for col in df.columns if col != 'see'] + ['see']]

        df = df.drop(columns=['timestamp'], errors='ignore')

        df.insert(0, 'participant', file_name.replace('.csv', ''))

        df.insert(1, 'trial', range(1, len(df) + 1))

        df['score'] = df['score'] / 10

        # Add the 'expertise' column based on participant names
        df['expertise'] = df['participant'].map(expertise_mapping)

        # Replace 'Novice/Intermediate' with 'Non-Expert' in the 'expertise' column
        df['expertise'] = df['expertise'].replace('Novice/Intermediate', 'Non-Expert')

        # Replace 'GT_N' in 'model left' with 'Ground Truth'
        df['model left'] = df['model left'].replace('GT_N', 'Ground Truth')

        # Specify the path for the new CSV file
        new_file_path = os.path.join(output_path, f'{file_name}')

        # Save the modified DataFrame to a new CSV file
        df.to_csv(new_file_path, index=False)
