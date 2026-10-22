# Delinquency Dataset Preprocessing Guide

## Quick Start

### Option 1: One-Line Solution (Recommended)

```python
from data_preprocessing import DelinquencyDataPreprocessor

# Run everything automatically
preprocessor = DelinquencyDataPreprocessor(
    "/Users/lexiloughlin/Desktop/Delinquency_prediction_dataset.xlsx"
)

clean_df = (preprocessor
            .run_full_pipeline(handle_imbalance=True,
                             save_path="Delinquency_CLEANED.xlsx")
            .get_processed_data())
```

**This solves ALL problems:**
- ✅ Employment_Status standardization
- ✅ Missing Income imputation
- ✅ Missing Loan_Balance imputation
- ✅ Missing Credit_Score handling
- ✅ Credit utilization over-limit flagging
- ✅ Payment pattern feature engineering
- ✅ Class imbalance (SMOTE)

---

## What Each Step Does

### 1. Clean Employment Status
**Problem:** Mixed case and encoding (employed, Employed, EMP, retired)

```python
preprocessor.clean_employment_status()
```

**Result:** Standardized to 4 categories
- Employed
- Unemployed
- Self-employed
- Retired

---

### 2. Handle Missing Income (7.8%)

```python
# Method 1: Employment-based imputation (RECOMMENDED)
preprocessor.handle_missing_income(method='employment_based')

# Method 2: Median imputation
preprocessor.handle_missing_income(method='median')

# Method 3: KNN imputation
preprocessor.handle_missing_income(method='knn')
```

**Why employment-based?** Preserves income differences by employment type.

---

### 3. Handle Missing Loan Balance (5.8%)

```python
# Method 1: Median imputation (RECOMMENDED)
preprocessor.handle_missing_loan_balance(method='median')

# Method 2: KNN imputation
preprocessor.handle_missing_loan_balance(method='knn')
```

---

### 4. Handle Missing Credit Score (0.4%)

```python
preprocessor.handle_missing_credit_score()
```

**Minimal impact** - only 2 records affected

---

### 5. Flag Over-Limit Customers

```python
preprocessor.flag_over_limit_customers()
```

**Creates:** `Over_Credit_Limit` binary feature
- Identifies customers with Credit_Utilization > 1.0
- High-risk financial distress indicator

---

### 6. Engineer Payment Features

```python
preprocessor.engineer_payment_features()
```

**Creates 5 new features from monthly payment data:**

| Feature | Description | Range |
|---------|-------------|-------|
| `Late_Payment_Count` | Number of late payments (Month_1-6) | 0-6 |
| `Missed_Payment_Count` | Number of missed payments | 0-6 |
| `On_Time_Payment_Count` | Number of on-time payments | 0-6 |
| `Payment_Consistency_Score` | On-time ratio (0-1) | 0.0-1.0 |
| `Total_Problem_Payments` | Late + Missed | 0-12 |
| `Payment_Deterioration` | Recent worse than early? | 0-1 |

---

### 7. Handle Class Imbalance (5.2:1)

**Problem:** Only 16% delinquent cases

```python
# SMOTE (Synthetic Minority Over-sampling) - RECOMMENDED
preprocessor.balance_classes(method='smote')

# Alternative: Random over-sampling
preprocessor.balance_classes(method='oversample')
```

**SMOTE vs Over-sampling:**
- **SMOTE:** Creates synthetic minority samples (less overfitting)
- **Oversample:** Duplicates existing samples (faster, may overfit)

---

## Step-by-Step Example

```python
from data_preprocessing import DelinquencyDataPreprocessor
import pandas as pd

# Initialize
preprocessor = DelinquencyDataPreprocessor(
    "/Users/lexiloughlin/Desktop/Delinquency_prediction_dataset.xlsx"
)

# Clean categorical data
preprocessor.clean_employment_status()

# Handle missing values
preprocessor.handle_missing_income(method='employment_based')
preprocessor.handle_missing_loan_balance(method='median')
preprocessor.handle_missing_credit_score()

# Add features
preprocessor.flag_over_limit_customers()
preprocessor.engineer_payment_features()

# Fix imbalance
preprocessor.balance_classes(method='smote')

# Generate report
preprocessor.create_quality_report()

# Get and save data
clean_df = preprocessor.get_processed_data()
preprocessor.save_processed_data("/Users/lexiloughlin/Desktop/Delinquency_CLEANED.xlsx")

# Check results
print(f"Shape: {clean_df.shape}")
print(f"Columns: {clean_df.columns.tolist()}")
print(f"Missing: {clean_df.isnull().sum().sum()}")
```

---

## Output Files

After running preprocessing:

**Original file:** `Delinquency_prediction_dataset.xlsx`
- 500 rows × 19 columns
- Missing values, imbalanced classes

**Cleaned file:** `Delinquency_CLEANED.xlsx`
- 840 rows × 25 columns (after SMOTE)
- No missing values
- Balanced classes (420:420)
- 6 new engineered features

---

## Features Removed/Flagged

Based on analysis:

### Weak Predictors (Consider Dropping)
- **Age:** Similar means for both groups (not predictive)
- **Loan_Balance:** Nearly identical for delinquent vs non-delinquent

```python
# Remove if desired
clean_df = clean_df.drop(['Age', 'Loan_Balance'], axis=1)
```

### Redundant Columns
- `Customer_ID`: Unique identifier, not predictive
- Monthly columns (`Month_1-6`): Replaced by aggregated features

```python
# Remove after engineering features
clean_df = clean_df.drop(['Month_1', 'Month_2', 'Month_3', 'Month_4', 'Month_5', 'Month_6', 'Customer_ID'], axis=1)
```

---

## Data Quality Checklist

After preprocessing:

- [ ] No missing values
- [ ] Employment_Status standardized
- [ ] Classes balanced (50:50)
- [ ] New payment features created
- [ ] Over-limit flag added
- [ ] Weak predictors identified
- [ ] Data saved to Excel

---

## Ready for Modeling

Your cleaned dataset can now be used for:

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Prepare data
X = clean_df.drop('Delinquent_Account', axis=1)
y = clean_df['Delinquent_Account']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
```

---

## Troubleshooting

**Issue:** "No module named 'imblearn'"
```bash
pip install imbalanced-learn
```

**Issue:** "No module named 'data_preprocessing'"
- Make sure `data_preprocessing.py` is in the same directory
- Or add to path: `import sys; sys.path.append('/path/to/repo')`

**Issue:** File not found
- Update file path in `DelinquencyDataPreprocessor("/path/to/file.xlsx")`

**Issue:** Want to skip SMOTE?
```python
preprocessor.run_full_pipeline(handle_imbalance=False)
```

---

## Questions?

Check the docstrings:
```python
help(DelinquencyDataPreprocessor)
help(DelinquencyDataPreprocessor.handle_missing_income)
```

Or examine method signatures in `data_preprocessing.py`
