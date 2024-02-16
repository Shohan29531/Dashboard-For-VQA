import pandas as pd
import plotly.graph_objects as go
import numpy as np
import time

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

# Calculate the average of all ratings for each model
avg_ratings = df.groupby('model left')['score'].mean()

# Create a scatter plot for average ratings against F1 scores
fig = go.Figure()

for model in F1:
    # Add a scatter plot trace
    fig.add_trace(go.Scatter(
        x=[avg_ratings[model]],
        y=[F1[model]],
        mode='markers',
        name=model,
        marker=dict(color='blue', size=8),
        text=model,  # Show model names on hover
        showlegend=True
    ))

# Add a correlation line
z = np.polyfit(avg_ratings, list(F1.values()), 1)
p = np.poly1d(z)
fig.add_trace(go.Scatter(
    x=avg_ratings,
    y=p(avg_ratings),
    mode='lines',
    name='Correlation Line',
    line=dict(color='red', width=2, dash='dash')
))

# Customize the layout
fig.update_layout(
    title=dict(
        text='Average User Ratings vs. F1 Scores for 8 Models',
        x=0.5,  # Center align the title
        font=dict(family='Arial', size=16, color='black')  # Use Arial font
    ),
    xaxis_title='Average User Rating',
    yaxis_title='F1 Score',
    plot_bgcolor='white',
    font=dict(family='Arial'),  # Use Arial font for all text
)

# Show the figure
fig.show()

# Save the figure as a PDF
fig.write_image('../Paper files/' + 'avg_user_ratings_vs_F1_scores.pdf', format='pdf')
time.sleep(0.5)
fig.write_image('../Paper files/' + 'avg_user_ratings_vs_F1_scores.pdf', format='pdf')
