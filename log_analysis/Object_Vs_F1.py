import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('../Logs/trimmed_logs/all.csv')

models = ['Random', 'GPV-1', 'BLIP', 'GPT4V', 'Ground Truth',]

bins = np.arange(0, 1.1, 0.1)

plt.figure(figsize=(14, 8))

plt.rc('font', size=20) 
plt.rc('axes', titlesize=24) 
plt.rc('axes', labelsize=24)  
plt.rc('xtick', labelsize=16)  
plt.rc('ytick', labelsize=16)  
plt.rc('legend', fontsize=20) 

colors = {
    'Random': 'red',
    'Ground Truth': 'green',
    'GPV-1': '#6012cc',  
    'BLIP': '#0dcfd6',   
    'GPT4V': '#0a63f2'  
}

legend_handles = []  

for i, model in enumerate(models):
    model_data = df[df['model left'] == model]
    
    if model == 'Ground Truth':

            median_quality = model_data['see_count'].median()
            percentile_2_5 = model_data['see_count'].quantile(0.025)
            percentile_97_5 = model_data['see_count'].quantile(0.975)
            
            errors = np.array([[median_quality - percentile_2_5, percentile_97_5 - median_quality]]).T
            
            plt.scatter(1, median_quality, color=colors[model], s=100, zorder=4, label=model)

            plt.errorbar(1, median_quality, yerr=errors, fmt='o', color=colors[model], capsize=3, elinewidth=0.5, label=model if index == 0 else "")

    else:
        model_data['F1-Base_bin'] = pd.cut(model_data['F1-Base'], bins, labels=bins[:-1], right=False)

        medians = model_data.groupby('F1-Base_bin')['see_count'].median().reset_index()

        all_bins = pd.DataFrame({'F1-Base_bin': bins[:-1]})
        medians_full = all_bins.merge(medians, on='F1-Base_bin', how='left')

        plt.scatter(medians['F1-Base_bin'].astype(float) + 0.05, medians['see_count'], color=colors[model], s=100, zorder=4, label=model)


        valid_indices = ~medians_full['see_count'].isna()

        plt.plot(medians_full['F1-Base_bin'][valid_indices].astype(float) + 0.05, medians_full['see_count'][valid_indices], color=colors[model], zorder=4, linewidth=2)


        summary_stats = model_data.groupby('F1-Base_bin')['see_count'].agg(['median', lambda x: x.quantile(0.025), lambda x: x.quantile(0.975)]).reset_index()
        
        # Plotting
        for index, row in summary_stats.iterrows():
            bin_center = float(row['F1-Base_bin']) + 0.05
            median_deviation = row['median']
            error = [[median_deviation - row['<lambda_0>']], [row['<lambda_1>'] - median_deviation]]
            
            plt.errorbar(bin_center, median_deviation, yerr=error, fmt='o', color=colors[model], capsize=3, elinewidth=0.5, label=model if index == 0 else "")

        for gap_start, gap_end in zip(medians_full.index[~valid_indices][:-1], medians_full.index[~valid_indices][1:]):
            if gap_end - gap_start == 1:  
                plt.plot(medians_full['F1-Base_bin'][gap_start:gap_end+1].astype(float) + 0.05, medians_full['see_count'][gap_start:gap_end+1], color=colors[model], linestyle=':', zorder=2)
    legend_handles.append(plt.Line2D([0], [0], marker='o', color='w', label=model, markerfacecolor=colors[model], markersize=10))            

plt.axvline(x=0.35, color='black', linestyle='--', linewidth=1)
plt.text(0.35, 14, ' F1 = 0.35', va='top', ha='right', rotation=90, color='black', fontsize=20, zorder = 2)
plt.axvline(x=0.75, color='black', linestyle='--', linewidth=1)
plt.text(0.75, 14, ' F1 = 0.75', va='top', ha='right', rotation=90, color='black', fontsize=20, zorder = 2)

plt.title('Objects Used Vs. F1 Score Across Models')
plt.xlabel('F1 Score')
plt.ylim(0, 16)
plt.ylabel('Objects Used')
plt.xticks(bins, labels=np.round(bins, 1))
plt.grid(axis='y')
plt.legend(handles=legend_handles, title='Model', title_fontsize='20', fontsize='18', loc='upper left')
plt.tight_layout()

plt.savefig('images/objects_vs_f1_all_models.pdf')
plt.show()
