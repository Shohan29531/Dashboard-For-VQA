import pandas as pd
import plotly.graph_objects as go
import time

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Define model pairs
models = ['Ground Truth', 'Random']

# Define expertise levels and corresponding colors
expertise_levels = ['Expert', 'Novice/Intermediate']
expertise_colors = {'Expert': 'black', 'Novice/Intermediate': 'lightgrey'}

# Find the common X-axis range
x_range = (
    min(df[df['model left'] == models[0]]['normalized_score'].min(), df[df['model left'] == models[1]]['normalized_score'].min()),
    max(df[df['model left'] == models[0]]['normalized_score'].max(), df[df['model left'] == models[1]]['normalized_score'].max())
)

for model in models:
    df_model = df[df['model left'] == model]

    fig = go.Figure()

    for i, expertise in enumerate(expertise_levels):
        # Create a histogram for each expertise level with the common X-axis range
        fig.add_trace(go.Histogram(
            x=df_model[df_model['expertise'] == expertise]['normalized_score'],
            name=expertise,
            marker_color=expertise_colors[expertise],
            opacity=0.7,
            xbins=dict(start=x_range[0], end=x_range[1], size=0.03),  # Specify the common X-axis range and bin size
            histnorm='percent',
            marker_line=dict(color='black', width=1)  # Add border to the bars
        ))

    # Customize the layout
    fig.update_layout(
        title=dict(
            text=f'Comparative User Ratings for {model}',
            x=0.5,
            font=dict(family='Arial', size=16, color='black')
        ),
        xaxis_title='Z-Normalized User Rating',
        yaxis_title='Percentage of Users',
        barmode='stack',
        xaxis=dict(
            range=x_range,  # Set the common X-axis range
            gridcolor='white',
            gridwidth=0.01
        ),
        yaxis=dict(
            gridcolor='lightgrey',
            gridwidth=0.01,
            showgrid=True
        ),
        plot_bgcolor='white',
        font=dict(family='Arial')
    )

    # Position the legend in the middle at the top
    fig.update_layout(
        width=600,
        height=500,
        legend=dict(
            title='Participant Expertise',
            orientation='v',
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            bordercolor='black',
            borderwidth=0.5
        )
    )

    fig.show()

    fig.write_image('../Paper files/' + f'{model}_stacked_histogram.pdf', format='pdf')
    time.sleep(0.5)
    fig.write_image('../Paper files/' + f'{model}_stacked_histogram.pdf', format='pdf')
