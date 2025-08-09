import streamlit as st
import pandas as pd
from io import BytesIO
from cleaning import clean_dataframe

st.set_page_config(page_title="Data Cleaning Master", page_icon="🧹", layout="wide")
st.title("Data Cleaning Master")
st.caption("Upload CSV or Excel. We remove duplicates, fill numeric nulls with mean, and drop rows missing in non-numeric columns.")

dataset_name = st.text_input("Dataset name", placeholder="e.g., jan_sales")
uploaded = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"]) 

def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")

if uploaded is not None:
    # Read file
    if uploaded.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded, encoding_errors="ignore")
    else:
        df = pd.read_excel(uploaded)

    st.write(f"Detected {df.shape[0]} rows × {df.shape[1]} columns")
    res = clean_dataframe(df)

    st.subheader("Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Original rows", res["originalRowCount"])
    c2.metric("Columns", res["originalColumnCount"])
    c3.metric("Duplicates", res["duplicateCount"])
    c4.metric("Cleaned rows", res["cleanedRowCount"])

    with st.expander("Missing values by column"):
        st.json(res["missingByColumn"]) 

    st.write("Numeric columns:", ", ".join(res["numericColumns"]) or "None")

    st.subheader("Cleaned data (preview)")
    st.dataframe(res["cleaned"].head(10), use_container_width=True)

    st.subheader("Duplicate records (preview)")
    if res["duplicateCount"]:
        st.dataframe(res["duplicates"].head(10), use_container_width=True)
    else:
        st.info("No duplicates detected.")

    dn = dataset_name or "dataset"
    st.download_button(
        "Download Clean CSV",
        data=to_csv_bytes(res["cleaned"]),
        file_name=f"{dn}_Clean_data.csv",
        mime="text/csv",
        type="primary",
    )
    st.download_button(
        "Download Duplicates CSV",
        data=to_csv_bytes(res["duplicates"]),
        file_name=f"{dn}_duplicates.csv",
        mime="text/csv",
        disabled=(res["duplicateCount"] == 0),
    )
else:
    st.info("Upload a CSV or XLSX file to begin.")
