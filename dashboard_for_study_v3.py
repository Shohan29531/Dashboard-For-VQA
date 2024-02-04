import os
import dash
from dash import dcc, html
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
from copy import deepcopy
import platform
from utils.obj_select import get_obj_list
from utils.get_prec_rec_f1 import calculate_model_ap_ar_af1 as get_f1
from utils.shadow_model_generator import get_dum_pred_from_f1 as get_shadow

PARTICIPANT_NAME = "Dummy"


class ImageViewerThread(threading.Thread):

    def __init__(self, image):
        super().__init__()
        self.image = image
        threading.Thread.__init__(self)

    def run(self):
        os_name = platform.system()
        print(os_name)
        if os_name == "Windows":
            os.system(f'start "" "{self.image}"')
        else:
            os.system(f'open "{self.image}"')

        #  arrow symbol copied from here: https://www.i2symbol.com/symbols/arrows


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Dashboard Data')
GROUND_TRUTH_DATA = os.path.join(DATA_DIR, 'GT')
IMAGE_DATA_DIR = os.path.join(DATA_DIR, 'Images')
LOG_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Logs')

base_folder = DATA_DIR
images_source_folder = IMAGE_DATA_DIR
files = os.listdir(GROUND_TRUTH_DATA)
all_video_files = [os.path.splitext(file)[0] for file in files if file.endswith(".csv")]
all_video_files = natsorted(all_video_files)

ignore_video = ['video-5', 'video-8', 'video-9', 'video-10']
ignore_video += ['video-'+str(i) for i in range(17, 25)]

ignore_vid_seg = []

for vid in all_video_files:
    for v in ignore_video:
        if v in vid:
            ignore_vid_seg.append(vid)
            break

for vid in ignore_vid_seg:
    del all_video_files[all_video_files.index(vid)]    

available_models = [
    'GPV-1',
    'GPV-1@Shadow',
    'BLIP',
    'BLIP@Shadow',
    'GPT4V',
    'GPT4V@Shadow',
    'GT_N',
    'Random'
]

shadow_models = [
    'GPV-1@Shadow',
    'BLIP@Shadow',
    'GPT4V@Shadow'
]

comparison_types = ['One Model', 'Two Models']
heatmap_types = ['Objects I See', 'Objects I do not See', 'Both']

# a global log file contains the following columns: timestamp, video, model, score, comments

COLUMNS = ['timestamp', 'video', 'model left', 'model right', 'winner model', 'see', 'not_see', 'score', 'comments','mode', 'F1-Base', 'F1-Shadow']

# default values
current_model = 'Model-0'  # 'GPV-1'
current_model_right = ""
current_file = 'video-1-segment-5'  # 'video-1-segment-5'
# current_text_see = ['Wall', 'Bicycle', 'Bridge', 'Building', 'Bus', 'Bus Stop']
# current_text_not_see = ['Guide dog', 'Gutter', 'Hose', 'Lamp Post', 'Mail box']
# current_text_see = ['Person', 'White Cane', 'Car', 'Road']
current_text_see = []
current_text_not_see = []
current_rating = 5
current_text_comments = ''
current_heatmap_type = 'Objects I See'
f1_model = 0.0
f1_shadow_model = 0.0

observe_typ = 'single'

best_model_side = ''

num_frames = 100
max_frames = 16
heatmap_highlight_line_width = 5

fixed_heatmap_height = 350
fixed_heatmap_width = 500
heatmap_x_axis_title = 'Frame'

color_white = 'rgb(255,255,255)'  # white
color_agreement = 'rgb(6, 200, 115)'  # green
color_disagreement = 'rgb(211, 6, 50)'  # red

completed_comparison = []
completed_videos = []

unchecked_image_ids = []

heatmap_1_clicks = []

bargraph_data = []

present_model = ''
present_selected_file = ''
first_test = True
last_entry = []

click_log_style = {
    'width': '100%',
    'height': '230px',
    'margin-top': '33pt',
    'fontSize': '12px',
    'color': 'gray',
}

bargraph_style = {
    'width': '80%',
    'height': '230px',
    'margin': 'auto',
    'fontSize': '12px',
    'color': 'gray',
}

models_to_show, reverse_model_map = [], []

coco_common_obj = ['Person', 'Bicycle', 'Car', 'Motorcycle', 'Bus', 'Traffic Signals', 'Fire hydrant', 'Stop sign'
                                                                                                       'Bench', 'Dog',
                   'Chair', 'Vegetation']

pfb_common_obj = ['Road', 'Sidewalk', 'Tree', 'Vegetation', 'Building', 'Fence', 'Traffic Signals',
                  'Fire hydrant', 'Chair', 'Trash on roads', 'Trash bins', 'Person', 'Car', 'Motorcycle',
                  'Bus']

reduce_object_model_coco = ['faster_rcnn', 'mask_rcnn', 'yolo_v7']
reduce_object_model_pfb = ['HRNet_V2']

non_ex_obj = 2
ex_obj = 4
tot_obj = 6
all_rand_obj = False

auto_select_button_style = {'background-color': 'lightgray', 'margin': 'auto', 'display': 'none'}


def randomize_data():
    random.seed(100)
    random_model = random.sample(range(0, len(available_models)), len(available_models))
    # a dictionary that maps model-{} to available models randomly
    global models_to_show, reverse_model_map
    models_to_show = {}
    reverse_model_map = {}
    for i in range(len(available_models)):
        models_to_show['Model-{}'.format(i)] = available_models[random_model[i]]
        reverse_model_map[available_models[random_model[i]]] = 'Model-{}'.format(i)



randomize_data()

def get_done_pairs(csv_path):
    df = pd.read_csv(csv_path)

    comp_df = df.loc[df['mode'] == 'double']

    done_pairs = []

    for _, row in comp_df.iterrows():
        left_model = row['model left']
        right_model = row['model right']
        video = row['video']
        if f'{left_model} vs {right_model}' not in done_pairs or \
                f'{right_model} vs {left_model}' not in done_pairs:
            done_pairs.append(f'{left_model} vs {right_model} in {video}')
            done_pairs.append(f'{right_model} vs {left_model} in {video}')

    return done_pairs


def get_done_models_vid(csv_path):
    df = pd.read_csv(csv_path)

    comp_df = df.loc[df['mode'] == 'single']

    done_setup = []
    done_videos = []

    for _, row in comp_df.iterrows():
        left_model = row['model left']
        video = row['video']
        if f'{left_model} in {video}' not in done_setup:
            done_setup.append(f'{left_model} in {video}')

        if video not in done_videos:
            done_videos.append(video)

    return done_setup, done_videos


user_log_path = os.path.join(LOG_DATA_DIR, PARTICIPANT_NAME + '.csv')

# if os.path.exists(user_log_path):
#     completed_comparison, completed_videos = get_done_models_vid(user_log_path)



