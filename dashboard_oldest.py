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



DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Dashboard Data')
LINE_GRAPH_DATA_DIR = os.path.join(DATA_DIR, 'Line graph data')
IMAGE_DATA_DIR = os.path.join(DATA_DIR, 'Images')



base_folder = DATA_DIR
images_source_folder = IMAGE_DATA_DIR
line_folder_path =  LINE_GRAPH_DATA_DIR
files = os.listdir(line_folder_path)
line_options = [os.path.splitext(file)[0] for file in files if file.endswith(".csv")]



available_models = ['GPV-1', 'BLIP']

num_frames = 100
fixed_heatmap_height = 350
heatmap_colorscale = [
    [0, 'rgb(211, 6, 50)'],
    [1, 'rgb(6, 200, 115)']
]

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])



def read_text_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content



@app.callback(
    Output('heatmap-1', 'style'), 
    Input('heatmap-1', 'figure'))
def show_hide_heatmap(heatmap_figure):
    if not heatmap_figure:
        return {'display': 'none'}
    return {'height': '40vh', 'width': '100%'}


# Define the layout
tab_1_layout = html.Div([

    html.Div([
        dcc.Dropdown(
            id='video-dropdown',
            options=[{'label': option, 'value': option} for option in line_options],
            placeholder='Select a file...',
            style={'width': '170px', 'margin': '10px'}
        ),
        dcc.Textarea(
            id='I-see',
            value='',
            placeholder='Things I see',
            style={'width': '300px', 'margin': '10px', 'color': 'grey', 'font-style': 'italic'}
        ),
        dcc.Textarea(
            id='I-dont-see',
            value='',
            placeholder='Things I do not see',
            style={'width': '300px', 'margin': '10px', 'color': 'grey', 'font-style': 'italic'}
        ),
        dcc.Dropdown(
            id='model-dropdown',
            options=[{'label': model, 'value': model} for model in available_models],
            placeholder='Select a Model',
            value=None,
            style={'width': '150px', 'margin': '10px'}
        ),
        html.Button('Update Heatmap', id='update-heatmap-button', n_clicks=0, 
                    style={'margin': '10px'}),
    ], 
    style={
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center',  # Vertically align items
        'gap': '10px'  # Set equal spacing between items
    }),



    html.Div(id='output-folder-creation', style={'margin': '10px'}),

    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='heatmap-1'), 
            ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),

            html.Div([
                html.Div(id='image-container', style={'display': 'flex', 'justify-content': 'center', 'flexWrap': 'wrap'},
                        children=[
                            html.Div([html.Div(f'{item}', style={'flex': '0 0 16.66%', 'padding': '10px'}) for item in []])
                        ]),
            ], style={'width': '70%', 'display': 'inline-block', 'display': 'flex', 'justify-content': 'center', 'flexWrap': 'wrap'})
            ,
            html.Div(
                dcc.Textarea(
                    id='text-file-content',
                    value=read_text_file_content('all_a11y_objects.txt'),  
                    readOnly=True,
                    style={'width': '95%', 'height': '120px', 'fontSize': '12px', 'margin-top': '50px'}
                ),
            ),
        ], style={'display': 'flex', 'justify-content': 'center', 'flex-direction': 'row'}),

        ## line graph hidden for now
        dcc.Graph(id='line-graph-1', style={'display': 'none'})
    ], style={'display': 'flex', 'justify-content': 'center', 'flex-direction': 'column'})
,


    html.Div(id='heatmap-click-coordinates', style={'display': 'none'}),

    dcc.Store(id='last-clicked-image-id'),

])

