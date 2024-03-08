import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

df = pd.read_csv('../Logs/trimmed_logs/all.csv')

df['quality of rating'] = 1 - abs(df['F1-Base'] - df['normalized_score'])

# List of models present in your dataset
models = ['Random', 'Ground Truth' ,'GPV-1', 'BLIP', 'GPT4V', 'GPV-1@Shadow', 'BLIP@Shadow', 'GPT4V@Shadow']

for model in models:
    # Filter data for the current model
    model_data = df[df['model left'] == model]
    
    # Define the figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot 'F1-Base' vs. 'normalized_score'
    scatter = ax.scatter(model_data['F1-Base'], model_data['quality of rating'], label=model, alpha=0.7)
    
    # Calculate regression line
    if model != 'Ground Truth': 
        slope, intercept, _, _, _ = linregress(model_data['F1-Base'], model_data['quality of rating'])
        regression_line_x = np.array([0, 1]) 
        regression_line_y = slope * regression_line_x + intercept
   
        ax.plot(regression_line_x, regression_line_y, color='red', linestyle='--', label='Regression Line')
    
    # Labeling the plot
    ax.set_title(f"{model} Ratings vs. F1 Score")
    ax.set_xlabel('F1 Score')
    ax.set_ylabel('Quality of Ratings')
    ax.set_xlim([0, 1])  # Assuming F1 score is between 0 and 1
    ax.set_ylim([0, 1])  # Assuming normalized ratings are between 0 and 1
    ax.legend()

    # Save the figure
    plt.tight_layout()
    plt.savefig(f'QR_data/{model}.pdf')
    plt.close()  
