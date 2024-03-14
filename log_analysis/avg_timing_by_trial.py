import pandas as pd
import matplotlib.pyplot as plt

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Specify the order of trials
trial_order = df['trial'].unique()

# Convert 'trial' column to a categorical type with specified order
df['trial'] = pd.Categorical(df['trial'], categories=trial_order, ordered=True)

# Calculate the average 'timing' for each trial
avg_timing_per_trial = df.groupby('trial')['timing'].mean().reset_index()

# Increase font sizes by 2
font_size = 6

# Set the width of the plot
plt.figure(figsize=(12, 6))

# Set Arial as the font
plt.rcParams['font.family'] = 'Arial'

# Plotting the bar graph
plt.bar(avg_timing_per_trial['trial'], avg_timing_per_trial['timing'], color='#888888', zorder=5)  # Slightly darker grey color

plt.xlabel('Trial', fontsize=14 + font_size)  # Increase font size by 2
plt.ylabel('Avg. Trial Completion Time (in Seconds)', fontsize=14 + font_size)  # Increase font size by 2
plt.title("Avg. Trial Completion Times by Trial", fontsize=15 + font_size)

# Set x-axis ticks to include all values from 0 to 25
plt.xticks(range(1, 25), rotation=0, ha='center', fontsize=13)  # Center-align x-axis ticks and increase font size

plt.yticks(fontsize=13)  # Increase font size by 2

# Add grid lines
plt.grid(True, linestyle='--', alpha=0.7, zorder=0)  # Set a lower zorder value for grid lines

# Save the plot as an image file (e.g., PDF)
plt.savefig('../Paper files/average_timing_per_trial.pdf')

# Show the plot
plt.show()
