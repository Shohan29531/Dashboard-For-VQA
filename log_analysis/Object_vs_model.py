import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the DataFrame from 'all.csv'
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Define the models of interest
models = ['Random', 'Ground Truth', 'GPV-1', 'BLIP', 'GPT4V', 'GPV-1@Shadow', 'BLIP@Shadow', 'GPT4V@Shadow']

# Filter the DataFrame to include only the specified models
df_filtered = df[df['model left'].isin(models)]

# Create the boxplot
plt.figure(figsize=(12, 8))  # Adjust the figure size as needed
sns.boxplot(data=df_filtered, x='model left', y='see_count', order=models)

plt.title('See Count Summary for 8 Models')
plt.xlabel('Model')
plt.ylabel('See Count')
plt.xticks(rotation=45)  # Rotate the model names for better readability

plt.tight_layout()  # Adjust layout
plt.show()
