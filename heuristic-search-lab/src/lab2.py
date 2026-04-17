import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor
import os

# Setup folders
os.makedirs('../notebooks', exist_ok=True)
os.makedirs('../outputs', exist_ok=True)

# Notebook initialize karo
nb = nbf.v4.new_notebook()
cells = []

# ==========================================
# MARKDOWN CELLS
# ==========================================
cells.append(nbf.v4.new_markdown_cell("""# Data Preprocessing Lab # 2

**Name:** Muhammad Muaz  
**Program:** BS Artificial Intelligence  
**Dataset:** Credit Scoring Dataset  
**Objective:** Apply comprehensive data preprocessing techniques for ML"""))

cells.append(nbf.v4.new_markdown_cell("""## Step 1: Data Collection & Initial Exploration (5 marks)
### Feature Descriptions
| Column | Type | Description |
|--------|------|-------------|
| children | Numerical | Number of children |
| days_employed | Numerical | Days of employment |
| dob_years | Numerical | Age of client in years |
| education | Categorical | Education level |
| family_status | Categorical | Marital status |
| gender | Categorical | Male/Female |
| income_type | Categorical | Employment type |
| debt | Binary | Has loan default (0=No, 1=Yes) |
| total_income | Numerical | Monthly income |
| purpose | Categorical | Loan purpose |"""))

cells.append(nbf.v4.new_markdown_cell("""## Step 2a: Handling Missing Values (10 marks)
### Approach
- Identify columns with missing values
- Visualize missing pattern using heatmap
- Use Median Imputation grouped by age category"""))

cells.append(nbf.v4.new_markdown_cell("""## Step 2b: Handling Outliers (10 marks)
### Approach
- Fix children column (replace 20 with 2, remove negatives)
- Fix days_employed (remove negatives, cap extremes > 200000)"""))

cells.append(nbf.v4.new_markdown_cell("""## Step 2c: Handling Duplicates (5 marks)"""))

cells.append(nbf.v4.new_markdown_cell("""## Step 3: Data Transformation (15 marks)
1. GroupBy Aggregation
2. Pivot Table
3. Categorical Bins"""))

cells.append(nbf.v4.new_markdown_cell("""## Step 4A: Impact of Scaling on Distance Algorithms (15 marks)"""))

cells.append(nbf.v4.new_markdown_cell("""## Step 4B: Normalization vs Standardization (10 marks)"""))

cells.append(nbf.v4.new_markdown_cell("""## Conclusion
Raw data is never ready for ML models. Preprocessing directly impacts model accuracy. Scaling is critical for distance-based and gradient-based algorithms."""))

# ==========================================
# CODE CELLS
# ==========================================

code_imports = """import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # Background mode for PyCharm
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MaxAbsScaler, MinMaxScaler, StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')
print("All libraries imported successfully!")"""
cells.append(nbf.v4.new_code_cell(code_imports))

code_load = """df = pd.read_csv("../data/credit_scoring_eng.csv", sep=" | ", engine="python")
print("=== Dataset Shape ===")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
display(df.head())"""
cells.append(nbf.v4.new_code_cell(code_load))

code_info = """df.info()"""
cells.append(nbf.v4.new_code_cell(code_info))

code_missing = """print("=== Missing Values Per Column ===")
print(df.isna().sum())"""
cells.append(nbf.v4.new_code_cell(code_missing))

code_heatmap = """plt.figure(figsize=(10,6))
sns.heatmap(df.isna().transpose(), cmap="YlGnBu", cbar_kws={'label': 'Missing Data'})
plt.title("Missing Data Heatmap")
plt.tight_layout()
plt.savefig("../outputs/missing_heatmap.png", dpi=150)
plt.close()
print("Heatmap saved.")"""
cells.append(nbf.v4.new_code_cell(code_heatmap))

code_impute = """df['age_category'] = pd.cut(df['dob_years'], bins=[0,25,40,60,100], labels=['young','adult','middle_age','senior'])

def data_imputation(data, col_group, col_fix):
    for val in data[col_group].unique():
        median_val = data.loc[(data[col_group] == val) & (data[col_fix].notna()), col_fix].median()
        data.loc[(data[col_group] == val) & (data[col_fix].isna()), col_fix] = median_val
    return data

df = data_imputation(df, 'age_category', 'total_income')
df = data_imputation(df, 'age_category', 'days_employed')

print("Missing Values After Fix:")
print(df.isna().sum())"""
cells.append(nbf.v4.new_code_cell(code_impute))

code_outliers1 = """print("Before:", df['children'].unique())
df['children'] = df['children'].replace(20, 2)
df['children'] = abs(df['children'])
print("After:", df['children'].unique())"""
cells.append(nbf.v4.new_code_cell(code_outliers1))

code_outliers2 = """df['days_employed'] = abs(df['days_employed'])
df.loc[df['days_employed'] > 200000, 'days_employed'] = df['days_employed'].median()

sns.boxplot(x=df['days_employed'])
plt.title("Days Employed After Fix")
plt.savefig("../outputs/days_employed_fix.png", dpi=150)
plt.close()
print("Outliers fixed and plot saved.")"""
cells.append(nbf.v4.new_code_cell(code_outliers2))

