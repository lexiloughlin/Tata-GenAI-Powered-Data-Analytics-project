"""
Practical Examples: How to Use the Delinquency Preprocessing Module

Run this file to see examples of different usage patterns.
"""

import pandas as pd
from data_preprocessing import DelinquencyDataPreprocessor


# =============================================================================
# EXAMPLE 1: Full Pipeline (One-Liner) - RECOMMENDED FOR MOST USERS
# =============================================================================
def example_1_full_pipeline():
    """Run complete preprocessing with one command"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Full Pipeline (Simplest)")
    print("="*70)
    
    preprocessor = DelinquencyDataPreprocessor(
        "/Users/lexiloughlin/Desktop/Delinquency_prediction_dataset.xlsx"
    )
    
    # Everything happens here
    clean_df = (preprocessor
                .run_full_pipeline(
                    handle_imbalance=True,
                    save_path="/Users/lexiloughlin/Desktop/Delinquency_CLEANED.xlsx"
                )
                .get_processed_data())
    
    print(f"\n✓ Done! Shape: {clean_df.shape}")
    print(f"Columns: {list(clean_df.columns)}")
    return clean_df


# =============================================================================
# EXAMPLE 2: Step-by-Step (For Jupyter Notebook / Experimentation)
# =============================================================================
def example_2_step_by_step():
    """Walk through each step individually"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Step-by-Step Control")
    print("="*70)
    
    preprocessor = DelinquencyDataPreprocessor(
        "/Users/lexiloughlin/Desktop/Delinquency_prediction_dataset.xlsx"
    )
    
    # Step 1: Clean categorical data
    print("\nStep 1: Cleaning Employment Status...")
    preprocessor.clean_employment_status()
    
    # Step 2: Handle missing values
    print("\nStep 2: Handling missing values...")
    preprocessor.handle_missing_credit_score()
    preprocessor.handle_missing_income(method='employment_based')
    preprocessor.handle_missing_loan_balance(method='median')
    
    # Step 3: Create features
    print("\nStep 3: Creating new features...")
    preprocessor.flag_over_limit_customers()
    preprocessor.engineer_payment_features()
    
    # Step 4: Balance classes
    print("\nStep 4: Balancing classes...")
    preprocessor.balance_classes(method='smote')
    
    # Step 5: Get results
    clean_df = preprocessor.get_processed_data()
    
    # Step 6: Report
    preprocessor.create_quality_report()
    preprocessor.save_processed_data(
        "/Users/lexiloughlin/Desktop/Delinquency_CLEANED.xlsx"
    )
    
    return clean_df


# =============================================================================
# EXAMPLE 3: No Imbalance Handling (For Comparison)
# =============================================================================
def example_3_without_smote():
    """Preprocessing without class balancing"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Preprocessing WITHOUT SMOTE (for comparison)")
    print("="*70)
    
    preprocessor = DelinquencyDataPreprocessor(
        "/Users/lexiloughlin/Desktop/Delinquency_prediction_dataset.xlsx"
    )
    
    clean_df = (preprocessor
                .run_full_pipeline(
                    handle_imbalance=False,  # Skip SMOTE
                    save_path="/Users/lexiloughlin/Desktop/Delinquency_NO_SMOTE.xlsx"
                )
                .get_processed_data())
    
    print(f"\n✓ Done! Shape: {clean_df.shape} (no SMOTE applied)")
    return clean_df


# =============================================================================
# EXAMPLE 4: Different Imputation Methods
# =============================================================================
def example_4_different_imputation():
    """Compare different missing value imputation approaches"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Trying Different Imputation Methods")
    print("="*70)
    
    # Method 1: Median imputation
    print("\n--- Method 1: Median Imputation ---")
    p1 = DelinquencyDataPreprocessor(
        "/Users/lexiloughlin/Desktop/Delinquency_prediction_dataset.xlsx"
    )
    p1.clean_employment_status()
    p1.handle_missing_income(method='median')
    p1.handle_missing_loan_balance(method='median')
    p1.handle_missing_credit_score()
    p1.engineer_payment_features()
    
    # Method 2: Employment-based imputation
    print("\n--- Method 2: Employment-Based Imputation ---")
    p2 = DelinquencyDataPreprocessor(
        "/Users/lexiloughlin/Desktop/Delinquency_prediction_dataset.xlsx"
    )
    p2.clean_employment_status()
    p2.handle_missing_income(method='employment_based')
    p2.handle_missing_loan_balance(method='median')
    p2.handle_missing_credit_score()
    p2.engineer_payment_features()
    
    # Compare results
    df1 = p1.get_processed_data()
    df2 = p2.get_processed_data()
    
    print(f"\nMedian imputation - Income mean: ${df1['Income'].mean():,.0f}")
    print(f"Employment-based - Income mean: ${df2['Income'].mean():,.0f}")
    
    return df1, df2


