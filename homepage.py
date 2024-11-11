import openai
import streamlit as st
import pandas as pd
from datetime import date
from ga4_data_pull import fetch_ga4_extended_data, summarize_acquisition_sources, summarize_landing_pages
from gsc_data_pull import fetch_search_console_data, summarize_search_queries
from llm_integration import initialize_llm_context, query_gpt
from urllib.parse import quote

# Page configuration
st.set_page_config(page_title="BizBuddy", layout="wide", page_icon = "🤓")
                  #,menu_items={
                  #'SEO Analysis': 'https://www.extremelycoolapp.com/help',
                  #'Paid Search Planner': "https://www.extremelycoolapp.com/bug",
                  #'Website Deep Dive': "# This is a header. This is an *extremely* cool app!"})

st.markdown("<h1 style='text-align: center;'>Welcome to your Bizness Buddy</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Let's take your business to the next level</h2>", unsafe_allow_html=True)


# Initialize LLM context with business context on app load
initialize_llm_context()

# Generate and display each summary with LLM analysis
def display_report_with_llm(summary_func, llm_prompt):
    # Generate summary
    summary = summary_func()

    # Query LLM with specific prompt
    llm_response = query_gpt(llm_prompt, summary)
    return llm_response


# Run main function
def main():

    col1, col2, = st.columns(2)

    with col1:
        st.markdown("<h3 style='text-align: center;'>Web Performance Overview</h3>", unsafe_allow_html=True)
    
  with col2:
    
        search_data = fetch_search_console_data()
        response = display_report_with_llm(
            lambda: summarize_search_queries(search_data),
            """
            Based on this Search Query Report from Google give tips as to possible Paid Search Strategy and SEO optimization. Try to best answer the question, 
            What are people searching for when they come to my site and how can I get more of these users? Give me a brief analysis then 4 bullet points with 
            concrete tips for improvement. Limit this repsonse to ~ 200 words!
            """
        )
      
# Execute the main function only when the script is run directly
if __name__ == "__main__":
    main()
  


