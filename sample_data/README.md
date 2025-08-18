# Sample Data: Juror Utilization (Redacted)

This folder contains a redacted sample of the full output from the jury utilization pipeline.

## 🔐 Redaction Notes

- **Case numbers** have been anonymized and replaced with placeholder values such as `CASE00001`, `CASE00002`, etc.
- **Location information and Source File** have been anonymized and replaced with placeholder values such as `X`
- **Only 100 rows** are included here to demonstrate structure and format without exposing sensitive data.
- The original data contains actual Santa Barbara Superior Court case numbers and was not uploaded due to confidentiality.

## 📄 File Contents

- `juror_etl_output_SAMPLE.csv`: Cleaned and normalized data with the following fields:
  - `Jurors Reporting`
  - `Jurors Used`
  - `Utilization Rate`
  - `Case Type`, `Civil`, `Case Category`
  - `Charges`, `Penal Codes`
  - `Year`, `Location`, `Source File`

This sample preserves the column structure, data types, and formatting of the real dataset and can be used to understand the pipeline's output.