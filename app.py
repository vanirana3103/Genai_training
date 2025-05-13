import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Excel Data Cleaner", layout="wide")
st.title("📊 Excel Data Cleaner & Report Generator")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.subheader("🔍 Raw Data")
        st.dataframe(df)

        # Clean data
        df_clean = df.drop_duplicates().dropna()

        st.subheader("✅ Cleaned Data")
        st.dataframe(df_clean)

        # Summary Report
        st.subheader("📈 Summary Statistics")
        summary = df_clean.describe(include='all')
        st.dataframe(summary)

        # Grade Distribution
        if "Grade" in df_clean.columns:
            st.subheader("📊 Grade-wise Student Count")
            grade_counts = df_clean["Grade"].value_counts()
            st.bar_chart(grade_counts)
        else:
            st.warning("⚠️ 'Grade' column not found. Skipping grade distribution.")

        # Download buttons
        def to_excel(df):
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False)
            buffer.seek(0)
            return buffer

        st.download_button("📥 Download Cleaned Data", to_excel(df_clean), "cleaned_data.xlsx")
        st.download_button("📥 Download Summary Report", to_excel(summary), "summary_report.xlsx")
        if "Grade" in df_clean.columns:
            st.download_button("📥 Download Grade Distribution", to_excel(grade_counts.reset_index()), "grade_distribution.xlsx")

    except Exception as e:
        st.error(f"Error processing file: {e}")
