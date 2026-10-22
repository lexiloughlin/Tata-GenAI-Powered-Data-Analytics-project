# Quick Start Guide - Delinquency Preprocessing

## TL;DR - Run This Now

```python
from data_preprocessing import DelinquencyDataPreprocessor

preprocessor = DelinquencyDataPreprocessor(
    "/Users/lexiloughlin/Desktop/Delinquency_prediction_dataset.xlsx"
)

clean_df = (preprocessor
            .run_full_pipeline(handle_imbalance=True,
                             save_path="Delinquency_CLEANED.xlsx")
            .get_processed_data())

print(f"✓ Done! Cleaned data shape: {clean_df.shape}")
```

**That's it!** All data quality issues are solved.

---

## What Just Happened?

✅ Fixed employment status encoding  
✅ Imputed missing income (7.8%)  
✅ Imputed missing loan balance (5.8%)  
✅ Imputed missing credit score (0.4%)  
✅ Flagged over-limit customers  
✅ Created 6 new predictive features  
✅ Balanced classes with SMOTE  
✅ Saved cleaned data to Excel  

---

## For Jupyter Notebook

Copy this into a cell:

```python
from data_preprocessing import DelinquencyDataPreprocessor

preprocessor = DelinquencyDataPreprocessor(
    "/Users/lexiloughlin/Desktop/Delinquency_prediction_dataset.xlsx"
)

clean_df = preprocessor.run_full_pipeline(
    handle_imbalance=True,
    save_path="Delinquency_CLEANED.xlsx"
).get_processed_data()

print(clean_df.head())
print(f"Shape: {clean_df.shape}")
print(f"Columns: {clean_df.columns.tolist()}")
```

---

## Check Results

```python
import pandas as pd

# Load cleaned data
clean_df = pd.read_excel("Delinquency_CLEANED.xlsx")

# Verify quality
print(f"Missing values: {clean_df.isnull().sum().sum()}")  # Should be 0
print(f"Class balance: {clean_df['Delinquent_Account'].value_counts().to_dict()}")  # Should be {0: 420, 1: 420}
print(f"New columns: {len(clean_df.columns)}")  # Should be 25
```

---

## Files in This Directory

| File | Purpose |
|------|---------|
| `data_preprocessing.py` | Main preprocessing module (use this!) |
| `QUICK_START.md` | This file |
| `PREPROCESSING_GUIDE.md` | Detailed explanation of each step |
| `USAGE_EXAMPLES.py` | 7 practical examples |
| `delinquency_preprocessing.ipynb` | Jupyter notebook template |

---

## Next Steps

### 1. Train a Model

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Prepare data
X = clean_df.drop('Delinquent_Account', axis=1)
y = clean_df['Delinquent_Account']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate
print(classification_report(y_test, model.predict(X_test)))
```

### 2. Explore Feature Importance

```python
import pandas as pd

# Get feature importance
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(importance.head(10))
```

### 3. Make Predictions

```python
# Predict on new data
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

# Get delinquency risk scores
risk_scores = pd.DataFrame({
    'Predicted_Delinquent': y_pred,
    'Risk_Score': y_pred_proba[:, 1]
})

print(risk_scores.head())
```

---

## Common Issues

### Issue: "No module named 'data_preprocessing'"
```python
# Make sure data_preprocessing.py is in the same directory
# Or add to path:
import sys
sys.path.append('/path/to/directory')
from data_preprocessing import DelinquencyDataPreprocessor
```

### Issue: "File not found"
```python
# Check the path exists:
import os
os.path.exists("/Users/lexiloughlin/Desktop/Delinquency_prediction_dataset.xlsx")
```

### Issue: "No module named 'imblearn'"
```bash
pip install imbalanced-learn
```

### Issue: Want to skip SMOTE?
```python
preprocessor.run_full_pipeline(handle_imbalance=False)
```

---

## Reference: New Features Created

After preprocessing, you'll have these new columns:

```
Late_Payment_Count           # Range: 0-6
Missed_Payment_Count         # Range: 0-6
On_Time_Payment_Count        # Range: 0-6
Payment_Consistency_Score    # Range: 0.0-1.0 (higher = better)
Total_Problem_Payments       # Late + Missed (Range: 0-12)
Payment_Deterioration        # Binary: recent worse than early?
Over_Credit_Limit            # Binary: Credit_Utilization > 1.0?
```

---

## Support

See `PREPROCESSING_GUIDE.md` for:
- Detailed step-by-step explanation
- Multiple imputation methods
- Feature engineering details
- Troubleshooting

See `USAGE_EXAMPLES.py` for:
- 7 complete working examples
- Different configuration options
- Model-ready data preparation

---

**Ready to go!** 🚀
