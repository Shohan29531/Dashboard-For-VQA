import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the DataFrame from 'all.csv'
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

plt.figure(figsize=(10, 6))
# df = df[df['model left'] != 'Ground Truth']

plt.scatter(df['F1-Base'], df['see_count'], alpha=0.5, label='Data Points')

plt.title('Objects Used vs. F1 ')
plt.xlabel('F1')
plt.ylabel('Objects Used')
plt.xlim(0, 1.1)
plt.xticks(np.arange(0, 1.1, 0.1))
# plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
