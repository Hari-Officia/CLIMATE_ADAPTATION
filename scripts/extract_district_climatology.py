"""
Extract historical climatological baselines (2010-2026) for all 38 Tamil Nadu districts.
Reads historical NASA POWER CSVs from ClimateData/ and computes:
- Monthly average and standard deviation for temp_max, temp_min, rainfall, soil_wetness, humidity, wind_speed
- Annual averages for SPI baseline estimates
Saves dictionary to data/feature_mappings/district_climatology.json
"""
import os
import json
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "ClimateData")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "feature_mappings", "district_climatology.json")

def extract_climatology():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    climatology = {}

    csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
    print(f"Found {len(csv_files)} district CSV files in {DATA_DIR}")

    for file_name in sorted(csv_files):
        district_name = file_name.replace(".csv", "")
        file_path = os.path.join(DATA_DIR, file_name)

        try:
            # NASA POWER CSVs have 17 header lines before table
            df = pd.read_csv(file_path, skiprows=17)

            # Check required columns
            # YEAR, DOY, T2M_RANGE, T2M_MAX, T2M_MIN, RH2M, WS2M, PS, ALLSKY_SFC_SW_DWN, GWETROOT, PRECTOTCORR
            # Clean missing values (-999)
            for col in ["T2M_MAX", "T2M_MIN", "RH2M", "WS2M", "GWETROOT", "PRECTOTCORR"]:
                if col in df.columns:
                    df[col] = df[col].replace(-999, np.nan)

            # Compute approximate month from DOY (1 to 366)
            # DOY 1-31 (Jan), 32-59 (Feb), 60-90 (Mar), etc.
            # Using pandas date reconstruction
            # Year and DOY to month
            df["month"] = pd.to_datetime(df["YEAR"].astype(str) + df["DOY"].astype(str).str.zfill(3), format="%Y%j").dt.month

            # Calculate monthly statistics
            monthly_stats = {}
            for month in range(1, 13):
                m_df = df[df["month"] == month]
                monthly_stats[str(month)] = {
                    "temp_max_mean": round(float(m_df["T2M_MAX"].mean()), 2) if not m_df["T2M_MAX"].empty else 32.0,
                    "temp_max_std": round(float(m_df["T2M_MAX"].std()), 2) if not m_df["T2M_MAX"].empty else 2.5,
                    "temp_min_mean": round(float(m_df["T2M_MIN"].mean()), 2) if not m_df["T2M_MIN"].empty else 23.0,
                    "temp_mean_mean": round(float(((m_df["T2M_MAX"] + m_df["T2M_MIN"]) / 2).mean()), 2) if not m_df["T2M_MAX"].empty else 27.5,
                    "rainfall_mean": round(float(m_df["PRECTOTCORR"].mean()), 2) if not m_df["PRECTOTCORR"].empty else 2.5,
                    "rainfall_std": round(float(m_df["PRECTOTCORR"].std()), 2) if not m_df["PRECTOTCORR"].empty else 5.0,
                    "humidity_mean": round(float(m_df["RH2M"].mean()), 2) if "RH2M" in m_df else 70.0,
                    "wind_speed_mean": round(float(m_df["WS2M"].mean()), 2) if "WS2M" in m_df else 3.0,
                    "soil_wetness_mean": round(float(m_df["GWETROOT"].mean()), 3) if "GWETROOT" in m_df else 0.5,
                }

            # Overall district normals
            overall_stats = {
                "temp_max_mean": round(float(df["T2M_MAX"].mean()), 2),
                "temp_min_mean": round(float(df["T2M_MIN"].mean()), 2),
                "rainfall_daily_mean": round(float(df["PRECTOTCORR"].mean()), 2),
                "rainfall_daily_std": round(float(df["PRECTOTCORR"].std()), 2),
                "humidity_mean": round(float(df["RH2M"].mean()), 2) if "RH2M" in df else 70.0,
                "wind_speed_mean": round(float(df["WS2M"].mean()), 2) if "WS2M" in df else 3.0,
                "soil_wetness_mean": round(float(df["GWETROOT"].mean()), 3) if "GWETROOT" in df else 0.5,
                "annual_rainfall_mm": round(float(df["PRECTOTCORR"].mean() * 365.25), 1)
            }

            climatology[district_name] = {
                "district_name": district_name,
                "district_id": district_name.lower(),
                "overall": overall_stats,
                "monthly": monthly_stats
            }
            print(f"Processed climatology for {district_name}")

        except Exception as e:
            print(f"Error processing {file_name}: {e}")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(climatology, f, indent=2)

    print(f"Successfully generated climatology baseline for {len(climatology)} districts -> {OUTPUT_PATH}")

if __name__ == "__main__":
    extract_climatology()
