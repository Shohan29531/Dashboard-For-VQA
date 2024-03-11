from scipy.stats import f_oneway
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Prepare a list to hold the completion times for each model
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Define the models of interest
models = ['Random', 'Ground Truth', 'GPV-1', 'BLIP', 'GPT4V', 'GPV-1@Shadow', 'BLIP@Shadow', 'GPT4V@Shadow']

# Filter the DataFrame to include only the specified models
df_filtered = df[df['model left'].isin(models)]

completion_times_by_model = [df_filtered[df_filtered['model left'] == model]['timing'] for model in models]

# Perform the F-test (ANOVA)
f_stat, p_value = f_oneway(*completion_times_by_model)

print(f"F-statistic: {f_stat:.2f}, P-value: {p_value:.4f}")

# Interpret the result
alpha = 0.05  # Typical level of significance
if p_value < alpha:
    print("We reject the null hypothesis, indicating significant differences in completion times across models.")
else:
    print("We fail to reject the null hypothesis, indicating no significant differences in completion times across models.")
