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

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Dashboard Data')
GROUND_TRUTH_DATA = os.path.join(DATA_DIR, 'GT')
IMAGE_DATA_DIR = os.path.join(DATA_DIR, 'Images')
LOG_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Logs')


base_folder = DATA_DIR
images_source_folder = IMAGE_DATA_DIR
files = os.listdir(GROUND_TRUTH_DATA)
all_video_files = [os.path.splitext(file)[0] for file in files if file.endswith(".csv")]
all_video_files = natsorted(all_video_files)


available_models = ['GPV-1', 'BLIP', 'GT', 'Random']


# a global log file contains the following columns: timestamp, video, model, score, comments
COLUMNS = ['timestamp', 'video', 'model', 'see', 'not_see', 'score', 'comments']

# default values
current_model = 'Model-0' #'GPV-1'
current_file = 'video-1-segment-5' # 'video-1-segment-5'
current_text_see = 'Wall, Bicycle, Bridge, Building, Bus, Bus Stop'
current_text_not_see = 'Guide dog, Gutter, Hose, Lamp Post, Mail box'
current_rating = 5
current_text_comments = ''


num_frames = 100
max_frames = 14

fixed_heatmap_height = 350
fixed_heatmap_width = 500

heatmap_colorscale = [
    [0, 'rgb(211, 6, 50)'],
    [1, 'rgb(6, 200, 115)']
]


def randomize_data():
    random_model = random.sample(range(0, len(available_models)), len(available_models))        
    # a dictionary that maps model-{} to available models randomly
    global models_to_show
    models_to_show = {}
    for i in range(len(available_models)):
        models_to_show['Model-{}'.format(i)] = available_models[random_model[i]]


# update models_to_show, a dictionary that maps model-{} to available models
randomize_data()


# Write or append log files
def save_log_file(new_row):    
    log_file = os.path.join(LOG_DATA_DIR, 'user_log.csv')
    print(log_file, LOG_DATA_DIR)            
    
    if os.path.exists(log_file):        
        df = pd.read_csv(log_file)
        df.loc[len(df)] = new_row
        # df = df.append(df_new, ignore_index=True)
        df.to_csv(log_file, index=False)
    else:
        df_log = pd.DataFrame(new_row,  columns=COLUMNS, index=[0])        
        df_log.to_csv(log_file, index=False)


def read_text_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

# css framework for layout and style
external_stylesheets = [ 'https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

# create the dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)

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
                    style={'background-color': 'lightgray'}
                )
            ], className='row'
        ),

        # model dropdown
        html.Div([
            dcc.Dropdown(
                id='model-dropdown',
                options=[{'label': model, 'value': model} for model in models_to_show],
                placeholder='Select a Model',
                value= current_model,
                style={'border-color': 'gray'}            
            )], className='row'
        ),
        
        html.Div([
            dcc.Dropdown(
                id='video-dropdown',
                options=[{'label': option, 'value': option} for option in all_video_files],
                placeholder='Select a video file...',
                # value=None,
                value= current_file,
                style={'border-color': 'gray'}            
                # style={'width': '200px', 'margin': '10px'}
            )],
            className='row'
        ),
        
        # I don't see text area
        html.Div([
            dcc.Markdown(children = '*Objects I **see** in the video:*'),
            dcc.Textarea(
                id='I-see',
                value=current_text_see,
                placeholder='Things I see',
                style={'width': '100%', 'color': 'grey', 'font-style': 'italic'}
            )], className='two columns', style={'background-color': 'rgba(6, 200, 115, 0.5)'}

        ),

        # Possible objects text area
        html.Div([
            dcc.Markdown(children = '*Possible Objects:*'),
			dcc.Textarea(
                id='text-file-content',
                value=read_text_file_content('all_a11y_objects.txt'),  
                readOnly=True,
                style={'width': '100%', 'color': 'grey', 'font-style': 'italic'}
            )], className = 'seven columns'
        ),


        # I don't see text area
        html.Div([
            dcc.Markdown('*Objects I **don\'t see** in the video:*'),            
            dcc.Textarea(
                id='I-dont-see',
                value='Guide dog, Gutter, Hose, Lamp Post, Mail box',
                placeholder='Things I do not see',
                style={'width': '100%', 'color': 'grey', 'font-style': 'italic'}      
            )], className='two columns', style={'background-color': 'rgba(211, 6, 50, 0.5)'} 
        ),

        # analyze button
        html.Div(
            [
                html.Button(
                    'Analyze', 
                    id='update-heatmap-button', 
                    n_clicks=0, 
                    style={'background-color': 'lightgray'}
                )
            ], className='row'
        )         
    ], className='row',
) 

