import _import_handler
import os
import dash
from dash import dcc, html, ClientsideFunction
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import re
import base64
from dash import ctx
from natsort import natsorted
import datetime
import random
import json
import dash_draggable
from PIL import Image
import threading
import numpy as np
import plotly.express as px
import csv
from convolution import *
from utils.shadow_model_generator import get_dum_pred_from_f1 as get_shadow





def pattern_match_score_2d(matrix, pattern):
    nrows, ncols = matrix.shape
    p_rows, p_cols = pattern.shape
    scores = []

    # Ensure the pattern can actually fit within the matrix
    if nrows < p_rows or ncols < p_cols:
        return scores
    
    for i in range(nrows - p_rows + 1):
        for j in range(ncols - p_cols + 1):
            submatrix = matrix[i:i+p_rows, j:j+p_cols]
            # Calculate match count
            match_count = np.sum(submatrix == pattern)
            scores.append(((i, j), match_count))
    
    return scores




# Load the modified CSV file
df = pd.read_csv('../Logs/trimmed_logs/all_mod.csv')
# df = df[df['participant'] == 'P12']
max_frames = 16
# Print each row
# for index, row in df.iterrows():
#     print(row['participant'])
# print(df)


DATA_DIR = '/Users/touhidshohan/Desktop/Others/Dashboard-For-VQA/Dashboard Data - New/'
base_folder = DATA_DIR

all_rows = [name_row]

for index, row in df.iterrows():
    score = row['score']
    normalized_score_mc = row['normalized_score_mc']
    normalized_score = row['normalized_score']

    model = row['model left']
    selected_file = row['video']
    see_textarea_value = row['see'].split(',')
    see_textarea_value_lower = [item.lower() for item in see_textarea_value]

    if model == 'Ground Truth':
        model = 'GT_N'



    if '@' in model:  
        random.seed(200)
        shadow_model_df = get_shadow(
                    os.path.join(base_folder, 'GT_N', f'{selected_file}.csv'),
                    row['F1-Base'], 1, see_textarea_value_lower, limit_frame_count=max_frames+1
                )[0]
        y_labels = list(shadow_model_df.iloc[:, 0])
        z_values = shadow_model_df.iloc[:, 1:].values.tolist()

    else:      
        file_path = os.path.join(base_folder, model, selected_file + '.csv')
        heat_map_file = pd.read_csv(file_path)

        y_labels = list(heat_map_file.iloc[:159, 0])
        z_values = heat_map_file.iloc[:159, 1:].values.tolist()


    for i in range(len(z_values)):
        for j in range(len(z_values[i])):
            if z_values[i][j] == -1:
                z_values[i][j] = 0



    filtered_indices_see = [i for i, label in enumerate(y_labels) if label.lower() in see_textarea_value_lower]

    filtered_indices = filtered_indices_see
    y_labels_filtered = []
    z_values_filtered = []

    for i in filtered_indices:
        if i != -1:
            y_labels_filtered.append(y_labels[i])
            z_values_filtered.append(z_values[i])

    y_labels = y_labels_filtered
    z_values = z_values_filtered

    y_labels = y_labels[:max_frames]
    z_values = z_values[:max_frames]


    sorted_indices = sorted(range(len(y_labels)), key=lambda k: not y_labels[k].startswith('*'))

    y_labels = [y_labels[i] for i in sorted_indices]
    z_values = [z_values[i] for i in sorted_indices]

    y_labels.reverse()
    z_values.reverse()

    matrix = np.array(z_values)
    csv_row = []
    for kernel_output_combo in all_kernels:
        kernel = kernel_output_combo[0]
        expected_output = kernel_output_combo[2]

        convolution_result = pattern_match_score_2d(matrix, kernel)

        # print(convolution_result[0][1])

        # matches = convolution_result == expected_output

        # rows = len(matches)
        # columns = len(matches[0])

        count = 0

        # print(matches)

        for i in range(len(convolution_result)):
            if convolution_result[i][1] == expected_output:
                count += 1


        print(count, end =' ')
        csv_row.append(count)

    csv_row.append(score)
    csv_row.append(normalized_score_mc)
    csv_row.append(normalized_score)

    all_rows.append(csv_row)


with open('output.csv', "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for row in all_rows:
        writer.writerow(row)    