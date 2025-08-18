import pandas as pd
import os
import re

INPUT_FILE = "juror_master.xlsx"
OUTPUT_FOLDER = "structure_samples"
LOG_FILE = "structure_log.csv"

REQUIRED_KEYWORDS = ['case', 'jurors', 'used']

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
log_data = []

def find_valid_header(df):
    for i in range(min(10, len(df))):
        row = df.iloc[i].astype(str).str.lower()
        match_count = sum(any(k in str(cell) for k in REQUIRED_KEYWORDS) for cell in row)
        if match_count >= 2:
            return i
    return None

xl = pd.ExcelFile(INPUT_FILE)
sheets = [s for s in xl.sheet_names if "yield" not in s.lower() and "consolidated" not in s.lower()]

print(f"📄 Sheets to process: {sheets}")

for sheet in sheets:
    try:
        df_raw = xl.parse(sheet, header=None, dtype=str)
        header_row_index = find_valid_header(df_raw)

        if header_row_index is None:
            log_data.append([sheet, "❌ No valid header found"])
            continue

        df = xl.parse(sheet, header=header_row_index)
        df.dropna(how="all", inplace=True)

        output_file = os.path.join(OUTPUT_FOLDER, f"{sheet.replace(' ', '_')}.csv")
        df.to_csv(output_file, index=False)

        log_data.append([sheet, f"✅ Processed with header at row {header_row_index + 1}", f"{len(df)} rows"])
        print(f"✅ Saved: {output_file}")

    except Exception as e:
        log_data.append([sheet, f"❌ Error: {str(e)}"])

pd.DataFrame(log_data, columns=["Sheet", "Status", "Details"]).to_csv(LOG_FILE, index=False)
print(f"📝 Log written to {LOG_FILE}")
