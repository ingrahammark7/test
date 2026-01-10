import warnings
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

# -----------------------------
# 0️⃣ Suppress warnings
# -----------------------------
warnings.filterwarnings("ignore")  # suppress all scikit-learn and user warnings

# -----------------------------
# 1️⃣ Load CSV
# -----------------------------
df = pd.read_csv("l2.csv", low_memory=False)

# -----------------------------
# 2️⃣ Remove fully empty columns
# -----------------------------
empty_cols = df.columns[df.isna().all()].tolist()
df = df.drop(columns=empty_cols)

# -----------------------------
# 3️⃣ Binary target
# -----------------------------
df['default_flag'] = df['loan_status'].apply(lambda x: 1 if x == 'Charged Off' else 0)
target = 'default_flag'

# -----------------------------
# 4️⃣ Drop high-cardinality text columns
# -----------------------------
text_cols = ['desc', 'title', 'emp_title', 'url']
df = df.drop(columns=[c for c in text_cols if c in df.columns])

# -----------------------------
# 5️⃣ Split features and target
# -----------------------------
X = df.drop(columns=[target, 'loan_status'])
y = df[target]

# -----------------------------
# 6️⃣ Numeric & categorical columns
# -----------------------------
numeric_features = X.select_dtypes(include=['int64','float64']).columns.tolist()
categorical_features = X.select_dtypes(include=['object']).columns.tolist()

# -----------------------------
# 7️⃣ Reduce categorical features to top N cardinality
# -----------------------------
MAX_CAT = 20
if len(categorical_features) > MAX_CAT:
    cat_card = X[categorical_features].nunique().sort_values(ascending=False)
    categorical_features = cat_card.head(MAX_CAT).index.tolist()

# -----------------------------
# 8️⃣ Preprocessing
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
# 9️⃣ Models
# -----------------------------
models = {
    'LogisticRegression': LogisticRegression(max_iter=500),
    'RidgeClassifier': RidgeClassifier(alpha=1.0),
    'RandomForest': RandomForestClassifier(n_estimators=50, max_depth=6, n_jobs=1, random_state=42),
    'GradientBoosting': GradientBoostingClassifier(n_estimators=50, max_depth=4, random_state=42)
}

# -----------------------------
# 🔟 Train/test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -----------------------------
# 1️⃣1️⃣ Train models with progress
# -----------------------------
best_auc = -float('inf')
best_model_name = None

for idx, (name, model) in enumerate(models.items(), 1):
    print(f"[{idx}/{len(models)}] Training {name}...")

    pipe = Pipeline([
        ('preprocessor', preprocessor),
        ('model', model)
    ])
    
    # Small partial fit first to reduce RAM spikes
    pipe.fit(X_train.head(50), y_train.head(50))
    
    # Full fit
    pipe.fit(X_train, y_train)
    
    # Predict
    y_pred = pipe.predict(X_test)
    y_proba = pipe.predict_proba(X_test)[:,1] if hasattr(pipe, "predict_proba") else y_pred
    
    # Metrics
    auc = roc_auc_score(y_test, y_proba)
    acc = accuracy_score(y_test, y_pred)
    print(f"    Accuracy: {acc:.4f}, ROC-AUC: {auc:.4f}")
    
    if auc > best_auc:
        best_auc = auc
        best_model_name = name

print(f"\n✅ Best model: {best_model_name} with ROC-AUC = {best_auc:.4f}")