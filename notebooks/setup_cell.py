# Shared setup cell. Paste into the first cell of a notebook and run it first, every session.
# Expected printed checks: (605, 62) / 50 / 15 35 / 33 27 5
import os
import numpy as np
import pandas as pd

# 1. Load the data (repo copy when cloned, otherwise straight from GitHub)
RAW_URL = 'https://raw.githubusercontent.com/shrfr/nafld-fibrosis-prediction/main/data/NAFLD.xlsx'
local_candidates = ['data/NAFLD.xlsx', '../data/NAFLD.xlsx']
path = next((p for p in local_candidates if os.path.exists(p)), RAW_URL)
df = pd.read_excel(path, sheet_name='Sheet1')
print('Loaded from:', path, df.shape)                     # expect (605, 62)

# 2. Working copy with short names for the biopsy-derived columns
data = df.copy().rename(columns={
    'Significant Fibrosis (No=0, Yes=1) (If Fibrosis 2 and above, there is Significant Fibrosis)': 'SigFibrosis',
    'Advanced Fibrosis (No=0, Yes=1) (If Fibrosis is 3 and above, there is Advanced Fibrosis)': 'AdvFibrosis',
    'NAS score>=4 and Fibrosis>=2 (If NAS score>=4 and Fibrosis>=2 = 1, If not = 0)': 'AtRiskNASH',
    'Cirrhosis (No=0, Yes=1) (If Fibrosis is 4, there is Cirrhosis)': 'Cirrhosis',
    'Fibrosis status (No=0, Yes=1) (Fibrosis 1 and above, there is Fibrosis)': 'FibrosisStatus',
    'NAS score according to Kleiner': 'NAS',
    'Diagnosis according to SAF (NASH=1, NAFL=2)': 'SAF_Diagnosis',
    'Type of Disease (Mild illness=1, Severe illness=2)': 'TypeOfDisease'})

# 3. Recomputed / derived targets
data['AtRiskNASH_calc'] = ((data['NAS'] >= 4) & (data['Fibrosis'] >= 2)).astype(int)
data['FibGroup'] = np.select([data['Fibrosis'] <= 1, data['Fibrosis'] == 2], [0, 1], default=2)

# 4. Leakage list and candidate features
biopsy_cols = ['Steatosis', 'Activity', 'Fibrosis', 'NAS', 'AtRiskNASH', 'AtRiskNASH_calc', 'FibrosisStatus',
               'SigFibrosis', 'AdvFibrosis', 'Cirrhosis', 'SAF_Diagnosis', 'TypeOfDisease', 'FibGroup']
feature_cols = [c for c in data.columns if c not in biopsy_cols + ['Patient No.']]
print(len(feature_cols))                                  # expect 50

# 5. Drop sparse columns (missing 45% or more; see the EDA handover for why)
miss = data[feature_cols].isna().mean()
drop_sparse = miss[miss > 0.45].index.tolist()
model_features = [c for c in feature_cols if c not in drop_sparse]
print(len(drop_sparse), len(model_features))              # expect 15, 35

# 6. Helper columns (created AFTER feature_cols so they never become features)
panel = ['INR', 'BUN', 'Creatinine', 'TSH', 'Ceruloplasmin', 'Insulin', 'Uric Acid']
data['n_panel'] = data[panel].notna().sum(axis=1)
data['in_panel'] = (data['n_panel'] >= 5).astype(int)
data['FIB4'] = (data['Age'] * data['AST']) / (data['Trombosit'] * np.sqrt(data['ALT']))

# 7. Optional: fix the 3 rows where BMI disagrees with height and weight
data['Body Mass Index'] = (data['Weight'] / (data['Height'] / 100) ** 2).round(1)

# 8. Final model inputs
SEED = 42
smoke = 'Smoking Status (Never Smoked=1, Left Smoking=2, Smoking=3)'
cat_like = [c for c in model_features if data[c].nunique() <= 3]
feats = [c for c in model_features if c not in ['Height', 'Weight']]
bin_cols = [c for c in cat_like if c in feats and c != smoke]
num_feats = [c for c in feats if c not in bin_cols + [smoke]]
print(len(feats), len(num_feats), len(bin_cols))          # expect 33, 27, 5

X, y = data[feats], data['SigFibrosis']
strata = y.astype(str) + '_' + data['in_panel'].astype(str)
