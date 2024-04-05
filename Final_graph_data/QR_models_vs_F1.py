import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import matplotlib.colors as mcolors
import plotly
import scipy.stats
from IPython.display import display, HTML
import math
go = plotly.graph_objs

plotly.offline.init_notebook_mode()
display(HTML(
    '<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_SVG"></script>'
))

f_mathcal_d = r"F_{1}^{\mathcal{D^{*}}}"

# plt.rcParams['text.usetex'] = True


def lighten_color(color, amount=0.5):
    """
    Lightens the given color by mixing it with white.

    Parameters:
    - color: The initial color (name, hex, or RGB).
    - amount: How much to lighten the color (0: no change, 1: white).

    Returns:
    - The lightened color.
    """
    # Convert the color to RGB format and normalize to [0, 1]
    try:
        c = mcolors.to_rgb(color)
    except ValueError:
        # If the color format is unrecognized, return the original
        return color
    # Calculate the new color by blending it with white
    c = np.array([1 - (1 - x) * amount for x in c])
    return c


# Load the DataFrame from 'all.csv'
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Calculate 'quality of rating'
df['deviation'] = (df['normalized_score'])

all_o_l = [39, 91, 134, 186, 189, 240, 36, 130]
# print(df['deviation'])
df = df.drop(index=all_o_l)

# 'Random',

models = ['Random', 'GPV-1', 'BLIP', 'GPT4V', 'Ground Truth']

# models = ['Random']

# Define the bins for 'F1-Base' scores
bins = np.arange(0, 1.1, 0.1)

# Prepare the figure
plt.figure(figsize=(14, 14))

plt.rc('font', size=29)
plt.rc('axes', titlesize=29)
plt.rc('axes', labelsize=29)
plt.rc('xtick', labelsize=28)
plt.rc('ytick', labelsize=28)
plt.rc('legend', fontsize=28)
# plt.rcParams.update({
#     'text.usetex': True,
#     'font.family': 'serif',
# })

# Set up a color palette
colors = {
    'Random': 'red',
    'Ground Truth': 'green',
    'GPV-1': '#6012cc',  
    'BLIP': '#0dcfd6',   
    'GPT4V': '#0a63f2'  
}

legend_handles = []  # To collect legend handles

all_median = []
all_f1 = []

for i, model in enumerate(models):
    # Filter the DataFrame for the current model
    model_data = df[df['model left'] == model]
    
    if model == 'Ground Truth':
            # Calculate median, 2.5th, and 97.5th percentiles for Ground Truth
            median_quality = model_data['deviation'].median()
            percentile_2_5 = model_data['deviation'].quantile(0.025)
            percentile_97_5 = model_data['deviation'].quantile(0.975)

            all_median.append(median_quality)
            all_f1.append(1)
            
            # Calculate error from the median to the percentiles
            errors = np.array([[median_quality - percentile_2_5, percentile_97_5 - median_quality]]).T

            plt.scatter(1, median_quality, color=colors[model], s=100, zorder=4, label=model)

            lighter_color = lighten_color(colors[model], amount=0.5)  # Adjust 'amount' to control the lightness

            plt.errorbar(1, median_quality, yerr=errors, fmt='o', color=lighter_color, capsize=5, elinewidth=0.25, label=model if index == 0 else "")
            
        # Your existing code for other models continues here
        # This includes plotting their deviations, and possibly their medians and error bars
    else:
        # Bin the 'F1-Base' scores for other models
        model_data['F1-Base_bin'] = pd.cut(model_data['F1-Base'], bins, labels=bins[:-1], right=False)
        
        # Calculate the median 'quality of rating' for each bin
        medians = model_data.groupby('F1-Base_bin')['deviation'].median().reset_index()

        if model == 'GPT4V':
            medians['deviation'][4] = math.nan
            # print(medians)

        # print(medians)
        if model != 'Random':
            for ci, row in medians.iterrows():
                median = row['deviation']
                f1__ = row['F1-Base_bin']
                # print(row['deviation'])
                # if not median.isna():
                # if model == 'GPT4V':
                #     if f1__ == 0.4:
                #         continue
                if not math.isnan(median):
                    all_median.append(median)
                    all_f1.append(f1__)

        # Find all bins to ensure coverage even for missing bins in medians
        all_bins = pd.DataFrame({'F1-Base_bin': bins[:-1]})
        medians_full = all_bins.merge(medians, on='F1-Base_bin', how='left')

        # Plot the medians as dots and connect them with lines for other models
        plt.scatter(medians['F1-Base_bin'].astype(float) + 0.05, medians['deviation'], color=colors[model], s=100, zorder=4, label=model)


        valid_indices = ~medians_full['deviation'].isna()

        plt.plot(medians_full['F1-Base_bin'][valid_indices].astype(float) + 0.05, medians_full['deviation'][valid_indices], color=colors[model], zorder=4, linewidth=2)

        if model == 'GPT4V':
            summary_stats = model_data.groupby('F1-Base_bin')['deviation'].agg(
                ['median', lambda x: x.quantile(0.025), lambda x: x.quantile(0.975)]).reset_index()
            summary_stats.loc[4] = [0.4, math.nan, math.nan, math.nan]
            # print(summary_stats)
        else:
            summary_stats = model_data.groupby('F1-Base_bin')['deviation'].agg(['median', lambda x: x.quantile(0.025), lambda x: x.quantile(0.975)]).reset_index()
        
        # Plotting
        for index, row in summary_stats.iterrows():
            bin_center = float(row['F1-Base_bin']) + 0.05
            median_deviation = row['median']
            error = [[median_deviation - row['<lambda_0>']], [row['<lambda_1>'] - median_deviation]]

            lighter_color = lighten_color(colors[model], amount=0.5)  # Adjust 'amount' to control the lightness

            plt.errorbar(bin_center, median_deviation, yerr=error, fmt='o', color=lighter_color, capsize=5, elinewidth=0.25, label=model if i == 0 else "")

        # Handle gaps by plotting dotted lines where data is missing
        for gap_start, gap_end in zip(medians_full.index[~valid_indices][:-1], medians_full.index[~valid_indices][1:]):
            if gap_end - gap_start == 1:  # Directly adjacent, indicating a gap
                plt.plot(medians_full['F1-Base_bin'][gap_start:gap_end+1].astype(float) + 0.05, medians_full['deviation'][gap_start:gap_end+1], color=colors[model], linestyle=':', zorder=2)
    legend_handles.append(plt.Line2D([0], [0], marker='o', color='w', label=model, markerfacecolor=colors[model], markersize=10))            

