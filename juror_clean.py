import pandas as pd
import numpy as np
import os
import re
from datetime import datetime

# Paths
input_folder = "structure_samples"
output_file = "juror_cleaned_output.csv"
log_file = "clean_log.csv"

# Utility: normalize messy headers into consistent text
def _normalize(col: str) -> str:
    c = str(col)
    c = c.replace("’", "'").replace("‐", "-").replace("–", "-").replace("—", "-")
    c = re.sub(r"\s+", " ", c).strip()
    return c

# Column finding helpers
def _find_col(cols, preferences):
    for kind, val in preferences:
        for c in cols:
            if kind == "eq" and c == val:
                return c
            if kind == "startswith" and c.startswith(val):
                return c
            if kind == "contains" and val in c:
                return c
            if kind == "regex" and re.search(val, c):
                return c
    return None

def _find_all_present(cols, preferences):
    found = []
    for pref in preferences:
        c = _find_col(cols, [pref])
        if c and c not in found:
            found.append(c)
    return found

def _consolidate_from_cols(row, colnames):
    for c in colnames:
        val = row.get(c, np.nan)
        if pd.notna(val) and str(val).strip() != "":
            return val
    return np.nan

cleaned_parts = []
log_rows = []

# Patterns for each canonical field
CASE_NO_PREFS = [("eq", "Case No."), ("startswith", "Case No."), ("contains", "Case No")]
JURORS_REPORTING_PREFS = [("eq", "Jurors Reporting"), ("startswith", "Jurors Reporting"), ("contains", "Total Jurors Reporting")]
JURORS_USED_PREFS = [("eq", "Jurors Used"), ("eq", "Used"), ("contains", "Used")]
CASE_TYPE_PREFS = [("eq", "Case Type"), ("contains", "Case Type")]
CIVIL_PREFS = [("eq", "Civil"), ("contains", "Civil")]
CHARGE_PREFS = [("regex", r"Description of Charges"), ("regex", r"\(Charges\)")]
PENAL_PREFS = [("regex", r"Penal Codes")]

# Walk input folder
for fname in sorted(os.listdir(input_folder)):
    if not fname.lower().endswith(".csv"):
        continue

    fpath = os.path.join(input_folder, fname)
    try:
        df = pd.read_csv(fpath, dtype=str, encoding="utf-8", low_memory=False)
    except Exception:
        try:
            df = pd.read_csv(fpath, dtype=str, encoding="latin-1", low_memory=False)
        except Exception as e:
            log_rows.append({"file": fname, "status": "❌ Error opening", "details": str(e)})
            continue

    if df.empty:
        log_rows.append({"file": fname, "status": "⚠️ Empty", "details": "no rows"})
        continue

    # Normalize headers
    original_cols = list(df.columns)
    norm_cols = [_normalize(c) for c in original_cols]
    norm_to_orig = dict(zip(norm_cols, original_cols))
    df.columns = norm_cols

    # Locate required columns
    case_no_col = _find_col(norm_cols, CASE_NO_PREFS)
    jr_col = _find_col(norm_cols, JURORS_REPORTING_PREFS)
    ju_col = _find_col(norm_cols, JURORS_USED_PREFS)
    ct_col = _find_col(norm_cols, CASE_TYPE_PREFS)
    civil_col = _find_col(norm_cols, CIVIL_PREFS)

    missing = [name for name, col in [
        ("Case No.", case_no_col),
        ("Jurors Reporting", jr_col),
        ("Jurors Used", ju_col),
    ] if col is None]

    if missing:
        log_rows.append({
            "file": fname,
            "status": "❌ Missing Columns",
            "details": f"missing {missing}. found headers={norm_cols}"
        })
        continue

    # Consolidate charges and penal codes
    charge_cols = _find_all_present(norm_cols, CHARGE_PREFS)
    penal_cols = _find_all_present(norm_cols, PENAL_PREFS)

    if charge_cols:
        df["Charges"] = df.apply(lambda r: _consolidate_from_cols(r, charge_cols), axis=1)
    else:
        df["Charges"] = np.nan

    if penal_cols:
        df["Penal Codes"] = df.apply(lambda r: _consolidate_from_cols(r, penal_cols), axis=1)

    # Build cleaned view
    out_cols = {
        "Case No.": case_no_col,
        "Jurors Reporting": jr_col,
        "Jurors Used": ju_col,
        "Case Type": ct_col if ct_col else "",
        "Civil": civil_col if civil_col else "",
        "Charges": "Charges",
    }
    if "Penal Codes" in df.columns:
        out_cols["Penal Codes"] = "Penal Codes"

    cleaned = df[[c for c in out_cols.values() if c]].copy()
    rename_map = {v: k for k, v in out_cols.items() if v}
    cleaned.rename(columns=rename_map, inplace=True)

    for num_col in ["Jurors Reporting", "Jurors Used"]:
        if num_col in cleaned.columns:
            cleaned[num_col] = pd.to_numeric(cleaned[num_col], errors="coerce")

    # ➕ Calculate Jurors Not Used
    if "Jurors Reporting" in cleaned.columns and "Jurors Used" in cleaned.columns:
        cleaned["Jurors Not Used"] = cleaned["Jurors Reporting"] - cleaned["Jurors Used"]

    # ➕ Calculate Utilization Rate (%)
    cleaned["Utilization Rate"] = np.where(
        cleaned["Jurors Reporting"] > 0,
        (cleaned["Jurors Used"] / cleaned["Jurors Reporting"]) * 100,
        np.nan
    )
    cleaned["Utilization Rate"] = cleaned["Utilization Rate"].round(1)

    cleaned["Source File"] = fname
    cleaned_parts.append(cleaned)

    log_rows.append({
        "file": fname,
        "status": "✅ Cleaned",
        "details": {
            "rows": int(len(cleaned)),
            "mapped": {
                "Case No.": case_no_col,
                "Jurors Reporting": jr_col,
                "Jurors Used": ju_col,
                "Case Type": ct_col,
                "Civil": civil_col,
                "Charge Cols": charge_cols,
                "Penal Cols": penal_cols,
            }
        }
    })

# Export combined data
if cleaned_parts:
    final_df = pd.concat(cleaned_parts, ignore_index=True)
    final_df["Jurors Not Used"] = pd.to_numeric(final_df["Jurors Not Used"], errors="coerce")
    final_df["Utilization Rate"] = pd.to_numeric(final_df["Utilization Rate"], errors="coerce")
    final_df.to_csv(output_file, index=False)

# Log output
pd.DataFrame(log_rows).to_csv(log_file, index=False)
print(f"Done. Wrote {output_file} and {log_file} at {datetime.now().isoformat(timespec='seconds')}")
