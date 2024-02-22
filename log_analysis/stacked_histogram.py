import pandas as pd
import plotly.graph_objects as go
import time

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Define model pairs
models = ['Ground Truth', 'Random']

# Define expertise levels and corresponding colors
expertise_levels = ['Expert', 'Non-Expert']
expertise_colors = {'Expert': 'black', 'Non-Expert': 'lightgrey'}

# Adjust the X-axis range
x_range = (-2.5, 2.5)

for model in models:
    df_model = df[df['model left'] == model]

    fig = go.Figure()

    for i, expertise in enumerate(expertise_levels):
        # Create a histogram for each expertise level with the adjusted X-axis range
        fig.add_trace(go.Histogram(
            x=df_model[df_model['expertise'] == expertise]['normalized_score'],
            name=expertise,
            marker_color=expertise_colors[expertise],
            opacity=0.7,
            xbins=dict(start=x_range[0], end=x_range[1], size=0.1),  # Specify the adjusted X-axis range and bin size
            histnorm='percent',
            marker_line=dict(color='black', width=1)  # Add a border to the bars
        ))

    # Customize the layout
    fig.update_layout(
        title=dict(
            text=f'Z-Normalized User Ratings for {model}',
            x=0.5,
            font=dict(family='Arial', size=18, color='black')  # Increased font size by 2
        ),
        xaxis_title=dict(
            text='Z-Normalized User Rating',
            font=dict(family='Arial', size=16)  # Increased font size by 2
        ),
        yaxis_title=dict(
            text='Percentage of Users',
            font=dict(family='Arial', size=16)  # Increased font size by 2
        ),
        barmode='stack',
        xaxis=dict(
            range=x_range,  # Set the adjusted X-axis range
            gridcolor='white',
            gridwidth=0.01,
            tickfont=dict(size=14)  # Increased font size by 2
        ),
        yaxis=dict(
            gridcolor='lightgrey',
            gridwidth=0.01,
            showgrid=True,
            tickfont=dict(size=14)  # Increased font size by 2
        ),
        plot_bgcolor='white',
        font=dict(family='Arial', size=14)  # Increased font size by 2
    )

    # Position the legend in the middle at the top
    fig.update_layout(
        width=600,
        height=500,
        legend=dict(
            title=dict(
                text='Participant Expertise',
                font=dict(family='Arial', size=16)  # Increased font size by 2
            ),
            orientation='v',
            x=0.2 if model == 'Ground Truth' else 0.8,
            y=0.95,
            xanchor='center',
            yanchor='top',
            bordercolor='black',
            borderwidth=0
        )
    )

    fig.show()

    fig.write_image('../Paper files/' + f'{model}_stacked_histogram.pdf', format='pdf')
    time.sleep(0.5)
    fig.write_image('../Paper files/' + f'{model}_stacked_histogram.pdf', format='pdf')
