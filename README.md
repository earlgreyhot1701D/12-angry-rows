# 12 Angry Rows: A Jury Utilization Pipeline

This project cleans and analyzes historical jury panel data from the Superior Court. It transforms multi-year/multi-location Excel exports into structured, analysis-ready datasets that can be used to evaluate how jurors were summoned, used, or not used — by case type, location, and year.

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
- No real case numbers, locations or source file information is included in the public repo.
- The file `juror_etl_output_SAMPLE.csv` contains **only sample data with anonymized case IDs**.
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

Their structure informed the design of a resilient cleaning and transformation pipeline for messy, multi-year court data.

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

## 🧪 How to Run This Project

This project requires **Python 3.9+** and basic knowledge of using the terminal or PowerShell.

### 🧰 Setup

1. Clone or download the repo:
   ```
   git clone https://github.com/yourusername/12-angry-rows.git
   cd 12-angry-rows
   ```

2. (Optional) Create a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate    # Windows
   ```

3. Install dependencies (only standard library used — no install needed unless you want to add tools like pandas profiling or Jupyter).

---

### 🧼 Run the Cleaning Pipeline

**Step 1: Split Excel workbook**
```bash
python juror_structure.py
```

**Step 2: Clean and consolidate CSVs**
```bash
python juror_clean.py
```

**Step 3: Transform and calculate metrics**
```bash
python juror_etl.py
```

Final output will be saved as:
```
juror_etl_output.csv
```

---

### 🧪 Sample Data

If you're not running the full pipeline, you can explore the structure using:

```
sample_data/juror_etl_output_SAMPLE.csv
```

---

