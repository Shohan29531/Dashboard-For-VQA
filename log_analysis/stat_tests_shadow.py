import pandas as pd
from scipy import stats

# Load the CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')
df['model left'] = df['model left'].astype(str)  # Ensure 'model left' is string

# Define model pairs for comparison
model_pairs = [
    ('GPT4V', 'GPT4V@Shadow'),
    ('BLIP', 'BLIP@Shadow'),
    ('GPV-1', 'GPV-1@Shadow'),
]

# Iterate through each model pair and perform a paired t-test
for model, shadow_model in model_pairs:
    # Filter scores for each model and its shadow
    model_scores = df[df['model left'] == model]['normalized_score'].dropna()
    shadow_scores = df[df['model left'] == shadow_model]['normalized_score'].dropna()
    
    # Ensure equal length by pairing scores based on minimal length
    min_length = min(len(model_scores), len(shadow_scores))
    model_scores = model_scores.head(min_length)
    shadow_scores = shadow_scores.head(min_length)
    
    # Perform the paired t-test
    t_stat, p_value = stats.ttest_rel(model_scores, shadow_scores)
    
    print(f"{model} vs. {shadow_model}: t-statistic = {t_stat}, p-value = {p_value}")
