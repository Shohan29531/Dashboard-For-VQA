import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm

# Reading data from CSV file
df = pd.read_csv('output.csv')
df = df[df['model'] == 'Random']

# Selecting independent variables (first 12 columns) and dependent variable
X = df.iloc[:, :14]  # Selects all rows and the first 12 columns for independent variables
y = df['MC_with_MinMax']  # Dependent variable

# Normalizing the independent variables
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)

# # # Convert the scaled data back to a DataFrame with original column names
# X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

# Splitting dataset into training and testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=42)

# Adding a constant for the intercept term
X_train_with_intercept = sm.add_constant(X_train)
# X_test_with_intercept = sm.add_constant(X_test)

# Model fitting using statsmodels for detailed statistics
model = sm.OLS(y_train, X_train_with_intercept).fit()

# Display the regression results, now with original variable names
print(model.summary())

# Predicting with statsmodels
y_pred = model.predict(X_train_with_intercept)

# Calculating R-squared for the test set manually
rss = ((y_train - y_pred) ** 2).sum()
tss = ((y_train - y_train.mean()) ** 2).sum()
r_squared_test = 1 - rss / tss
print(f"Test R-squared: {r_squared_test}")
