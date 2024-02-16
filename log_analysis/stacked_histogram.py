import pandas as pd
import plotly.graph_objects as go
import time

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# df = df[~df['participant'].isin(['P9'])]

# Define model pairs
# models = ['Ground Truth', 'Random', 'BLIP', 'BLIP@Shadow', 'GPV-1', 'GPV-1@Shadow', 'GPT4V', 'GPT4V@Shadow']

models = ['Ground Truth', 'Random']

# Define expertise levels and corresponding colors
expertise_levels = ['High', 'Moderate', 'Low']
expertise_colors = {'High': 'green', 'Moderate': 'yellow', 'Low': 'red'}

for model in models:
    df_model = df[df['model left'] == model]

    fig = go.Figure()

    for i, expertise in enumerate(expertise_levels):
        # Count occurrences of each user rating for both models and each expertise level
        count = (((df_model[df_model['expertise'] == expertise]['normalized_score']*10).round())/10).value_counts().sort_index().to_dict()

        # Ensure x_data and y_data have a length of 11
        x_data = [i/10 for i in range(11)]
        y_data = [count[i/10] if i/10 in count else 0 for i in range(11)]

        # Add a trace for each expertise level with corresponding color
        fig.add_trace(go.Bar(
            x=x_data,
            y=y_data,
            text=y_data,
            textposition='auto',
            hoverinfo='y+text',
            name=expertise,
            marker_color=expertise_colors[expertise],
        ))

    # Customize the layout
    fig.update_layout(
        title=dict(
            text=f'Comparative User Ratings for {model}',
            x=0.5,
            font=dict(family='Arial', size=16, color='black')
        ),
        xaxis_title='User Rating',
        yaxis_title='Number of Users with this Rating',
        barmode='stack',
        xaxis=dict(
            tickmode='array',
            tickvals=[i/10 for i in range(11)],
            ticktext=[str(i/10) for i in range(11)],
            gridcolor='lightgrey',
            gridwidth=0.01
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=list(range(0, max(y_data) + 2, 2)),
            ticktext=list(range(0, max(y_data) + 2, 2)),
            gridcolor='lightgrey',
            gridwidth=0.01,
            showgrid=True  # Add this line to display the grid and y-axis labels
        ),
        plot_bgcolor='white',
        font=dict(family='Arial')
    )

    fig.update_layout(
        width=600,
        height=500
    )

    fig.show()

    fig.write_image('../Paper files/' + f'{model}_stacked_histogram_color.pdf', format='pdf')
    time.sleep(0.5)
    fig.write_image('../Paper files/' + f'{model}_stacked_histogram_color.pdf', format='pdf')
