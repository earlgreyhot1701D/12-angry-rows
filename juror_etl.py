import pandas as pd

# Load the cleaned Frankenstein output
df = pd.read_csv("juror_cleaned_output.csv")

# Normalize column names
df.columns = [c.strip() for c in df.columns]

# Extract Year and Location from "Source File"
def parse_source(file):
    parts = str(file).replace(".csv", "").split("_")
    if len(parts) == 2:
        year, loc = parts
        return pd.Series([year, loc])
    return pd.Series([None, None])

df[["Year", "Location"]] = df["Source File"].apply(parse_source)

# Drop rows with missing critical values
df = df.dropna(subset=["Case No.", "Jurors Reporting", "Jurors Not Used"])

# Convert numeric fields
df["Jurors Reporting"] = pd.to_numeric(df["Jurors Reporting"], errors="coerce")
df["Jurors Not Used"] = pd.to_numeric(df["Jurors Not Used"], errors="coerce")

# Calculate Jurors Used (Calculated)
df["Jurors Used (Calculated)"] = df["Jurors Reporting"] - df["Jurors Not Used"]

# Optional: compare to any existing "Jurors Used" column from source
used_source_col = None
for col in df.columns:
    if col.lower().strip() in ["jurors used", "used"]:
        used_source_col = col
        break

if used_source_col:
    df["Jurors Used (Source)"] = pd.to_numeric(df[used_source_col], errors="coerce")
    df["Used Mismatch?"] = df["Jurors Used (Source)"] != df["Jurors Used (Calculated)"]
else:
    df["Jurors Used (Source)"] = ""
    df["Used Mismatch?"] = ""

# Calculate Utilization Rate
df["Utilization Rate"] = (df["Jurors Used (Calculated)"] / df["Jurors Reporting"]).round(4)

# Add Case Category if missing
if "Case Category" not in df.columns:
    df["Case Category"] = ""

# Ensure required final columns exist
final_cols = [
    "Case No.",
    "Jurors Reporting",
    "Jurors Not Used",
    "Jurors Used (Calculated)",
    "Jurors Used (Source)",
    "Used Mismatch?",
    "Utilization Rate",
    "Case Type",
    "Civil",
    "Case Category",
    "Charges",
    "Penal Codes",
    "Year",
    "Location",
    "Source File"
]

for col in final_cols:
    if col not in df.columns:
        df[col] = ""

# Reorder and export
df = df[final_cols]
df.to_csv("juror_etl_output.csv", index=False)

print("ETL complete. Output saved to juror_etl_output.csv.")
