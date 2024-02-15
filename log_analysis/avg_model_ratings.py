import pandas as pd
import plotly.graph_objects as go



F1 = {
 'GT_N': 1.0,
 'GPT4V': 0.8992731048805815,
 'GPT4V@Shadow': 0.8992731048805815,
 'BLIP': 0.8222433460076046,
 'BLIP@Shadow': 0.8222433460076046,
 'GPV-1': 0.7855787476280834,
 'GPV-1@Shadow': 0.7855787476280834,
 'Random': 0.3337837837837838,
}


# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Calculate average scores for each model
average_scores = df.groupby('model left')['score'].mean().sort_values()

# Create boxplots for each model, ordered by average score
fig = go.Figure()

# Iterate over each model in the sorted order
for model in average_scores.index:
    # Filter data for the current model
    model_data = df[df['model left'] == model]

    # Add a boxplot trace
    fig.add_trace(go.Box(
        x=[model] * len(model_data),
        y=model_data['score'],
        name=model,
        marker_color='#888888'
    ))

# Customize the layout
fig.update_layout(
    title=dict(
        text='Average User Ratings for 8 Models',
        x=0.5,  # Center align the title
        font=dict(family='Arial', size=16, color='black')  # Use Arial font
    ),
    xaxis_title='Model',
    yaxis_title='User Rating',
    plot_bgcolor='white',
    font=dict(family='Arial'),  # Use Arial font for all text
    xaxis=dict(
        tickmode='array',
        tickvals=list(average_scores.index),
        ticktext=list(average_scores.index),
        tickangle=45,  # Rotate tick labels for better readability
        gridcolor='lightgrey',  # Set gridline color
        gridwidth=0.1  # Set gridline width
    ),
    yaxis=dict(
        gridcolor='lightgrey',  # Set gridline color
        gridwidth=0.1  # Set gridline width
    ),
)

# Show the figure
fig.show()
