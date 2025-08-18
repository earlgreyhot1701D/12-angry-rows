# juror_clean.py
import os
import pandas as pd
import numpy as np

input_dir = "structure_samples"
output_file = "juror_cleaned_output.csv"
log_file = "clean_log.csv"

def clean_column_name(col):
    if pd.isnull(col):
        return ""
    return str(col).strip().lower()

def find_column(columns, keywords):
    for col in columns:
        if any(k in col for k in keywords):
            return col
    return None

all_data = []
log_entries = []

for filename in os.listdir(input_dir):
    if not filename.endswith(".csv"):
        continue

    filepath = os.path.join(input_dir, filename)
    df = pd.read_csv(filepath)

    columns = [clean_column_name(col) for col in df.columns]
    df.columns = columns

    case_no_col = find_column(columns, ["case"])
    reporting_col = find_column(columns, ["jurors reporting", "reporting"])
    not_used_col = find_column(columns, ["not used", "not used from pool", "unused"])
    went_trial_col = find_column(columns, ["went to trial", "went", "trial"])
    not_trial_col = find_column(columns, ["did not go to trial", "didn't go", "didn’t go"])

    if not case_no_col or not reporting_col:
        log_entries.append(f"{filename},SKIPPED,Missing required columns")
        continue

    df["Jurors Reporting"] = pd.to_numeric(df[reporting_col], errors="coerce")

    if not_used_col:
        df["Jurors Not Used"] = pd.to_numeric(df[not_used_col], errors="coerce")
        df["Jurors Used"] = df["Jurors Reporting"] - df["Jurors Not Used"]
    else:
        df["Jurors Used"] = np.nan
        df["Jurors Not Used"] = np.nan

    df["Charge Description"] = df[went_trial_col].fillna("") + " | " + df[not_trial_col].fillna("")
    df["Source File"] = filename

    output_df = df[[
        case_no_col,
        "Jurors Reporting",
        "Jurors Used",
        "Jurors Not Used",
        "Charge Description",
        "Source File"
    ]].copy()

    output_df.rename(columns={case_no_col: "Case No."}, inplace=True)

    # 🧼 DROP incomplete rows
    output_df = output_df.dropna(subset=["Case No.", "Jurors Reporting"])

    all_data.append(output_df)
    log_entries.append(f"{filename},OK,Processed")

combined = pd.concat(all_data, ignore_index=True)
combined.to_csv(output_file, index=False)

with open(log_file, "w") as f:
    f.write("Filename,Status,Message\n")
    for entry in log_entries:
        f.write(entry + "\n")

print(f"Cleaning complete. Output saved to {output_file}.")



