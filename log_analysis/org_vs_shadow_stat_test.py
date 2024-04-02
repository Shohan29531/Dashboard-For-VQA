from scipy.stats import mannwhitneyu
import pandas as pd
import numpy as np

df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Convert 'model left' column to string
df['model left'] = df['model left'].astype(str)


desired_order = ['GPV-1@Shadow', 'GPV-1', 'BLIP@Shadow', 'BLIP', 'GPT4V@Shadow', 'GPT4V']

results = []

for i in range(0, len(desired_order), 2):
    shadow_model = desired_order[i]
    base_model = desired_order[i+1]
    
    # Extract scores for each model
    shadow_scores = df[df['model left'] == shadow_model]['normalized_score']
    base_scores = df[df['model left'] == base_model]['normalized_score']

    # if base_model == 'BLIP':
        # unq_scores, unq_counts = np.unique(scores, return_counts=True)
    mean = np.mean(list(base_scores))
    std = np.std(list(base_scores))

    threshold = 2.0
    outliers_index = []

    for i_, x in base_scores.iteritems():
        z_score = (x - mean) / std
        # print(z_score)
        if abs(z_score) > threshold:
            outliers_index.append(i_)

    # for o_i in outliers_index:
    #     del base_scores[o_i]
    base_scores = base_scores.drop(index=outliers_index)

    mean = np.mean(list(shadow_scores))
    std = np.std(list(shadow_scores))

    threshold = 2.0
    outliers_index = []

    for i_, x in shadow_scores.iteritems():
        z_score = (x - mean) / std
        # print(z_score)
        if abs(z_score) > threshold:
            outliers_index.append(i_)

    # for o_i in outliers_index:
    #     del shadow_scores[o_i]
    shadow_scores = shadow_scores.drop(index=outliers_index)
    
    # Perform the Mann-Whitney U test
    stat, p_value = mannwhitneyu(shadow_scores, base_scores, alternative='two-sided')

    # print(stat, p_value)
    
    # Determine significance
    significance = "NS"  # Not significant
    if p_value <= 0.001:
        significance = "***"
    elif p_value <= 0.01:
        significance = "**"
    elif p_value <= 0.05:
        significance = "*"
    
    # Print and store results
    result_text = f"{shadow_model} vs. {base_model}: U={stat:.2f}, p={p_value:.3f} {significance}"
    print(result_text)
    results.append((shadow_model, base_model, stat, p_value, significance))

# If needed, you can further process or display `results` in your analysis or plots
