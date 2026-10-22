# Missing Data Handling Strategy

## Overview
This document outlines the approach for handling missing values in the delinquency prediction dataset.

## Missing Data Issues & Treatment

| # | Feature | Missing Data | Handling Method | Justification |
|---|---------|--------------|-----------------|---------------|
| 1 | **Income** | 39 (7.8%) | **Employment-Based Median Imputation** | Preserves income differences by employment type |
| 2 | **Loan_Balance** | 29 (5.8%) | **Median Imputation** | Simple, maintains distribution; missing appears random |
| 3 | **Credit_Score** | 2 (0.4%) | **Median Imputation** | Minimal missing (0.4%); low model impact |


## Detailed Rationale

### Income (7.8% missing)
- **Why employment-based?** Different employment types have different income ranges
- **Preserves patterns** without distorting the income distribution
- **Avoids over-smoothing** from global median imputation

### Loan_Balance (5.8% missing)
- **Why median?** Missing appears random (MCAR); no pattern with delinquency
- **Robust method** that maintains statistical distribution
- **Retains records** without unnecessarily removing 5.8% of data

### Credit_Score (0.4% missing)
- **Why simple median?** Minimal missing data has low impact
- **Fast & reliable** for small amounts of missing values
- **Statistically safe** given the small proportion

## Implementation

```python
from data_preprocessing import DelinquencyDataPreprocessor

preprocessor = DelinquencyDataPreprocessor(
    "/Users/lexiloughlin/Desktop/Delinquency_prediction_dataset.xlsx"
)

# Apply all missing data handling
preprocessor.handle_missing_income(method='employment_based')
preprocessor.handle_missing_loan_balance(method='median')
preprocessor.handle_missing_credit_score()

clean_df = preprocessor.get_processed_data()

# Verify
print(f"Missing values after treatment: {clean_df.isnull().sum().sum()}")  # Should be 0
```

## Results

| Metric | Before | After |
|--------|--------|-------|
| Total Missing Values | 70 | 0 |
| Income Missing | 39 (7.8%) | 0 |
| Loan_Balance Missing | 29 (5.8%) | 0 |
| Credit_Score Missing | 2 (0.4%) | 0 |
| Data Completeness | 99.3% | 100% |