def save_log_file(new_row):
    global completed_comparison, completed_videos
    log_file = user_log_path  # os.path.join(LOG_DATA_DIR, PARTICIPANT_NAME + '.csv')
    print(log_file, LOG_DATA_DIR)

    if os.path.exists(log_file):
        df = pd.read_csv(log_file)
        df.loc[len(df)] = new_row
        # df = df.append(df_new, ignore_index=True)
        df.to_csv(log_file, index=False)
    else:
        df_log = pd.DataFrame(new_row, columns=COLUMNS, index=[0])
        df_log.to_csv(log_file, index=False)

    completed_comparison, completed_videos = [], []
    #get_done_models_vid(log_file)


def read_text_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def get_vetical_axis_lines(x_labels):
    vertical_lines = []

    for i in range(len(x_labels)):
        vertical_lines.append({
            'type': 'line',
            'x0': i / len(x_labels),
            'x1': i / len(x_labels),
            'y0': 0,
            'y1': 1,
            'xref': 'paper',
            'yref': 'paper',
            'line': {
                'color': 'black',
                'width': 1,
            },
            'opacity': 0.5
        })

    return vertical_lines


def get_horizontal_axis_lines(y_labels):
    horizontal_lines = []

    for i in range(len(y_labels) + 1):
        horizontal_lines.append({
            'type': 'line',
            'x0': 0,
            'x1': 1,
            'y0': i / len(y_labels),
            'y1': i / len(y_labels),
            'xref': 'paper',
            'yref': 'paper',
            'line': {
                'color': 'black',
                'width': 1,
            },
            'opacity': 0.5
        })

    return horizontal_lines


def get_heatmap_highlight_lines_from_heatmap_click(x_labels, y_labels, x_coord, y_coord):
    if y_coord not in y_labels:
        return []

    y_coord_index = y_labels.index(y_coord)

    highlight_lines = []

    highlight_lines.extend([
        {
            'type': 'line',
            'x0': 0,
            'x1': 1,
            'y0': y_coord_index - 0.5,
            'y1': y_coord_index - 0.5,
            'xref': 'paper',
            'yref': 'y',
            'line': {
                'color': 'yellow',
                'width': heatmap_highlight_line_width,
            },
            'opacity': 1
        },
        {
            'type': 'line',
            'x0': 0,
            'x1': 1,
            'y0': y_coord_index + 0.5,
            'y1': y_coord_index + 0.5,
            'xref': 'paper',
            'yref': 'y',
            'line': {
                'color': 'yellow',
                'width': heatmap_highlight_line_width,
            },
            'opacity': 1
        },
        {
            'type': 'line',
            'x0': float(x_coord) - 0.5,
            'x1': float(x_coord) - 0.5,
            'y0': 0,
            'y1': 1,
            'xref': 'x',
            'yref': 'paper',
            'line': {
                'color': 'yellow',
                'width': heatmap_highlight_line_width,
            },
            'opacity': 1
        },
        {
            'type': 'line',
            'x0': float(x_coord) + 0.5,
            'x1': float(x_coord) + 0.5,
            'y0': 0,
            'y1': 1,
            'xref': 'x',
            'yref': 'paper',
            'line': {
                'color': 'yellow',
                'width': heatmap_highlight_line_width,
            },
            'opacity': 1
        },
    ])

    return highlight_lines


def get_heatmap_highlight_lines_from_image_container_click(x_coord):
    highlight_lines = []

    highlight_lines.extend([
        {
            'type': 'line',
            'x0': float(x_coord) - 0.5,
            'x1': float(x_coord) - 0.5,
            'y0': 0,
            'y1': 1,
            'xref': 'x',
            'yref': 'paper',
            'line': {
                'color': 'yellow',
                'width': heatmap_highlight_line_width,
            },
            'opacity': 1
        },
        {
            'type': 'line',
            'x0': float(x_coord) + 0.5,
            'x1': float(x_coord) + 0.5,
            'y0': 0,
            'y1': 1,
            'xref': 'x',
            'yref': 'paper',
            'line': {
                'color': 'yellow',
                'width': heatmap_highlight_line_width,
            },
            'opacity': 1
        },
    ])

    return highlight_lines


def get_see_text(model_name):
    title = "Objects you SEE that " + "<span style='color:blue;'>" + model_name + "</span>" + " also SEEs (" + "<span style='color:rgb(6, 200, 115);'>" + "green, agreement" + "</span>" + ") <br> and that the model DOESN'T SEE (" + "<span style='color:rgb(211, 6, 50);'>" + "red, disagreement" + "</span>" + ") "

    return title


def get_dont_see_text(model_name):
    title = "Objects you DON'T SEE that " + "<span style='color:blue;'>" + model_name + "</span>" + " also DOESN'T SEE (" + "<span style='color:rgb(6, 200, 115);'>" + "green, <br> agreement" + "</span>" + ") and that the model does SEE (" + "<span style='color:rgb(211, 6, 50);'>" + "red, disagreement" + "</span>" + ") "

    return title


suggestions = read_text_file_content('all_a11y_objects.txt').split(', ')

# css framework for layout and style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

# create the dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)


all_tasks = ['Multi-Object Classification in Video']


# top row layout
top_row = html.Div(
    [
        # random button
        html.Div(
            [
                html.Button(
                    'Randomize Models',
                    id='random-button',
                    n_clicks=0,
                    style={'background-color': 'lightgray', 'display': 'none'}
                )
            ], className='row'
        ),

        # model dropdown
        html.Div([
            dcc.Dropdown(
                id='model-dropdown',
                options=[{'label': model, 'value': model} for model in models_to_show],
                placeholder='Select a Model',
                value=current_model,
                clearable=False,
                style={'border-color': 'gray'}
            )], className='three columns'
        ),

        # html.Div([
        # 		# empty
        # 	], className = 'one column'
        # ),

        html.Div([
            dcc.Dropdown(
                id='task-dropdown',
                options=[{'label': option, 'value': option} for option in all_tasks],
                placeholder='Select a Task...',
                value='Multi-Object Classification in Video',
                style={'border-color': 'gray'}
            )],
            className='four columns'
        ),

        html.Div([
            dcc.Dropdown(
                id='video-dropdown',
                options=[{'label': option, 'value': option} for option in all_video_files],
                placeholder='Select a video file...',

                style={'border-color': 'gray'}
            )],
            className='three columns'
        ),

        html.Div([
            dcc.Store(id='current-second-model'),
            dcc.Dropdown(
                id='model-dropdown-2',
                options=[{'label': model, 'value': model} for model in []],
                placeholder='Select Another Model to Comapre',
                value=None,
                style={'border-color': 'gray', 'display': 'none'}
            )
        ], className=''
        ),

        ## select the types of objects for which you wish to see the heatmaps
        html.Div([
            dcc.Dropdown(
                id='heatmap-type-dropdown',
                options=[{'label': option, 'value': option} for option in heatmap_types[:1]],
                placeholder='I wish to see the model results for...',
                value=heatmap_types[0],
                style={'border-color': 'gray', 'display': 'none'}
            )],
            className='row'
        ),

        # I don't see text area
        html.Div([
            dcc.Markdown(children='*Objects I **don\'t see** in the video:*',
                         id='I-dont-see-markdown'),
            dcc.Dropdown(
                id='I-dont-see',
                options=[{'label': suggestion, 'value': suggestion} for suggestion in suggestions],
                multi=True,
                value=current_text_not_see,
                placeholder='Things I do not see',
            )
        ], id='I-dont-see-container', className='five columns', style={'background-color': 'rgba(211, 6, 50, 0.5)'}),

    ], className='row',
)

