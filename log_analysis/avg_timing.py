import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')
# df = df[df['model left'] == 'BLIP']
# Specify the order of participants
participant_order = ['P1', 'P4', 'P5', 'P11', 'P12', 'P14', 'P15', 'P2', 'P3', 'P6', 'P7', 'P8', 'P9', 'P10', 'P13']

# Convert 'participant' column to a categorical type with specified order
df['participant'] = pd.Categorical(df['participant'], categories=participant_order, ordered=True)

# Specify the order of expertise levels
expertise_order = ['Expert', 'Non-Expert']

# Convert 'expertise' column to a categorical type with specified order
df['expertise'] = pd.Categorical(df['expertise'], categories=expertise_order, ordered=True)

# Set the figure size and font
plt.figure(figsize=(12, 6))
plt.rcParams['font.family'] = 'Arial'

# Increase font sizes
font_size = 6
plt.rcParams.update({'font.size': 12 + font_size})

# Plotting the boxplot with seaborn
sns.boxplot(x='participant', y='timing', data=df, hue='expertise', palette='gray', order=participant_order)

# sns.stripplot(x='participant', y='timing', data=df, order=participant_order, color='red', size=3, jitter=True, alpha=0.6)

plt.title("Avg. Trial Completion Times by Participants", fontsize=15 + font_size)
plt.xlabel('Participant', fontsize=14 + font_size)
plt.ylabel('Trial Completion Time (in Seconds)', fontsize=14 + font_size)
plt.xticks(rotation=45, ha='right', fontsize=13)  # Rotate participant labels for better readability
plt.yticks(fontsize=13)
plt.legend(title='Participant Expertise', title_fontsize='14', fontsize='12')

# Optional: Adjust y-axis limits if necessary
plt.ylim(0, 500)

# Draw vertical lines to visually separate different participant groups, if needed
plt.axvline(x=6.5, color='black', linestyle='-', linewidth=3, zorder=10)

# Adjust layout and save the plot as a PDF file
plt.tight_layout()
plt.savefig('../Paper files/average_timing_per_participant.pdf')

# Show the plot
plt.show()
