import warnings
warnings.filterwarnings("ignore")

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression

# -----------------------------
# Random sample fraction
# -----------------------------
SAMPLE_FRAC = 0.01  # adjust as needed

# -----------------------------
# Load CSV
# -----------------------------
df = pd.read_csv("l2.csv", low_memory=False)

# -----------------------------
# Binary target
# -----------------------------
df['default_flag'] = df['loan_status'].apply(lambda x: 1 if x == 'Charged Off' else 0)
target = 'default_flag'

# -----------------------------
# Drop high-cardinality text columns
# -----------------------------
for c in ['desc', 'title', 'emp_title', 'url']:
    if c in df.columns:
        df = df.drop(columns=c)

# -----------------------------
# Shrink dataset
# -----------------------------
df = df.sample(frac=SAMPLE_FRAC, random_state=42).reset_index(drop=True)

# -----------------------------
# Features and target
# -----------------------------
X = df.drop(columns=[target, 'loan_status'])
y = df[target]

# -----------------------------
# Numeric & categorical
# -----------------------------
numeric_features = X.select_dtypes(include=['int64','float64']).columns.tolist()
categorical_features = X.select_dtypes(include=['object']).columns.tolist()

MAX_CAT = 20
if len(categorical_features) > MAX_CAT:
    cat_card = X[categorical_features].nunique().sort_values(ascending=False)
    categorical_features = cat_card.head(MAX_CAT).index.tolist()

# -----------------------------
# Preprocessing
# -----------------------------
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])
preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

# -----------------------------
# Pipeline
# -----------------------------
pipe = Pipeline([
    ('preprocessor', preprocessor),
    ('model', LinearRegression())
])

# -----------------------------
# Fit model
# -----------------------------
pipe.fit(X, y)

# -----------------------------
# Prepare submission
# -----------------------------
sk_id = X['id'] if 'id' in X.columns else X.index
submission = pd.DataFrame({
    'SK_ID_CURR': sk_id,
    'TARGET': pipe.predict(X).clip(0,1)
})

# -----------------------------
# Print CSV only
# -----------------------------
print(submission.to_csv(index=False))