tab_2_layout =  html.Div([

    html.Div([
        dcc.Dropdown(
            id= 'video-dropdown-2',
            #'dropdown-2',
            options=[{'label': option, 'value': option} for option in line_options],
            placeholder='Select a file...',

            style={
                'width': '200px',
                'margin': '10px'
            }
        )
    ], style={'display': 'flex', 'justify-content': 'center'}),


    html.Div(id='output-folder-creation-2', style={'margin': '10px'}),

    html.Div([
        html.Div([
            dcc.Graph(id='heatmap-gpv', style={'height': '50vh', 'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='heatmap-lavis', style={'height': '50vh', 'width': '50%', 'display': 'inline-block'}),
        ], style={'width': '100%', 'display': 'inline-block'}),

        html.Div([
            html.Div(id='image-container-2', style={'display': 'flex', 'justify-content': 'center', 'flexWrap': 'wrap'},
                     children=[
                         html.Div(
                             [html.Div(f'{item}', style={'flex': '0 0 16.66%', 'padding': '10px'}) for item in []])
                     ]),
        ], style={'width': '100%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justify-content': 'center'}),

])


app.layout = html.Div([
    dcc.Tabs(id="tabs", value="tab-1", children=[
        dcc.Tab(label="Tab 1", value="tab-1",),
        dcc.Tab(label="Tab 2", value="tab-2",),
    ]),
    html.Div(id="tab-content"),
])



@app.callback(Output("tab-content", "children"), Input("tabs", "value"))
def render_tab_content(tab):
    if tab == "tab-1":
        return tab_1_layout

    elif tab == "tab-2":
        return tab_2_layout



@app.callback(Output('output-folder-creation', 'children'), Input('upload-csv', 'contents'), State('upload-csv', 'filename'))
def handle_csv_upload(contents, filename):
    if contents is not None and filename.endswith('.csv'):
        # Define the destination folder
        destination_folder = r"C:\Users\arish\OneDrive\Desktop\Dashboard\Organized Data\Questions"
        # Create the destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)


        # Extract the base64-encoded content from the Data URL
        match = re.match(r'data:.*;base64,(.*)', contents)
        if match:
            base64_content = match.group(1)
            # Decode the base64 content
            decoded_content = base64.b64decode(base64_content)

            # Save the decoded content to the destination folder
            uploaded_csv_path = os.path.join(destination_folder, filename)
            with open(uploaded_csv_path, 'wb') as f:
                f.write(decoded_content)


        return f'Successfully uploaded and saved CSV file.'
    return ''




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
        style={'position': 'absolute', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'margin': '5px', 'padding': '0', 'border': 'none', 'background': 'transparent'} 
    )

    frame_number_label = html.Label(
        frame_number,
        style={'position': 'absolute', 'top': '0px', 'left': '0px', 'color': 'rgb(252, 194, 3)', 'background-color': 'black', 'padding': '2px', 'font-weight': 'bold'}
    )

    image_div = html.Div(
        [
            dbc.CardImg(src=encoded_image, style={'width': '100%', 'height': 'auto'}),
            action_button,
            frame_number_label
        ],
    )

    card = dbc.Card(
        [
            image_div
        ],
        style={"width": "12rem", 'border': border_style, 'margin': '5px'},
        id={"type": "image-card", "index": frame_number}
    )
    return card






@app.callback(
        Output('image-container', 'children'),
        Output('last-clicked-image-id', 'data'),
        Input('video-dropdown', 'value'),
        Input('heatmap-1', 'hoverData'),
        [Input({"type": "action-button", "index": ALL}, "n_clicks_timestamp")],
        State({"type": "image-card", "index": ALL}, "id"),
        )
def update_image_container(selected_option,
                            hoverData,
                            click_timestamps, 
                            image_card_id
                            ):

    # print(selected_option, clickData, click_timestamps, image_card_id)

    trigger = ctx.triggered_id
    # if trigger:
    #     print("Trigger:" , trigger)


    if trigger != 'heatmap-1':
    # Handle image container click 
        if selected_option != None and image_card_id != []:
            print("For image container click.")
            latest_click_index = None
            latest_click_time = 0
            for i, timestamp in enumerate(click_timestamps):
                if timestamp and timestamp > latest_click_time:
                    latest_click_time = timestamp
                    latest_click_index = i

            chosen_frame_number = trigger["index"]

            image_names = os.listdir(images_source_folder)
            selected_option = selected_option.lower()
            image_names = [img.lower() for img in image_names]

            filtered_images = [img.strip() for img in image_names if img.startswith(selected_option)]

            filtered_images.sort(key=extract_frame_number)

            image_elements = []

            for image_name in filtered_images:
                frame_number = extract_frame_number(image_name)
                if frame_number == chosen_frame_number:
                    image_element = get_image_card(image_name, frame_number, True)
                else:
                    image_element = get_image_card(image_name, frame_number, False)

                image_elements.append(image_element)

            return image_elements, chosen_frame_number


    if hoverData and 'points' in hoverData and hoverData['points']:
        clicked_point = hoverData['points'][0]
        x_coord = str(clicked_point['x']).lower()
        y_coord = clicked_point['y']
    else:
        x_coord, y_coord = None, None  


    if selected_option:
        print("For Heatmap click.")
        image_names = os.listdir(images_source_folder)
        selected_option = selected_option.lower()
        image_names = [img.lower() for img in image_names]

        filtered_images = [img.strip() for img in image_names if img.startswith(selected_option)]

        filtered_images.sort(key=extract_frame_number)

        image_elements = []

        for image_name in filtered_images:
            frame_number = extract_frame_number(image_name)
            if f"frame-{frame_number}" == x_coord:
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
    Input('line-graph-1', 'clickData'),
    Input('heatmap-1', 'clickData'),
    Input('update-heatmap-button', 'n_clicks'),
    State('I-see', 'value'), 
    State('I-dont-see', 'value'),
    State('last-clicked-image-id', 'data'),
    [Input({"type": "action-button", "index": ALL}, "n_clicks_timestamp")],
    State({"type": "image-card", "index": ALL}, "id") 
)
def update_heatmaps(
    model, 
    selected_file, 
    line_graph_clickData,
    heatmap_clickData,
    n_clicks,                  
    textarea_example_value,    
    textarea_example_2_value, 
    last_clicked_image_id,
    dummy_1,
    dummy_2
):
    if n_clicks > 0 and model and selected_file:
        file_path = os.path.join(base_folder, model, selected_file + '.csv')
        heat_map_file = pd.read_csv(file_path)

        x_labels = [col for col in heat_map_file.columns if col != "Object"] 

        y_labels = list(heat_map_file.iloc[:80, 0])  
        z_values = heat_map_file.iloc[:80, 1:].values.tolist()  


        filtered_indices_see = [i for i, label in enumerate(y_labels) if label.lower() in textarea_example_value.lower()]
        filtered_indices_dont_see = [i for i, label in enumerate(y_labels) if label.lower() in textarea_example_2_value.lower()]
        
 
        filtered_indices = filtered_indices_see + [-1] + filtered_indices_dont_see
        
        y_labels_filtered = []
        z_values_filtered = []

        for i in filtered_indices:
            if i != -1:
                y_labels_filtered.append(y_labels[i])
                z_values_filtered.append(z_values[i])
            else:
                y_labels_filtered.append("")  # Add a blank label
                z_values_filtered.append([0.5] * len(x_labels))  # Blank row

        # ... (your existing code for creating heatmap)

        y_labels = y_labels_filtered
        z_values = z_values_filtered


        heatmap = go.Heatmap(
            x=x_labels,
            y=y_labels,
            z=z_values,
            colorscale=heatmap_colorscale,
            showscale = False
        )

        layout = go.Layout(
            title_x=0.5, 
            title_y=0.95,  
            margin={'t': 10, 'l': 10},
            coloraxis=dict(colorscale=heatmap_colorscale),
            height=len(y_labels) * 40, 
            width=len(x_labels) * 30,
            xaxis=dict(showgrid=False, dtick=1, gridwidth=1, tickfont=dict(size=11)), 
            yaxis=dict(showgrid=False, dtick=1, gridwidth=1, tickfont=dict(size=11))
        )

        heatmap_line_column = None
        if last_clicked_image_id:
            clicked_frame_number = last_clicked_image_id
            heatmap_line_column = x_labels.index(f'Frame-{clicked_frame_number}')
            heatmap_clickData = None



        # Initialize layout_shapes_list
        layout_shapes_list = []


        if line_graph_clickData and 'points' in line_graph_clickData and line_graph_clickData['points']:
            heatmap_clickData = None
            clicked_point = line_graph_clickData['points'][0]
            x_coord = str(clicked_point['x']).lower()

            frame_number = int(re.findall(r'\d+', x_coord)[-1])

            column_width = len(x_labels) * 30 / len(x_labels)  

            layout_shapes_list.append({
                'type': 'line',
                'x0': frame_number,
                'x1': frame_number,
                'y0': 0,
                'y1': 1,
                'xref': 'x',
                'yref': 'paper',
                'line': {
                    'color': 'white',  # Set the line color
                    'width': 15,  # Set the line width
                },
                'opacity': 0.8
            })

        if heatmap_clickData and 'points' in heatmap_clickData and heatmap_clickData['points']:
        # Remove the image click highlight
            last_clicked_image_id = None

            # Add the horizontal and vertical line shapes for heatmap click
            clicked_point = heatmap_clickData['points'][0]
            x_coord = clicked_point['x']
            y_coord = clicked_point['y']

            row_height = len(y_labels) * 15 / len(y_labels)  # Calculate row height

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
                        'color': 'yellow',  # Set the line color
                        'width': 15,  # Set the line width
                    },
                    'opacity': 0.8
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
                        'color': 'yellow',  # Set the line color
                        'width': 15,  # Set the line width
                    },
                    'opacity': 0.8
                }
            ])


        for i in range(len(x_labels)):
            layout_shapes_list.append({
                'type': 'line',
                'x0': i / len(x_labels),
                'x1': i / len(x_labels),
                'y0': 0,
                'y1': 1,
                'xref': 'paper',  # Set xref to 'paper'
                'yref': 'paper',  # Set yref to 'paper'
                'line': {
                    'color': 'black',  # Set the line color
                    'width': 1,  # Set the line width
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
                'yref': 'paper',  # Set yref to 'paper'
                'line': {
                    'color': 'black',  # Set the line color
                    'width': 1,  # Set the line width
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
                    'color': 'yellow',  # Set the line color
                    'width': 15,  # Set the line width
                },
                'opacity': 0.8
            })

        layout['shapes'] = tuple(layout_shapes_list)
        heat_map = go.Figure(data=heatmap, layout=layout)

        return heat_map

    return {}







@app.callback(Output('line-graph-1', 'figure'), Input('video-dropdown', 'value'), Input('heatmap-1', 'clickData'))
def update_line_graphs(selected_file, clickData):
    if selected_file:
        file_path = os.path.join(line_folder_path, selected_file + '.csv')
        line_graph_file = pd.read_csv(file_path)
        line_graph_file_modified = line_graph_file[["frame pair", "Similarity (Human)", "Similarity (VQA-based)", "resnet-50 feature similarity"]].copy()

        data = []
        excluded_column = "frame pair"

        for column in line_graph_file_modified.columns:
            if column != excluded_column:
                line = go.Scatter(
                    x=line_graph_file_modified["frame pair"],
                    y=line_graph_file_modified[column],
                    mode='lines',
                    name=column
                )
                data.append(line)

        layout = go.Layout(
            title='Line Graph',
            xaxis=dict(title='X-axis'),
            yaxis=dict(title='Y-axis'),
            showlegend=True,
            height=300  # height 300 pixels to fit within the page
        )

        #clicked tiles coordinates
        if clickData and 'points' in clickData and clickData['points']:
            clicked_point = clickData['points'][0]
            x_coord = str(clicked_point['x']).lower()
            y_coord = clicked_point['y']

            # Extract the frame number from x_coord
            frame_number = int(x_coord.split('-')[-1])

            # Add a vertical line shape to the layout
            layout['shapes'] = [{
                'type': 'line',
                'x0': frame_number, #width of the line
                'x1': frame_number,
                'y0': 0, #length of the line
                'y1': 1,  
                'xref': 'x',
                'yref': 'paper',
                'line': {
                    'color': 'black',
                    'width': 3
                }
            }]

        line_graph = go.Figure(data=data, layout=layout)
        return line_graph

    return {}






@app.callback(Output('image-container-2', 'children'), Input('video-dropdown-2', 'value'))
def update_image_container_2(selected_option):

    if selected_option:
        # Get the list of images in the current directory
        image_names = os.listdir(images_source_folder)

        # selected_option and image_names to lowercase
        selected_option = selected_option.lower()
        image_names = [img.lower() for img in image_names]

        # Filter images
        filtered_images = [img.strip() for img in image_names if img.startswith(selected_option)]

        # Sort images based on the frame number
        filtered_images.sort(key=extract_frame_number)

        image_elements = []

        for image_name in filtered_images:
            encoded_image = get_encoded_image(image_name)

            # Extract frame number from the image filename
            frame_number = extract_frame_number(image_name)

            image_element = get_image_card(image_name, frame_number, False)
            image_elements.append(image_element)

        return image_elements
    else:
        return []






@app.callback(Output('heatmap-gpv', 'figure'), Input('video-dropdown-2', 'value'))
def update_heatmap_gpv(selected_file):
    if selected_file:
        model = 'model GPV'
        file_path = os.path.join(base_folder, model, selected_file + '.csv')
        heat_map_file = pd.read_csv(file_path)

        x_labels = [col for col in heat_map_file.columns if col != "Object"] 

        # taking only the first 45 to fit within the page
        y_labels = list(heat_map_file.iloc[:45, 0])  
        z_values = heat_map_file.iloc[:45, 1:].values.tolist()  


        heatmap = go.Heatmap(
            x=x_labels,
            y=y_labels,
            z=z_values,
            colorscale=heatmap_colorscale
        )

        layout = go.Layout(
            title='Heatmap GPV',
            title_x=0.5, 
            title_y=0.95,  
            coloraxis=dict(colorscale=heatmap_colorscale, colorbar=dict(tickvals=[0, 1], ticktext=["Not Present", "Present"])),
            height=len(y_labels) * 15, 
            width=len(x_labels) * 30,
            xaxis=dict(showgrid=True, dtick=1, gridwidth=2),  
            yaxis=dict(showgrid=True, dtick=1, gridwidth=2)  
        )

        heat_map = go.Figure(data=heatmap, layout=layout)

        return heat_map

    return {}



@app.callback(Output('heatmap-lavis', 'figure'), Input('video-dropdown-2', 'value'))
def update_heatmap_gpv(selected_file):
    if selected_file:
        model = 'model LAVIS'
        file_path = os.path.join(base_folder, model, selected_file + '.csv')
        heat_map_file = pd.read_csv(file_path)

        x_labels = [col for col in heat_map_file.columns if col != "Object"] 

        # taking only the first 45 to fit within the page
        y_labels = list(heat_map_file.iloc[:45, 0])  
        z_values = heat_map_file.iloc[:45, 1:].values.tolist()  

        heatmap = go.Heatmap(
            x=x_labels,
            y=y_labels,
            z=z_values,
            colorscale=heatmap_colorscale
        )

        layout = go.Layout(
            title='Heatmap LAVIS',
            title_x=0.5, 
            title_y=0.95,  
            coloraxis=dict(colorscale=heatmap_colorscale, colorbar=dict(tickvals=[0, 1], ticktext=["Not Present", "Present"])),
            height=len(y_labels) * 15, 
            width=len(x_labels) * 30,
            xaxis=dict(showgrid=True, dtick=1, gridwidth=2),  
            yaxis=dict(showgrid=True, dtick=1, gridwidth=2)  
        )

        heat_map = go.Figure(data=heatmap, layout=layout)

        return heat_map

    return {}




if __name__ == '__main__':
    app.run_server(debug=False)