import pandas as pd
import glob
import os


model_name = 'GT_N'

# Specify the input and output folders containing CSV files
input_folder_path = 'E:/Projects/Dashboard-For-VQA/Dashboard Data/' + model_name + '/'
output_folder_path = 'E:/Projects/Dashboard-For-VQA/Dashboard Data - New/' + model_name + '/'

# Get a list of all CSV files in the input folder
csv_files = glob.glob(input_folder_path + '*.csv')

# Iterate over each CSV file
for csv_file in csv_files:
    # Load the CSV file
    df = pd.read_csv(csv_file)

    # Get the list of columns dynamically
    columns = df.columns

    # Create a list to store the modified rows
    modified_rows = []

    # Iterate through each row in the original DataFrame
    for index, row in df.iterrows():
        # Create a new row with '+' sign added to the object's name
        new_row_plus = row.copy()
        new_row_plus['Object'] = new_row_plus['Object']
        modified_rows.append(new_row_plus)

        # Create a new row with '-' sign added to the object's name and all columns flipped
        new_row_minus = row.copy()

        new_row_minus['Object'] = '*' + new_row_minus['Object'][0].upper() + new_row_minus['Object'][1:]
        new_row_minus[columns[1:]] = new_row_minus[columns[1:]]
        modified_rows.append(new_row_minus)

    # Create a new DataFrame from the modified rows
    new_df = pd.DataFrame(modified_rows)

    # Save the modified DataFrame to a new CSV file in the output folder
    output_file_path = os.path.join(output_folder_path, os.path.basename(csv_file))
    new_df.to_csv(output_file_path, index=False)