heatmaps = html.Div(
    [

        # I see text area
        html.Div(
            [
                dcc.Markdown(children='**Interesting Objects** in the video:', id='I-see-markdown'),
                dcc.Dropdown(
                    id='I-see',
                    options=[{'label': suggestion, 'value': suggestion} for suggestion in suggestions],
                    multi=True,
                    value=current_text_see,
                    placeholder='Things I see',
                ),

                html.Button(
                    'Auto Select Objects',
                    id='auto-select-obj',
                    n_clicks=0,
                    style=auto_select_button_style
                )

            ],
            id='I-see-container',
            className='three columns',
            style={'background-color': 'rgba(255, 255, 255, 1)'}
        ),

        html.Div(
            [
                dcc.Graph(
                    id='heatmap-1',
                    config={'displayModeBar': False}
                ),
            ], className='four columns', style={}
        ),

        # html.Div([], className='one column'),

        html.Div(
            [
                dcc.Graph(
                    id='bar-graph',
                    style=bargraph_style
                ),
            ], className='three columns'
        ),

        html.Div(
            [
                dcc.Graph(
                    id='heatmap-2',
                    config={'displayModeBar': False}
                ),
            ], className='one column'  # Change to one column
        ),

        # analyze button
        html.Div(
            [
                html.Button(
                    'Analyze',
                    id='update-heatmap-button',
                    n_clicks=0,
                    style={'background-color': 'lightgray', 'display': 'none'}
                )
            ], className='row'
        ),

    ], className='row', style={'margin-right': '0', 'margin-left': '0'}
)

image_modal = dash_draggable.GridLayout(
    id='modal-container',
    style={'display': 'block'},
    children=[
        html.Div(
            id="custom-modal",
            style={
                "display": "none",
                "position": "fixed",
                "top": "0",
                "left": "0",
                "width": "100%",
                "height": "100%",
                "background-color": "rgba(0, 0, 0, 0.7)",
                "overflow": "auto",
                "display": "flex",
                "z-index": 1001,
            },
            children=[
                html.Label(
                    id="modal-frame-label",
                    children="No Frame Selected",
                    style={
                        'position': 'absolute',
                        'top': '10px',
                        'left': '0px',
                        'color': 'blue',
                        'background-color': 'rgb(232, 237, 235)',
                        'padding': '2px',
                        'font-weight': 'bold',
                        'font-size': '16px',
                    }
                ),
                html.Div(
                    style={
                        "max-width": "100%",
                        "max-height": "90vh",
                        "background-color": "white",
                        "border-radius": "5px",
                        "box-shadow": "0px 0px 10px rgba(0, 0, 0, 0.5)",
                        "overflow": "hidden",
                    },
                    children=[
                        html.Div(
                            style={
                                "position": "absolute",
                                "top": "10px",
                                "right": "0px",
                                "cursor": "pointer",
                                "font-size": "20px",
                                "color": "red",
                                "background-color": "white",
                                "border-radius": "50%",
                                "width": "30px",
                                "height": "30px",
                                "display": "flex",
                                "justify-content": "center",
                                "align-items": "center",
                            },
                            children=["❌"],
                            id="close-custom-modal-button",
                        ),
                        dbc.CardImg(id="custom-modal-image", style={"max-width": "100%"}),
                    ],
                )
            ],
        )
    ],
)
# 3rd row: image layout
image_map = html.Div(
    [
        html.Div(
            id='image-container',
            style={'display': 'flex', 'justify-content': 'center', 'flexWrap': 'wrap', 'margin': '0'},
            children=[],
            className='row',
        ),
    ],
)
second_and_third_row = html.Div(
    [
        html.Div(
            [
                heatmaps,
                image_map
            ],
        ),
        dcc.Store(id='last-clicked-image-id'),
    ], className='row'
)
modal_row = html.Div(
    [
        html.Div(
            [
                image_modal
            ],
        ),
    ], className='row'
)
# 4th row: rating layout
rating_row = html.Div(
    [
        # rating slider
        html.Div(
            [
                dcc.Markdown(
                    '''
                        #### Please rate your **Perceived Performance** of this model on a scale from 0 to 10
                        *(0: not good at all; 5: about average; 10: very good):*                    
                    '''),
                dcc.Slider(
                    id="rating-slider",
                    min=0,
                    max=10,
                    step=1,
                    value=5,
                    tooltip={"placement": "bottom", "always_visible": True},
                    # marks = None,
                ),
            ], id="slider-div", className='five columns', style={'display': 'block'}
        ),

        html.Div(
            [
                dcc.Markdown(
                    '''
                        #### Please select the model that performs better between the two selected models                   
                    '''),
                dcc.RadioItems(
                    id="rating-radio-button",
                    options=[
                        {'label': 'Left Model', 'value': 'L'},
                        {'label': 'Right Model', 'value': 'R'},
                        {'label': 'Indistinguishable', 'value': 'E'}
                    ],
                    # marks = None,
                ),
            ], id="radio-button-div", className='five columns', style={'display': 'none'}
        ),

        # raw feedback
        html.Div(
            [
                dcc.Markdown('*Comments (optional):*'),
                dcc.Textarea(
                    id='comments-textarea',
                    value=None,
                    placeholder='Please explain why did you rate the model this way',
                    style={'width': '100%', 'color': 'grey', 'font-style': 'italic'}
                )
            ], className='four columns',
        ),

        # status feedback
        html.Div(
            [
                dcc.Markdown(
                    id='status-textarea',
                    children='*Status:  Not saved*',
                )
            ], className='two columns',
        ),

        # save button
        html.Div(
            [
                html.Button(
                    'Record Response and Resest',
                    id='save-button',
                    n_clicks=0,
                    style={'background-color': 'lightgray'}
                )
            ], className='row'
        ),
    ], className='row'
)
# entire layout
app.layout = html.Div(
    [
        top_row,
        second_and_third_row,
        rating_row,
        dcc.ConfirmDialog(
            id='confirm-danger',
            message='You have already studied this pair, Please try another pair!',
        ),
    ],
)