# 2nd row: heatmap layout
heatmaps = html.Div(
    [        
        html.Div(
            [        
                dcc.Graph(
                    id='heatmap-1',
                ),
                html.Div(
                    id='heatmap-popover-1',
                    style={'position': 'relative'},
                ),                  
            ], className='five columns'
        ),

        html.Div([
				# empty								
			], className = 'one column'
        ),

        html.Div(
            [        
                dcc.Graph(
                    id='heatmap-2',
                ),
                html.Div(
                    id='heatmap-popover-2',
                    style={'position': 'relative'},
                ),                  
            ], className='five columns'
        ),
    ], className='row'
)

# 3rd row: image layout
image_map = html.Div(
    [
        html.Div(
            id='image-container', 
            style={'display': 'flex', 'justify-content': 'center', 'flexWrap': 'wrap'},
            children=[]
        )
    ],
     className= 'row'
)

second_and_third_row = html.Div(
    [
        html.Div(
            [
                heatmaps,
                image_map,            
            ], 
        ),            
        dcc.Store(id='last-clicked-image-id'),
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
                    #### Please rate the reliability of this model on a scale from 0 to 10
                    *(0: not reliable at all; 5: neutral; 10: very reliable):*                    
                '''),
                dcc.Slider(
                    id = "rating-slider",
                    min = 0,
                    max = 10,
                    step = 1,
                    value = 5,
                    tooltip={"placement": "bottom", "always_visible": True},
                    # marks = None,
                ),
            ], className='five columns'
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
                    children= '*Status:  Not saved*',                    
                )                
            ], className='two columns',  
        ),

        # save button
        html.Div(
            [
                html.Button(
                    'Record Response', 
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
        html.Div(id='output-folder-creation', style={'margin': '10px', 'display': 'none'}),
        second_and_third_row,    
        rating_row
    ]
)

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


def get_image_card(image_name, frame_number, is_selected):
    image_path = os.path.join(images_source_folder, image_name)
    encoded_image = get_encoded_image(image_name)

    border_style = '5px solid yellow' if is_selected else 'none'

    action_button = dbc.Button(
        "",
        color="danger",  
        size="sm",  
        id={"type": "action-button", "index": frame_number},
        n_clicks=0,
        style={'position': 'absolute', 'top': '0', 'right': '0', 'width': '100%', 'height': '100%', 'margin': '0', 'padding': '0', 'border': 'none', 'background': 'transparent'} 
    )

    frame_number_label = html.Label(
        frame_number,
        style={'position': 'absolute', 'top': '0px', 'left': '0px', 'color': 'blue', 'background-color': 'rgb(232, 237, 235)', 'padding': '2px', 'font-weight': 'bold'}
    )

    image_div = html.Div(
        [
            dbc.CardImg(src=encoded_image, style={'width': '100%'}),
            action_button,
            frame_number_label
        ],
        style={'position': 'relative', 'width': '100%', 'height': '100%'}
    )

    card = dbc.Card(
        [
            image_div
        ],
        style={"width": "20rem", 'border': border_style, 'margin': '5px'},
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
    State({"type": "image-card", "index": ALL}, "id")
)
def update_image_container(
    selected_option,
    hoverData_heatmap1,
    hoverData_heatmap2,
    click_timestamps, 
    image_card_id
):

    trigger = ctx.triggered_id
    if trigger:
        print("Trigger:" , trigger)

    x_coord, y_coord = None, None
    if trigger != 'heatmap-1' and trigger != 'heatmap-2':
        if selected_option != None and image_card_id != []:
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
                    image_element = get_image_card(image_name, frame_number, True)
                else:
                    image_element = get_image_card(image_name, frame_number, False)

                image_elements.append(image_element)

            return image_elements, chosen_frame_number

    else:
        if trigger == 'heatmap-1':
            clicked_point = hoverData_heatmap1['points'][0]
            x_coord = str(clicked_point['x']).lower()
            y_coord = clicked_point['y']
        elif trigger == 'heatmap-2':
            clicked_point = hoverData_heatmap2['points'][0]
            x_coord = str(clicked_point['x']).lower()
            y_coord = clicked_point['y']
        else:
            x_coord, y_coord = None, None      


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

            if x_coord is not None and int(frame_number) == int(x_coord):
                image_element = get_image_card(image_name, frame_number, True)
            else:
                image_element = get_image_card(image_name, frame_number, False)

            image_elements.append(image_element)

        return image_elements, None
    else:
        return [], None



color_white = 'rgb(255,255,255)' # white
color_agreement = 'rgb(6, 200, 115)' # green
color_disagreement = 'rgb(211, 6, 50)' # red

@app.callback(
    Output('heatmap-1', 'figure'), 
    Input('model-dropdown', 'value'), 
    Input('video-dropdown', 'value'),     
    Input('heatmap-1', 'hoverData'),
    Input('heatmap-1', 'clickData'),
    # Input('heatmap-dropdown-1', 'value'),
    Input('update-heatmap-button', 'n_clicks'),
    State('I-see', 'value'), 
    State('last-clicked-image-id', 'data'),
    [Input({"type": "action-button", "index": ALL}, "n_clicks_timestamp")],
    State({"type": "image-card", "index": ALL}, "id") 
)
def update_heatmap_1(
    model, 
    selected_file,     
    heatmap_hoverData,
    heatmap_clickData,
    # heatmap_dropdownData,
    n_clicks,                  
    textarea_example_value,    
    last_clicked_image_id,
    dummy_1,
    dummy_2
):
    model = models_to_show[model]

    if n_clicks > 0 and model and selected_file:
        file_path = os.path.join(base_folder, model, selected_file + '.csv')
        heat_map_file = pd.read_csv(file_path)

        x_labels = [col for col in heat_map_file.columns if col != "Object"] 

        longest_x_label = max(x_labels, key=len)
        length_of_longest_x_label = len(longest_x_label)

        y_labels = list(heat_map_file.iloc[:80, 0])  
        z_values = heat_map_file.iloc[:80, 1:].values.tolist()  


        filtered_indices_see = [i for i, label in enumerate(y_labels) if label.lower() in textarea_example_value.lower()]

        
        filtered_indices = filtered_indices_see 
        y_labels_filtered = []
        z_values_filtered = []

        for i in filtered_indices:
            if i != -1:
                y_labels_filtered.append(y_labels[i])
                z_row = [1 if val == 1 else val for val in z_values[i]]
                z_values_filtered.append(z_row)
        y_labels = y_labels_filtered
        z_values = z_values_filtered
        
        # colorscale_heatmap1 = [
                                
        #                         [0, 'rgb(255,255,255)'], # disagreement
        #                         [1, 'rgb(6, 200, 115)'],
        #                       ]
        
        ## for the "i see" heatmap (left one), 1 is agreement
        ## because, 1 means the model sees, which is exactly what my view is
        colorscale_heatmap1 = [
                                
                                [0, color_disagreement], # disagreement
                                [1, color_agreement],
                              ]
        
        ## green means model sees
        ## white means model does not see 

        x_labels = [label.replace('Frame-', '') for label in x_labels]


        x_labels = x_labels[:max_frames]
        y_labels = y_labels[:max_frames]
        z_values = z_values[:max_frames]

        heatmap = go.Heatmap(
            x=x_labels,
            y=y_labels,
            z=z_values,
            colorscale=colorscale_heatmap1,
            showscale = False
        )

        heatmap_cell_width = ( fixed_heatmap_width - 50 )  / ( len(x_labels) + ( length_of_longest_x_label / 6) )
        heatmap_cell_height = ( fixed_heatmap_height - 125 )/ len(y_labels)

        print("heatmap-1: ", heatmap_cell_width, heatmap_cell_height)

        border_line = {
            'type': 'rect',
            'x0': -0.5,  
            'x1': len(x_labels)-0.5, 
            'y0': -0.5,  
            'y1': len(y_labels)-0.5,  
            'xref': 'x',
            'yref': 'y',
            'line': {
                'color': 'rgb(6, 200, 115)',  
                'width': 5, 
            },
            'fillcolor': 'rgba(0,0,0,0)',  
            'opacity': 1,
        }

    #  and that model doesn't see (White)
        layout = go.Layout(
            title="Objects you SEE that the model also SEEs (green, agreement) and <br> that the model DOESN'T SEE (red, disagreement)",
            title_x=0.10,
            title_y=0.95,
            # title_font=dict(color='rgb(6, 200, 115)', family='Arial Black', size=12 ),
            title_font=dict(family='Arial Black', size=12 ),
            height=fixed_heatmap_height,
            width=fixed_heatmap_width,
            margin=dict(l=30, r=30, t=50, b=70),
            xaxis=dict(
                showgrid=False,
                dtick=1,
                gridwidth=1,
                tickfont=dict(size=10.5, color='blue', family='Arial Black'),
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
                    text='Frames',  
                    showarrow=False,  
                    font=dict(size=12, family='Arial Black'),
                )
            ]
        )

        heatmap_line_column = None
        if last_clicked_image_id:
            clicked_frame_number = last_clicked_image_id
            heatmap_line_column = x_labels.index(f'{clicked_frame_number}')
            heatmap_hoverData = None

        layout_shapes_list = []
        
        layout_shapes_list.append(border_line)
       

        if heatmap_hoverData and 'points' in heatmap_hoverData and heatmap_hoverData['points']:
            last_clicked_image_id = None

            clicked_point = heatmap_hoverData['points'][0]
            x_coord = clicked_point['x']
            y_coord = clicked_point['y']

            layout_shapes_list.extend([
                {
                    'type': 'line',
                    'x0': 0,
                    'x1': 1,
                    'y0': y_coord,
                    'y1': y_coord,
                    'xref': 'paper',
                    'yref': 'y',
                    'line': {
                        'color': 'yellow',  
                        'width': heatmap_cell_height, 
                    },
                    'opacity': 0.5
                },
                {
                    'type': 'line',
                    'x0': x_coord,
                    'x1': x_coord,
                    'y0': 0,
                    'y1': 1,
                    'xref': 'x',
                    'yref': 'paper',
                    'line': {
                        'color': 'yellow',  
                        'width': heatmap_cell_width, 
                    },
                    'opacity': 0.5
                }
            ])


        for i in range(len(x_labels)):
            layout_shapes_list.append({
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
                'opacity': 0.2
            })

        for i in range(len(y_labels) + 1):
            layout_shapes_list.append({
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
                'opacity': 0.2
            })

        if heatmap_line_column is not None:
            layout_shapes_list.append({
                'type': 'line',
                'x0': heatmap_line_column,
                'x1': heatmap_line_column,
                'y0': 0,
                'y1': 1,
                'xref': 'x',
                'yref': 'paper',
                'line': {
                    'color': 'yellow', 
                    'width': heatmap_cell_width, 
                },
                'opacity': 0.5
            })

        if heatmap_clickData:
            x_coord = int(heatmap_clickData['points'][0]['x']) 
            y_coord = heatmap_clickData['points'][0]['y']


        layout['shapes'] = tuple(layout_shapes_list)
        heat_map = go.Figure(data=heatmap, layout=layout)

        return heat_map

    return {}



@app.callback(
    Output('heatmap-popover-1', 'children'),
    Output('heatmap-popover-1', 'style'),
    Input('heatmap-1', 'clickData'),
)
def render_popover_1(click_data):
    if click_data:
        x_coord = int(click_data['points'][0]['x']) 
        y_coord = click_data['points'][0]['y']
        options = ['Minor', 'Moderate', 'Severe']

        dropdown = dcc.Dropdown(
            id='heatmap-dropdown-1',
            options=[{'label': option, 'value': option} for option in options],
            value=None,
            clearable=True,
            style={'width': '100px'},
            placeholder='The Error Is:'
        )

        print(x_coord, y_coord)

        dropdown_style = {
            'position': 'absolute',
            'left': f'{480}px',  
            'top': f'{253}px', 
            'z-index': 1000  
        }

        return dropdown, dropdown_style

    return html.Div(), {'display': 'none'}

@app.callback(
    Output('heatmap-popover-2', 'children'),
    Output('heatmap-popover-2', 'style'),
    Input('heatmap-2', 'clickData'),
)
def render_popover_2(click_data):
    if click_data:
        x_coord = int(click_data['points'][0]['x']) 
        y_coord = 5
        options = ['Minor', 'Moderate', 'Severe']

        dropdown = dcc.Dropdown(
            id='heatmap-dropdown-2',
            options=[{'label': option, 'value': option} for option in options],
            value=None,
            clearable=True,
            style={'width': '100px'},
            placeholder='The Error Is:'
        )

        print(x_coord, y_coord)

        dropdown_style = {
            'position': 'absolute',
            'left': f'{1315}px',  
            'top': f'{253}px', 
            'z-index': 1000  
        }

        return dropdown, dropdown_style

    return html.Div(), {'display': 'none'}


@app.callback(
    Output('heatmap-2', 'figure'), 
    Input('model-dropdown', 'value'), 
    Input('video-dropdown', 'value'), 
    # Input('line-graph-1', 'clickData'),
    Input('heatmap-2', 'hoverData'),
    Input('update-heatmap-button', 'n_clicks'),
    State('I-dont-see', 'value'),
    State('last-clicked-image-id', 'data'),
    [Input({"type": "action-button", "index": ALL}, "n_clicks_timestamp")],
    State({"type": "image-card", "index": ALL}, "id") 
)
def update_heatmap_2(
    model, 
    selected_file, 
    # line_graph_clickData,
    heatmap_hoverData,
    n_clicks,                      
    textarea_example_2_value, 
    last_clicked_image_id,
    dummy_1,
    dummy_2
):
    model = models_to_show[model]

    if n_clicks > 0 and model and selected_file:
        file_path = os.path.join(base_folder, model, selected_file + '.csv')
        heat_map_file = pd.read_csv(file_path)

        x_labels = [col for col in heat_map_file.columns if col != "Object"] 

        longest_x_label = max(x_labels, key=len)
        length_of_longest_x_label = len(longest_x_label)

        y_labels = list(heat_map_file.iloc[:80, 0])  
        z_values = heat_map_file.iloc[:80, 1:].values.tolist()  


        filtered_indices_dont_see = [i for i, label in enumerate(y_labels) if label.lower() in textarea_example_2_value.lower()]
        
 
        filtered_indices = filtered_indices_dont_see
        
        y_labels_filtered = []
        z_values_filtered = []

        for i in filtered_indices:
            if i != -1:
                y_labels_filtered.append(y_labels[i])
                z_values_filtered.append(z_values[i])



        y_labels = y_labels_filtered
        z_values = z_values_filtered


        # colorscale_heatmap2 = [                          
        #                          [0, 'rgb(255, 255, 255)'],
        #                          [1, 'rgb(211, 6, 50)'], 
        #                        ]

        ## for the "i don't see" heatmap (right one), 0 is agreement
        ## because, 0 means the model does not see, which is exactly what my view is
        colorscale_heatmap2 = [                          
                                 [0, color_agreement],
                                 [1, color_disagreement], 
                               ]
        
        x_labels = [label.replace('Frame-', '') for label in x_labels]


        x_labels = x_labels[:max_frames]
        y_labels = y_labels[:max_frames]
        z_values = z_values[:max_frames]

        heatmap = go.Heatmap(
            x=x_labels,
            y=y_labels,
            z=z_values,
            colorscale=colorscale_heatmap2,
            showscale = False
        ) 

        border_line = {
            'type': 'rect',
            'x0': -0.5,  
            'x1': len(x_labels)-0.5, 
            'y0': -0.5,  
            'y1': len(y_labels)-0.5,  
            'xref': 'x',
            'yref': 'y',
            'line': {
                'color': 'rgb(211, 6, 50)',  
                'width': 5, 
            },
            'fillcolor': 'rgba(0,0,0,0)',  
            'opacity': 1,
        }

        heatmap_cell_width = ( fixed_heatmap_width - 50 )  / ( len(x_labels) + ( length_of_longest_x_label / 6) )
        heatmap_cell_height = ( fixed_heatmap_height - 125 )/ len(y_labels)

        print("heatmap-2: ", heatmap_cell_width, heatmap_cell_height)            

        layout = go.Layout(
            title="Objects you DON'T SEE that the model also DOESN'T SEE (green, <br> agreement) and that the model does SEE (red, disagreement)",
            # title="Things You Do Not See",
            title_x=0.10,
            title_y=0.95,
            # title_font=dict(color='rgb(211, 6, 50)', family='Arial Black' ),
            title_font=dict(family='Arial Black', size=12 ),
            height=fixed_heatmap_height,
            width=fixed_heatmap_width,
            margin=dict(l=5, r=0, t=50, b=70),
            xaxis=dict(
                showgrid=False,
                dtick=1,
                gridwidth=1,
                tickfont=dict(size=10.5, color='blue', family='Arial Black'),
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
                    text='Frames',  
                    showarrow=False,  
                    font=dict(size=12, family='Arial Black'),
                )
            ]
        )



        heatmap_line_column = None
        if last_clicked_image_id:
            clicked_frame_number = last_clicked_image_id
            heatmap_line_column = x_labels.index(f'{clicked_frame_number}')
            heatmap_hoverData = None

        layout_shapes_list = []

        layout_shapes_list.append(border_line)

       
        if heatmap_hoverData and 'points' in heatmap_hoverData and heatmap_hoverData['points']:

            last_clicked_image_id = None

            clicked_point = heatmap_hoverData['points'][0]
            x_coord = clicked_point['x']
            y_coord = clicked_point['y']

            layout_shapes_list.extend([
                {
                    'type': 'line',
                    'x0': 0,
                    'x1': 1,
                    'y0': y_coord,
                    'y1': y_coord,
                    'xref': 'paper',
                    'yref': 'y',
                    'line': {
                        'color': 'yellow', 
                        'width': heatmap_cell_height,  
                    },
                    'opacity': 0.5
                },
                {
                    'type': 'line',
                    'x0': x_coord,
                    'x1': x_coord,
                    'y0': 0,
                    'y1': 1,
                    'xref': 'x',
                    'yref': 'paper',
                    'line': {
                        'color': 'yellow', 
                        'width': heatmap_cell_width, 
                    },
                    'opacity': 0.5
                }
            ])


        for i in range(len(x_labels)):
            layout_shapes_list.append({
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
                'opacity': 0.2
            })

        for i in range(len(y_labels) + 1):
            layout_shapes_list.append({
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
                'opacity': 0.2
            })

        if heatmap_line_column is not None:
            layout_shapes_list.append({
                'type': 'line',
                'x0': heatmap_line_column,
                'x1': heatmap_line_column,
                'y0': 0,
                'y1': 1,
                'xref': 'x',
                'yref': 'paper',
                'line': {
                    'color': 'yellow', 
                    'width': heatmap_cell_width, 
                },
                'opacity': 0.5
            })

        layout['shapes'] = tuple(layout_shapes_list)
        heat_map = go.Figure(data=heatmap, layout=layout)

        return heat_map

    return {}

                

@app.callback(
    Output('status-textarea', 'children', allow_duplicate=True), 
    Input('model-dropdown', 'value'),
    prevent_initial_call=True
)
def update_model(model):
    global current_model        
    current_model = model
    return f"Model: {current_model}: {models_to_show[current_model]}" if current_model else "Model: None"

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
    current_rating  = rating
    return f"Rating: {current_rating}" if current_rating else "Rating: None"

@app.callback(
    Output('status-textarea', 'children', allow_duplicate=True), 
    Input('I-see', 'value'),    
    prevent_initial_call=True
)
def update_see(text_see):
    global current_text_see        
    current_text_see  = text_see
    return f"I see: {current_text_see}" if current_text_see else "I see: None"


@app.callback(
    Output('status-textarea', 'children', allow_duplicate=True), 
    Input('I-dont-see', 'value'),
    prevent_initial_call=True
)
def update_donot_see(text_donot_see):        
    global current_text_not_see
    current_text_not_see  = text_donot_see
    return f"I don't see: {current_text_not_see}" if current_text_not_see else "I don't see: None"

@app.callback(
    Output('status-textarea', 'children', allow_duplicate=True), 
    Input('comments-textarea', 'value'), 
    prevent_initial_call=True
)
def update_comment(text_comments):        
    global current_text_comments
    current_text_comments  = text_comments
    return f"Comments: {current_text_comments}" if current_text_comments else "Comments: None"


@app.callback(
    Output('status-textarea', 'children'),      
    Input('save-button', 'n_clicks')
)

def save_data(n_clicks):
    if n_clicks > 0:
        
        current_time = datetime.datetime.now().strftime('%Y-%m-%d::%H:%M:%S')
        data = {'timestamp': str(current_time), 
                'video': current_file, 
                'model': models_to_show[current_model], 
                'see': current_text_see.lower(), 
                'not_see': current_text_not_see.lower(), 
                'score': current_rating, 
                'comments': current_text_comments.lower() if current_text_comments else '' 
            }

        # write data to file        
        print(data)
        save_log_file(data)

        return "**Saved at: " + current_time + "**"
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



if __name__ == '__main__':
    app.run_server(debug=True)