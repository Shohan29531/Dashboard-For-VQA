import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Define model pairs
model_pairs = [('GT_N', 'Random'), ('BLIP', 'BLIP@Shadow'), ('GPV-1', 'GPV-1@Shadow'), ('GPT4V', 'GPT4V@Shadow')]

for model_1, model_2 in model_pairs:
    plt.rcParams['font.family'] = 'Arial'

    plt.figure(figsize=(12, 6))
    df_model_1 = df[df['model left'] == model_1]
    df_model_2 = df[df['model left'] == model_2]

    # Create scatter plot
    sns.scatterplot(data=df_model_1, x='F1-Base', y='score', label=model_1, alpha=0.7, zorder=5, color='#4499bf')
    sns.scatterplot(data=df_model_2, x='F1-Base', y='score', label=model_2, alpha=0.7, zorder=5, color='#A21143')

    # Customize plot labels and title
    plt.xlabel('F1 Score', fontsize=14)  # Set font size for X-axis label
    plt.ylabel('User rating', fontsize=14)  # Set font size for Y-axis label
    plt.title("Scatter Plot for " + model_1 + ' Vs. ' + model_2, fontsize=15)

    # Add legend
    plt.legend(title='Models', title_fontsize='14', fontsize='12', loc='upper left')

    # Add grid lines with lower zorder value
    plt.grid(True, linestyle='--', alpha=0.7, zorder=0)

    # Save the plot as an image file (e.g., PDF)
    plt.savefig('../Paper files/' + model_1 + "_vs_" + model_2 + '_scatter.pdf')
    # Show the plot
    plt.show()
