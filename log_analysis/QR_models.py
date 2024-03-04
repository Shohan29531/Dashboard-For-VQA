import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# List of models present in your dataset
models = ['BLIP', 'BLIP@Shadow']

# Create a scatter plot for each model
fig, ax = plt.subplots(len(models), figsize=(20, 10*len(models)))  # Adjust figure size as needed

for i, model in enumerate(models):
    # Filter data for the current model
    model_data = df[df['model left'] == model]
    
    # Define colors based on 'F1-Base' scores
    colors = model_data['normalized_score']
    
    # Plot 'trial' vs. 'normalized_score' with colors based on 'F1-Base'
    scatter = ax[i].scatter(model_data['trial'], model_data['F1-Base'], c=colors, cmap='RdYlGn', label=model, alpha=0.5)
    
    # Adding a colorbar to show the mapping of 'F1-Base' scores to colors
    cbar = plt.colorbar(scatter, ax=ax[i])
    cbar.set_label('Normalized Ratings')
    
    # Labeling the plot
    ax[i].set_title(f"{model} Scores")
    ax[i].set_xlabel('Trial')
    ax[i].set_ylabel('F1 Score')
    ax[i].set_ylim([0, 1])
    ax[i].legend()

plt.tight_layout()
plt.show()
