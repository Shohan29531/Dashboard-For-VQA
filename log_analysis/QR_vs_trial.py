import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

df = pd.read_csv('../Logs/trimmed_logs/all.csv')

df['quality of rating'] = 1 - abs(df['F1-Base'] - df['normalized_score'])

# List of models present in your dataset
models = ['Random', 'GPV-1', 'BLIP', 'GPT4V', 'GPV-1@Shadow', 'BLIP@Shadow', 'GPT4V@Shadow']

for model in models:
    # Filter data for the current model
    model_data = df[df['model left'] == model]
    
    # Ensure 'trial' is treated as numeric for regression analysis
    model_data['trial'] = pd.to_numeric(model_data['trial'], errors='coerce')
    
    # Define the figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot 'trial' vs. 'quality of rating'
    scatter = ax.scatter(model_data['trial'], model_data['quality of rating'], label=model, alpha=0.7)
    
    # Attempt regression line calculation if 'trial' and 'quality of rating' have no NaNs
    if not model_data[['trial', 'quality of rating']].isnull().values.any():
        # Calculate regression line
        slope, intercept, _, _, _ = linregress(model_data['trial'], model_data['quality of rating'])
        regression_line_x = np.linspace(model_data['trial'].min(), model_data['trial'].max(), num=100)  # Generating X values
        regression_line_y = slope * regression_line_x + intercept
        
        # Plot regression line
        ax.plot(regression_line_x, regression_line_y, color='red', linestyle='--', label='Regression Line')
    
    # Labeling the plot
    ax.set_title(f"{model} Quality of Ratings vs. Trial")
    ax.set_xlabel('Trial')
    ax.set_ylabel('Quality of Ratings')
    ax.set_ylim([0, 1])  # Assuming 'quality of rating' is normalized between 0 and 1
    ax.legend()

    # Save the figure
    plt.tight_layout()
    plt.savefig(f'QR_data/trial_{model}.png')
    plt.close()  # Close the figure to reset for the next iteration
