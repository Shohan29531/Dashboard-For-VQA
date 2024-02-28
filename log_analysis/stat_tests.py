import pandas as pd
from scipy import stats

df = pd.read_csv('../Logs/trimmed_logs/all.csv')
# Ensure 'model left' is of type string for filtering
df['model left'] = df['model left'].astype(str)

# Filtering based on the specified models
models = ['Random', 'Ground Truth', 'GPV-1', 'BLIP', 'GPT4V']
df_filtered = df[df['model left'].isin(models)]

# Separate the scores for each model
random_scores = df_filtered[df_filtered['model left'] == 'Random']['normalized_score'].dropna()
ground_truth_scores = df_filtered[df_filtered['model left'] == 'Ground Truth']['normalized_score'].dropna()
gpv1_scores = df_filtered[df_filtered['model left'] == 'GPV-1']['normalized_score'].dropna()
blip_scores = df_filtered[df_filtered['model left'] == 'BLIP']['normalized_score'].dropna()
gpt4v_scores = df_filtered[df_filtered['model left'] == 'GPT4V']['normalized_score'].dropna()

# Statistical test between Random and Ground Truth
# Check for equality of variances
_, p_var = stats.levene(random_scores, ground_truth_scores)
if p_var > 0.05:
    # Variances are equal, use two-sample t-test
    t_stat, p_value = stats.ttest_ind(random_scores, ground_truth_scores, equal_var=True)
else:
    # Variances are not equal, use Welch's t-test
    t_stat, p_value = stats.ttest_ind(random_scores, ground_truth_scores, equal_var=False)

print(f"Random vs. Ground Truth: t-statistic = {t_stat}, p-value = {p_value}")

# Statistical test among GPV-1, BLIP, GPT4V
f_stat, p_value_anova = stats.f_oneway(gpv1_scores, blip_scores, gpt4v_scores)

print(f"ANOVA among GPV-1, BLIP, GPT4V: F-statistic = {f_stat}, p-value = {p_value_anova}")
