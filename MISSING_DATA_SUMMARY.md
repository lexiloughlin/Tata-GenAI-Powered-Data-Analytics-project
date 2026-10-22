# Missing Data Strategy & Treatment

## Executive Summary

The delinquency dataset contains **70 missing values (0.74%)** across 3 features. All missing values will be imputed using appropriate statistical methods that preserve data integrity and maintain realistic distributions.

---

## Missing Data Issues & Treatment Methods

| # | Feature | Missing Count | Percentage | Handling Method | Justification |
|---|---------|---------------|-----------|-----------------|---------------|
| 1 | **Income** | 39 | 7.8% | **Employment-Based Median Imputation** | Preserves income differences by employment type; avoids distorting distribution |
| 2 | **Loan_Balance** | 29 | 5.8% | **Median Imputation** | MCAR pattern; simple median maintains distribution; low missingness |
| 3 | **Credit_Score** | 2 | 0.4% | **Median Imputation** | Minimal missing (0.4%); median safe for low-impact features |

---

## Detailed Rationale for Each Method

### 1. Income (7.8% Missing)

**Treatment:** Employment-Based Median Imputation

**Why this method?**
- **Preserves patterns:** Different employment types have different income distributions
  - Employed: ~$108,610 median
  - Unemployed: ~$106,314 median  
  - Retired: ~$108,468 median
  - Self-employed: ~$102,235 median
- **Avoids bias:** Using global median would distort the relationship between employment and income
- **Statistical integrity:** Maintains realistic income ranges for each employment category

**Alternative considered:**
- Global median imputation: ❌ Would flatten legitimate income differences
- KNN imputation: ❌ Overcomplicated for manageable 7.8% missingness
- Removal: ❌ Would lose 39 valid records with other usable features

---

### 2. Loan Balance (5.8% Missing)

**Treatment:** Median Imputation

**Why this method?**
- **MCAR pattern:** Missing appears random; no correlation with delinquency status
- **Robust & simple:** Median is resistant to outliers and maintains distribution shape
- **Data retention:** Imputation preserves 471 valid records vs. losing 29
- **Minimal relationship:** Loan balance shows weak predictive power anyway (means nearly identical for delinquent vs. non-delinquent)

**Alternative considered:**
- Employment-based: ❌ No strong relationship with employment type
- KNN: ❌ Unnecessary complexity for simple random missingness
- Removal: ❌ Wastes 5.8% of otherwise valid data

---

### 3. Credit Score (0.4% Missing)

**Treatment:** Median Imputation

**Why this method?**
- **Negligible impact:** Only 2 records affected (0.4%)
- **Fast & reliable:** Simple median for minimal missingness
- **Statistically safe:** Low proportion won't bias any analysis
- **No over-engineering:** Complex methods unnecessary for this scale

**Alternative considered:**
- Employment-based: ❌ Credit score independent of employment
- KNN: ❌ Overkill for 2 values
- Removal: ❌ Unnecessary for such minimal missingness

---

## Implementation

```python
from data_preprocessing import DelinquencyDataPreprocessor

# Initialize preprocessor
preprocessor = DelinquencyDataPreprocessor(
    "/Users/lexiloughlin/Desktop/Delinquency_prediction_dataset.xlsx"
)

# Apply missing data handling
preprocessor.handle_missing_income(method='employment_based')
preprocessor.handle_missing_loan_balance(method='median')
preprocessor.handle_missing_credit_score()

# Get cleaned data
clean_df = preprocessor.get_processed_data()

# Verify results
print(f"Missing values: {clean_df.isnull().sum().sum()}")  # Should print: 0
print(f"Data shape: {clean_df.shape}")  # Should print: (500, 19)
```

---

## Results & Impact

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Total Missing Values** | 70 | 0 | -100% |
| **Data Completeness** | 99.3% | 100.0% | +0.7% |
| **Income Missing** | 39 (7.8%) | 0 | ✓ Imputed |
| **Loan Balance Missing** | 29 (5.8%) | 0 | ✓ Imputed |
| **Credit Score Missing** | 2 (0.4%) | 0 | ✓ Imputed |
| **Usable Records** | 461-471 | 500 | All rows retained |

---

## Quality Assurance

✓ **Verification Checklist:**
- [ ] No missing values remain after imputation
- [ ] Income distributions preserve employment-type differences
- [ ] Median values fall within expected ranges
- [ ] No outliers introduced by imputation
- [ ] Model training can proceed with full dataset

```python
# Verification code
assert clean_df.isnull().sum().sum() == 0, "Missing values detected!"
assert len(clean_df) == 500, "Record count changed!"
assert clean_df['Income'].min() > 0, "Invalid income values!"
print("✓ All quality checks passed!")
```

---

## Recommendation

**Proceed with employment-based and median imputation** as outlined above. This approach:
1. ✓ Handles all missing data appropriately
2. ✓ Maintains data integrity and realistic distributions
3. ✓ Retains all usable records
4. ✓ Requires no removal or synthetic generation
5. ✓ Ready for immediate modeling

