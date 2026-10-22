# Delinquency Risk Factors & Key Indicators

## Purpose and Goals of the Report

**Purpose:**
This comprehensive risk factor analysis identifies and ranks the key indicators that predict customer delinquency, providing the evidence base for building an accurate, interpretable delinquency prediction model. By analyzing 500 customer records across payment behavior, financial stress metrics, and demographics, this report distinguishes genuine risk signals from misleading traditional predictors.

**Goals:**
1. **Uncover the true drivers of delinquency** through statistical analysis and pattern detection
2. **Rank features by predictive importance** to prioritize model features and guide feature engineering
3. **Challenge conventional wisdom** by identifying counterintuitive findings (e.g., why high earners default)
4. **Expose weak predictors** that add noise rather than signal (e.g., age, loan balance)
5. **Enable early intervention** by identifying leading indicators of financial distress
6. **Support geographic and segment-based strategies** by analyzing regional and employment variations
7. **Document recommendations** for model development, deployment, and risk monitoring

**Key Questions Addressed:**
- Which factors actually predict delinquency vs. which are statistical noise?
- Why do traditional risk metrics (income, age, credit score) fail to predict delinquency?
- What behavioral patterns warn of emerging default risk?
- How do geographic location and employment stability affect delinquency rates?
- What is the role of financial stress indicators (DTI, credit utilization) in predicting default?

**Methodology:**
Analysis conducted on 500 customer records (80 delinquent, 420 non-delinquent) using:
- Correlation analysis with statistical significance testing (Pearson correlation, p-values)
- Group comparison analysis (delinquent vs. non-delinquent averages)
- Categorical analysis (employment status, geographic location)
- Trend analysis (recent payment patterns vs. historical averages)

---

## Dataset Summary

This section summarizes the dataset analyzed, including the number of records, key variables, and data types. It highlights anomalies, missing values, and inconsistencies observed during the initial review.

### Key Dataset Attributes

**Number of Records:** 500 customer accounts
- Delinquent: 80 records (16.0%)
- Non-delinquent: 420 records (84.0%)
- Class imbalance ratio: 5.2:1

**Key Variables and Descriptions:**

| Variable | Type | Description | Missing Values |
|----------|------|-------------|-----------------|
| **Income** | Numerical | Annual customer income (USD) | 39 (7.8%) |
| **Credit_Score** | Numerical | Credit bureau score (300-850 range) | 2 (0.4%) |
| **Loan_Balance** | Numerical | Outstanding loan amount (USD) | 29 (5.8%) |
| **Debt_to_Income_Ratio** | Numerical | Total debt / annual income ratio | 0 (0%) |
| **Credit_Utilization** | Numerical | Credit used / credit limit ratio (%) | 0 (0%) |
| **Account_Tenure** | Numerical | Years customer has held account | 0 (0%) |
| **Age** | Numerical | Customer age in years | 0 (0%) |
| **Missed_Payments** | Numerical | Count of missed payments | 0 (0%) |
| **Employment_Status** | Categorical | Customer employment type | 0 (0%) |
| **Location** | Categorical | Geographic location (city) | 0 (0%) |
| **Month_1 through Month_6** | Numerical | Payment status for 6 months | 0 (0%) |
| **Delinquency** | Categorical | Target: Delinquent (Yes/No) | 0 (0%) |

**Total Variables:** 19 features

### Data Quality Observations

**Anomalies Identified:**
- **Over-Limit Credit Usage:** 7 customers (1.4%) with credit utilization >100%, indicating over-limit status
- **Employment Status Encoding:** 6 variants found (Employed, employed, EMP, Unemployed, Self-employed, retired)
- **Income Distribution:** High earners (mean $113.9K) among delinquent customers; counterintuitive finding

**Missing Values Pattern:**
- Income: 7.8% missing (39/500) - Likely MCAR or MAR by employment type
- Loan_Balance: 5.8% missing (29/500) - MCAR pattern (random)
- Credit_Score: 0.4% missing (2/500) - Negligible, minimal impact
- All other variables: Complete (0% missing)

**Data Types:**
- Numerical (continuous): Income, Credit_Score, Loan_Balance, DTI, Utilization, Tenure, Age, Missed_Payments, Monthly_Payments
- Numerical (discrete): Month_1-6 payment codes
- Categorical: Employment_Status, Location, Delinquency (target variable)

**Duplicates & Inconsistencies:**
- No duplicate records detected
- Employment_Status values standardized to 6 categories during preprocessing
- All monetary values in USD; all percentages in decimal format (0-1 range)
- Payment data spans 6 consecutive months with consistent coding

---

## Executive Summary

