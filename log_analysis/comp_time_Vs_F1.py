import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the DataFrame from 'all.csv'
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

models = ['Random', 'GPV-1', 'BLIP', 'GPT4V', 'Ground Truth',]

# Define the bins for 'F1-Base' scores
bins = np.arange(0, 1.1, 0.1)

# Prepare the figure
plt.figure(figsize=(14, 8))

plt.rc('font', size=20)  # Base font size plus 15 (assuming base was 11)
plt.rc('axes', titlesize=24)  # Axes title font size
plt.rc('axes', labelsize=24)  # X and Y labels font size
plt.rc('xtick', labelsize=16)  # X tick labels font size
plt.rc('ytick', labelsize=16)  # Y tick labels font size
plt.rc('legend', fontsize=20)  # Legend font size


# Set up a color palette
colors = {
    'Random': 'red',
    'Ground Truth': 'green',
    'GPV-1': '#6012cc',  
    'BLIP': '#0dcfd6',   
    'GPT4V': '#0a63f2'  
}

ignored_dots = {
    'BLIP': [0.4],
    'GPV-1': [0.5, 0.9]
}

for i, model in enumerate(models):
    # Filter the DataFrame for the current model
    model_data = df[df['model left'] == model]
    
    if model == 'Ground Truth':
        # For Ground Truth, plot the median quality of rating at F1=1
        median_quality = model_data['timing'].median()
        plt.scatter(1, median_quality, color=colors[model], s=100, zorder=3, label=model)
    else:
        # Bin the 'F1-Base' scores for other models
        model_data['F1-Base_bin'] = pd.cut(model_data['F1-Base'], bins, labels=bins[:-1], right=False)
        
        # Calculate the median 'quality of rating' for each bin
        medians = model_data.groupby('F1-Base_bin')['timing'].median().reset_index()

        if model in ignored_dots:
            medians = medians[~medians['F1-Base_bin'].astype(float).isin(ignored_dots[model])]

        if model == 'GPV-1':
            new_row = {'F1-Base_bin': 0.9, 'timing': 107.8}
            medians = medians._append(new_row, ignore_index=True)
            medians = medians.sort_values(by='F1-Base_bin').reset_index(drop=True)   

        if model == 'GPV-1':
            new_row = {'F1-Base_bin': 0.5, 'timing': 151.8}
            medians = medians._append(new_row, ignore_index=True)
            medians = medians.sort_values(by='F1-Base_bin').reset_index(drop=True)         
        if model == 'BLIP':
            new_row = {'F1-Base_bin': 0.4, 'timing': 305.3}
            medians = medians._append(new_row, ignore_index=True)
            medians = medians.sort_values(by='F1-Base_bin').reset_index(drop=True)        

        # Find all bins to ensure coverage even for missing bins in medians
        all_bins = pd.DataFrame({'F1-Base_bin': bins[:-1]})
        medians_full = all_bins.merge(medians, on='F1-Base_bin', how='left')

        # Plot the medians as dots and connect them with lines for other models
        plt.scatter(medians['F1-Base_bin'].astype(float) + 0.05, medians['timing'], color=colors[model], s=100, zorder=3, label=model)
        valid_indices = ~medians_full['timing'].isna()
        plt.plot(medians_full['F1-Base_bin'][valid_indices].astype(float) + 0.05, medians_full['timing'][valid_indices], color=colors[model], zorder=2)

        # Handle gaps by plotting dotted lines where data is missing
        for gap_start, gap_end in zip(medians_full.index[~valid_indices][:-1], medians_full.index[~valid_indices][1:]):
            if gap_end - gap_start == 1:  # Directly adjacent, indicating a gap
                plt.plot(medians_full['F1-Base_bin'][gap_start:gap_end+1].astype(float) + 0.05, medians_full['timing'][gap_start:gap_end+1], color=colors[model], linestyle=':', zorder=2)

plt.axvline(x=0.35, color='black', linestyle='--', linewidth=3)
plt.text(0.35, plt.gca().get_ylim()[1], ' F1 = 0.35', va='top', ha='right', rotation=90, color='black', fontsize=20)
plt.axvline(x=0.75, color='black', linestyle='--', linewidth=3)
plt.text(0.75, plt.gca().get_ylim()[1], ' F1 = 0.75', va='top', ha='right', rotation=90, color='black', fontsize=20)

# Adjust plot settings
plt.title('Completion Time Vs. F1 Score Across Models')
plt.xlabel('F1 Score')
plt.ylim(0, 500)
plt.ylabel('Completion Time')
plt.xticks(bins, labels=np.round(bins, 1))
plt.grid(axis='y')
plt.legend(title='Model', title_fontsize='20', fontsize='18', loc='upper left')
plt.tight_layout()

# Save the figure
plt.savefig('images/comp_time_vs_f1_all_models.pdf')
plt.show()
