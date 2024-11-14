import streamlit as st
from gaw_data_pull import fetch_keyword_data
import streamlit as st
import pandas as pd
from llm_integration import query_gpt  # Importing for potential future use

# Set Streamlit page configuration
st.set_page_config(page_title="Google Ads Keyword Planner", layout="wide")

# Streamlit App Title
st.title("Google Ads Keyword Planner")

# Load Keyword Data from File
st.subheader("Keyword Data")
uploaded_file = "KeywordStats_Washington_CWN.csv"  # File name

# Read and display the file
try:
    df = pd.read_csv(uploaded_file, skiprows=2)  # Skip the first two rows

    # Search Functionality
    search_query = st.text_input("Search for Keywords:", value="")
    if search_query:
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    else:
        filtered_df = df

    with st.expander("View Keyword Data", expanded=True):
        st.dataframe(filtered_df, use_container_width=True)

except FileNotFoundError:
    st.error(f"File '{uploaded_file}' not found. Please check the file name or location.")
except Exception as e:
    st.error(f"An error occurred: {e}")

# Sidebar Instructions
st.sidebar.header("Instructions")
st.sidebar.write(
    """
    1. The app loads keyword data from the `KeywordStats_Washington_CWN.csv` file.
    2. Use the search box to filter the data for specific keywords.
    """
)

st.sidebar.subheader("Notes:")
st.sidebar.write(
    """
    - Ensure the CSV file is in the correct location.
    - The data is pre-fetched and no API calls are made in this module.
    """
)
