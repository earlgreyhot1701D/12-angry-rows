# juror_etl.py
# Transforms juror_cleaned_output.csv into analysis-ready juror_etl_output.csv

import pandas as pd
import numpy as np
import re

INPUT_FILE = "juror_cleaned_output.csv"
OUTPUT_FILE = "juror_etl_output.csv"

def classify_case(row):
    civil_raw = str(row.get("Civil", "")).strip().lower()
    ct_raw = str(row.get("Case Type", "")).strip().lower()
    if civil_raw in {"y", "yes", "true", "1"} or "civil" in ct_raw:
        return "Civil"
    if any(k in ct_raw for k in ["felony", "fel", "f "]) or ct_raw == "f":
        return "Felony"
    if any(k in ct_raw for k in ["misdemeanor", "misd", "m "]) or ct_raw == "m":
        return "Misdemeanor"
    return "Unknown"

def clean_charges(x):
    if pd.isna(x): return x
    s = str(x).strip()
    if s.startswith("[") and s.endswith("]"): s = s[1:-1]
    return re.sub(r'["\']', "", s.strip())

def main():
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"❌ Error: {INPUT_FILE} not found.")
        return

    # Drop fully blank rows
    df = df[~(df["Case No."].isna() & df["Jurors Reporting"].isna() & df["Jurors Used"].isna())].copy()

    # Fix numeric types
    df["Jurors Reporting"] = pd.to_numeric(df["Jurors Reporting"], errors="coerce")
    df["Jurors Used"] = pd.to_numeric(df["Jurors Used"], errors="coerce")

    # Classification + Utilization
    df["Case Category"] = df.apply(classify_case, axis=1)
    valid = (df["Jurors Reporting"] > 0) & df["Jurors Used"].notna()
    df["Utilization Rate"] = np.where(valid, df["Jurors Used"] / df["Jurors Reporting"], np.nan)
    df["Utilization Rate"] = df["Utilization Rate"].round(4)

    # Clean up charges
    if "Charges" in df.columns:
        df["Charges"] = df["Charges"].apply(clean_charges)

    # Extract Year and Location
    df["Year"] = df["Source File"].str.extract(r"^(\d{4})")[0]
    df["Location"] = df["Source File"].str.extract(r"_(\w+)\.")[0]

    # Reorder
    cols = ["Case No.", "Jurors Reporting", "Jurors Used", "Utilization Rate",
            "Case Type", "Civil", "Case Category", "Charges", "Penal Codes",
            "Year", "Location", "Source File"]
    cols_present = [c for c in cols if c in df.columns]
    df = df[cols_present]

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ ETL complete. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
