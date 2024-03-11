import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
from scipy.stats import mannwhitneyu


# Load the DataFrame from 'all.csv'
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Ignore all rows where 'trial' equals 1
df = df[df['trial'] != 1]

# Ensure 'frames' column is present and has meaningful values

# Define the models of interest
models = ['Random', 'Ground Truth', 'GPV-1', 'BLIP', 'GPT4V', 'GPV-1@Shadow', 'BLIP@Shadow', 'GPT4V@Shadow']

# Calculate 'time per frame' as a new metric
df['time_per_frame'] = df['timing'] / df['frames']

# Filter the DataFrame to include only the specified models
df_filtered = df[df['model left'].isin(models)]

# Plotting the new metric
plt.figure(figsize=(12, 8))  # Adjust the figure size as needed
sns.boxplot(x='model left', y='time_per_frame', data=df_filtered, order=models)

plt.title('Completion Time per Frame for Each Model')
plt.xlabel('Model')
plt.ylabel('Completion Time per Frame')
plt.ylim(0, 40)  # Adjust the y-axis limit as needed
plt.xticks(rotation=45)  # Rotate the model names for better readability

plt.tight_layout()  # Adjust layout
plt.show()

pairs = [
    ('Random', 'GPT4V'),
    ('Random', 'Ground Truth'),
    ('Ground Truth', 'GPV-1')
]

for model1, model2 in pairs:
    group1 = df_filtered[df_filtered['model left'] == model1]['time_per_frame']
    group2 = df_filtered[df_filtered['model left'] == model2]['time_per_frame']
    
    # Perform t-test
    t_stat, p_value = ttest_ind(group1, group2, nan_policy='omit')  # 'omit' to ignore NaNs
    
    print(f"T-test between {model1} and {model2}:")
    print(f"  T-statistic: {t_stat:.3f}, P-value: {p_value:.4f}")
    
    # Determine significance
    alpha = 0.05  # Typical level of significance
    if p_value < alpha:
        print("  Result: Statistically significant differences.\n")
    else:
        print("  Result: No statistically significant differences.\n")