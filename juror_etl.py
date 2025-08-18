# juror_etl.py
# Transforms juror_cleaned_output.csv into analysis-ready juror_etl_output.csv

import pandas as pd

df = pd.read_csv("juror_cleaned_output.csv")

# Normalize columns
df.columns = [c.strip() for c in df.columns]

# Add Year and Location from filename
def parse_source(file):
    parts = file.replace(".csv", "").split("_")
    if len(parts) == 2:
        year, loc = parts
        return pd.Series([year, loc])
    return pd.Series([None, None])

df[["Year", "Location"]] = df["Source File"].apply(parse_source)

# Calculate Utilization Rate
df["Utilization Rate"] = df["Jurors Used"] / df["Jurors Reporting"]
df["Utilization Rate"] = df["Utilization Rate"].round(2)

# Reorder columns for clarity
cols = [
    "Case No.",
    "Jurors Reporting",
    "Jurors Not Used",
    "Jurors Used",
    "Utilization Rate",
    "Charge Description",
    "Year",
    "Location",
    "Source File"
]
df = df[cols]

# Save to file
df.to_csv("juror_etl_output.csv", index=False)
print("ETL complete. Output saved to juror_etl_output.csv.")
