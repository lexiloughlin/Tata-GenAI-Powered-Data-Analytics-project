"""
Verification Script - Confirms all preprocessing tools are working correctly
Run this to validate the setup
"""

import os
import sys

print("\n" + "="*70)
print("PREPROCESSING TOOLKIT VERIFICATION")
print("="*70)

# Check 1: Required files
print("\n1. Checking files...")
files_to_check = [
    'data_preprocessing.py',
    'QUICK_START.md',
    'PREPROCESSING_GUIDE.md',
    'USAGE_EXAMPLES.py',
    'delinquency_preprocessing.ipynb'
]

all_files_exist = True
for file in files_to_check:
    exists = os.path.exists(file)
    status = "✓" if exists else "✗"
    print(f"  {status} {file}")
    if not exists:
        all_files_exist = False

if all_files_exist:
    print("  ✓ All files present!")
else:
    print("  ✗ Some files missing!")
    sys.exit(1)

# Check 2: Dependencies
print("\n2. Checking dependencies...")
dependencies = {
    'pandas': 'Data manipulation',
    'openpyxl': 'Excel file handling',
    'sklearn': 'Machine learning tools',
    'imblearn': 'Class balancing (SMOTE)',
    'numpy': 'Numerical computing'
}

all_deps_available = True
for package, description in dependencies.items():
    try:
        __import__(package)
        print(f"  ✓ {package:.<30} {description}")
    except ImportError:
        print(f"  ✗ {package:.<30} NOT INSTALLED")
        all_deps_available = False

if not all_deps_available:
    print("\n  Install missing packages with:")
    print("  pip install pandas openpyxl scikit-learn imbalanced-learn numpy")
    sys.exit(1)

# Check 3: Module import
print("\n3. Checking module import...")
try:
    from data_preprocessing import DelinquencyDataPreprocessor
    print("  ✓ Successfully imported DelinquencyDataPreprocessor")
except ImportError as e:
    print(f"  ✗ Failed to import: {e}")
    sys.exit(1)

# Check 4: Data file
print("\n4. Checking data file...")
data_file = "/Users/lexiloughlin/Desktop/Delinquency_prediction_dataset.xlsx"
if os.path.exists(data_file):
    print(f"  ✓ Data file found: {data_file}")
else:
    print(f"  ✗ Data file NOT found: {data_file}")
    print("  Make sure Delinquency_prediction_dataset.xlsx is on your Desktop")

# Check 5: Quick test
print("\n5. Running quick test...")
try:
    import pandas as pd
    preprocessor = DelinquencyDataPreprocessor(data_file)
    print("  ✓ Successfully loaded dataset")
    print(f"    Shape: {preprocessor.df.shape}")
    print(f"    Missing values: {preprocessor.df.isnull().sum().sum()}")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Success
print("\n" + "="*70)
print("✓ ALL CHECKS PASSED!")
print("="*70)

print("\nYou're ready to preprocess your data!")
print("\nQuick start:")
print("  from data_preprocessing import DelinquencyDataPreprocessor")
print("  preprocessor = DelinquencyDataPreprocessor('/path/to/file.xlsx')")
print("  clean_df = preprocessor.run_full_pipeline(handle_imbalance=True).get_processed_data()")

print("\nFor more help:")
print("  - Read: QUICK_START.md")
print("  - Detailed: PREPROCESSING_GUIDE.md")
print("  - Examples: USAGE_EXAMPLES.py")
print("\n")
