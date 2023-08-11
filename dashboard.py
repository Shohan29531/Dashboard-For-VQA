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


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Dashboard Data')
GROUND_TRUTH_DATA = os.path.join(DATA_DIR, 'GT')
IMAGE_DATA_DIR = os.path.join(DATA_DIR, 'Images')



base_folder = DATA_DIR
images_source_folder = IMAGE_DATA_DIR
files = os.listdir(GROUND_TRUTH_DATA)
all_video_files = [os.path.splitext(file)[0] for file in files if file.endswith(".csv")]
all_video_files = natsorted(all_video_files)



models_to_show = ['Model-1', 'Model-2']

available_models = ['GPV-1', 'BLIP', 'GT', 'Random']

num_frames = 100
max_frames = 14

fixed_heatmap_height = 350
fixed_heatmap_width = 500

heatmap_colorscale = [
    [0, 'rgb(211, 6, 50)'],
    [1, 'rgb(6, 200, 115)']
]

external_stylesheets = [ 'https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]  #

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)


def read_text_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


@app.callback(
    Output('heatmap-1', 'style'), 
    Input('heatmap-1', 'figure'))
def show_hide_heatmap_1(heatmap_figure):
    if not heatmap_figure:
        return {'display': 'none'}
    return {'height': '40vh', 'width': '100%'}


@app.callback(
    Output('heatmap-2', 'style'), 
    Input('heatmap-2', 'figure'))
def show_hide_heatmap_2(heatmap_figure):
    if not heatmap_figure:
        return {'display': 'none'}
    return {'height': '40vh', 'width': '100%'}

# top row
top_row = html.Div(
    [
        html.Div([
            dcc.Dropdown(
                id='video-dropdown',
                options=[{'label': option, 'value': option} for option in all_video_files],
                placeholder='Select a video file...',
                # value=None,
                value='video-1-segment-5',
                style={'border-color': 'gray'}            
                # style={'width': '200px', 'margin': '10px'}
            )],
            className='row'
        ),

        # I see text area
        html.Div([
            dcc.Dropdown(
                id='model-dropdown',
                options=[{'label': model, 'value': model} for model in available_models],
                placeholder='Select a Model',
                value='GPV-1',
                style={'border-color': 'gray'}            
            )], className='row'
        ),
        
        # I don't see text area
        html.Div([
            dcc.Markdown(children = '*Objects I **see** in the video:*'),
            dcc.Textarea(
                id='I-see',
                value='Wall, Bicycle, Bridge, Building, Bus, Bus Stop',
                placeholder='Things I see',
                style={'width': '100%', 'color': 'grey', 'font-style': 'italic'}
            )], className='two columns', style={'background-color': 'rgba(6, 200, 115, 0.5)'}

        ),

        html.Div([
            dcc.Markdown(children = '*Possible Objects:*'),
			dcc.Textarea(
                id='text-file-content',
                value=read_text_file_content('all_a11y_objects.txt'),  
                readOnly=True,
                style={'width': '100%', 'color': 'grey', 'font-style': 'italic'}
            )], className = 'seven columns'
        ),



        html.Div([
            dcc.Markdown('*Objects I **don\'t see** in the video:*'),            
            dcc.Textarea(
                id='I-dont-see',
                value='Guide dog, Gutter, Hose, Lamp Post, Mail box',
                placeholder='Things I do not see',
                style={'width': '100%', 'color': 'grey', 'font-style': 'italic'}      
            )], className='two columns', style={'background-color': 'rgba(211, 6, 50, 0.5)'} 
        ),

        html.Div([
            html.Button(
                'Analyze', 
                id='update-heatmap-button', 
                n_clicks=0, 
                style={'background-color': 'lightgray'}
            )], className='row'
        )         
    ], 
        className='row',
) 



heatmaps = html.Div(
    [        
        html.Div([        
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

        html.Div([        
            dcc.Graph(
                id='heatmap-2',
            ),
        html.Div(
                id='heatmap-popover-2',
                style={'position': 'relative'},
            ),                  
          ], className='five columns'
        ),
    ],
        className='row', 
)




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


tab_1_layout = html.Div(
    [        
        top_row,
        html.Div(id='output-folder-creation', style={'margin': '10px', 'display': 'none'}),

        html.Div(
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
    ]
)


app.layout = html.Div([
    html.Div(id="tab-content"),
])

@app.callback(Output("tab-content", "children"), Input("tabs", "value"))
def render_tab_content(tab):
    if tab == "tab-1":
        return tab_1_layout

app.layout.children[0].children = tab_1_layout


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
        
        colorscale_heatmap1 = [
                                
                                [0, 'rgb(255,255,255)'],
                                [1, 'rgb(6, 200, 115)'],
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

        layout = go.Layout(
            title="Things You See",
            title_x=0.55,
            title_y=0.95,
            title_font=dict(color='rgb(6, 200, 115)', family='Arial Black' ),
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


        colorscale_heatmap2 = [                          
                                 [0, 'rgb(255, 255, 255)'],
                                 [1, 'rgb(211, 6, 50)'], 
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
            title="Things You Do Not See",
            title_x=0.55,
            title_y=0.95,
            title_font=dict(color='rgb(211, 6, 50)', family='Arial Black' ),
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

if __name__ == '__main__':
    app.run_server(debug=True)