import streamlit as st
from gaw_data_pull import fetch_keyword_data

# Streamlit App Title
st.title("Google Ads Keyword Planner")

# Input Fields
st.subheader("Enter Details for Keyword Ideas:")
page_url = st.text_input("Website URL", value="https://example.com")
customer_id = "6318131495"
location_ids = ["1014044"]  # Seattle, WA
language_id = "1000"  # English

# Fetch Button
if st.button("Fetch Keyword Data"):
    with st.spinner("Fetching keyword data..."):
        df = fetch_keyword_data(customer_id, location_ids, language_id, page_url)
        if not df.empty:
            st.success("Data fetched successfully!")
            st.dataframe(df)
        else:
            st.warning("No data returned. Please check your inputs or API setup.")

# Instructions for Use
st.sidebar.header("Instructions")
st.sidebar.write(
    """
    1. Enter your **Customer ID** (Test Account only).
    2. Provide a valid **Website URL**.
    3. Click **Fetch Keyword Data** to see keyword suggestions.
    """
)

st.sidebar.subheader("Notes:")
st.sidebar.write(
    """
    - Data is sourced from the Google Ads Keyword Planner API.
    - Ensure your `secrets.toml` contains valid credentials.
    """
)
