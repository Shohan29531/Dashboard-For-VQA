import pandas as pd
import plotly.express as px

# Assuming your DataFrame is named df and contains the relevant data
# Load the combined CSV

par = 'P2'

df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Filter data for participant P1
df_p1 = df[df['participant'] == par]
df_p1 = df_p1[df_p1['model left'].isin(['Ground Truth', 'Random'])]

# Create a histogram
fig = px.bar(
    df_p1,
    x='model left',
    y='score',
    color='model left',
    labels={'score': 'Score', 'model left': 'Model'},
    title='Scores for Participant ' + par + ' Across 24 Trials',
)

# Customize the layout
fig.update_layout(
    barmode='group',
    xaxis=dict(tickmode='array', tickvals=df_p1['model left'].unique()),  # Display each model on the x-axis
)

# Show the figure
fig.show()