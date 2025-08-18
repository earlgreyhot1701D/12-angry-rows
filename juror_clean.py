# juror_clean.py
# Processes structure_samples/*.csv and generates juror_cleaned_output.csv with correct "Jurors Used"

import os
import re
import pandas as pd
import numpy as np

input_folder = "structure_samples"
output_file = "juror_cleaned_output.csv"
log_file = "clean_log.csv"

# Helpers
def _normalize(col):
    c = str(col)
    c = c.replace("’", "'").replace("‐", "-").replace("–", "-").replace("—", "-")
    c = re.sub(r"\s+", " ", c).strip()
    return c

def _find_col(cols, options):
    for opt in options:
        for c in cols:
            if opt in c:
                return c
    return None

def _consolidate_from_cols(row, colnames):
    for c in colnames:
        val = row.get(c, np.nan)
        if pd.notna(val) and str(val).strip() != "":
            return val
    return np.nan

# Start cleaning
cleaned_parts = []
log = []

for fname in sorted(os.listdir(input_folder)):
    if not fname.endswith(".csv"):
        continue

    fpath = os.path.join(input_folder, fname)
    try:
        df = pd.read_csv(fpath, dtype=str, encoding="utf-8", low_memory=False)
    except:
        try:
            df = pd.read_csv(fpath, dtype=str, encoding="latin-1", low_memory=False)
        except Exception as e:
            log.append({"file": fname, "status": "❌ Error opening", "details": str(e)})
            continue

    if df.empty:
        log.append({"file": fname, "status": "⚠️ Empty", "details": "no rows"})
        continue

    df.columns = [_normalize(c) for c in df.columns]

    # Find required columns
    case_no_col = _find_col(df.columns, ["Case No"])
    reporting_col = _find_col(df.columns, ["Total Jurors Reporting", "Jurors Reporting"])
    not_used_col = _find_col(df.columns, ["Not Used", "Not Used From Pool", "Unused"])
    case_type_col = _find_col(df.columns, ["Case Type"])
    civil_col = _find_col(df.columns, ["Civil"])
    charge_cols = [c for c in df.columns if "Description of Charges" in c or "(Charges)" in c]
    penal_cols = [c for c in df.columns if "Penal Code" in c or "Penal Codes" in c]

    if not case_no_col or not reporting_col:
        log.append({"file": fname, "status": "❌ Missing", "details": f"case_no={case_no_col}, reporting={reporting_col}"})
        continue

    # Calculate Jurors Used
    df["Jurors Reporting"] = pd.to_numeric(df[reporting_col], errors="coerce")
    df["Not Used"] = pd.to_numeric(df.get(not_used_col, np.nan), errors="coerce")

    if "Not Used" in df:
        df["Jurors Used"] = df["Jurors Reporting"] - df["Not Used"]
    else:
        df["Jurors Used"] = np.nan  # Leave blank if "Not Used" column isn't present

    # Get charges and penal codes
    df["Charges"] = df.apply(lambda r: _consolidate_from_cols(r, charge_cols), axis=1) if charge_cols else np.nan
    df["Penal Codes"] = df.apply(lambda r: _consolidate_from_cols(r, penal_cols), axis=1) if penal_cols else np.nan

    # Collect final columns
    output = pd.DataFrame({
        "Case No.": df[case_no_col],
        "Jurors Reporting": df["Jurors Reporting"],
        "Jurors Used": df["Jurors Used"],
        "Case Type": df[case_type_col] if case_type_col else "",
        "Civil": df[civil_col] if civil_col else "",
        "Charges": df["Charges"],
        "Penal Codes": df["Penal Codes"],
        "Source File": fname
    })

    cleaned_parts.append(output)

    log.append({
        "file": fname,
        "status": "✅ Cleaned",
        "details": {
            "rows": len(output),
            "used_formula": f"{reporting_col} - {not_used_col if not_used_col else '???'}"
        }
    })

# Final output
if cleaned_parts:
    all_cleaned = pd.concat(cleaned_parts, ignore_index=True)
    all_cleaned.to_csv(output_file, index=False)

pd.DataFrame(log).to_csv(log_file, index=False)
print(f"Done. Output written to {output_file} and {log_file}")