code_dup = """dup = df.duplicated().sum()
print(f"Duplicates Found: {dup}")
df = df.drop_duplicates().reset_index(drop=True)
print(f"New Shape After Removing Duplicates: {df.shape}")"""
cells.append(nbf.v4.new_code_cell(code_dup))

code_trans1 = """income_by_edu = df.groupby('education')['total_income'].agg(['mean', 'count']).round(2)
print("Income by Education:")
display(income_by_edu)"""
cells.append(nbf.v4.new_code_cell(code_trans1))

code_trans2 = """debt_pivot = df.pivot_table(values='debt', index='income_type', columns='gender', aggfunc='mean').round(4) * 100
print("Default Rate (%) by Income & Gender:")
display(debt_pivot)"""
cells.append(nbf.v4.new_code_cell(code_trans2))

code_trans3 = """df['income_category'] = pd.cut(df['total_income'], bins=[0, 20000, 50000, 100000, float('inf')], labels=['Low', 'Medium', 'High', 'Very High'])
sns.countplot(x='income_category', data=df, palette='Blues_d')
plt.title("Income Categories")
plt.savefig("../outputs/income_categories.png", dpi=150)
plt.close()"""
cells.append(nbf.v4.new_code_cell(code_trans3))

code_knn_setup = """feature_names = ['dob_years', 'children', 'total_income']
for c in feature_names:
    df[c] = df[c].fillna(df[c].median())

def get_knn(data, n, k, metric):
    nbrs = NearestNeighbors(n_neighbors=k, metric=metric, algorithm='brute')
    nbrs.fit(data[feature_names])
    distances, indices = nbrs.kneighbors([data.iloc[n][feature_names]])
    return pd.concat([data.iloc[indices[0]], pd.DataFrame(distances.T, index=indices[0], columns=['distance'])], axis=1)

print("=== UNSCALED kNN Distances ===")
print(get_knn(df, 1, 5, 'euclidean')['distance'].values.round(2))"""
cells.append(nbf.v4.new_code_cell(code_knn_setup))

code_knn_scaled = """scaler = StandardScaler()
df_scaled = df.copy()
df_scaled[feature_names] = scaler.fit_transform(df[feature_names])

print("=== SCALED kNN Distances ===")
print(get_knn(df_scaled, 1, 5, 'euclidean')['distance'].values.round(2))

plt.figure(figsize=(6,5))
plt.scatter(df_scaled['dob_years'], df_scaled['total_income'], alpha=0.2, c='gray')
nbrs = get_knn(df_scaled, 1, 5, 'euclidean')
plt.scatter(df_scaled.iloc[nbrs.index]['dob_years'], df_scaled.iloc[nbrs.index]['total_income'], s=150, c='red')
plt.title("kNN Scaled Neighbors")
plt.savefig("../outputs/knn_comparison.png", dpi=150)
plt.close()"""
cells.append(nbf.v4.new_code_cell(code_knn_scaled))

code_lr = """df_encoded = df.copy()
for col in ['education', 'family_status', 'gender', 'income_type', 'purpose', 'age_category', 'income_category']:
    df_encoded[col] = LabelEncoder().fit_transform(df_encoded[col].astype(str))

X = df_encoded.drop('debt', axis=1)
y = df_encoded['debt']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

results = []
for name, xtr, xte in [
    ("Unscaled", X_train, X_test),
    ("Normalized", pd.DataFrame(MinMaxScaler().fit_transform(X_train), columns=X.columns), pd.DataFrame(MinMaxScaler().transform(X_test), columns=X.columns)),
    ("Standardized", pd.DataFrame(StandardScaler().fit_transform(X_train), columns=X.columns), pd.DataFrame(StandardScaler().transform(X_test), columns=X.columns))
]:
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(xtr, y_train)
    y_pred = model.predict(xte)
    results.append({"Method": name, "F1": round(f1_score(y_test, y_pred), 4), "AUC": round(roc_auc_score(y_test, model.predict_proba(xte)[:,1]), 4)})

print("=== Model Comparison ===")
display(pd.DataFrame(results))"""
cells.append(nbf.v4.new_code_cell(code_lr))

# ==========================================
# NOTEBOOK BUILD & EXECUTE
# ==========================================
nb['cells'] = cells

# 1. Save unexecuted notebook
with open('../notebooks/data_preprocessing_lab.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Generating notebook and executing cells... (This may take 30-60 seconds)")

# 2. Execute notebook in background
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
try:
    ep.preprocess(nb, {'metadata': {'path': '../notebooks/'}})

    # 3. Save executed notebook (with outputs)
    with open('../notebooks/data_preprocessing_lab.ipynb', 'w') as f:
        nbf.write(nb, f)

    print("\n" + "=" * 50)
    print("✅ SUCCESS! NOTEBOOK GENERATED!")
    print("=" * 50)
    print("Check folder: notebooks/data_preprocessing_lab.ipynb")
    print("Images saved in: outputs/")
except Exception as e:
    print(f"\n❌ Error: {e}")