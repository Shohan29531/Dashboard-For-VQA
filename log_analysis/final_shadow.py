import pandas as pd
# import plotly.graph_objects as go
import time
import numpy as np
import plotly
# import plotly.graph_objs as go
from IPython.display import display, HTML

go = plotly.graph_objs

plotly.offline.init_notebook_mode()
display(HTML(
    '<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_SVG"></script>'
))


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
# exclude_videos = ['video-6-segment-2', 'video-7-segment-2', 'video-13-segment-2', 'video-1-segment-5']
# df = df[~df['video'].isin(exclude_videos)]

# Define the desired order and ensure it matches F1 dictionary
desired_order = ['GPV-1@Shadow', 'GPV-1', 'BLIP@Shadow', 'BLIP', 'GPT4V@Shadow', 'GPT4V']

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

# Colors for original and shadow models
color_original = 'rgb(55, 83, 109)'  # Darker color
color_shadow = 'rgb(164, 194, 244)'  # Lighter color

# Generate ticktext with model names and F1 scores, and calculate tickvals
f_mathcal_d = r"F_{1}^{\mathcal{O}}"
ticktext = []
tickvals = []
for model in desired_order:
    if model not in ticktext:  # Avoid duplicates
        ticktext.append(r"$\text{" + f"{model}" + r"}" + r"\\(" + f_mathcal_d + f": {F1[model]:.3f})" + r"$")
        tickvals.append(x_positions[model])


colors = {
    'GPV-1': '#6012cc', 
    'GPV-1@Shadow': '#c2b5e9',  # Much lighter version of #6012cc
    'BLIP': '#0dcfd6', 
    'BLIP@Shadow': '#a0eff2',   # Much lighter version of #0dcfd6
    'GPT4V': '#0a63f2',  
    'GPT4V@Shadow': '#b0d3fa',  # Much lighter version of #0a63f2
}




# Iterate over each model in the desired order
for model in desired_order:
    # Determine color based on the presence of '@Shadow'
    color = colors[model]
    
    # Extract scores for the current model
    scores = df[df['model left'] == model]['normalized_score']
    
    # Add box plot trace for the current model with adjusted box width and specific x position
    fig.add_trace(go.Box(
        y=scores,
        name=f"{model} ({F1[model]:.3f})",  # Include F1 score in the name for legend
        marker=dict(
            color=color  # Color for the markers if boxpoints is enabled
        ),
        line=dict(
            color=color,  # Color for the box outline and whiskers
            width=2  # Set line width for box
        ),
        fillcolor='white',  # Set the fill color of the box to white
        boxpoints=False,  # Do not show all data points
        showlegend=False,
        width=0.35,  # Adjust box width here
        x=[x_positions[model]] * len(scores)  # Set x positions for boxes
    ))


# Adjust the figure's layout
fig.update_layout(
    title=dict(
        text='User Ratings for Original and Shadow Models',
        x=0.5,  # Center align the title
        font=dict(family='Arial', size=22, color='black'),  # Increased font size
    ),
    yaxis_title='User Rating',
    xaxis=dict(
        title='Model',
        ticktext=ticktext,
        tickvals=tickvals,
    ),
    plot_bgcolor='white',
    font=dict(family='Arial', size=22),  # Increased font size
    yaxis=dict(
        showgrid=True,  # Show horizontal gridlines
        gridwidth=0.5,
        gridcolor='lightgrey',
        dtick=0.1,  # Set gridline interval
        range=[0, 1]
    ),
    width=800,  # Adjusted width
    height=800,
    boxmode='group'  # Group boxes by x position
)

fig.update_xaxes(tickangle=45)


def add_stat_signf(x0, x1, y, signf_level, fig):

    # Add a horizontal line from x=0 to x=1 at y=0.95
    fig.add_shape(type="line",
                x0=x0, y0=y, x1=x1, y1=y,
                line=dict(color="black", width=1))

    # Adding caps to the horizontal line to create tips at both ends
    fig.add_shape(type="line",
                x0=x0, y0=y-0.005, x1=x0, y1=y+0.005,
                line=dict(color="black", width=1))

    fig.add_shape(type="line",
                x0=x1, y0=y-0.005, x1=x1, y1=y+0.005,
                line=dict(color="black", width=1))

    # Add annotation at the center of the line
    if signf_level != 'NS':
        fig.add_annotation(x=(x0+x1)/2, y=y, text=signf_level,
                        showarrow=False, font=dict(family="Arial", size=20))
    else:
         fig.add_annotation(x=(x0+x1)/2, y=y+0.02, text=signf_level,
                        showarrow=False, font=dict(family="Arial", size=20))


add_stat_signf(1, 1.5, 0.95, '*', fig=fig)
add_stat_signf(3, 3.5, 0.95, 'NS', fig=fig)
add_stat_signf(5, 5.5, 0.95, '***', fig=fig)




# Show the figure
fig.show()

# Save the figure as a PDF
fig.write_image('../paper_files_latex/' + 'all_shadow_model_scores.pdf', format='pdf')
time.sleep(2.5)  # Ensure the file is saved before attempting to save again
fig.write_image('../paper_files_latex/' + 'all_shadow_model_scores.pdf', format='pdf')
