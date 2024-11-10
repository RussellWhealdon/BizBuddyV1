import openai
import streamlit as st
import pandas as pd
from datetime import date
from ga4_data_pull import fetch_ga4_extended_data, summarize_acquisition_sources, summarize_landing_pages
from gsc_data_pull import fetch_search_console_data, summarize_search_queries
from llm_integration import initialize_llm_context, query_gpt
from urllib.parse import quote

# Page configuration
st.set_page_config(page_title="BizBuddy", layout="wide", page_icon = "🤓", 
                  menu_items={
                  'SEO Analysis': 'https://www.extremelycoolapp.com/help',
                  'Paid Search Planner': "https://www.extremelycoolapp.com/bug",
                  'Website Deep Dive': "# This is a header. This is an *extremely* cool app!"
                  )

st.markdown("<h1 style='text-align: center;'>Welcome to your Bizness Buddy</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Let's take your business to the next level</h2>", unsafe_allow_html=True)



