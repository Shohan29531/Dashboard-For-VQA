import pandas as pd
import plotly.graph_objects as go
import time

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# df = df[~df['participant'].isin(['P9'])]

# Define model pairs
# models = ['Ground Truth', 'Random', 'BLIP', 'BLIP@Shadow', 'GPV-1', 'GPV-1@Shadow', 'GPT4V', 'GPT4V@Shadow']

models = ['Ground Truth', 'Random']

# Define shades of red, grey, and green
red_shades = ['#FF0000', '#FF3333', '#FF4D4D', '#FF8080', '#FFCCCC']
grey_shade = '#CCCCCC'
green_shades = ['#E0F8E0', '#A4D49A', '#68B055', '#409827', '#2E8B22']

for model in models:
    df_model = df[df['model left'] == model]

    # Count occurrences of each user rating for both models
    count = (((df_model['normalized_score']*10).round())/10).value_counts().sort_index().to_dict()

    # Ensure x_data and y_data have a length of 11
    x_data = [i/10 for i in range(11)]
    y_data = [count[i/10] if i/10 in count else 0 for i in range(11)]

    fig = go.Figure()

    fig.add_trace(go.Bar(x=x_data, y=y_data, name=model, marker_color=red_shades + [grey_shade] + green_shades))

    # Add a vertical line at x=5 with a specified width (above gridlines)
    fig.add_shape(
        go.layout.Shape(
            type="line",
            x0=0.5,
            x1=0.5,
            y0=y_data[5],
            y1=max(y_data) + 2,  # Adjust this value based on your data
            line=dict(color="black", width=2),
            layer='above'  # Ensure the line is above the gridlines but below the bars
        )
    )

    # Add a horizontal line at y=0 (above bars)
    fig.add_shape(
        go.layout.Shape(
            type="line",
            x0=-0.05,
            x1=1.05,
            y0=0,
            y1=0,
            line=dict(color="black", width=2),
            layer='above'  # Ensure the line is above the bars
        )
    )

    # Customize the layout
    fig.update_layout(
        title=dict(
            text=f'Comparative User Ratings for {model}',
            x=0.5,  # Center align the title
            font=dict(family='Arial', size=16, color='black')  # Use Arial font
        ),
        xaxis_title='User Rating',
        yaxis_title='Number of Users with this Rating',
        barmode='group',
        xaxis=dict(
            tickmode='array',
            tickvals=x_data,
            ticktext=[str(round(val, 1)) for val in x_data],
            gridcolor='lightgrey',  # Set gridline color
            gridwidth=0.01  # Set gridline width
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=list(range(0, max(y_data) + 1, 2)),
            ticktext=list(range(0, max(y_data) + 1, 2)),
            gridcolor='lightgrey',  # Set gridline color
            gridwidth=0.01  # Set gridline width
        ),
        plot_bgcolor='white',
        font=dict(family='Arial')  # Use Arial font for all text
    )

    fig.update_layout(
        width=600,
        height=500
    )

    fig.show()

    fig.write_image('../Paper files/' + f'{model}_histogram.pdf', format='pdf')
    time.sleep(0.5)
    fig.write_image('../Paper files/' + f'{model}_histogram.pdf', format='pdf')
