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
    
    # Generate and display GA4 metrics
    current_summary = summarize_monthly_data(ga_data)[0]
    last_month_summary = summarize_last_month_data(ga_data)[0]
    
    # Use LLM to generate insights based on GA data
    ga_llm_prompt = """
    Based on the following website performance metrics, provide a short analysis. Highlight key improvements, areas needing attention, 
    and how these metrics compare to typical industry standards. Limit your response to 2-3 bullet points.
    """
        
    # Combine summaries into data string for LLM
    metric_summary_text = "\n".join([f"{row['Metric']}: {row['Value']}" for _, row in current_summary.iterrows()])
    
    ga_insights = query_gpt(ga_llm_prompt, metric_summary_text)
    
    st.markdown("### Insights from AI")
    st.markdown(ga_insights)

  
  with col2:
    st.markdown("### Acquisition Overview")
    acq_col1, acq_col2 = st.columns(2)
    with acq_col1:
      plot_acquisition_pie_chart_plotly(summarize_monthly_data(ga_data)[1])
    with acq_col2:
      describe_top_sources(summarize_monthly_data(ga_data)[1])
      temp_url = "https://www.google.com/"
      st.link_button("Paid Search - Helper", temp_url)
      st.link_button("Social Ads - Helper", temp_url)

  
  ###landing page analysis section
  st.divider()

  col3, col4 = st.columns(2)
  with col3:
    st.markdown("### Landing Page Overview")
    
    # Ensure the 'Date' column is in the correct format
    ga_data['Date'] = pd.to_datetime(ga_data['Date'], errors='coerce').dt.date

    # Get the date 30 days ago
    today = date.today()
    start_of_period = today - timedelta(days=30)

    # Filter data for the last 30 days
    last_30_days_data = ga_data[ga_data['Date'] >= start_of_period]
    landing_page_summary = summarize_landing_pages(last_30_days_data)[1]
    
    # Display the DataFrame for landing page performance
    generate_page_summary(landing_page_summary)

    llm_input = st.session_state.get("page_summary_llm", "")
    response = query_gpt("Provide insights based on the following page performance data, note that there is no CTAs on any page besides the Home. We need to think of ways to drive more people to the contact page:", llm_input)
    st.markdown(f"### LLM Analysis\n{response}")
 
    
      
# Execute the main function only when the script is run directly
if __name__ == "__main__":
    main()
  