# =============================================================================
# EXAMPLE 5: Feature Analysis After Cleaning
# =============================================================================
def example_5_feature_analysis():
    """Analyze the cleaned dataset features"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Feature Analysis")
    print("="*70)
    
    clean_df = pd.read_excel("/Users/lexiloughlin/Desktop/Delinquency_CLEANED.xlsx")
    
    print(f"\nDataset Shape: {clean_df.shape}")
    print(f"\nNew Features Created:")
    new_features = [
        'Payment_Consistency_Score',
        'Late_Payment_Count',
        'Missed_Payment_Count',
        'Total_Problem_Payments',
        'Payment_Deterioration',
        'Over_Credit_Limit'
    ]
    
    for feat in new_features:
        if feat in clean_df.columns:
            print(f"\n  {feat}:")
            if clean_df[feat].dtype in ['float64', 'int64']:
                print(f"    Range: {clean_df[feat].min()} - {clean_df[feat].max()}")
                print(f"    Mean: {clean_df[feat].mean():.3f}")
            else:
                print(f"    Values: {clean_df[feat].unique()}")
    
    print(f"\nCorrelation with Target (Delinquent_Account):")
    corr = clean_df.corr(numeric_only=True)['Delinquent_Account'].sort_values(ascending=False)
    print(corr.head(10))
    
    return clean_df


# =============================================================================
# EXAMPLE 6: Prepare for Model Training
# =============================================================================
def example_6_model_ready():
    """Show data formatted for model training"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Model-Ready Data Preparation")
    print("="*70)
    
    clean_df = pd.read_excel("/Users/lexiloughlin/Desktop/Delinquency_CLEANED.xlsx")
    
    # Remove identifier columns
    df_model = clean_df.drop(['Customer_ID'], axis=1, errors='ignore')
    
    # Optional: Remove weak predictors
    df_model = df_model.drop(['Age', 'Loan_Balance'], axis=1, errors='ignore')
    
    # Optional: Remove original monthly columns (already captured in features)
    monthly_cols = [col for col in df_model.columns if col.startswith('Month_')]
    df_model = df_model.drop(monthly_cols, axis=1, errors='ignore')
    
    # Separate features and target
    X = df_model.drop('Delinquent_Account', axis=1)
    y = df_model['Delinquent_Account']
    
    print(f"\nFeature Matrix (X) Shape: {X.shape}")
    print(f"Target (y) Distribution:\n{y.value_counts()}")
    print(f"\nFeatures Ready for Modeling:")
    for i, col in enumerate(X.columns, 1):
        dtype = X[col].dtype
        print(f"  {i:2d}. {col:.<40} ({dtype})")
    
    # Show train/test split example
    from sklearn.model_selection import train_test_split
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTrain/Test Split (80/20 stratified):")
    print(f"  Train: {X_train.shape[0]} samples")
    print(f"  Test:  {X_test.shape[0]} samples")
    print(f"  Features: {X_train.shape[1]}")
    
    return X, y


# =============================================================================
# EXAMPLE 7: Quality Comparison (Before vs After)
# =============================================================================
def example_7_before_after_comparison():
    """Show what changed with preprocessing"""
    print("\n" + "="*70)
    print("EXAMPLE 7: Before vs After Comparison")
    print("="*70)
    
    original = pd.read_excel(
        "/Users/lexiloughlin/Desktop/Delinquency_prediction_dataset.xlsx"
    )
    cleaned = pd.read_excel(
        "/Users/lexiloughlin/Desktop/Delinquency_CLEANED.xlsx"
    )
    
    print("\nORIGINAL DATA:")
    print(f"  Shape: {original.shape}")
    print(f"  Missing values: {original.isnull().sum().sum()}")
    print(f"  Duplicate rows: {original.duplicated().sum()}")
    print(f"  Delinquency rate: {original['Delinquent_Account'].mean()*100:.1f}%")
    print(f"  Class balance: {(original['Delinquent_Account']==0).sum()}:{(original['Delinquent_Account']==1).sum()}")
    
    print("\nCLEANED DATA:")
    print(f"  Shape: {cleaned.shape}")
    print(f"  Missing values: {cleaned.isnull().sum().sum()}")
    print(f"  Duplicate rows: {cleaned.duplicated().sum()}")
    print(f"  Delinquency rate: {cleaned['Delinquent_Account'].mean()*100:.1f}%")
    print(f"  Class balance: {(cleaned['Delinquent_Account']==0).sum()}:{(cleaned['Delinquent_Account']==1).sum()}")
    
    new_features = set(cleaned.columns) - set(original.columns)
    print(f"\nNEW FEATURES ADDED ({len(new_features)}):")
    for feat in sorted(new_features):
        print(f"  + {feat}")


# =============================================================================
# MAIN: Run All Examples
# =============================================================================
if __name__ == "__main__":
    
    # Uncomment the examples you want to run
    
    # SIMPLEST - Use this for production
    clean_df = example_1_full_pipeline()
    
    # For understanding the process
    # clean_df = example_2_step_by_step()
    
    # For comparison
    # clean_no_smote = example_3_without_smote()
    
    # For experimentation
    # df_median, df_employment = example_4_different_imputation()
    
    # For analysis
    # example_5_feature_analysis()
    
    # For model training
    # X, y = example_6_model_ready()
    
    # For documentation
    # example_7_before_after_comparison()
    
    print("\n" + "="*70)
    print("✓ Examples complete! Your cleaned data is ready.")
    print("="*70)
