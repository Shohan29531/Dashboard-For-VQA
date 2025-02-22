import os
import pandas as pd

input_dir = 'C:/Users/Touhid Shohan/Downloads/GT/Ground_Truth_Annotation'
output_dir = 'C:/Users/Touhid Shohan/Downloads/GT/Outputs'
predefined_list_file = 'all_a11y_objects.txt'

with open(predefined_list_file, 'r') as file:
    predefined_list = [item.strip() for item in file.read().split(',')]

xlsx_files = [f for f in os.listdir(input_dir) if f.endswith('.xlsx')]


for xlsx_file in xlsx_files:
    xlsx_path = os.path.join(input_dir, xlsx_file)
    csv_file = os.path.splitext(xlsx_file)[0].replace('_', '-') + '.csv'
    csv_path = os.path.join(output_dir, csv_file)

    df = pd.read_excel(xlsx_path)

    new_column_names = [col.replace('frame_', 'Frame-') if col.startswith('frame_') else col for col in df.columns]
    df.columns = new_column_names

    df['Object'] = df['Object'].apply(lambda item: next((obj for obj in predefined_list if obj.lower() == item.lower()), item))

    df = df[df['Object'].str.lower().isin(item.lower() for item in predefined_list)]

    df.to_csv(csv_path, index=False)

    print(f'Converted {xlsx_file} to {csv_file}')
