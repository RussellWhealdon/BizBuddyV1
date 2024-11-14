import streamlit as st
import pandas as pd
from llm_integration import query_gpt  # Importing for GPT functionality

def load_data(file_path):
    """
    Load keyword data from a CSV file, skipping the first two rows.
    """
    try:
        df = pd.read_csv(file_path, skiprows=2)  # Skip the first two rows
        return df
    except FileNotFoundError:
        st.error(f"File '{file_path}' not found. Please check the file name or location.")
        return pd.DataFrame()  # Return an empty DataFrame if file is not found
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return pd.DataFrame()

def filter_data(df, query):
    """
    Filter the dataframe based on a search query.
    """
    if query:
        return df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    return df

def display_sidebar():
    """
    Display sidebar instructions and notes.
    """
    st.sidebar.header("Instructions")
    st.sidebar.write(
        """
        1. The app loads keyword data from the `KeywordStats_Washington_CWN.csv` file.
        2. Use the search box to filter the data for specific keywords.
        3. Select 5 keywords that directly impact your business and submit them.
        """
    )

    st.sidebar.subheader("Notes:")
    st.sidebar.write(
        """
        - Ensure the CSV file is in the correct location.
        - The data is pre-fetched and no API calls are made in this module.
        """
    )

def generate_ppc_plan(keywords):
    """
    Generate a PPC plan using GPT based on the selected keywords.
    """
    prompt = (
        "You are an expert PPC marketer. Using the following 5 keywords, create a PPC plan. "
        "Include match type recommendations, conversion types, business context, and some example ad copy for each keyword.\n\n"
        f"Keywords: {', '.join(keywords)}"
    )
    return query_gpt(prompt)

def main():
    """
    Main function to run the Streamlit app.
    """
    # Set page configuration
    st.set_page_config(page_title="Google Ads Keyword Planner", layout="wide")

    # App title
    st.title("Google Ads Keyword Planner")

    # Load data
    uploaded_file = "KeywordStats_Washington_CWN.csv"
    df = load_data(uploaded_file)

    # Search functionality
    search_query = st.text_input("Search for Keywords:", value="")
    filtered_df = filter_data(df, search_query)

    # Display data
    st.subheader("Keyword Data")
    with st.expander("View Keyword Data", expanded=True):
        st.dataframe(filtered_df, use_container_width=True)

    # Keyword Selection
    st.subheader("Select 5 keywords that have search volume and are directly related to your business/website.")
    selected_keywords = []
    for i in range(5):
        keyword = st.text_input(f"Keyword {i+1}")
        if keyword:
            selected_keywords.append(keyword)

    if st.button("Submit Keywords"):
        if len(selected_keywords) < 5:
            st.error("Please enter all 5 keywords before submitting.")
        else:
            st.success("You have successfully submitted your keywords!")
            st.write("Selected Keywords:", selected_keywords)

            # Generate PPC Plan
            with st.spinner("Generating PPC Plan..."):
                ppc_plan = generate_ppc_plan(selected_keywords)
                st.subheader("Generated PPC Plan")
                st.write(ppc_plan)

    # Sidebar
    display_sidebar()

# Run the main function
if __name__ == "__main__":
    main()
