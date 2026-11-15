import os
import glob
import json
import csv
import hashlib
import joblib
import pandas as pd
import numpy as np

from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    brier_score_loss,
    log_loss,
    matthews_corrcoef,
    confusion_matrix
)

base_dir = r"c:\Users\haris\OneDrive\Desktop\PROJECT_DATA"

# 1. Load Raw Climate Dataset
files = sorted(glob.glob(os.path.join(base_dir, 'ClimateData', '*.csv')))
dfs = []
for f in files:
    dname = os.path.basename(f).replace('.csv', '').lower()
    if dname == 'nilgris': dname = 'nilgiris'
    if dname == 'thirupathur': dname = 'tirupathur'
    df = pd.read_csv(f, skiprows=17)
    df['district'] = dname
    dfs.append(df)

df_raw = pd.concat(dfs, ignore_index=True)
df_raw['date'] = pd.to_datetime(df_raw['YEAR'].astype(str) + df_raw['DOY'].astype(str).str.zfill(3), format='%Y%j')
df_raw = df_raw.sort_values(['date', 'district']).reset_index(drop=True)

# 2. Rename features to match training contract
df_raw['temp_max'] = df_raw['T2M_MAX']
df_raw['temp_min'] = df_raw['T2M_MIN']
df_raw['temp_mean'] = (df_raw['temp_max'] + df_raw['temp_min']) / 2.0
df_raw['temp_range'] = df_raw['T2M_RANGE']
df_raw['humidity'] = df_raw['RH2M']
df_raw['wind_speed'] = df_raw['WS2M']
df_raw['rainfall'] = df_raw['PRECTOTCORR']
df_raw['soil_wetness'] = df_raw['GWETROOT']

# 3. Rolling rainfall features per district
df_raw['rainfall_3d'] = df_raw.groupby('district')['rainfall'].transform(lambda x: x.rolling(3, min_periods=1).sum())
df_raw['rainfall_7d'] = df_raw.groupby('district')['rainfall'].transform(lambda x: x.rolling(7, min_periods=1).sum())
df_raw['rainfall_30d'] = df_raw.groupby('district')['rainfall'].transform(lambda x: x.rolling(30, min_periods=1).sum())

# 4. Temperature & rainfall anomalies
df_raw['month'] = df_raw['date'].dt.month
d_temp_mean = df_raw.groupby(['district', 'month'])['temp_max'].transform('mean')
df_raw['temp_anomaly'] = df_raw['temp_max'] - d_temp_mean

d_rain_mean = df_raw.groupby(['district', 'month'])['rainfall'].transform('mean')
df_raw['rainfall_anomaly'] = df_raw['rainfall'] - d_rain_mean
df_raw['rainfall_anomaly'] = df_raw['rainfall_anomaly'].fillna(0.0)

# 5. Standardized Precipitation Index (SPI_3, SPI_6 approximation)
# SPI_3 = (rainfall_30d - mean) / std
d_r30_mean = df_raw.groupby('district')['rainfall_30d'].transform('mean')
d_r30_std = df_raw.groupby('district')['rainfall_30d'].transform('std').replace(0, 1.0)
df_raw['SPI_3'] = (df_raw['rainfall_30d'] - d_r30_mean) / d_r30_std

df_raw['rainfall_180d'] = df_raw.groupby('district')['rainfall'].transform(lambda x: x.rolling(180, min_periods=1).sum())
d_r180_mean = df_raw.groupby('district')['rainfall_180d'].transform('mean')
d_r180_std = df_raw.groupby('district')['rainfall_180d'].transform('std').replace(0, 1.0)
df_raw['SPI_6'] = (df_raw['rainfall_180d'] - d_r180_mean) / d_r180_std

# 6. Targets
df_raw['flood'] = ((df_raw['rainfall_3d'] >= 100.0) | (df_raw['rainfall'] >= 70.0)).astype(int)
df_raw['heatwave'] = ((df_raw['temp_max'] >= 40.0) | (df_raw['temp_anomaly'] >= 4.5)).astype(int)
df_raw['drought'] = ((df_raw['SPI_3'] <= -1.0) | (df_raw['SPI_6'] <= -1.0)).astype(int)

# 7. One-hot district encoding
df_ml = pd.get_dummies(df_raw, columns=['district'], dtype=int)

