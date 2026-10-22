"""
Delinquency Dataset Preprocessing & Data Cleaning
Solves all identified data quality issues
"""

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings('ignore')


class DelinquencyDataPreprocessor:
    """Handle data cleaning and preprocessing for delinquency prediction model"""
    
    def __init__(self, filepath):
        """Initialize with dataset path"""
        self.df = pd.read_excel(filepath)
        self.original_df = self.df.copy()
        print(f"✓ Loaded dataset: {self.df.shape[0]} rows × {self.df.shape[1]} columns")
    
    def clean_employment_status(self):
        """Standardize inconsistent Employment_Status encoding"""
        print("\n" + "="*60)
        print("1. CLEANING EMPLOYMENT_STATUS")
        print("="*60)
        
        print("Before:")
        print(self.df['Employment_Status'].value_counts())
        
        # Mapping inconsistent values
        employment_mapping = {
            'Employed': 'Employed',
            'employed': 'Employed',
            'EMP': 'Employed',
            'Unemployed': 'Unemployed',
            'Self-employed': 'Self-employed',
            'retired': 'Retired'
        }
        
        self.df['Employment_Status'] = self.df['Employment_Status'].map(employment_mapping)
        
        print("\nAfter:")
        print(self.df['Employment_Status'].value_counts())
        print("✓ Employment_Status standardized")
        
        return self
    
    def handle_missing_income(self, method='median'):
        """
        Handle missing Income values
        method: 'median', 'mean', or 'employment_based'
        """
        print("\n" + "="*60)
        print("2. HANDLING MISSING INCOME")
        print("="*60)
        
        missing_count = self.df['Income'].isnull().sum()
        print(f"Missing values: {missing_count} ({missing_count/len(self.df)*100:.2f}%)")
        
        if method == 'employment_based':
            # Impute by employment status
            print("Using Employment Status-based imputation...")
            for status in self.df['Employment_Status'].unique():
                mask = (self.df['Employment_Status'] == status) & (self.df['Income'].isnull())
                median_income = self.df[self.df['Employment_Status'] == status]['Income'].median()
                self.df.loc[mask, 'Income'] = median_income
                print(f"  {status}: ${median_income:,.0f}")
        
        elif method == 'knn':
            # KNN imputation using surrounding features
            print("Using KNN imputation...")
            imputer = KNNImputer(n_neighbors=5)
            numeric_cols = ['Age', 'Income', 'Credit_Score', 'Loan_Balance', 'Debt_to_Income_Ratio']
            self.df[numeric_cols] = imputer.fit_transform(self.df[numeric_cols])
        
        else:  # median
            print("Using median imputation...")
            self.df['Income'].fillna(self.df['Income'].median(), inplace=True)
        
        print(f"✓ Missing Income values handled")
        print(f"  Remaining missing: {self.df['Income'].isnull().sum()}")
        
        return self
    
    def handle_missing_loan_balance(self, method='median'):
        """Handle missing Loan_Balance values"""
        print("\n" + "="*60)
        print("3. HANDLING MISSING LOAN_BALANCE")
        print("="*60)
        
        missing_count = self.df['Loan_Balance'].isnull().sum()
        print(f"Missing values: {missing_count} ({missing_count/len(self.df)*100:.2f}%)")
        
        if method == 'knn':
            print("Using KNN imputation...")
            imputer = KNNImputer(n_neighbors=5)
            numeric_cols = ['Age', 'Income', 'Credit_Score', 'Loan_Balance', 'Debt_to_Income_Ratio']
            self.df[numeric_cols] = imputer.fit_transform(self.df[numeric_cols])
        else:
            print("Using median imputation...")
            self.df['Loan_Balance'].fillna(self.df['Loan_Balance'].median(), inplace=True)
        
        print(f"✓ Missing Loan_Balance values handled")
        print(f"  Remaining missing: {self.df['Loan_Balance'].isnull().sum()}")
        
        return self
    
    def handle_missing_credit_score(self):
        """Handle missing Credit_Score (minimal impact)"""
        print("\n" + "="*60)
        print("4. HANDLING MISSING CREDIT_SCORE")
        print("="*60)
        
        missing_count = self.df['Credit_Score'].isnull().sum()
        print(f"Missing values: {missing_count} ({missing_count/len(self.df)*100:.2f}%)")
        
        if missing_count > 0:
            self.df['Credit_Score'].fillna(self.df['Credit_Score'].median(), inplace=True)
            print(f"✓ Missing Credit_Score values imputed with median")
        
        return self
    
    def flag_over_limit_customers(self):
        """Flag customers with Credit_Utilization > 1.0 (over-limit)"""
        print("\n" + "="*60)
        print("5. FLAGGING HIGH-RISK CUSTOMERS (Over-limit)")
        print("="*60)
        
        over_limit = (self.df['Credit_Utilization'] > 1.0).sum()
        print(f"Customers over credit limit: {over_limit}")
        
        if over_limit > 0:
            self.df['Over_Credit_Limit'] = (self.df['Credit_Utilization'] > 1.0).astype(int)
            print(f"✓ Created 'Over_Credit_Limit' flag")
            print(f"  Distribution: {self.df['Over_Credit_Limit'].value_counts().to_dict()}")
        
        return self
    
    def engineer_payment_features(self):
        """Create derived features from monthly payment patterns"""
        print("\n" + "="*60)
        print("6. ENGINEERING PAYMENT PATTERN FEATURES")
        print("="*60)
        
        monthly_cols = ['Month_1', 'Month_2', 'Month_3', 'Month_4', 'Month_5', 'Month_6']
        
        # Count late/missed payments
        self.df['Late_Payment_Count'] = (self.df[monthly_cols] == 'Late').sum(axis=1)
        self.df['Missed_Payment_Count'] = (self.df[monthly_cols] == 'Missed').sum(axis=1)
        self.df['On_Time_Payment_Count'] = (self.df[monthly_cols] == 'On-time').sum(axis=1)
        
        # Payment consistency score (0-1: higher is better)
        self.df['Payment_Consistency_Score'] = self.df['On_Time_Payment_Count'] / len(monthly_cols)
        
        # Payment health (combined late + missed)
        self.df['Total_Problem_Payments'] = self.df['Late_Payment_Count'] + self.df['Missed_Payment_Count']
        
        # Check for recent deterioration (Month 5-6 worse than Month 1-2)
        recent_problems = (self.df[['Month_5', 'Month_6']] != 'On-time').sum(axis=1)
        early_problems = (self.df[['Month_1', 'Month_2']] != 'On-time').sum(axis=1)
        self.df['Payment_Deterioration'] = (recent_problems > early_problems).astype(int)
        
        print("✓ Created payment pattern features:")
        print(f"  - Late_Payment_Count: range {self.df['Late_Payment_Count'].min()}-{self.df['Late_Payment_Count'].max()}")
        print(f"  - Missed_Payment_Count: range {self.df['Missed_Payment_Count'].min()}-{self.df['Missed_Payment_Count'].max()}")
        print(f"  - Payment_Consistency_Score: mean={self.df['Payment_Consistency_Score'].mean():.3f}")
        print(f"  - Payment_Deterioration: {self.df['Payment_Deterioration'].sum()} customers")
        
        return self
    
    def identify_weak_features(self):
        """Identify and flag weak predictive features"""
        print("\n" + "="*60)
        print("7. IDENTIFYING WEAK FEATURES")
        print("="*60)
        
        weak_features = {
            'Age': 'Similar means between groups (47.1 vs 46.1)',
            'Loan_Balance': 'Nearly identical means (~$48.5k for both)'
        }
        
        print("Weak Predictors to Consider Removing/Investigating:")
        for feature, reason in weak_features.items():
            print(f"  - {feature}: {reason}")
        
        return self
    
    def balance_classes(self, method='smote', random_state=42):
        """
        Handle class imbalance
        method: 'smote', 'oversample', or 'class_weights'
        """
        from sklearn.preprocessing import LabelEncoder
        
        print("\n" + "="*60)
        print("8. HANDLING CLASS IMBALANCE")
        print("="*60)
        
        print(f"Before balancing:")
        print(self.df['Delinquent_Account'].value_counts())
        print(f"Ratio: {self.df['Delinquent_Account'].value_counts()[0] / self.df['Delinquent_Account'].value_counts()[1]:.1f}:1")
        
        if method == 'smote':
            print("\nApplying SMOTE (Synthetic Minority Over-sampling)...")
            
            # Separate features and target
            X = self.df.drop(['Delinquent_Account', 'Customer_ID'], axis=1)
            y = self.df['Delinquent_Account']
            
            # Encode categorical variables for SMOTE
            X_encoded = X.copy()
            label_encoders = {}
            categorical_cols = X_encoded.select_dtypes(include=['object']).columns
            
            for col in categorical_cols:
                le = LabelEncoder()
                X_encoded[col] = le.fit_transform(X_encoded[col].astype(str))
                label_encoders[col] = le
            
            # Apply SMOTE
            smote = SMOTE(random_state=random_state, k_neighbors=3)
            X_smote, y_smote = smote.fit_resample(X_encoded, y)
            
            # Reconstruct dataframe with original categorical values
            X_smote_df = pd.DataFrame(X_smote, columns=X_encoded.columns)
            
            # Decode categorical columns
            for col in categorical_cols:
                X_smote_df[col] = X_smote_df[col].astype(int)
                X_smote_df[col] = label_encoders[col].inverse_transform(X_smote_df[col])
            
            # Reconstruct full dataframe
            self.df = X_smote_df.copy()
            self.df['Delinquent_Account'] = y_smote
            
            print(f"\nAfter SMOTE:")
            print(self.df['Delinquent_Account'].value_counts())
            print(f"New ratio: {self.df['Delinquent_Account'].value_counts()[0] / self.df['Delinquent_Account'].value_counts()[1]:.1f}:1")
            self.smote_applied = True
        
        elif method == 'oversample':
            print("\nApplying random over-sampling...")
            minority_class = self.df[self.df['Delinquent_Account'] == 1]
            majority_class = self.df[self.df['Delinquent_Account'] == 0]
            
            minority_upsampled = minority_class.sample(
                n=len(majority_class),
                replace=True,
                random_state=random_state
            )
            self.df = pd.concat([majority_class, minority_upsampled], ignore_index=True)
            
            print(f"\nAfter over-sampling:")
            print(self.df['Delinquent_Account'].value_counts())
            self.smote_applied = False
        
        print("✓ Class imbalance handled")
        
        return self
    
    def create_quality_report(self):
        """Generate data quality report after cleaning"""
        print("\n" + "="*60)
        print("DATA QUALITY REPORT (AFTER CLEANING)")
        print("="*60)
        
        report = {
            'Total Records': len(self.df),
            'Total Features': len(self.df.columns),
            'Missing Values': self.df.isnull().sum().sum(),
            'Duplicates': self.df.duplicated().sum(),
            'Delinquency Rate': f"{self.df['Delinquent_Account'].mean()*100:.1f}%",
            'Class Balance': f"{(self.df['Delinquent_Account']==0).sum()}:{(self.df['Delinquent_Account']==1).sum()}"
        }
        
        for key, value in report.items():
            print(f"{key:.<40} {value}")
        
        return self
    
    def get_processed_data(self):
        """Return cleaned dataframe"""
        return self.df
    
    def save_processed_data(self, output_path):
        """Save cleaned data to Excel"""
        self.df.to_excel(output_path, index=False)
        print(f"\n✓ Processed data saved to: {output_path}")
        
        return self
    
    def run_full_pipeline(self, handle_imbalance=True, save_path=None):
        """Run complete preprocessing pipeline"""
        print("\n" + "🚀 STARTING FULL PREPROCESSING PIPELINE")
        print("="*60)
        
        (self
         .clean_employment_status()
         .handle_missing_credit_score()
         .handle_missing_income(method='employment_based')
         .handle_missing_loan_balance(method='median')
         .flag_over_limit_customers()
         .engineer_payment_features()
         .identify_weak_features()
        )
        
        if handle_imbalance:
            self.balance_classes(method='smote')
        
        self.create_quality_report()
        
        if save_path:
            self.save_processed_data(save_path)
        
        print("\n" + "="*60)
        print("✓ PREPROCESSING COMPLETE!")
        print("="*60)
        
        return self


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    
    # Example 1: Full pipeline with all defaults
    print("\n" + "🔧 EXAMPLE 1: Full Pipeline")
    preprocessor = DelinquencyDataPreprocessor(
        "/Users/lexiloughlin/Desktop/Delinquency_prediction_dataset.xlsx"
    )
    
    clean_df = (preprocessor
                .run_full_pipeline(
                    handle_imbalance=True,
                    save_path="/Users/lexiloughlin/Desktop/Delinquency_CLEANED.xlsx"
                )
                .get_processed_data())
    
    print("\nCleaned Data Preview:")
    print(clean_df.head())
    print(f"\nShape: {clean_df.shape}")
    
    # ========================================================================
    
    # Example 2: Step-by-step control (for Jupyter notebook)
    """
    from data_preprocessing import DelinquencyDataPreprocessor
    
    preprocessor = DelinquencyDataPreprocessor(
        "/path/to/Delinquency_prediction_dataset.xlsx"
    )
    
    # Clean employment status
    preprocessor.clean_employment_status()
    
    # Handle missing values (different methods)
    preprocessor.handle_missing_income(method='employment_based')
    preprocessor.handle_missing_loan_balance(method='median')
    preprocessor.handle_missing_credit_score()
    
    # Add features
    preprocessor.flag_over_limit_customers()
    preprocessor.engineer_payment_features()
    
    # Handle imbalance
    preprocessor.balance_classes(method='smote')
    
    # Get cleaned data
    clean_df = preprocessor.get_processed_data()
    
    # Save
    preprocessor.save_processed_data("/path/to/output.xlsx")
    """
