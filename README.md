# 12 Angry Rows: A Jury Utilization Pipeline

This project cleans and analyzes historical jury panel data from the Santa Barbara Superior Court. It transforms multi-year/multi-location Excel exports into structured, analysis-ready datasets that can be used to evaluate how jurors were summoned, used, or not used — by case type, location, and year.

This is a civic-tech project built with transparency, reproducibility, and local court impact in mind.

---

## 🎯 Goal

To understand and quantify **jury panel utilization rates** by:

- Extracting 11+ years of Excel-based court data
- Cleaning and consolidating inconsistently formatted CSVs
- Calculating `Jurors Used = Total Reporting − Not Used`
- Classifying case types as Civil, Felony, or Misdemeanor
- Producing a normalized, ready-to-analyze file
- Enabling future dashboarding and analytics

---

## 📁 Project Structure

```
juror_project/
├── juror_structure.py             # Extracts sheets from the Excel master file
├── juror_clean.py                 # Cleans and normalizes each sheet's CSV
├── juror_etl.py                   # Adds classification and utilization rates
├── juror_cleaned_output.csv       # (Not uploaded) Cleaned dataset with real case numbers
├── juror_etl_output.csv           # (Not uploaded) Final data with derived fields
├── sample_data/
│   ├── juror_etl_output_SAMPLE.csv  # ✅ Scrubbed sample for sharing
│   └── README.md                    # Notes on redaction
├── clean_log.csv                  # Per-file processing log
├── structure_samples/             # Split sheets (ignored from Git)
├── juror_master.xlsx              # Original data source (not uploaded)
└── README.md                      # You are here
```

---

## 🔐 Data Ethics and Redaction

To protect confidentiality:
- No real case numbers are included in the public repo.
- The file `juror_etl_output_SAMPLE.csv` contains **only sample data with anonymized case IDs and calculated 'Jurors Not Used' column**.
- Real exports are retained privately and used only for internal analysis.

---

## 🧰 Tools and Techniques

- Python (Pandas, Regex)
- Manual Excel → CSV export
- Rule-based classification
- Text normalization
- Version control for reproducibility

---

## 🙌 Inspiration

This project was influenced by [Financial Audit AI Tool](https://github.com/flwrsfralgernn/Financial-Audit-AI-Tool), particularly in its approach to:

- Treating each Excel sheet as a unique data source
- Using repeatable logic to normalize semi-structured inputs
- Adding contextual columns like “Source File” (adapted here to extract Year and Location)
- Prioritizing signal-bearing columns and ignoring unnecessary noise
- Using regex + rule-based classification instead of complex models when appropriate

Their structure informed our design of a resilient cleaning and transformation pipeline for messy, multi-year court data.

---

## ⚙️ How This Was Built

This project was developed in collaboration with [ChatGPT](https://openai.com/chatgpt) as a real-time thought partner and code assistant.

ChatGPT helped:
- Refactor the Python scripts
- Interpret messy column logic
- Design the final ETL schema
- Debug failures quickly
- Maintain project structure

The human behind the project (👋 that’s me) made all final decisions, validated the logic, and ensured that the outputs made operational sense for jury administration.

---

## 🧑‍💻 About the Developer

I'm a **civic technologist** working in California trial courts, using data, automation, and now AI to improve transparency and efficiency in government systems.

This project is part of a broader portfolio, including [Your Honor, I Object (to Jury Duty)](https://github.com/earlgreyhot1701D/your-honor-i-object-to-jury-duty-v9), a prototype chatbot designed to answer juror eligibility questions using California legal code.

---

## 📈 Next Steps

- [ ] Build a dashboard in Power BI or Excel to visualize:
  - Juror utilization by year and location
  - Criminal vs Civil case trends
  - Cases with high/low panel efficiency
- [ ] Publish a blog post summarizing findings
- [ ] Explore export automation from court systems

---

## 🧠 Lessons Learned

- Always double-check what a column *actually* means — `"Juror"` ≠ `"Jurors Used"`
- Never trust column names; normalize everything
- Most “AI problems” can be solved with rules
- Redaction matters — plan for open data, even in messy projects
- Git is not just for code. It’s for thinking in the open.

---

## 🤝 Acknowledgments

Thanks to:
- **DxHub @ Cal Poly & AWS** for helping me see what’s possible with public-sector data transformation
- The OpenAI team for ChatGPT, which served as my sixth person off the bench editor and coding copilot

---

---

## 🗂️ Version History

### v1.2 – August 2025

- Finalized `juror_etl.py` with dual-path handling and normalized formatting  
- Added validation confidence reporting with traceable column mapping  
- Introduced anonymized 20-row sample dataset for public reference  
- Updated `README.md` to reflect current pipeline, and added new **Validation** section  
- Emphasized that this is a **baseline directional analysis** to support future jury operations insights  

### v1.1 – August 2025
- Added `Jurors Not Used` as a calculated column (Reporting - Used)
- Filtered out rows missing essential values (`Case No.` or `Jurors Reporting`)
- Improved consistency across edge-case CSVs

### v1.0 – Initial Release
- Extracted multi-year, multi-sheet jury data from Excel
- Cleaned and standardized reporting fields
- Consolidated charges from multiple description columns
- Tagged each row with its source file (e.g., by year or location)

## 🔎 Validation Process

To ensure confidence in calculated *Jurors Not Used* values across 11 years of manually structured jury data, I implemented a dual-path validation process:

- Cleaned values were programmatically extracted via `juror_clean.py`.
- Utilization Rates were recalculated and compared against source-provided figures.
- A Validation Confidence Report was generated, identifying:
  - Missing values in 33.1% of records
  - Mismatches in 11.5% of rows
- Where discrepancies occurred, calculated values were favored, with clear documentation provided.

This project is **directional, not empirical**. It establishes a baseline for long-term operational improvement, and is transparent about limitations in legacy reporting tools.

📊 Future Dashboard Integration (Phase 2)

In Phase 2 of this project, a visual dashboard will be added to explore trends in jury utilization across 11 years of court operations. This dashboard will include:

- Year-over-year utilization rates
- Jurors Not Used vs. Jurors Reporting by location
- Charge-type filtering (Misdemeanor, Felony, Civil)
- Visualized gaps in data completeness
- Directional insights for operational planning

This upcoming visualization layer will be built using accessible tools such as Excel, Power BI, or Streamlit — depending on performance and cost constraints.

Stay tuned for updates in the next commit cycle.


