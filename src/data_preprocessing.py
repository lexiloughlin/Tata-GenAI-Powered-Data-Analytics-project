"""
Delinquency dataset preprocessing (Geldium, Tata GenAI-Powered Data Analytics, Task 1).

Cleans the raw dataset without changing its size:
  1. Standardize Employment_Status spellings
  2. Impute missing Income (by employment group), Loan_Balance and Credit_Score (median)
  3. Flag over-limit customers and engineer payment-history features
  4. Report data quality issues, including the Missed_Payments vs monthly-history conflict

Class balancing (SMOTE) is deliberately NOT part of cleaning. Use
`smote_on_training_data()` after the train/test split so the test set stays real.
"""

from pathlib import Path

import pandas as pd

MONTH_COLS = [f"Month_{i}" for i in range(1, 7)]

EMPLOYMENT_MAP = {
    "Employed": "Employed",
    "employed": "Employed",
    "EMP": "Employed",
    "Unemployed": "Unemployed",
    "Self-employed": "Self-employed",
    "retired": "Retired",
}


class DelinquencyDataPreprocessor:
    """Chainable cleaning steps for the delinquency dataset."""

    def __init__(self, filepath, verbose=True):
        self.df = pd.read_excel(filepath)
        self.original_df = self.df.copy()
        self.verbose = verbose
        self._log(f"Loaded {self.df.shape[0]} rows x {self.df.shape[1]} columns")

    def _log(self, msg):
        if self.verbose:
            print(msg)

    # ---- cleaning ---------------------------------------------------------

    def clean_employment_status(self):
        before = self.df["Employment_Status"].nunique()
        self.df["Employment_Status"] = self.df["Employment_Status"].map(EMPLOYMENT_MAP)
        unmapped = self.df["Employment_Status"].isnull().sum()
        if unmapped:
            raise ValueError(f"{unmapped} Employment_Status values were not in EMPLOYMENT_MAP")
        self._log(f"Employment_Status: {before} spellings -> {self.df['Employment_Status'].nunique()} categories")
        return self

    def handle_missing_income(self):
        """Median income within each Employment_Status group (run clean_employment_status first)."""
        n = self.df["Income"].isnull().sum()
        group_median = self.df.groupby("Employment_Status")["Income"].transform("median")
        self.df["Income"] = self.df["Income"].fillna(group_median)
        self._log(f"Income: imputed {n} values with employment-group medians")
        return self

    def handle_missing_loan_balance(self):
        n = self.df["Loan_Balance"].isnull().sum()
        self.df["Loan_Balance"] = self.df["Loan_Balance"].fillna(self.df["Loan_Balance"].median())
        self._log(f"Loan_Balance: imputed {n} values with the median")
        return self

    def handle_missing_credit_score(self):
        n = self.df["Credit_Score"].isnull().sum()
        self.df["Credit_Score"] = self.df["Credit_Score"].fillna(self.df["Credit_Score"].median())
        self._log(f"Credit_Score: imputed {n} values with the median")
        return self

    # ---- features -----------------------------------------------------------

    def flag_over_limit_customers(self):
        self.df["Over_Credit_Limit"] = (self.df["Credit_Utilization"] > 1.0).astype(int)
        self._log(f"Over_Credit_Limit: {self.df['Over_Credit_Limit'].sum()} customers above 100% utilization")
        return self

    def engineer_payment_features(self):
        months = self.df[MONTH_COLS]
        self.df["Late_Payment_Count"] = (months == "Late").sum(axis=1)
        self.df["Missed_Payment_Count"] = (months == "Missed").sum(axis=1)
        self.df["On_Time_Payment_Count"] = (months == "On-time").sum(axis=1)
        self.df["Payment_Consistency_Score"] = self.df["On_Time_Payment_Count"] / len(MONTH_COLS)
        self.df["Total_Problem_Payments"] = self.df["Late_Payment_Count"] + self.df["Missed_Payment_Count"]
        recent = (self.df[["Month_5", "Month_6"]] != "On-time").sum(axis=1)
        early = (self.df[["Month_1", "Month_2"]] != "On-time").sum(axis=1)
        self.df["Payment_Deterioration"] = (recent > early).astype(int)
        self._log("Added 6 payment-history features")
        return self

    # ---- checks -------------------------------------------------------------

    def payment_consistency_report(self):
        """Compare Missed_Payments with the count of 'Missed' months in the history."""
        from_history = (self.original_df[MONTH_COLS] == "Missed").sum(axis=1)
        mismatch = from_history != self.original_df["Missed_Payments"]
        zero_but_missed = (self.original_df["Missed_Payments"] == 0) & (from_history > 0)
        return {
            "records": len(self.original_df),
            "mismatched": int(mismatch.sum()),
            "zero_missed_but_history_missed": int(zero_but_missed.sum()),
        }

    def quality_report(self):
        y = self.df["Delinquent_Account"]
        return {
            "records": len(self.df),
            "columns": self.df.shape[1],
            "missing_values_before": int(self.original_df.isnull().sum().sum()),
            "missing_values_after": int(self.df.isnull().sum().sum()),
            "duplicates": int(self.df.duplicated().sum()),
            "delinquency_rate": round(float(y.mean()), 3),
            "class_counts": {int(k): int(v) for k, v in y.value_counts().sort_index().items()},
        }

    # ---- pipeline -----------------------------------------------------------

    def run_full_pipeline(self, save_path=None):
        (self.clean_employment_status()
             .handle_missing_income()
             .handle_missing_loan_balance()
             .handle_missing_credit_score()
             .flag_over_limit_customers()
             .engineer_payment_features())
        if save_path:
            self.save(save_path)
        return self

    def get_processed_data(self):
        return self.df

    def save(self, output_path):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if output_path.suffix == ".csv":
            self.df.to_csv(output_path, index=False)
        else:
            self.df.to_excel(output_path, index=False)
        self._log(f"Saved cleaned data to {output_path}")
        return self


def smote_on_training_data(X_train, y_train, random_state=42):
    """Balance classes with SMOTE on the TRAINING split only.

    X_train must already be numeric (e.g. one-hot encoded). Never call this on the
    full dataset: synthetic rows built from test customers would leak into training.
    """
    from imblearn.over_sampling import SMOTE

    return SMOTE(random_state=random_state, k_neighbors=3).fit_resample(X_train, y_train)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    pre = DelinquencyDataPreprocessor(root / "data" / "Delinquency_prediction_dataset.xlsx")
    pre.run_full_pipeline(save_path=root / "data" / "Delinquency_cleaned.csv")
    print(pre.quality_report())
    print(pre.payment_consistency_report())
