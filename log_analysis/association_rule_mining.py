import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

# Load the dataset
df = pd.read_csv('../Logs/trimmed_logs/all_mod.csv')

# Assuming 'see' column contains strings of objects separated by commas
df['see'] = df['see'].apply(lambda x: x.split(','))

# List of transactions
transactions = df['see'].tolist()

# One-hot encode the transaction data
encoder = TransactionEncoder()
onehot = encoder.fit_transform(transactions)
onehot_df = pd.DataFrame(onehot, columns=encoder.columns_)

# Apply Apriori algorithm to find frequent itemsets including singles, pairs, and trios
frequent_itemsets = apriori(onehot_df, min_support=0.005, use_colnames=True, max_len=6)

# Sort the frequent itemsets by support in decreasing order
frequent_itemsets_sorted = frequent_itemsets.sort_values(by='support', ascending=False)

# Filter itemsets for singles, pairs, and trios
frequent_singles = frequent_itemsets_sorted[frequent_itemsets_sorted['itemsets'].apply(lambda x: len(x) == 1)]
frequent_pairs = frequent_itemsets_sorted[frequent_itemsets_sorted['itemsets'].apply(lambda x: len(x) == 2)]
frequent_trios = frequent_itemsets_sorted[frequent_itemsets_sorted['itemsets'].apply(lambda x: len(x) == 3)]
frequent_4 = frequent_itemsets_sorted[frequent_itemsets_sorted['itemsets'].apply(lambda x: len(x) == 4)]
frequent_5 = frequent_itemsets_sorted[frequent_itemsets_sorted['itemsets'].apply(lambda x: len(x) == 5)]
frequent_6 = frequent_itemsets_sorted[frequent_itemsets_sorted['itemsets'].apply(lambda x: len(x) == 6)]

# Saving the frequent itemsets to separate CSV files
frequent_singles.to_csv('frequent_singles.csv', index=False)
frequent_pairs.to_csv('frequent_pairs.csv', index=False)
frequent_trios.to_csv('frequent_trios.csv', index=False)

frequent_4.to_csv('frequent_4.csv', index=False)
frequent_5.to_csv('frequent_5.csv', index=False)
frequent_6.to_csv('frequent_6.csv', index=False)