# Standardize column casing for district one-hot
# Model expects: district_Ariyalur, district_Chengalpattu, etc.
district_cols = [c for c in df_ml.columns if c.startswith('district_')]
rename_map = {}
for c in district_cols:
    d_clean = c.replace('district_', '').lower()
    # capitalize proper name
    d_proper = d_clean.capitalize()
    if d_clean == 'kallakurichi': d_proper = 'Kallakurichi'
    if d_clean == 'kancheepuram': d_proper = 'Kancheepuram'
    if d_clean == 'kanniyakumari': d_proper = 'Kanniyakumari'
    if d_clean == 'mayiladuthurai': d_proper = 'Mayiladuthurai'
    if d_clean == 'nagapattinam': d_proper = 'Nagapattinam'
    if d_clean == 'ramanathapuram': d_proper = 'Ramanathapuram'
    if d_clean == 'tiruchirappalli': d_proper = 'Tiruchirappalli'
    if d_clean == 'tirunelveli': d_proper = 'Tirunelveli'
    if d_clean == 'tirupathur': d_proper = 'Tirupathur'
    if d_clean == 'tiruppur': d_proper = 'Tiruppur'
    if d_clean == 'tiruvallur': d_proper = 'Tiruvallur'
    if d_clean == 'tiruvannamalai': d_proper = 'Tiruvannamalai'
    if d_clean == 'tiruvarur': d_proper = 'Tiruvarur'
    if d_clean == 'viluppuram': d_proper = 'Viluppuram'
    if d_clean == 'virudhunagar': d_proper = 'Virudhunagar'
    rename_map[c] = f"district_{d_proper}"

df_ml = df_ml.rename(columns=rename_map)

print('Constructed df_ml shape:', df_ml.shape)

# Load saved models
models = {
    'flood': joblib.load(os.path.join(base_dir, 'Models', 'flood_xgboost.pkl')),
    'drought': joblib.load(os.path.join(base_dir, 'Models', 'drought_xgboost.pkl')),
    'heatwave': joblib.load(os.path.join(base_dir, 'Models', 'heatwave_xgboost.pkl'))
}

# Create predictions directory
os.makedirs(os.path.join(base_dir, 'verified_predictions'), exist_ok=True)

# Splits definition matching notebook
splits = {
    'flood_val': df_ml[(df_ml['date'] >= '2018-01-01') & (df_ml['date'] < '2020-01-01')].copy(),
    'flood_test': df_ml[(df_ml['date'] >= '2020-01-01') & (df_ml['date'] < '2023-01-01')].copy(),
    'drought_test': df_ml[df_ml['date'] >= '2024-01-01'].copy(),
    'heatwave_test': df_ml[df_ml['date'] >= '2024-01-01'].copy()
}

metrics_verif_rows = []

for m_name in ['flood', 'drought', 'heatwave']:
    model = models[m_name]
    feature_names = list(model.feature_names_in_)
    
    # Check split
    if m_name == 'flood':
        eval_splits = [('Validation Set', splits['flood_val']), ('Test Set', splits['flood_test'])]
    elif m_name == 'drought':
        eval_splits = [('Test Set', splits['drought_test'])]
    else:
        eval_splits = [('Test Set', splits['heatwave_test'])]
    
    for split_name, eval_df in eval_splits:
        X_eval = eval_df.reindex(columns=feature_names, fill_value=0)
        y_true = eval_df[m_name].values
        
        y_prob = model.predict_proba(X_eval)[:, 1]
        y_pred = (y_prob >= 0.5).astype(int)
        
        # Save verified predictions CSV
        pred_df = pd.DataFrame({
            'row_index': eval_df.index,
            'date': eval_df['date'].dt.strftime('%Y-%m-%d'),
            'y_true': y_true,
            'y_pred': y_pred,
            'y_probability': y_prob
        })
        pred_path = os.path.join(base_dir, 'verified_predictions', f'{m_name}_{split_name.lower().replace(" ", "_")}_predictions.csv')
        pred_df.to_csv(pred_path, index=False)
        print(f'Saved raw predictions to {pred_path}')
        
        # Compute exact metrics
        cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
        tn, fp, fn, tp = cm.ravel()
        
        acc = accuracy_score(y_true, y_pred)
        bal_acc = balanced_accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, zero_division=0)
        rec = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
        roc = roc_auc_score(y_true, y_prob) if len(np.unique(y_true)) > 1 else 0.0
        pr_auc = average_precision_score(y_true, y_prob) if len(np.unique(y_true)) > 1 else 0.0
        brier = brier_score_loss(y_true, y_prob)
        lloss = log_loss(y_true, y_prob)
        mcc = matthews_corrcoef(y_true, y_pred)
        
        prev = y_true.mean()
        
        print(f"\n==========================================")
        print(f"VERIFIED {m_name.upper()} ({split_name}) METRICS")
        print(f"==========================================")
        print(f"N: {len(y_true)}, Pos: {tp+fn}, Neg: {tn+fp}, Prev: {prev*100:.4f}%")
        print(f"Confusion Matrix: TN={tn}, FP={fp}, FN={fn}, TP={tp}")
        print(f"Accuracy: {acc:.5f}")
        print(f"Balanced Accuracy: {bal_acc:.5f}")
        print(f"Precision: {prec:.5f}")
        print(f"Recall: {rec:.5f}")
        print(f"F1-Score: {f1:.5f}")
        print(f"Specificity: {spec:.5f}")
        print(f"ROC-AUC: {roc:.5f}")
        print(f"PR-AUC: {pr_auc:.5f}")
        print(f"Brier Score: {brier:.5f}")
        print(f"Log Loss: {lloss:.5f}")
        print(f"MCC: {mcc:.5f}")

print("\n>>> ALL FORENSIC METRICS RECOMPUTED SUCCESSFULLY <<<")