@app.callback(
    Output(component_id='slider-div', component_property='style', allow_duplicate=True),
    Output(component_id='radio-button-div', component_property='style', allow_duplicate=True),
    Input(component_id='model-dropdown-2', component_property='value'),
    prevent_initial_call=True
)
def hide_show_slider_radio(model_right_pseudonym):
    global observe_typ
    global current_model_right

    current_model_right = model_right_pseudonym

    if model_right_pseudonym in models_to_show:
        observe_typ = 'double'
        return {'display': 'none'}, {'display': 'block'}
    else:
        observe_typ = 'single'
        return {'display': 'block'}, {'display': 'none'}

@app.callback(
    Output('video-dropdown', 'options'),
    Input('model-dropdown', 'value'),
)
def update_video_list(model_left_pseudonym):
    global current_model
    current_model = model_left_pseudonym
    updated_list = []
    for v_ in all_video_files:
        if v_ not in completed_videos:
            updated_list.append({"label": v_, "value": v_})

    if len(updated_list) == 0:
        return dash.no_update
    return updated_list


@app.callback(
    Output('confirm-danger', 'displayed'),
    Input('model-dropdown', 'value'),
    Input('video-dropdown', 'value'),
)
def show_warn(model_left_pseudonym, video_name):
    if model_left_pseudonym is None or model_left_pseudonym == '' or \
            video_name == '' or video_name is None:
        return False
    model_vid_setup = f'{models_to_show[model_left_pseudonym]} in {video_name}'

    prev_log = os.listdir(LOG_DATA_DIR)

    print()

    # print(model_vid_setup, completed_comparison)
    if model_vid_setup in completed_comparison:
        return True
    else:
        return False


@app.callback(
    Output('status-textarea', 'children', allow_duplicate=True),
    Input(component_id='rating-radio-button', component_property='value'),
    prevent_initial_call=True
)
def get_comparing_result(radio_button_value):
    global best_model_side
    print(radio_button_value)
    best_model_side = radio_button_value
    return f"Selected: {best_model_side}, Type: {observe_typ}" if best_model_side else "Rating: None"


@app.callback(
    Output('heatmap-type-dropdown', 'options'),
    Output('current-second-model', 'data'),
    Output('heatmap-1', 'figure', allow_duplicate=True),
    Output('heatmap-2', 'figure', allow_duplicate=True),
    Output('I-see-container', 'style', allow_duplicate=True),
    Output('I-dont-see-container', 'style', allow_duplicate=True),
    Output('heatmap-type-dropdown', 'value'),
    Input('model-dropdown-2', 'value'),
    State('current-second-model', 'data'),
    prevent_initial_call=True

)
def update_heatmap_and_reset_inputs(selected_model, previous_second_model):
    if selected_model is None:
        options = [{'label': option, 'value': option} for option in heatmap_types]

        return options, None, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    else:
        if previous_second_model is None:
            custom_heatmap_types = ['Objects I See', 'Objects I do not See']
            options = [{'label': option, 'value': option} for option in custom_heatmap_types]  # Customize this list

            return options, selected_model, {}, {}, {'display': 'none'}, {'display': 'none'}, None
        else:
            custom_heatmap_types = ['Objects I See', 'Objects I do not See']
            options = [{'label': option, 'value': option} for option in custom_heatmap_types]

            return options, selected_model, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update


# to update the see/don't see input areas based on the heatmap type dropdown
@app.callback(
    Output('I-see-container', 'style'),
    Output('I-see-markdown', 'style'),
    Output('I-see', 'style'),
    Output('I-dont-see-container', 'style'),
    Output('I-dont-see-markdown', 'style'),
    Output('I-dont-see', 'style'),
    Input('heatmap-type-dropdown', 'value'),
)
def update_image_container(
        selected_heatmap_type
):
    selected_heatmap_type = 'Objects I See'
    see_style_original = {'background-color': 'rgba(6, 200, 115, 0.5)'}
    see_style_white = {'background-color': 'white', 'height': '190px', 'margin-top': '60px', 'margin-bottom': '60px',
                       'textAlign': 'center'}
    dont_see_style_original = {'background-color': 'rgba(211, 6, 50, 0.5)'}
    dont_see_style_white = {'background-color': 'white'}

    see_container_style = {'background-color': 'white', 'height': '150px'}

    if selected_heatmap_type == 'Objects I See':
        return see_style_white, {'display': 'block'}, see_container_style, dont_see_style_white, {'display': 'none'}, {
            'display': 'none'}

    elif selected_heatmap_type == 'Objects I do not See':
        return see_style_white, {'display': 'none'}, {'display': 'none'}, dont_see_style_original, {
            'display': 'block'}, {'display': 'block'}

    elif selected_heatmap_type == 'Both':
        return see_style_original, {'display': 'block'}, {'display': 'block'}, dont_see_style_original, {
            'display': 'block'}, {'display': 'block'}

    return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {
        'display': 'none'}


# callback for updating the heatmap
@app.callback(
    Output('heatmap-1', 'style'),
    Input('heatmap-1', 'figure')
)
def show_hide_heatmap_1(heatmap_figure):
    if not heatmap_figure:
        return {'display': 'none'}
    return {'height': '40vh', 'width': '100%'}


@app.callback(
    Output('heatmap-1-clicks-textarea', 'style'),
    Input('heatmap-1', 'clickData')
)
def show_hide_click_log(clickData):
    if clickData:
        return click_log_style
    return {'display': 'none'}


@app.callback(
    Output('bar-graph', 'style'),
    Input('heatmap-1', 'clickData')
)
def show_hide_click_log(clickData):
    ## needs update
    if clickData:
        return bargraph_style
    return {'display': 'none'}


@app.callback(
    Output('heatmap-2', 'style'),
    Input('heatmap-2', 'figure')
)
def show_hide_heatmap_2(heatmap_figure):
    if not heatmap_figure:
        return {'display': 'none'}
    return {'height': '40vh', 'width': '100%'}


def extract_frame_number(filename):
    frame_match = re.search(r"frame-(\d+)\.jpeg", filename)
    if frame_match:
        return int(frame_match.group(1))
    else:
        return 0


def get_encoded_image(image_name):
    image_path = os.path.join(images_source_folder, image_name)
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded_image}"


