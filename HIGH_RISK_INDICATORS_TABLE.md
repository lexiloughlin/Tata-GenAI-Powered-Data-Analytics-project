# High-Risk Indicators for Delinquency Prediction
## Summary Table for Analytics Documents

---

## Purpose and Goals of the Report

**Purpose:**
This report identifies and ranks the key risk factors that predict customer delinquency, providing data-driven guidance for building an accurate, interpretable delinquency prediction model. By analyzing payment behavior, financial stress indicators, and demographic factors against historical delinquency outcomes, this analysis separates strong predictors from weak or misleading signals.

**Goals:**
1. **Identify high-impact risk indicators** that meaningfully differentiate delinquent from non-delinquent customers
2. **Rank features by predictive importance** to guide model feature selection and prioritization
3. **Expose weak predictors and contradictions** in traditional risk assessment (e.g., income paradox, age irrelevance)
4. **Document surprising findings** that require further investigation and may reshape lending strategy
5. **Provide actionable recommendations** for model development, deployment, and risk monitoring
6. **Enable early warning capabilities** through identification of leading indicators like payment deterioration
7. **Support regional and segment-based risk profiling** by analyzing geographic and employment variations

**Key Question Answered:**
*Which factors actually predict delinquency, and which factors are red herrings that add only noise to predictive models?*

---

## Dataset Summary

**Source Data:** Delinquency_prediction_dataset.xlsx

**Number of Records:** 500 customer accounts
- Delinquent: 80 records (16%)
- Non-delinquent: 420 records (84%)

**Key Variables:** 19 features including:
- **Financial Metrics:** Income, Credit_Score, Loan_Balance, Debt_to_Income_Ratio, Credit_Utilization
- **Account Information:** Account_Tenure, Age
- **Payment History:** Missed_Payments, Month_1 through Month_6 payment status
- **Categorical:** Employment_Status, Location, Delinquency (target)

**Data Quality:**
- Missing values: Income 7.8%, Loan_Balance 5.8%, Credit_Score 0.4%
- Over-limit accounts: 7 customers with >100% credit utilization
- Employment encoding: 6 variants (standardized to consistent categories)
- No duplicates detected

**Data Types:** Numerical (continuous & discrete) and Categorical
- All monetary values in USD
- All percentages in decimal format (0-1 range)
- Payment codes consistent across 6-month period

---

## Table 1: Top Risk Indicators (Priority Ranked)

| # | Risk Indicator | One-Line Explanation |
|---|---|---|
| 1 | **Missed Payments History** | Customers with recent/frequent missed payments are the core behavioral signal of default risk. |
| 2 | **Debt-to-Income Ratio (DTI)** | Delinquent customers have 3% higher DTI (0.306 vs 0.297); less discretionary income to cover obligations. |
| 3 | **Credit Utilization Rate** | Delinquent customers use 3.8% more credit (50.7% vs 48.9%); indicates maxed-out capacity and financial pressure. |
| 4 | **Recent Payment Deterioration** | Worsening payment patterns in recent months (Month 5-6 worse than Month 1-2) signal early warning of financial distress. |
| 5 | **Account Tenure** | Newer accounts (9.2 vs 9.8 years) show slightly higher risk; less established payment relationship with lender. |

---

## Table 2: Surprising Findings (Require Investigation)

| Finding | Data | Implication |
|---|---|---|
| **Income NOT Protective** | Delinquent: $113.9K vs Non-delinquent: $107.3K (+6.1%) | High earners still default; spending/debt behavior matters more than raw income |
| **Age is Weak Predictor** | Delinquent: 47.1 vs Non-delinquent: 46.1 years (1 year diff) | Demographics are poor risk signals; behavioral factors dominate |
| **Loan Balance Irrelevant** | Delinquent: $48.4K vs Non-delinquent: $48.7K (-0.7%) | Loan amount does NOT predict default; ability to pay matters |
| **Higher Credit Scores** | Delinquent: 591 vs Non-delinquent: 575 (+16 points) | Historical credit scores weak predictor; recent payment behavior more important |

---

## Table 3: Employment Status Risk Levels

| Employment Status | Delinquency Rate | Risk Level |
|---|---|---|
| Unemployed | 19.4% | 🔴 **Highest** |
| Employed (unstandardized) | 18.3% | 🟠 High |
| Self-employed | 16.3% | 🟡 Moderate |
| Employed (standardized) | 15.6% | 🟡 Moderate |
| Coded Employment | 14.8% | ⚪ Low |
| Retired | 11.5% | ⚪ **Lowest** |

---

## Table 4: Geographic Risk Profile

| Location | Delinquency Rate | Volume | Risk Level |
|---|---|---|---|
| Los Angeles | 19.6% | 107 | 🔴 **Highest** |
| Houston | 16.8% | 95 | 🟡 Moderate-High |
| Phoenix | 16.5% | 103 | 🟡 Moderate |
| Chicago | 14.6% | 103 | 🟡 Moderate-Low |
| New York | 12.0% | 92 | ⚪ **Lowest** |

---

## Key Takeaways for Model Development

✅ **INCLUDE in Predictive Model:**
- Missed/Late Payment History
- Debt-to-Income Ratio  
- Credit Utilization Rate
- Recent Payment Trends
- Employment Status

❌ **EXCLUDE from Model:**
- Age (nearly identical)
- Loan Balance (not predictive)
- Income alone (paradoxically high for delinquent)
- Historical Credit Score (weak signal)

---

## One-Page Executive Summary

The delinquency dataset reveals that **behavioral and financial stress indicators far outweigh demographics** in predicting default risk. 

**Critical finding:** Missed payments, DTI ratio, and credit utilization are the strongest predictors, while income, age, and loan amount show minimal correlation. Surprisingly, delinquent customers have *higher* average income and credit scores, indicating that traditional metrics are insufficient—real-time payment behavior and financial stress indicators must drive the model.

**Recommendation:** Prioritize recent payment patterns and financial pressure metrics; remove age and loan balance from consideration; monitor geographic and employment variations.

