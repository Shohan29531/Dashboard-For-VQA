import pandas as pd
import scipy.stats as stats

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Specify the order of participants
participant_order = ['P1', 'P5', 'P11', 'P12', 'P3', 'P6', 'P7', 'P10', 'P2', 'P4', 'P8', 'P9', 'P13']

# Convert 'participant' column to a categorical type with specified order
df['participant'] = pd.Categorical(df['participant'], categories=participant_order, ordered=True)

# Specify the order of expertise levels
expertise_order = ['High', 'Moderate', 'Low']

# Convert 'expertise' column to a categorical type with specified order
df['expertise'] = pd.Categorical(df['expertise'], categories=expertise_order, ordered=True)

# Extract timing data for each expertise level
high_expertise = df[df['expertise'] == 'High']['timing']
moderate_expertise = df[df['expertise'] == 'Moderate']['timing']
low_expertise = df[df['expertise'] == 'Low']['timing']

# Perform one-way ANOVA
anova_result = stats.f_oneway(high_expertise, moderate_expertise, low_expertise)

# Display the ANOVA summary
print("ANOVA Summary:")
print("F-statistic:", anova_result.statistic)
print("P-value:", anova_result.pvalue)

# Check if the differences are significant
alpha = 0.05
if anova_result.pvalue < alpha:
    print("\nThe timing differences among expertise levels are statistically significant.")
else:
    print("\nThe timing differences among expertise levels are not statistically significant.")
