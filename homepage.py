import openai
import streamlit as st
import pandas as pd
from datetime import date
from ga4_data_pull import *
from gsc_data_pull import *
from llm_integration import *
from urllib.parse import quote

# Page configuration
st.set_page_config(page_title="BizBuddy", layout="wide", page_icon = "🤓")
                  #,menu_items={
                  #'SEO Analysis': 'https://www.extremelycoolapp.com/help',
                  #'Paid Search Planner': "https://www.extremelycoolapp.com/bug",
                  #'Website Deep Dive': "# This is a header. This is an *extremely* cool app!"})

st.markdown("<h1 style='text-align: center;'>Welcome to your Bizness Buddy</h1>", unsafe_allow_html=True)


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

  ga_data = fetch_ga4_extended_data()
  search_data = fetch_search_console_data()

  
  col1, col2, = st.columns(2)
  
  with col1:
    st.markdown("<h3 style='text-align: center;'>Web Performance Overview</h3>", unsafe_allow_html=True)
    #st.write(ga_data)
    generate_all_metrics_copy(summarize_monthly_data(ga_data)[0], summarize_last_month_data(ga_data)[0])
    # Use LLM to generate insights based on GA data
    ga_llm_prompt = """
    Based on the following website performance metrics, provide a short analysis. Highlight key improvements, areas needing attention, 
    and how these metrics compare to typical industry standards. Limit your response to 3-4 sentences.
    """
        
    # Combine summaries into data string for LLM
    metric_summary_text = "\n".join([f"{row['Metric']}: {row['Value']}" for _, row in current_summary.iterrows()])
    
    ga_insights = query_gpt(ga_llm_prompt, metric_summary_text)
    
    st.markdown("### Insights from AI")
    st.markdown(ga_insights)

  with col2:
    response = (
        lambda: summarize_search_queries(search_data),
        """
        Based on this Search Query Report from Google give tips as to possible Paid Search Strategy and SEO optimization. Try to best answer the question, 
        What are people searching for when they come to my site and how can I get more of these users? Give me a brief analysis then 4 bullet points with 
        concrete tips for improvement. Limit this repsonse to ~ 200 words!
        """
    )
    #st.write(summarize_last_month_data(ga_data)[0])

    
      
# Execute the main function only when the script is run directly
if __name__ == "__main__":
    main()
  


