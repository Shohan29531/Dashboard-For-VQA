import pandas as pd
import matplotlib.pyplot as plt

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Specify the order of participants
participant_order = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12', 'P13', 'P14']

# Convert 'participant' column to a categorical type with specified order
df['participant'] = pd.Categorical(df['participant'], categories=participant_order, ordered=True)

# Calculate the average number of objects used for each participant
avg_objects_per_participant = df.groupby('participant')['see_count'].mean()

# Increase font sizes by 2
font_size = 2
plt.figure(figsize=(10, 5))
plt.rcParams['font.family'] = 'Arial'

# Plotting the bar graph with a slightly darker grey color
bars = plt.bar(avg_objects_per_participant.index, avg_objects_per_participant, color='#888888', zorder=5)  # Slightly darker grey color

plt.xlabel('Participant', fontsize=14 + font_size)  # Increase font size by 2
plt.ylabel('Avg. Number of Objects Used', fontsize=14 + font_size)  # Increase font size by 2
plt.title("Avg. Number of Objects Used Per Trial by Participants", fontsize=15 + font_size)
plt.xticks(rotation=0, ha='center', fontsize=11)  # Center-align x-axis ticks and increase font size
plt.yticks(fontsize=13)  # Increase font size by 2

# Add grid lines
plt.grid(True, linestyle='--', alpha=0.7, zorder=0)  # Set a lower zorder value for grid lines

# Save the plot as an image file (e.g., PDF)
plt.savefig('../Paper files/average_objects_per_participant.pdf')

# Show the plot
plt.show()
