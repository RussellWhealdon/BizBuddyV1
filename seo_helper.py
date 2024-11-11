import streamlit as st
from urllib.parse import unquote
import gsc_data_pull 
import requests
from bs4 import BeautifulSoup
from llm_integration import query_gpt 

# Page configuration
st.set_page_config(layout="wide")

def fetch_page_copy(url):
    try:
        # Fetch the content of the page
        response = requests.get(url)
        response.raise_for_status()  # Check if request was successful

        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title tag
        title = soup.title.string if soup.title else "No title found"

        # Extract the meta description
        meta_description = ""
        description_tag = soup.find("meta", attrs={"name": "description"})
        if description_tag and description_tag.get("content"):
            meta_description = description_tag["content"]
        else:
            meta_description = "No meta description found"

        # Extract meta keywords
        meta_keywords = ""
        keywords_tag = soup.find("meta", attrs={"name": "keywords"})
        if keywords_tag and keywords_tag.get("content"):
            meta_keywords = keywords_tag["content"]
        else:
            meta_keywords = "No meta keywords found"

        # Extract main text from <p> and heading tags
        paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3'])
        page_text = "\n\n".join([para.get_text(strip=True) for para in paragraphs])

        # Combine all extracted data into a dictionary
        seo_data = {
            "Title": title,
            "Meta Description": meta_description,
            "Meta Keywords": meta_keywords,
            "Page Copy": page_text if page_text else "No main content found on this page."
        }

        return seo_data
    except requests.RequestException as e:
        return {"Error": f"An error occurred while fetching the page: {e}"}

def display_report_with_llm(llm_prompt):
    # Query the LLM with the prompt
    llm_response = query_gpt(llm_prompt)
    st.write("GPT-4 Analysis:")
    st.write(llm_response)

def main():
    # Ensure session_summary is initialized in session state
    if "session_summary" not in st.session_state:
        st.session_state["session_summary"] = ""  # Initialize with an empty string or default value

    
    # Pull the same dataframe as in the main app
    df = gsc_data_pull.fetch_search_console_data()  # Replace 'pull_data' with the actual function name
    
    # Retrieve message from URL parameter
    query_params = st.experimental_get_query_params()
    message = query_params.get("message", ["No message received"])[0]

    # Display SEO helper app
    st.title("SEO Helper")
    st.write("This is the SEO helper app.")

    # Input field for the URL to scrape
    url = st.text_input("Enter a URL to scrape", placeholder="https://example.com")
    
    if url:
        st.write("Fetching content...")
        seo_data = fetch_page_copy(url)

        with st.expander("See Website Copy"):
            st.subheader("SEO Information")
            st.write(f"**Title:** {seo_data['Title']}")
            st.write(f"**Meta Description:** {seo_data['Meta Description']}")
            st.write(f"**Meta Keywords:** {seo_data['Meta Keywords']}")
            st.subheader("Page Copy")
            st.write(seo_data["Page Copy"])

        # Generate the prompt for LLM analysis
        llm_prompt = (
            f"Here is the SEO information and page copy from a webpage:\n\n"
            f"Title: {seo_data['Title']}\n"
            f"Meta Description: {seo_data['Meta Description']}\n"
            f"Meta Keywords: {seo_data['Meta Keywords']}\n"
            f"Page Copy: {seo_data['Page Copy']}\n\n"
            f"Based on this SEO information, please suggest possible improvements. Have one section main section that talks about overall SEO strategy. Below that have another section where you identify actual pieces of text you see that could be tweaked."
            f"Use the following context to guide your suggestions: {message}. "
            f"This is an analysis from an initial look at the search query report from this website."
        )

        # Display LLM analysis
        display_report_with_llm(llm_prompt)
 
if __name__ == "__main__":
     main()