@app.callback(
    Output("custom-modal", "style"),
    Output("custom-modal-image", "src"),
    Output("custom-modal-image", "alt"),
    Output("modal-frame-label", "children"),
    Output("modal-container", "style"),
    Input('video-dropdown', 'value'),
    Input("close-custom-modal-button", "n_clicks"),
    State('last-clicked-image-id', 'data'),
    [Input({"type": "action-button", "index": ALL}, "n_clicks_timestamp")],
    State({"type": "image-card", "index": ALL}, "id"),
    Input('heatmap-1', 'hoverData'),
    Input('heatmap-2', 'hoverData'),

)
def open_custom_modal_from_button(selected_option,
                                  close_modal_clicks,
                                  last_clicked_image_id,
                                  dummy_1,
                                  dummy_2,
                                  hoverData_heatmap1,
                                  hoverData_heatmap2
                                  ):
    ctx = dash.callback_context

    if "close-custom-modal-button" in ctx.triggered[0]["prop_id"]:
        return {"display": "none"}, "", "", "", {"display": "none"}

    if selected_option and last_clicked_image_id is not None:
        image_names = os.listdir(images_source_folder)
        selected_option = selected_option.lower()
        image_names = [img.lower() for img in image_names]

        filtered_images = [img.strip() for img in image_names if img.startswith(selected_option)]
        filtered_images.sort(key=extract_frame_number)
        filtered_images = filtered_images[:max_frames]

        popup_button_index = last_clicked_image_id
        print("popup_button_index", popup_button_index)
        image_name = filtered_images[popup_button_index]

        return {"display": "block"}, get_encoded_image(image_name), image_name, "Frame " + str(last_clicked_image_id), {
            "display": "block"}

    trigger = ctx.triggered_id
    x_coord, y_coord = None, None
    if trigger == 'heatmap-1' or trigger == 'heatmap-2' and selected_option:
        if trigger == 'heatmap-1':
            hovered_point = hoverData_heatmap1['points'][0]
            x_coord = str(hovered_point['x']).lower()
            y_coord = hovered_point['y']
        elif trigger == 'heatmap-2':
            hovered_point = hoverData_heatmap2['points'][0]
            x_coord = str(hovered_point['x']).lower()
            y_coord = hovered_point['y']
        else:
            x_coord, y_coord = None, None

        image_names = os.listdir(images_source_folder)
        selected_option = selected_option.lower()
        image_names = [img.lower() for img in image_names]

        filtered_images = [img.strip() for img in image_names if img.startswith(selected_option)]

        filtered_images.sort(key=extract_frame_number)

        filtered_images = filtered_images[:max_frames]

        for image_name in filtered_images:

            frame_number = extract_frame_number(image_name)

            if x_coord is not None and int(frame_number) == int(x_coord):
                return {"display": "block"}, get_encoded_image(image_name), image_name, "Frame " + str(frame_number), {
                    "display": "block"}

        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, {"display": "block"}

    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, {"display": "block"}


def get_image_card(image_name, frame_number, is_selected, is_unchecked):
    image_path = os.path.join(images_source_folder, image_name)
    encoded_image = get_encoded_image(image_name)

    border_style = '5px solid yellow' if is_selected else 'none'

    action_button_style = {'position': 'absolute', 'top': '0', 'right': '0', 'width': '100%', 'height': '100%',
                           'margin': '0', 'padding': '0', 'border': 'none', 'background': 'transparent'}

    if is_unchecked:
        action_button_style['display'] = 'none'

    action_button = dbc.Button(
        "",
        color="",
        size="sm",
        id={"type": "action-button", "index": frame_number},
        n_clicks=0,
        style=action_button_style
    )

    frame_number_label = html.Label(
        frame_number,
        style={
            'position': 'absolute',
            'top': '0px',
            'left': '0px',
            'color': 'blue',
            'background-color': 'rgb(232, 237, 235)',
            'padding': '2px',
            'font-weight': 'bold',
            'font-size': '16px'
        }
    )

    overlay_div = html.Div(
        style={'position': 'absolute', 'width': '100%', 'height': '100%',
               'background-color': 'rgba(0, 0, 0, 0.75)' if is_unchecked else 'transparent', 'z-index': 1, 'top': '-0%'}
    )

    image_div = html.Div(
        [
            dbc.CardImg(src=encoded_image, style={'width': '100%'}),
            overlay_div,
            action_button,
            frame_number_label,
        ],
        style={'position': 'relative', 'width': '100%', 'height': '100%', 'border': border_style}
    )

    checkbox = dcc.Checklist(
        id={'type': 'image-checkbox', 'index': frame_number},
        options=[{'label': '', 'value': frame_number}],
        value=[None if is_unchecked else frame_number],
        style={'position': 'relative', 'left': '50%', 'margin-top': '5px'}
    )

    card = dbc.Card(
        [
            image_div,
            checkbox,
        ],
        style={"width": "20rem", 'margin-top': '5px'},
        id={"type": "image-card", "index": frame_number}
    )
    return card


