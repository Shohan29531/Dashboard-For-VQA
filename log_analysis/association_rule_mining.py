import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

# Load the dataset
df = pd.read_csv('../Logs/trimmed_logs/all_mod.csv')

# Assuming 'see' column contains strings of objects separated by commas
df['see'] = df['see'].apply(lambda x: x.split(','))  # Adjust based on your actual data format

# List of transactions
transactions = df['see'].tolist()

# One-hot encode the transaction data
encoder = TransactionEncoder()
onehot = encoder.fit_transform(transactions)
onehot_df = pd.DataFrame(onehot, columns=encoder.columns_)

# Apply Apriori algorithm to find frequent itemsets with at least 2 items
# Adjust min_support as needed to find relevant itemsets
frequent_itemsets = apriori(onehot_df, min_support=0.01, use_colnames=True, max_len=2)

# Filter itemsets to only include those with exactly 2 items if you only want pairs
frequent_pairs = frequent_itemsets[frequent_itemsets['itemsets'].apply(lambda x: len(x) == 2)]

# Saving the frequent itemsets and pairs to CSV files
frequent_itemsets.to_csv('frequent_itemsets.csv', index=False)
frequent_pairs.to_csv('frequent_pairs.csv', index=False)
