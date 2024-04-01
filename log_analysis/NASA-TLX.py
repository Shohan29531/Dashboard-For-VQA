import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
data = pd.read_csv('E://Projects//Dashboard-For-VQA//log_analysis//NASA-TLX.csv')

# Increase font sizes
plt.rc('font', size=17)  # Base font size
plt.rc('axes', titlesize=24)  # Axes title font size
plt.rc('axes', labelsize=22)  # Axes labels font size
plt.rc('xtick', labelsize=17)  # X tick labels font size
plt.rc('ytick', labelsize=17)  # Y tick labels font size
plt.rc('legend', fontsize=17)  # Legend font size

# Create a figure and axis object
fig, ax = plt.subplots(figsize=(12, 9))

# Define properties for boxplot components
boxprops = dict(linestyle='-', linewidth=2, color='black', facecolor='white')
medianprops = dict(linestyle='-', linewidth=2, color='black')
whiskerprops = dict(linestyle='-', linewidth=2, color='black')
capprops = dict(linestyle='-', linewidth=2, color='black')
flierprops = dict(marker='o', markerfacecolor='black', markersize=5, linestyle='none', markeredgecolor='black')

data.boxplot(column=['MD', 'PD', 'TD', 'Performance', 'Effort', 'Frustration', 'Overall'], 
             ax=ax, 
             boxprops=boxprops, 
             medianprops=medianprops, 
             whiskerprops=whiskerprops, 
             capprops=capprops, 
             flierprops=flierprops,
             patch_artist=True)

# Set the title and axis labels
ax.set_title('NASA-TLX Load Indices for Using IKIWISI')
ax.set_xlabel('Metric')
ax.set_ylabel('Load Index')

# Rotate the x-axis labels for better readability
plt.xticks(rotation=0)

# Bring back horizontal gridlines for better readability
ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=0.5)

# Display the plot
plt.savefig('NASA-TLX.pdf', format='pdf')
plt.show()