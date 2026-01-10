import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

# ------------------------
# 1. Load data
# ------------------------
data = pd.read_csv("l2.csv", low_memory=False)

# ------------------------
# 2. Create binary target
# ------------------------
# 1 = default / charged off, 0 = fully paid / current
default_statuses = ['Charged Off', 'Default', 'Late (31-120)']
data['default_flag'] = data['loan_status'].apply(lambda x: 1 if x in default_statuses else 0)

# ------------------------
# 3. Drop useless columns
# ------------------------
drop_cols = ['id', 'member_id', 'url', 'desc', 'title', 'loan_status']  # remove identifiers and text
data = data.drop(columns=drop_cols, errors='ignore')

# ------------------------
# 4. Separate features and target
# ------------------------
X = data.drop(columns=['default_flag'])
y = data['default_flag']

# ------------------------
# 5. Handle missing values
# ------------------------
# Numeric columns: fill missing with median
num_cols = X.select_dtypes(include=['int64', 'float64']).columns
num_imputer = SimpleImputer(strategy='median')
X[num_cols] = num_imputer.fit_transform(X[num_cols])

# Categorical columns: fill missing with 'missing'
cat_cols = X.select_dtypes(include=['object']).columns
cat_imputer = SimpleImputer(strategy='constant', fill_value='missing')
X[cat_cols] = cat_imputer.fit_transform(X[cat_cols])

# One-hot encode categorical features
encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
X_cat = pd.DataFrame(encoder.fit_transform(X[cat_cols]), columns=encoder.get_feature_names_out(cat_cols))
X = X.drop(columns=cat_cols)
X = pd.concat([X.reset_index(drop=True), X_cat.reset_index(drop=True)], axis=1)

# ------------------------
# 6. Train/test split
# ------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ------------------------
# 7. Train Logistic Regression
# ------------------------
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate quickly
acc = model.score(X_test, y_test)
roc_auc = model.predict_proba(X_test)[:,1]
print(f"Accuracy: {acc:.4f}, ROC-AUC: {pd.Series(roc_auc).mean():.4f}")

# ------------------------
# 8. Create submission
# ------------------------
# Use all data for prediction to simulate test submission
preds = model.predict_proba(X)[:,1]

submission = pd.DataFrame({
    "SK_ID_CURR": data['funded_amnt'].index,  # if SK_ID_CURR not in data, use row index
    "TARGET": preds
})

submission.to_csv("submission.csv", index=False)
print("Submission saved as submission.csv")