@app.callback(
    Output('image-container', 'children'),
    Output('last-clicked-image-id', 'data'),
    Input('video-dropdown', 'value'),
    Input('heatmap-1', 'hoverData'),
    Input('heatmap-2', 'hoverData'),
    [Input({"type": "action-button", "index": ALL}, "n_clicks_timestamp")],
    [Input({'type': 'image-checkbox', 'index': ALL}, 'value')],
    State({"type": "image-card", "index": ALL}, "id")
)
def update_image_container(
        selected_option,
        hoverData_heatmap1,
        hoverData_heatmap2,
        click_timestamps,
        checkbox_id,
        image_card_id
):
    trigger = ctx.triggered_id
    # if trigger:
    #     print("Trigger:" , trigger)

    x_coord, y_coord = None, None
    global unchecked_image_ids

    if trigger != 'heatmap-1' and trigger != 'heatmap-2':
        if selected_option != None and image_card_id != []:

            if 'type' in trigger and trigger['type'] == 'image-checkbox':
                print(trigger["index"])
                print("For image checkbox click.")
                if int(trigger["index"]) in unchecked_image_ids:
                    unchecked_image_ids.remove(int(trigger["index"]))
                else:
                    unchecked_image_ids.append(int(trigger["index"]))

            elif 'type' in trigger and trigger['type'] == 'action-button':
                print("For image container click.")

            latest_click_index = None
            latest_click_time = 0
            for i, timestamp in enumerate(click_timestamps):
                if timestamp and timestamp > latest_click_time:
                    latest_click_time = timestamp
                    latest_click_index = i

            chosen_frame_number = None
            if trigger != "video-dropdown":
                chosen_frame_number = trigger["index"]

            image_names = os.listdir(images_source_folder)
            selected_option = selected_option.lower()
            image_names = [img.lower() for img in image_names]

            filtered_images = [img.strip() for img in image_names if img.startswith(selected_option)]

            filtered_images.sort(key=extract_frame_number)

            filtered_images = filtered_images[:max_frames]

            image_elements = []

            for image_name in filtered_images:
                frame_number = extract_frame_number(image_name)
                if frame_number == chosen_frame_number:
                    if frame_number in unchecked_image_ids:
                        image_element = get_image_card(image_name, frame_number, True, True)

                        print(image_name)

                        if trigger['type'] != 'image-checkbox':
                            # pop_img = Image.open(
                            #     os.path.join(
                            #         images_source_folder,
                            #         image_name
                            #     )
                            # )
                            ImageViewerThread(image=os.path.join(
                                images_source_folder,
                                image_name
                            )).start()
                            # pop_img.show(title=f"{frame_number}")

                    else:
                        image_element = get_image_card(image_name, frame_number, True, False)

                        print(image_name)

                        if trigger['type'] != 'image-checkbox':
                            # pop_img = Image.open(
                            #     os.path.join(
                            #         images_source_folder,
                            #         image_name
                            #     )
                            # )
                            ImageViewerThread(image=os.path.join(
                                images_source_folder,
                                image_name
                            )).start()
                            # pop_img.show(title=f"{frame_number}")

                else:
                    if frame_number in unchecked_image_ids:
                        image_element = get_image_card(image_name, frame_number, False, True)
                    else:
                        image_element = get_image_card(image_name, frame_number, False, False)

                image_elements.append(image_element)

            return image_elements, chosen_frame_number

    elif trigger == 'heatmap-1' or trigger == 'heatmap-2':
        if trigger == 'heatmap-1':
            clicked_point = hoverData_heatmap1['points'][0]
            x_coord = str(clicked_point['x']).lower()
            y_coord = clicked_point['y']
        else:
            clicked_point = hoverData_heatmap2['points'][0]
            x_coord = str(clicked_point['x']).lower()
            y_coord = clicked_point['y']

    print(selected_option)

    if selected_option:

        image_names = os.listdir(images_source_folder)
        selected_option = selected_option.lower()
        image_names = [img.lower() for img in image_names]

        filtered_images = [img.strip() for img in image_names if img.startswith(selected_option)]

        filtered_images.sort(key=extract_frame_number)

        filtered_images = filtered_images[:max_frames]

        image_elements = []

        for image_name in filtered_images:

            frame_number = extract_frame_number(image_name)

            if frame_number in unchecked_image_ids:
                if x_coord is not None and int(frame_number) == int(x_coord):
                    image_element = get_image_card(image_name, frame_number, True, True)
                else:
                    image_element = get_image_card(image_name, frame_number, False, True)
            else:
                if x_coord is not None and int(frame_number) == int(x_coord):
                    image_element = get_image_card(image_name, frame_number, True, False)
                else:
                    image_element = get_image_card(image_name, frame_number, False, False)

            image_elements.append(image_element)

        return image_elements, None
    else:
        return [], None


def save_heatmap_click_log():
    header = ['Object', 'Frame', 'Presence']

    model = present_model
    selected_file = present_selected_file

    click_log_file = LOG_DATA_DIR + '/' + PARTICIPANT_NAME + '-' + model + '-' + selected_file + '.csv'

    with open(click_log_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header)
        csv_writer.writerows(heatmap_1_clicks)


def flip(val):
    if val == 1:
        return 0
    return 1


def transform_x_coord(val):
    new_mapping = {}
    print(unchecked_image_ids)
    j = 0

    for i in range(max_frames):
        if i not in unchecked_image_ids:
            new_mapping[str(i)] = str(j)
            j += 1

    print(new_mapping)

    return new_mapping[str(val)]


