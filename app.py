# app.py
import streamlit as st
import pandas as pd
import json
import io
import os

st.set_page_config(page_title="CSV to JSON Converter", page_icon="📊", layout="centered")

st.title("📊 CSV to JSON Converter")
st.markdown("Upload your CSV file and get clean JSON output ready for APIs.")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], accept_multiple_files=False)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.error("The uploaded CSV file is empty. Please upload a file with data.")
        else:
            st.success(f"File loaded successfully! Found {len(df)} rows and {len(df.columns)} columns.")
            st.subheader("Preview (first 5 rows)")
            st.dataframe(df.head())
            
            # Convert to JSON
            json_data = df.to_json(orient="records", indent=2)
            json_obj = json.loads(json_data)
            
            st.subheader("JSON Output")
            st.json(json_obj)
            
            # Download button
            json_bytes = json.dumps(json_obj, indent=2).encode("utf-8")
            st.download_button(
                label="Download JSON",
                data=json_bytes,
                file_name=uploaded_file.name.replace(".csv", ".json"),
                mime="application/json"
            )
    except pd.errors.EmptyDataError:
        st.error("The uploaded file is empty or not a valid CSV.")
    except pd.errors.ParserError:
        st.error("Could not parse the CSV file. Please check the file format.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
else:
    st.info("Drag and drop a CSV file above to get started.")
    st.markdown("""
    ### How to use:
    1. Upload your CSV file using the file uploader above
    2. Preview the data to ensure it's correct
    3. View the JSON output
    4. Download the JSON file
    
    ### Features:
    - No coding required
    - Handles large files
    - Clean, API-ready JSON output
    - Works with any CSV file
    """)