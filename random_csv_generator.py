import os
import pandas as pd
import random

input_dir = '/Users/imrankabir/Desktop/research/vqa_accessibility/Dashboard-For-VQA/Dashboard Data/GT'
output_dir = '/Users/imrankabir/Desktop/research/vqa_accessibility/Dashboard-For-VQA/Dashboard Data/Random'
predefined_list_file = 'all_a11y_objects.txt'

random.seed(42)

with open(predefined_list_file, 'r') as file:
    predefined_list = [item.strip() for item in file.read().split(',')]

xlsx_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]

for xlsx_file in xlsx_files:
    xlsx_path = os.path.join(input_dir, xlsx_file)
    csv_file = os.path.splitext(xlsx_file)[0].replace('_', '-') + '.csv'
    csv_path = os.path.join(output_dir, csv_file)

    df = pd.read_csv(xlsx_path)

    new_column_names = [col.replace('frame_', 'Frame-') if col.startswith('frame_') else col for col in df.columns]
    df.columns = new_column_names

    df['Object'] = df['Object'].apply(lambda item: next((obj for obj in predefined_list if obj.lower() == item.lower()), item))

    for col in new_column_names[1:]:
        df[col] = [random.choice([0, 1]) for _ in range(len(df))]

    df.to_csv(csv_path, index=False)

    print(f'Converted {xlsx_file} to {csv_file}')
