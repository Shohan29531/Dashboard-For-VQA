import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd, MultiComparison

# Load the DataFrame
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Convert 'model left' column to string
df['model left'] = df['model left'].astype(str)

# Define the desired order of models for the analysis
desired_order = ['Random', 'GPV-1', 'BLIP', 'GPT4V', 'Ground Truth']

# Filter dataframe based on the desired order
df_filtered = df[df['model left'].isin(desired_order)]

df = df_filtered

# Kruskal-Wallis Test
kruskal_results = stats.kruskal(
    df_filtered[df_filtered['model left'] == 'Random']['normalized_score'],
    df_filtered[df_filtered['model left'] == 'GPV-1']['normalized_score'],
    df_filtered[df_filtered['model left'] == 'BLIP']['normalized_score'],
    df_filtered[df_filtered['model left'] == 'GPT4V']['normalized_score'],
    df_filtered[df_filtered['model left'] == 'Ground Truth']['normalized_score']
)

print(f"Kruskal-Wallis Test: H-statistic = {kruskal_results.statistic}, p-value = {kruskal_results.pvalue}")


if kruskal_results.pvalue < 0.05:
    mc = MultiComparison(df['normalized_score'], df['model left'])
    posthoc_result = mc.tukeyhsd(alpha=0.05 / 5)  # Bonferroni correction (adjust alpha value)
    print(posthoc_result.summary())
    
    # Convert the result to a DataFrame for easier processing
    posthoc_result_df = pd.DataFrame(data=posthoc_result._results_table.data[1:], columns=posthoc_result._results_table.data[0])
    
    # Now, posthoc_result_df contains the comparison result which you can use for annotations
