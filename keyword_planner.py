import streamlit as st
from gaw_data_pull import fetch_keyword_data

import streamlit as st
import pandas as pd

# Set Streamlit page configuration
st.set_page_config(page_title="Google Ads Keyword Planner", layout="wide")


# Streamlit App Title
st.title("Google Ads Keyword Planner")

# Load Keyword Data from File
st.subheader("Keyword Data")
uploaded_file = "KeywordStats_Washington_CWN.csv"  # File name

# Read and display the file
try:
    df = pd.read_csv(uploaded_file)
    with st.expander("View Keyword Data", expanded=True):
        st.dataframe(df, use_container_width=True)
except FileNotFoundError:
    st.error(f"File '{uploaded_file}' not found. Please check the file name or location.")
except Exception as e:
    st.error(f"An error occurred: {e}")

# Sidebar Instructions
st.sidebar.header("Instructions")
st.sidebar.write(
    """
    1. The app loads keyword data from the `KeywordStats_Washington_CWN.csv` file.
    2. View the data in the main panel under **Keyword Data**.
    """
)

st.sidebar.subheader("Notes:")
st.sidebar.write(
    """
    - Ensure the CSV file is in the correct location.
    - The data is pre-fetched and no API calls are made in this module.
    """
)
