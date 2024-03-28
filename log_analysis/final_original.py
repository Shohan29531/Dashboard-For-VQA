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
    '<script type="text/javascript" async src="hhttps://cdnjs.cloudflare.com/ajax/libs/mathjax/3.0.0/es5/latest?tex-mml-chtml.js"></script>'
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
desired_order = ['Random', 'GPV-1', 'BLIP', 'GPT4V', 'Ground Truth']

# Filter dataframe based on desired order
df = df[df['model left'].isin(desired_order)]

# Create boxplot


# Adjustments for thinner boxes and increased spacing
box_width = 0.35  # Decrease box width for thinner boxes

# Generate ticktext with model names and F1 scores
f_mathcal_d = r"F_{1}^{\mathcal{D}}"
ticktext = [r"$\text{" + f"{model}" + r"}" + r" \\ (" + f_mathcal_d + f": {F1[model]:.3f})" + r"$" for model in desired_order]
# html.P('''\(Area\)(\(m^2\)) ''')
# ticktext = [r"<span>This is a vector: </span>$\vec{v} = \begin{bmatrix}x \\ y \\ z\end{bmatrix}$" for model in desired_order]


fig = go.Figure()

colors = {
    'Random': 'red',
    'Ground Truth': 'green',
    'GPV-1': '#6012cc',  
    'BLIP': '#0dcfd6',   
    'GPT4V': '#0a63f2'  
}

# Iterate over each model in the desired order
for model in desired_order:
    # Determine color based on the presence of 'Shadow'
    color = colors[model]
    
    # Extract scores for the current model
    scores = df[df['model left'] == model]['normalized_score']
    
    # Add box plot trace for the current model with adjusted box width
    fig.add_trace(go.Box(
        y=scores,
        name=f"{model} ({F1[model]:.3f})",  # Include F1 score in the name for legend
        marker=dict(
            color=color,  # Color for the box outline and whiskers
        ),
        line=dict(
            color=color,  # Ensure this matches marker color for consistency
            width=2  # Set line width for box
        ),
        fillcolor='white',  # Set the fill color of the box to white
        boxpoints=False,  # Do not show all data points
        showlegend=False,
        width=box_width  # Adjust box width here
    ))

# Adjust the figure's layout to indirectly increase spacing between boxes by manipulating the figure's overall width
fig.update_layout(
    title=dict(
        text='Normalized User Ratings for Different Models',
        x=0.5,  # Center align the title
        font=dict(family='Arial', size=20, color='black'),  # Increased font size
    ),
    yaxis_title='Normalized User Rating',
    xaxis=dict(
        title='Model',
        ticktext=ticktext,
        tickvals=list(range(len(desired_order))),  # Position each tick
    ),
    plot_bgcolor='white',
    font=dict(family='Arial', size=14),  # Increased font size
    yaxis=dict(
        showgrid=True,  # Show horizontal gridlines
        gridwidth=0.5,
        gridcolor='lightgrey',
        dtick=0.1,  # Set gridline interval
        range=[0, 1.25]
    ),
    width=600,  # Adjusted width
    height=700
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
                        showarrow=False, font=dict(family="Arial", size=16))
    else:
         fig.add_annotation(x=(x0+x1)/2, y=y+0.02, text=signf_level,
                        showarrow=False, font=dict(family="Arial", size=16))           


add_stat_signf(0, 4, 1.2, '***', fig=fig)

add_stat_signf(0, 3, 1.175, '***', fig=fig)
add_stat_signf(1, 4, 1.15, '***', fig=fig)

add_stat_signf(0, 2, 1.125, '***', fig=fig)
add_stat_signf(1, 3, 1.1, '**', fig=fig)
add_stat_signf(2, 4, 1.075, '***', fig=fig)

add_stat_signf(0, 1, 1.05, '***', fig=fig)
add_stat_signf(3, 4, 1.025, '***', fig=fig)

add_stat_signf(1, 2, 0.95, 'NS', fig=fig)
add_stat_signf(2, 3, 0.975, 'NS', fig=fig)









fig.show()

# Save the figure as a PDF
fig.write_image('../paper_files_latex/' + 'all_org_model_scores.pdf', format='pdf')
time.sleep(1.5)  # Ensure the file is saved before attempting to save again
fig.write_image('../paper_files_latex/' + 'all_org_model_scores.pdf', format='pdf')