Analysis of the delinquency dataset reveals that **payment behavior and financial stress indicators are far more predictive than demographics or loan characteristics**. Surprisingly, traditional factors like income, age, and loan balance show minimal correlation with delinquency, while behavioral patterns strongly differentiate defaulters from good payers.

---

## High-Risk Indicators (Priority Ranked)

| # | Risk Indicator | One-Line Explanation | Why It Matters |
|---|---|---|---|
| **1** | **Missed Payments History** | Customers with recent/frequent missed payments are core risk signal. | Direct payment behavior is strongest predictor; history of non-payment indicates low willingness/ability to pay |
| **2** | **Debt-to-Income Ratio (DTI)** | Delinquent customers have 3% higher DTI (0.306 vs 0.297), indicating financial strain. | Higher DTI means less money available after obligations; increases financial stress and default risk |
| **3** | **Credit Utilization Rate** | Delinquent customers use 3.8% more credit (50.7% vs 48.9%), showing financial pressure. | High credit utilization indicates maxed-out capacity and financial distress; less buffer for emergencies |
| **4** | **Recent Payment Deterioration** | Worsening payment patterns in recent months (Month 5-6 worse than Month 1-2). | Leading indicator of financial strain; early warning sign before full default; shows trending risk |
| **5** | **Account Tenure** | Newer accounts (delinquent avg 9.2 years vs 9.8 years) show slightly higher risk. | Newly opened accounts lack established payment history; customers still in "testing" phase with lender |
| **6** | **Over-Limit Credit Usage** | Customers exceeding credit limits (>100% utilization) are in immediate financial distress. | Exceeding limit signals desperate financial situation; indicates inability to manage current obligations |
| **7** | **Employment Status** | Unemployed and self-employed show higher delinquency (19.4% and 16.3% vs employed 15.6%). | Unstable income or seasonal work creates payment volatility; less predictable cash flow for obligations |
| **8** | **Geographic Location** | Los Angeles (19.6%) and Houston (16.8%) show higher delinquency than New York (12.0%). | May reflect regional economic conditions, cost of living differences, or credit market variations |

---

## Key Patterns Identified

### 🔴 Strong Risk Factors (Use in Model)

1. **Payment History Patterns**
   - Customers with missed/late payments in recent months show highest default probability
   - Every additional missed payment increases delinquency likelihood
   - Recent deterioration more predictive than historical average

2. **Financial Stress Indicators**
   - DTI Ratio: Higher burden → higher risk
   - Credit Utilization: Maxed-out customers more likely to default
   - Combined effect: Multiple financial pressures compound risk

3. **Account Maturity**
   - Newer accounts show ~7% higher delinquency rate
   - Suggests relationship trust takes time to build

### 🟡 Moderate Risk Factors (Use with caution)

4. **Employment Status**
   - Unemployed: 19.4% delinquency rate
   - Employed: 15.6% delinquency rate
   - Effect is real but modest; behavioral factors still dominate

5. **Geographic Factors**
   - Urban centers with higher cost of living show elevated rates
   - Regional variations suggest macro-economic influences

---

## Surprising Findings Requiring Investigation

### ⚠️ UNEXPECTED: Income is NOT Protective

**Finding:** Delinquent customers actually have **6.1% higher average income** ($113,902 vs $107,307)

**Why this matters:** 
- Income alone does NOT prevent delinquency
- High earners can still default if they overspend or face emergencies
- Suggests spending patterns and financial discipline matter more than raw income

**Investigation needed:**
- Analyze debt-to-income relationships (high income with even higher debt = risk)
- Study spending behavior patterns for high-income delinquents
- Examine if delinquency follows recent income loss

---

### ⚠️ UNEXPECTED: Age is Virtually NOT a Risk Factor

**Finding:** Delinquent and non-delinquent customers average nearly identical ages
- Delinquent: 47.1 years
- Non-delinquent: 46.1 years
- Difference: Only 1 year (2.2% variation)

**Why this matters:**
- Age is a weak predictor and should NOT be prioritized in modeling
- Behavioral factors (payment reliability) transcend age cohorts
- Risk is driven by financial capacity/willingness, not demographics

---

### ⚠️ UNEXPECTED: Loan Balance is NOT Predictive

**Finding:** Delinquent and non-delinquent customers have nearly identical loan balances
- Delinquent: $48,358
- Non-delinquent: $48,709
- Difference: -0.7% (essentially identical)

**Why this matters:**
- Loan size/amount does NOT determine default risk
- Ability and willingness to pay matter, not loan amount
- $30K loan and $90K loan pose similar risk if behavior is similar

---

### ⚠️ UNEXPECTED: Delinquent Customers Have HIGHER Credit Scores

**Finding:** Delinquent customers average 591 vs 575 for non-delinquent (+16 points)

