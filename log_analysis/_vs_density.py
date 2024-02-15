import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Define model pairs
model_pairs = [('GT_N', 'Random'), ('BLIP', 'BLIP@Shadow'), ('GPV-1', 'GPV-1@Shadow'), ('GPT4V', 'GPT4V@Shadow')]

# Set Arial as the font


for model_1, model_2 in model_pairs:
    plt.rcParams['font.family'] = 'Arial'

    plt.figure(figsize=(12, 6))
    df_model_1 = df[df['model left'] == model_1]
    df_model_2 = df[df['model left'] == model_2]

    # Create probability density function (PDF) using Seaborn with higher zorder
    sns.kdeplot(data=df_model_1['score'], label=model_1, fill=True, alpha=0.7, zorder=5, color = '#4499bf')
    sns.kdeplot(data=df_model_2['score'], label=model_2, fill=True, alpha=0.7, zorder=5, color='#A21143')

    # Customize plot labels and title
    plt.xlabel('User Rating', fontsize=14)  # Set font size for X-axis label
    plt.ylabel('Probability Density', fontsize=14)  # Set font size for Y-axis label
    plt.title("Probability Density Function for " + model_1 + ' Vs. ' + model_2, fontsize=15)

    # Add legend
    plt.legend(title='Models', title_fontsize='14', fontsize='12', loc='upper left')

    # Add grid lines with lower zorder value
    plt.grid(True, linestyle='--', alpha=0.7, zorder=0)

    # Save the plot as an image file (e.g., PDF)
    plt.savefig('../Paper files/' + model_1 + "_vs_" + model_2 + '_density.pdf')
    # Show the plot
    plt.show()

