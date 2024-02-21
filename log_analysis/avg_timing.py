import pandas as pd
import matplotlib.pyplot as plt

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Specify the order of participants
participant_order = ['P1', 'P4', 'P5', 'P11', 'P12', 'P14', 'P2', 'P3', 'P6', 'P7', 'P8', 'P9', 'P10', 'P13']

# Convert 'participant' column to a categorical type with specified order
df['participant'] = pd.Categorical(df['participant'], categories=participant_order, ordered=True)

# Specify the order of expertise levels
expertise_order = ['Expert', 'Novice/Intermediate']

# Convert 'expertise' column to a categorical type with specified order
df['expertise'] = pd.Categorical(df['expertise'], categories=expertise_order, ordered=True)

# Assign shades of grey to each expertise level
colors = {'Expert': 'black', 'Novice/Intermediate': 'lightgrey'}

# Calculate the average 'timing' for each participant
avg_timing_per_participant = df.groupby(['participant', 'expertise'])['timing'].mean().reset_index()

# Increase font sizes by 2
font_size = 2

# Set the width of the plot
plt.figure(figsize=(12, 6))

# Set Arial as the font
plt.rcParams['font.family'] = 'Arial'

# Plotting the bar graph with expertise-based colors
for expertise_level, color in colors.items():
    subset_df = avg_timing_per_participant[avg_timing_per_participant['expertise'] == expertise_level]
    plt.bar(subset_df['participant'], subset_df['timing'], color=color, label=expertise_level, zorder=5)

plt.xlabel('Participant', fontsize=14 + font_size)  # Increase font size by 2
plt.ylabel('Avg. Trial Completion Time (in Seconds)', fontsize=14 + font_size)  # Increase font size by 2
plt.title("Avg. Trial Completion Times by Participants", fontsize=15 + font_size)
plt.xticks(rotation=0, ha='center', fontsize=13)  # Center-align x-axis ticks and increase font size
plt.yticks(fontsize=13)  # Increase font size by 2

# Add grid lines
plt.grid(True, linestyle='--', alpha=0.7, zorder=0)  # Set a lower zorder value for grid lines

# Add legend
plt.legend(title='Participant Expertise', title_fontsize='14', fontsize='12')

# Set y-axis limits
plt.ylim(0, 230)

# # Draw vertical lines after 4 and 8 bars
# plt.axvline(x=3.5, color='black', linestyle='-', linewidth=3, zorder=10)  # After 4 bars
plt.axvline(x=5.5, color='black', linestyle='-', linewidth=3, zorder=10)  # After 8 bars

# Save the plot as an image file (e.g., PDF)
plt.savefig('../Paper files/average_timing_per_participant.pdf')

# Show the plot
plt.show()