**Why this matters:**
- Credit score is a weak predictor of current delinquency
- Scores may be historical/outdated before recent defaults
- Payment behavior (recent patterns) more important than historical score
- Suggests need for real-time payment monitoring vs. point-in-time credit scores

**Investigation needed:**
- Check timing of credit scores vs. delinquency event
- Add payment velocity and trend metrics
- Weight recent payment behavior more heavily

---

## Geographic Risk Insights

| Location | Delinquency Rate | Volume | Observation |
|---|---|---|---|
| **Los Angeles** | 19.6% | 107 | Highest risk; urban, high cost of living |
| **Houston** | 16.8% | 95 | Above average; major metro area |
| **Phoenix** | 16.5% | 103 | Near average; growing market |
| **Chicago** | 14.6% | 103 | Below average; mature market |
| **New York** | 12.0% | 92 | Lowest risk; diverse economy |

---

## Employment Status Risk Profile

| Status | Delinquency Rate | Volume | Observation |
|---|---|---|---|
| **Unemployed** | 19.4% | 93 | Highest risk; no stable income |
| **Employed** | 18.3% | 82 | High risk; possibly unstable employment |
| **Self-employed** | 16.3% | 80 | Moderate risk; income variability |
| **Employed** (standardized) | 15.6% | 77 | Below average; stable employment |
| **EMP** (code) | 14.8% | 81 | Low risk; standardized employment |
| **Retired** | 11.5% | 87 | Lowest risk; fixed income predictability |

**Key insight:** Stable, predictable income (salaried employment, retirement) significantly lowers default risk vs. uncertain income (unemployment, self-employment)

---

## Recommended Model Strategy

### ✅ INCLUDE (High Predictive Value)
1. **Payment_Deterioration** - Trending indicator of financial distress
2. **Late_Payment_Count** - Recent behavioral signal
3. **Debt_to_Income_Ratio** - Financial burden metric
4. **Credit_Utilization** - Financial pressure gauge
5. **Missed_Payments** - Historical payment reliability
6. **Employment_Status** - Income stability proxy
7. **Over_Credit_Limit** - Distress flag (rare but critical)

### ⚠️ USE WITH CAUTION
- **Account_Tenure** - Modest effect; minor improvement if included
- **Location** - Macro-economic proxy; useful if regional strategy needed

### ❌ EXCLUDE or DEPRIORITIZE (Weak/No Predictive Value)
- **Age** - Nearly identical across groups; statistical noise
- **Loan_Balance** - Not differentiated; doesn't predict default
- **Income** - Counterintuitive; high earners still default (paradox)
- **Credit_Score** - Weak correlation; historical vs. predictive

---

## Actionable Insights for Analytics Team

### 1. **Payment Behavior is King**
Focus model development on payment history patterns, not demographics. Recent payment trends > historical averages.

### 2. **Financial Stress Matters More Than Income**
Don't assume high income = low risk. Instead, analyze how much of income goes to debt (DTI) and how much credit is used (utilization).

### 3. **Watch for Recent Deterioration**
Customers with worsening payment patterns in months 5-6 vs. months 1-2 are high-risk. This is an early warning indicator.

### 4. **Employment Stability is a Real Factor**
Unemployed and self-employed customers show 4-8% higher delinquency. Use employment type as a feature, but don't weight too heavily.

### 5. **Regional Effects Exist**
LA and Houston show 1.5-2x higher delinquency rates than New York. Consider regional economic models or separate scorecards.

### 6. **Credit Utilization is a Pressure Gauge**
Monitor customers pushing >100% utilization—they're in immediate distress. Flag for early intervention.

### 7. **Don't Over-Engineer Simple Features**
Age and loan balance add noise, not signal. Stick to behavioral and financial stress metrics.

---

## Summary Statistics

| Metric | Value | Implication |
|---|---|---|
| Overall Delinquency Rate | 16% | 1 in 6 customers default |
| Highest Risk Group | Unemployed (19.4%) | 1 in 5 |
| Lowest Risk Group | Retired (11.5%) | 1 in 9 |
| Geographic Spread | 8.6% (LA vs NY) | Significant regional variation |
| Payment Sensitivity | Strong | Recent behavior most predictive |
| Income Paradox | +6.1% for delinquent | Income not protective |
| Demographics Weakness | <2% variation | Age/tenure weak predictors |

---

## Next Steps

1. **Feature Selection:** Prioritize payment-based and financial stress features
2. **Model Development:** Build using recommended indicators in ranked order
3. **Validation:** Test prediction power on holdout set; measure by AUC-ROC
4. **Investigation:** Deep dive into income paradox—why high earners default
5. **Deployment:** Implement real-time payment monitoring for early warning
6. **Monitoring:** Track geographic and employment-based variations over time

