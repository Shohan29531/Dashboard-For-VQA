import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress

# Load the DataFrame from 'all.csv'
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

models = ['Random', 'Ground Truth', 'GPT4V', 'GPV-1', 'BLIP']

# Create a new column for 'see_count' * 'frames'
df['see_count_times_frames'] = df['see_count'] * df['frames']

for model in models:
    df_model = df[df['model left'] == model]

    # Perform linear regression
    slope, intercept, r_value, _, _ = linregress(df_model['see_count'], df_model['timing'])

    # Calculate R^2
    r_squared = r_value**2

    plt.figure(figsize=(10, 6))
    sns.regplot(data=df_model, x='see_count', y='timing', scatter_kws={'alpha':0.6}, line_kws={'label':f'R² = {r_squared:.2f}'})

    plt.title(f'Task Completion Time Vs. Objects Used for {model} Model')
    plt.xlabel('Number of Objects Used')
    plt.ylabel('Task Completion Time')
    plt.ylim(0, 400)
    plt.grid(True) 
    plt.legend()

    plt.tight_layout()
    plt.savefig('images/' + model + '.pdf')
    plt.close()  # Close the plot to ensure a new plot is created for each model