@app.callback(
    Output('heatmap-1', 'figure'),
    # Output('heatmap-1-clicks-textarea', 'value'),
    Output('bar-graph', 'figure'),
    Input('model-dropdown', 'value'),
    Input('video-dropdown', 'value'),
    Input('heatmap-type-dropdown', 'value'),
    Input('heatmap-1', 'hoverData'),
    Input('heatmap-1', 'clickData'),
    Input('update-heatmap-button', 'n_clicks'),
    Input('I-see', 'value'),
    State('I-dont-see', 'value'),
    State('last-clicked-image-id', 'data'),
    [Input({"type": "action-button", "index": ALL}, "n_clicks_timestamp")],
    State({"type": "image-card", "index": ALL}, "id"),
    Input('model-dropdown-2', 'value'),
    [Input({'type': 'image-checkbox', 'index': ALL}, 'value')],
    prevent_initial_call=True

)
def update_heatmap_1(
        model,
        selected_file,
        selected_heatmap_type,
        heatmap_hoverData,
        heatmap_clickData,
        n_clicks,
        see_textarea_value,
        dont_see_textarea_value,
        last_clicked_image_id,
        dummy_1,
        dummy_2,
        second_model,
        unchecked_image_id
):
    global f1_model, f1_shadow_model, current_model
    selected_heatmap_type = heatmap_types[0]
    first_model_name = model
    model = models_to_show[model]

    print(model)
    print(see_textarea_value)

    if model and selected_file and len(see_textarea_value) >=1 and (
            selected_heatmap_type == 'Objects I See' or selected_heatmap_type == 'Both') and (
            second_model == None or second_model == ''):

        shadow_error = False

        if model in shadow_models:
            random.seed(200)
            see_textarea_value_lower = [item.lower() for item in see_textarea_value]
            _, _, f1___, _ = get_f1(
                os.path.join(base_folder, 'GT_N'), [f'{selected_file}.csv'],
                os.path.join(base_folder, model.split('@')[0]),
                obj_list=see_textarea_value_lower,
                limit_frame_count=max_frames+1
            )
            if f1___ == 0:
                f1___ = 0.01

            print(f"{model.split('@')[0]} F1 : {f1___:.4f}")
            try:
                shadow_model_df = get_shadow(
                    os.path.join(base_folder, 'GT_N', f'{selected_file}.csv'),
                    f1___, 1, see_textarea_value_lower, limit_frame_count=max_frames+1
                )[0]

                if not os.path.exists(os.path.join(base_folder, model)):
                    os.makedirs(os.path.join(base_folder, model))

                shadow_model_df.to_csv(os.path.join(base_folder, model, f'{selected_file}.csv'), index=False)
                _, _, f1___shadow, _ = get_f1(
                    os.path.join(base_folder, 'GT_N'), [f'{selected_file}.csv'],
                    os.path.join(base_folder, model),
                    obj_list=see_textarea_value_lower,
                    limit_frame_count=max_frames+1
                )
                print(f"{model} F1 : {f1___shadow:.4f}")

                f1_model = f1___
                f1_shadow_model = f1___shadow

                x_labels = [col for col in shadow_model_df.columns if col != "Object"]

                longest_x_label = max(x_labels, key=len)
                length_of_longest_x_label = len(longest_x_label)

                y_labels = list(shadow_model_df.iloc[:, 0])
                z_values = shadow_model_df.iloc[:, 1:].values.tolist()

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
            except:
                shadow_error = True

        if model not in shadow_models or shadow_error:
            if model in shadow_models:
                model = model.split('@')[0]
            file_path = os.path.join(base_folder, model, selected_file + '.csv')
            heat_map_file = pd.read_csv(file_path)

            x_labels = [col for col in heat_map_file.columns if col != "Object"]

            longest_x_label = max(x_labels, key=len)
            length_of_longest_x_label = len(longest_x_label)

            y_labels = list(heat_map_file.iloc[:80, 0])
            z_values = heat_map_file.iloc[:80, 1:].values.tolist()

            for i in range(len(z_values)):
                for j in range(len(z_values[i])):
                    if z_values[i][j] == -1:
                        z_values[i][j] = 0

            see_textarea_value_lower = [item.lower() for item in see_textarea_value]

            _, _, f1___, _ = get_f1(
                os.path.join(base_folder, 'GT_N'), [f'{selected_file}.csv'],
                os.path.join(base_folder, model),
                obj_list=see_textarea_value_lower,
                limit_frame_count=max_frames+1
            )

            f1_model = f1___
            f1_shadow_model = 'N/A'

            print(f"{model} F1 : {f1___:.4f}")

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

        ## for the "i see" heatmap (left one), 1 is agreement
        ## because, 1 means the model sees, which is exactly what my view is
        colorscale_heatmap1 = [[0, color_disagreement], [1, color_agreement], ]

        x_labels = [label.replace('Frame-', '').replace('frame_', '') for label in x_labels]

        x_labels = x_labels[:max_frames]
        y_labels = y_labels[:max_frames]
        z_values = z_values[:max_frames]

        ## handle the unchecked images here for heatmap display and bargraph data
        global bargraph_data
        global unchecked_image_ids
        global present_model
        global present_selected_file
        global heatmap_1_clicks
        global last_entry

        for image_id in unchecked_image_ids:
            x_labels.remove(str(image_id))
            for i in range(len(y_labels)):
                del z_values[i][int(image_id)]

        heatmap_cell_width = (fixed_heatmap_width - 50) / (len(x_labels) + (length_of_longest_x_label / 6))
        heatmap_cell_height = (fixed_heatmap_height - 125) / len(y_labels)

        layout = go.Layout(
            title=get_see_text(first_model_name),
            title_x=0.10,
            title_y=0.95,
            title_font=dict(family='Arial Black', size=12),
            height=fixed_heatmap_height,
            width=fixed_heatmap_width,
            margin=dict(l=30, r=30, t=50, b=70),
            xaxis=dict(
                showgrid=False,
                dtick=1,
                gridwidth=1,
                tickfont=dict(size=10.5, color='blue', family='Arial'),
            ),
            yaxis=dict(
                showgrid=False,
                dtick=1,
                gridwidth=1,
                tickfont=dict(size=11, family='Arial')
            ),
            annotations=[
                dict(
                    x=0.5,
                    y=-0.15,
                    xref='paper',
                    yref='paper',
                    text=heatmap_x_axis_title,
                    showarrow=False,
                    font=dict(size=12, family='Arial'),
                )
            ]
        )

        heatmap_line_column = None
        if last_clicked_image_id is not None:
            clicked_frame_number = last_clicked_image_id
            if f'{clicked_frame_number}' in x_labels:
                heatmap_line_column = x_labels.index(f'{clicked_frame_number}')
            heatmap_hoverData = None

        layout_shapes_list = []

        if heatmap_hoverData and 'points' in heatmap_hoverData and heatmap_hoverData['points']:
            print("Hover Data:")
            print(heatmap_hoverData['points'][0]['x'], heatmap_hoverData['points'][0]['y'])

            last_clicked_image_id = None

            clicked_point = heatmap_hoverData['points'][0]
            x_coord = clicked_point['x']
            y_coord = clicked_point['y']

            if int(x_coord) not in unchecked_image_ids:
                x_coord = transform_x_coord(x_coord)

                layout_shapes_list.extend(
                    get_heatmap_highlight_lines_from_heatmap_click(x_labels, y_labels, x_coord, y_coord))

        if model != present_model or selected_file != present_selected_file:
            heatmap_1_clicks = []
            temp = {'Frame': [str(i) for i in range(max_frames)],
                    'Number of Modifications': [0 for i in range(max_frames)]}

            bargraph_data = pd.DataFrame(temp)
            present_model = model
            unchecked_image_ids = []
            present_selected_file = selected_file

        if heatmap_clickData and 'points' in heatmap_clickData and heatmap_clickData['points']:
            print("CLick Data:")
            print(heatmap_clickData['points'][0]['x'], heatmap_clickData['points'][0]['y'])

            clicked_point = heatmap_clickData['points'][0]
            x_coord = clicked_point['x']
            y_coord = clicked_point['y']
            z_coord = clicked_point['z']

            candidate_entry = [y_coord, x_coord, flip(z_coord)]

            if candidate_entry != last_entry:
                latest_entry = None

                for entry in reversed(heatmap_1_clicks):
                    if entry[:2] == [y_coord, x_coord]:
                        latest_entry = entry
                        break

                if latest_entry == None:
                    heatmap_1_clicks.append(candidate_entry)
                    last_entry = candidate_entry
                    present_model = model
                    present_selected_file = selected_file
                    first_test = False
                    bargraph_data.loc[bargraph_data['Frame'] == x_coord, 'Number of Modifications'] += 1
                else:
                    if latest_entry[2] != candidate_entry[2]:
                        heatmap_1_clicks.append(candidate_entry)
                        bargraph_data.loc[bargraph_data['Frame'] == x_coord, 'Number of Modifications'] += 1
                        last_entry = candidate_entry

        for click in heatmap_1_clicks:
            if str(click[1]) in x_labels:
                x_number = x_labels.index(click[1])
                y_number = y_labels.index(click[0])
                z_values[y_number][x_number] = flip(z_values[y_number][x_number])

        if heatmap_line_column is not None:
            layout_shapes_list.extend(get_heatmap_highlight_lines_from_image_container_click(heatmap_line_column))

        layout_shapes_list.extend(get_vetical_axis_lines(x_labels))
        layout_shapes_list.extend(get_horizontal_axis_lines(y_labels))

        layout['shapes'] = tuple(layout_shapes_list)

        heatmap = go.Heatmap(
            x=x_labels,
            y=y_labels,
            z=z_values,
            colorscale=colorscale_heatmap1,
            showscale=False,
            zmin=0,
            zmax=1
        )

        heat_map = go.Figure(data=heatmap, layout=layout)
        # heat_map.update_layout(xaxis=dict(ticks='', showticklabels=False))

        filtered_heatmap_1_clicks = []

        for i, entry1 in enumerate(heatmap_1_clicks):
            x1, y1, z1 = entry1
            opposite_z1 = 1 if z1 == 0 else 0
            is_duplicate = False

            for j, entry2 in enumerate(heatmap_1_clicks):
                x2, y2, z2 = entry2

                if i != j and x1 == x2 and y1 == y2 and z1 == 1 - z2:
                    is_duplicate = True
                    break

            if not is_duplicate:
                filtered_heatmap_1_clicks.append(entry1)

        bargraph_data_filtered = bargraph_data[~bargraph_data['Frame'].astype(int).isin(unchecked_image_ids)].copy()

        bargraph_data_filtered['Frame'] = bargraph_data_filtered['Frame'].astype(str)

        bargraph = px.bar(bargraph_data_filtered, x='Frame', y='Number of Modifications',
                  title=f'Total Modifications: <b>{bargraph_data_filtered["Number of Modifications"].sum()}</b>',
                  height=300, width=550)

        bargraph.update_layout(title_x=0.5)
        bargraph.update_traces(marker_color='#A9A9A9')
        bargraph.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',  # Set transparent background
            showlegend=False,
            yaxis_gridcolor='rgba(128,128,128,0.2)'
        )

        return heat_map, bargraph

    return {}, {}


