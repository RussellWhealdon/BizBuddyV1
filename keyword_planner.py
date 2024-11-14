import streamlit as st
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

def fetch_website_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        st.error(f"Failed to fetch content from {url}")
        return ""

def extract_keywords(text, num_keywords=6):
    # Tokenize the text
    words = nltk.word_tokenize(text.lower())
    # Remove stopwords and non-alphabetic tokens
    words = [word for word in words if word.isalpha() and word not in stopwords.words('english')]
    # Get the most common words
    freq_dist = Counter(words)
    common_words = freq_dist.most_common(num_keywords)
    return [word for word, _ in common_words]

def main():
    st.set_page_config(page_title="Google Ads Keyword Planner", layout="wide")
    st.title("Google Ads Keyword Planner")

    # Fetch and display keyword suggestions
    st.subheader("Suggested Keywords Based on Your Website")
    url = "https://www.chelseawnutrition.com/"
    html_content = fetch_website_content(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        keywords = extract_keywords(text)
        st.write(", ".join(keywords))

    # Load and display keyword data
    st.subheader("What People Are Searching for Related to Your Website")
    uploaded_file = "KeywordStats_Washington_CWN.csv"
    try:
        df = pd.read_csv(uploaded_file, skiprows=2)
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

    # Keyword selection and PPC plan generation
    st.subheader("Select 5 Keywords That Have Search Volume and Are Directly Related to Your Business/Website.")
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
            # Placeholder for PPC plan generation
            st.write("PPC plan generation functionality goes here.")

    # Sidebar instructions
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

if __name__ == "__main__":
    main()