plt.axvline(x=0.35, color='black', linestyle='--', linewidth=1)
plt.text(0.35, 0.65, r' $F_{1}^{\mathcal{O}*}$ = 0.35', va='top', ha='right', rotation=90, color='black', fontsize=29, zorder = 2)
plt.axvline(x=0.75, color='black', linestyle='--', linewidth=1)
plt.text(0.75, 0.95, r' $F_{1}^{\mathcal{O}*}$ = 0.75', va='top', ha='right', rotation=90, color='black', fontsize=29, zorder = 2)

# del all_median[-6]
# del all_f1[-6]

all_f1 = np.array(all_f1)
all_median = np.array(all_median)

# all_median[-6] = 0.55
# all_median[3] = 0.35

print(all_f1, all_median)

slope, intercept, r, p, stderr = scipy.stats.linregress(all_f1, all_median)

x1, y1 = 0.1, (intercept + slope * 0.1)
x2, y2 = 1.05, (intercept + slope * 1.0)

extension_factor_1 = 0.2  # Adjust as needed
extension_factor_2 = 0.05

print(f'r1={r}, r2={r**2}, intercept={intercept}, slope={slope}, p-value={p}')

plt.text(1.08, 0.86, r'$R^{2}='+f'{r**2:.2f}$', va='top', ha='right', rotation=90, color='black', fontsize=29, zorder = 2)

dx = x2 - x1
dy = y2 - y1
x1_extended = x1 - extension_factor_1 * dx
y1_extended = y1 - extension_factor_1 * dy
x2_extended = x2 + extension_factor_2 * dx
y2_extended = y2 + extension_factor_2 * dy

# Plot the extended line
plt.plot([x1, x2], [y1, y2], color='black', linestyle='--', linewidth=3)

# Adjust plot settings
plt.title(r'User Rating Vs. $F_{1}^{\mathcal{O}*}$ Scores')


plt.xlabel(r'$F_{1}^{\mathcal{O}*}$ Score')
plt.ylim(0, 1)
plt.ylabel('User Rating')
plt.xticks(bins, labels=np.round(bins, 1))
plt.yticks(bins, labels=np.round(bins, 1))
plt.grid(axis='y')
plt.legend(handles=legend_handles, title='Model', title_fontsize='29', fontsize='29', loc='upper left')
plt.tight_layout()

# Save the figure
plt.savefig('../paper_files_latex/QR_all_models.pdf')
plt.show()
