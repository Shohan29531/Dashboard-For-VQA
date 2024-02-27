import pandas as pd
import plotly.graph_objects as go
import time
import numpy as np

# F1 scores
F1 = {
    'Ground Truth': 1.0,
    'GPT4V': 0.899,
    'GPT4V@Shadow': 0.899,
    'BLIP': 0.822,
    'BLIP@Shadow': 0.822,
    'GPV-1': 0.786,
    'GPV-1@Shadow': 0.786,
    'Random': 0.334,
}

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Convert 'model left' column to string
df['model left'] = df['model left'].astype(str)

# Exclude participants P2, P6, P9, and P14
exclude_videos = ['video-6-segment-2', 'video-7-segment-2', 'video-13-segment-2', 'video-1-segment-5']
df = df[~df['video'].isin(exclude_videos)]

# Define the desired order and ensure it matches F1 dictionary
desired_order = ['GPV-1@Shadow', 'GPV-1','BLIP@Shadow', 'BLIP',  'GPT4V@Shadow', 'GPT4V']

# Filter dataframe based on desired order
df = df[df['model left'].isin(desired_order)]

# Create boxplot
fig = go.Figure()

# Manual x positions to control spacing
x_positions = {
    'GPV-1': 1, 'GPV-1@Shadow': 1.5,
    'BLIP': 3, 'BLIP@Shadow': 3.5,
    'GPT4V': 5, 'GPT4V@Shadow': 5.5,
}

# Generate ticktext with model names and F1 scores, and calculate tickvals
ticktext = []
tickvals = []
for model in desired_order:
    if model not in ticktext:  # Avoid duplicates
        ticktext.append(f"{model}<br>(F1: {F1[model]:.3f})")
        tickvals.append(x_positions[model])

# Iterate over each model in the desired order
for model in desired_order:
    # Determine color based on the presence of 'Shadow'
    color = 'rgb(100, 100, 100)'
    
    # Extract scores for the current model
    scores = df[df['model left'] == model]['normalized_score']
    
    # Add box plot trace for the current model with adjusted box width and specific x position
    fig.add_trace(go.Box(
        y=scores,
        name=f"{model} ({F1[model]:.3f})",  # Include F1 score in the name for legend
        marker_color=color,
        boxpoints=False,  # Do not show all data points
        line=dict(width=2),  # Set line width for box
        showlegend=False,
        width=0.35,  # Adjust box width here
        x=[x_positions[model]] * len(scores)  # Set x positions for boxes
    ))

# Adjust the figure's layout to indirectly increase spacing between boxes by manipulating the figure's overall width
fig.update_layout(
    title=dict(
        text='Normalized User Ratings for Different Models',
        x=0.5,  # Center align the title
        font=dict(family='Arial', size=20, color='black'),  # Increased font size
    ),
    yaxis_title='Normalized User Data',
    xaxis=dict(
        title='Model',
        ticktext=ticktext,
        tickvals=tickvals,
    ),
    plot_bgcolor='white',
    font=dict(family='Arial', size=14),  # Increased font size
    yaxis=dict(
        showgrid=True,  # Show horizontal gridlines
        gridwidth=0.5,
        gridcolor='lightgrey',
        dtick=0.1,  # Set gridline interval
        range=[0, 1]
    ),
    width=800,  # Adjusted width
    height=600,
    boxmode='group'  # Group boxes by x position
)

# Show the figure
fig.show()

# Save the figure as a PDF
fig.write_image('../Paper files/' + 'all_shadow_model_scores.pdf', format='pdf')
time.sleep(0.5)  # Ensure the file is saved before attempting to save again
fig.write_image('../Paper files/' + 'all_shadow_model_scores.pdf', format='pdf')
