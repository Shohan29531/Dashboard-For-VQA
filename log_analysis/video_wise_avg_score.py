import pandas as pd
import matplotlib.pyplot as plt

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# exclusion_video_list = ['video-15-segment-3', 'video-14-segment-1', 'video-16-segment-3']

# Filter data for the 'Ground Truth' model
df_gt = df[df['model left'] == 'Ground Truth']

# Exclude videos in the exclusion list
exclusion_video_list = ['video-15-segment-3', 'video-14-segment-1', 'video-16-segment-3']
df_gt = df_gt[~df_gt['video'].isin(exclusion_video_list)]

# Group by 'video' and get the score values for each video
score_per_video_gt = [group['normalized_score'].values for name, group in df_gt.groupby('video')]

# Set Arial as the font
plt.rcParams['font.family'] = 'Arial'

# Set the width of the plot
plt.figure(figsize=(12, 8))

# Plotting the boxplot
plt.boxplot(score_per_video_gt, labels=df_gt['video'].unique(), patch_artist=True, boxprops=dict(facecolor='#888888'))  # Slightly darker grey color

plt.xlabel('Video', fontsize=14)  # Increase font size by 2
plt.ylabel('Score', fontsize=14)  # Increase font size by 2
plt.title("Boxplot of Scores per Video for Ground Truth Model", fontsize=15)

plt.xticks(rotation=45, ha='right', fontsize=13)  # Rotate x-axis labels for better visibility
plt.yticks(fontsize=13)  # Increase font size by 2

# Add grid lines
plt.grid(True, linestyle='--', alpha=0.7, zorder=0)  # Set a lower zorder value for grid lines

# Save the plot as an image file (e.g., PDF)
plt.savefig('../Paper files/boxplot_scores_per_video_ground_truth.pdf')

# Show the plot
plt.show()