@app.callback(
    Output('status-textarea', 'children', allow_duplicate=True),
    Input('video-dropdown', 'value'),
    prevent_initial_call=True
)
def update_file(selected_file):
    global current_file
    current_file = selected_file
    return f"File: {current_file}" if current_file else "File: None"


@app.callback(
    Output('status-textarea', 'children', allow_duplicate=True),
    Input('rating-slider', 'value'),
    prevent_initial_call=True
)
def update_rating(rating):
    global current_rating
    current_rating = rating
    return f"Rating: {current_rating}" if current_rating else "Rating: None"


@app.callback(
    Output('status-textarea', 'children', allow_duplicate=True),
    Input('I-see', 'value'),
    prevent_initial_call=True
)
def update_see(text_see):
    global current_text_see
    current_text_see = text_see
    return f"I see: {current_text_see}" if current_text_see else "I see: None"


@app.callback(
    Output('status-textarea', 'children', allow_duplicate=True),
    Input('I-dont-see', 'value'),
    prevent_initial_call=True
)
def update_donot_see(text_donot_see):
    global current_text_not_see
    current_text_not_see = text_donot_see
    return f"I don't see: {current_text_not_see}" if current_text_not_see else "I don't see: None"


@app.callback(
    Output('status-textarea', 'children', allow_duplicate=True),
    Input('comments-textarea', 'value'),
    prevent_initial_call=True
)
def update_comment(text_comments):
    global current_text_comments
    current_text_comments = text_comments
    return f"Comments: {current_text_comments}" if current_text_comments else "Comments: None"




@app.callback(
    Output('status-textarea', 'children', allow_duplicate=True),
    Output('video-dropdown', 'options', allow_duplicate=True),
    Output('video-dropdown', 'value', allow_duplicate=True),
    Output('image-container', 'children', allow_duplicate=True),
    Output('heatmap-1', 'figure', allow_duplicate=True),
    # Output('heatmap-1-clicks-textarea', 'style', allow_duplicate = True),
    Output('auto-select-obj', 'style', allow_duplicate=True),
    Output('bar-graph', 'style', allow_duplicate=True),
    Output('I-see', 'value', allow_duplicate=True ),
    Output('rating-slider', 'value'),
    Output('comments-textarea', 'value'),
    Input('save-button', 'n_clicks'),
    prevent_initial_call=True
)
def save_data(n_clicks):
    global current_model, current_model_right, f1_model, f1_shadow_model
    if n_clicks > 0:

        current_time = datetime.datetime.now().strftime('%Y-%m-%d::%H:%M:%S')
        data = {
            'timestamp': str(current_time),
            'video': current_file,
            'model left': models_to_show[current_model],
            'model right': models_to_show[current_model_right] if current_model_right else 'N/A',
            'winner model': best_model_side if observe_typ == 'double' else 'N/A',
            'see': ','.join(current_text_see),
            'not_see': ','.join(current_text_not_see),
            'score': current_rating if observe_typ == 'single' else 'N/A',
            'comments': current_text_comments.lower() if current_text_comments else '',
            'mode': observe_typ,
            'F1-Base': f1_model,
            'F1-Shadow': f1_shadow_model
        }

        # write data to file
        print(data)
        save_log_file(data)
        if len(heatmap_1_clicks) > 0:
            save_heatmap_click_log()

        updated_list = []
        for v_ in all_video_files:
            if v_ not in completed_videos:
                updated_list.append({"label": v_, "value": v_})

        if len(updated_list) == 0:
            return "**Saved at: " + current_time + "**", dash.no_update, dash.no_update, dash.no_update, dash.no_update, auto_select_button_style, {
                'display': 'none'}, [], 5, ''

        return "**Saved at: " + current_time + "**", updated_list, None, [], {}, auto_select_button_style, {
            'display': 'none'}, [], 5, ''
    else:
        return "*Not Saved*"


# convert models_to_show  to string


@app.callback(
    Output('status-textarea', 'children', allow_duplicate=True),
    Input('random-button', 'n_clicks'),
    prevent_initial_call=True
)
def randomize_event(n_clicks):
    if n_clicks > 0:
        randomize_data()
        current_time = datetime.datetime.now().strftime('%Y-%m-%d::%H:%M:%S')

        return "**Randomized at: " + current_time + str(models_to_show) + "**"
    else:
        return "*Not Randomized*"


@app.callback(
    Output('I-see', 'value', allow_duplicate=True),
    Input('video-dropdown', 'value'),
    prevent_initial_call=True
)
def auto_select_objects(video):
    if video == [] or video == None:
        return []
    global current_model, current_model_right
    gt_file = os.path.join(GROUND_TRUTH_DATA, f'{current_file}.csv')

    l_model = models_to_show[current_model]
    # r_model = models_to_show[current_model_right]

    if l_model in reduce_object_model_coco:
        obj_list_ref = coco_common_obj
        frm_gvn_lst = True
    elif l_model in reduce_object_model_pfb:
        obj_list_ref = pfb_common_obj
        frm_gvn_lst = True
    else:
        obj_list_ref = []
        frm_gvn_lst = False

    # obj_list_ref = list(set(coco_common_obj) & set(pfb_common_obj))
    # frm_gvn_lst = True

    if 0 < len(obj_list_ref) < ex_obj + non_ex_obj:
        e_obj = len(obj_list_ref) // 2
        non_e_obj = len(obj_list_ref) - e_obj
    else:
        e_obj = ex_obj
        non_e_obj = non_ex_obj

    obj_list = get_obj_list(gt_file, e_obj=e_obj, non_e_obj=non_e_obj, total_obj=all_rand_obj, all_random=False,
                            from_given_list=frm_gvn_lst, given_list=obj_list_ref)
    print(obj_list)
    return obj_list


if __name__ == '__main__':
    app.run_server(debug=True)
