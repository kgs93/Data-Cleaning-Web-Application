# Data Cleaning Master (Python Web App)

This is a standalone Streamlit app that mirrors your data cleaning workflow:
- Removes duplicates (and keeps a copy)
- Fills numeric nulls with mean
- Drops rows that have missing values in non-numeric columns
- Lets you preview and download cleaned and duplicate CSVs

## Quick start
1) Create and activate a virtual environment (recommended)
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate

2) Install dependencies
   pip install -r requirements.txt

3) Run the app
   streamlit run app.py

4) Open the URL shown in the terminal (usually http://localhost:8501)

## Notes
- CSV and XLSX files are supported.
- Large files depend on your machine's memory; Streamlit handles in-memory processing.
