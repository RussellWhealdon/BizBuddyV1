import pandas as pd
from datetime import date, timedelta
import calendar
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
import streamlit as st

# Load the secrets for the service account path and property ID
service_account_info = st.secrets["google_service_account"]
property_id = st.secrets["google_service_account"]["property_id"]

# Initialize GA Client using the service account JSON
client = BetaAnalyticsDataClient.from_service_account_info(service_account_info)

# Get todays date
today = date.today().strftime("%Y-%m-%d")

def fetch_ga4_extended_data():
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name="date"),                     # Break down by date
            Dimension(name="pagePath"),                 # For content performance
            Dimension(name="sessionSource"),            # Traffic source
            Dimension(name="firstUserCampaignName"),    # Campaign details
            Dimension(name="firstUserSourceMedium"),    # Original source/medium
            Dimension(name="landingPagePlusQueryString"),
            Dimension(name="eventName"),             # For exit pages
        ],
        metrics=[
            Metric(name="activeUsers"),                # Total visitors (unique users)
            Metric(name="sessions"),                   # Total sessions
            Metric(name="screenPageViews"),            # Total pageviews
            Metric(name="bounceRate"),                 # Bounce rate
            Metric(name="averageSessionDuration"),     # Avg. session duration
            Metric(name="newUsers"),                   # New visitors
            Metric(name="eventCount"),                 # Event counts (e.g., leads)                       
        ],
        date_ranges=[DateRange(start_date="2024-01-01", end_date=today)],  # Define date range
    )
    
    response = client.run_report(request)
    
    # Parse the response and create a DataFrame
    rows = []
    for row in response.rows:
        date = row.dimension_values[0].value
        page_path = row.dimension_values[1].value
        session_source = row.dimension_values[2].value
        campaign_name = row.dimension_values[3].value
        source_medium = row.dimension_values[4].value
        lp_query = row.dimension_values[5].value
        event_name = row.dimension_values[6].value
            
        active_users = row.metric_values[0].value
        sessions = row.metric_values[1].value
        pageviews = row.metric_values[2].value
        bounce_rate = row.metric_values[3].value
        avg_session_duration = row.metric_values[4].value
        new_users = row.metric_values[5].value
        event_count = row.metric_values[6].value
        
        rows.append([
            date, page_path, session_source, campaign_name, source_medium, lp_query, event_name,
            active_users, sessions, pageviews, bounce_rate, avg_session_duration, 
            new_users, event_count
        ])
    
    # Create DataFrame
    df = pd.DataFrame(rows, columns=[
        'Date', 'Page Path', 'Session Source', 'Campaign Name', 'Source/Medium', 'Lp/Query', 'Event Name',
        'Total Visitors', 'Sessions', 'Pageviews', 'Bounce Rate', 'Avg. Session Duration',
        'New Users', 'Event Count'
    ])
    
    # Process date columns for easier handling
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)

    # Create new 'Leads' column based on "generate_lead"
    df['Leads'] = df.apply(lambda row: float(row['Event Count']) if row['Event Name'] == "generate_lead" else 0, axis=1)

    return df

# Get summary of acquisition sources
def summarize_acquisition_sources(acquisition_data):
    # Check if required columns are in the dataframe
    required_cols = ["Session Source", "Sessions", "Bounce Rate", "Event Count"]
    if not all(col in acquisition_data.columns for col in required_cols):
        raise ValueError("Data does not contain required columns.")
    
    # Convert columns to numeric, if possible, and fill NaNs
    acquisition_data["Sessions"] = pd.to_numeric(acquisition_data["Sessions"], errors='coerce').fillna(0)
    acquisition_data["Bounce Rate"] = pd.to_numeric(acquisition_data["Bounce Rate"], errors='coerce').fillna(0)
    acquisition_data["Leads"] = pd.to_numeric(acquisition_data["Leads"], errors='coerce').fillna(0)

    # Group by Session Source to get aggregated metrics
    source_summary = acquisition_data.groupby("Session Source").agg(
        Sessions=("Sessions", "sum"),
        Bounce_Rate=("Bounce Rate", "mean"),
        Conversions=("Leads", "sum")
    ).reset_index()

    # Calculate Conversion Rate
    source_summary["Conversion Rate (%)"] = (source_summary["Conversions"] / source_summary["Sessions"] * 100).round(2)

    # Sort by Sessions in descending order
    source_summary = source_summary.sort_values(by="Sessions", ascending=False)
    
    # Format summary text for LLM
    summary = "Traffic Source Performance Summary:\n"
    summary += "Source | Sessions | Avg. Bounce Rate (%) | Conversion Rate (%)\n"
    summary += "-" * 60 + "\n"

    for _, row in source_summary.iterrows():
        source = row["Session Source"]
        sessions = row["Sessions"]
        bounce_rate = round(row["Bounce_Rate"], 2)
        conversion_rate = row["Conversion Rate (%)"]
        
        summary += f"{source} | {sessions} | {bounce_rate}% | {conversion_rate}%,\n"

    return summary, source_summary


# Summarize landing pages
def summarize_landing_pages(acquisition_data):
    # Check if required columns are in the dataframe
    required_cols = ["Page Path", "Sessions", "Bounce Rate", "Leads"]
    if not all(col in acquisition_data.columns for col in required_cols):
        raise ValueError("Data does not contain required columns.")
    
    # Convert columns to numeric, if possible, and fill NaNs
    acquisition_data["Sessions"] = pd.to_numeric(acquisition_data["Sessions"], errors='coerce').fillna(0)
    acquisition_data["Bounce Rate"] = pd.to_numeric(acquisition_data["Bounce Rate"], errors='coerce').fillna(0)
    acquisition_data["Leads"] = pd.to_numeric(acquisition_data["Leads"], errors='coerce').fillna(0)

    # Group by Page Path to get aggregated metrics
    page_summary = acquisition_data.groupby("Page Path").agg(
        Sessions=("Sessions", "sum"),
        Bounce_Rate=("Bounce Rate", "mean"),
        Conversions=("Leads", "sum")  # Use Leads for conversions
    ).reset_index()

    # Calculate Conversion Rate
    page_summary["Conversion Rate (%)"] = (page_summary["Conversions"] / page_summary["Sessions"] * 100).round(2)

    # Sort by Sessions in descending order
    page_summary = page_summary.sort_values(by="Sessions", ascending=False)
    
    # Format summary text for LLM
    summary = "Landing Page Performance Summary:\n"
    summary += "Page Path | Sessions | Avg. Bounce Rate (%) | Conversion Rate (%)\n"
    summary += "-" * 70 + "\n"

    for _, row in page_summary.iterrows():
        page_path = row["Page Path"]
        sessions = row["Sessions"]
        bounce_rate = round(row["Bounce_Rate"], 2)
        conversion_rate = row["Conversion Rate (%)"]
        
        summary += f"{page_path} | {sessions} | {bounce_rate}% | {conversion_rate}%,\n"

    return summary, page_summary


def summarize_monthly_data(acquisition_data):
    # Ensure the Date column is in datetime format, then convert to date
    if 'Date' not in acquisition_data.columns:
        raise ValueError("Data does not contain a 'Date' column.")
    
    acquisition_data['Date'] = pd.to_datetime(acquisition_data['Date'], errors='coerce').dt.date

    # Get the date 30 days ago
    today = date.today()
    start_of_period = today - timedelta(days=30)
    
    # Filter data for the last 30 days
    monthly_data = acquisition_data[acquisition_data['Date'] >= start_of_period]
    
    # Check if required columns are in the dataframe
    required_cols = ["Total Visitors", "New Users", "Sessions", "Leads", "Avg. Session Duration", "Session Source"]
    if not all(col in monthly_data.columns for col in required_cols):
        raise ValueError("Data does not contain required columns.")
    
    # Convert columns to numeric, if possible, and fill NaNs
    numeric_cols = ["Total Visitors", "New Users", "Sessions", "Leads", "Avg. Session Duration"]
    for col in numeric_cols:
        monthly_data[col] = pd.to_numeric(monthly_data[col], errors='coerce').fillna(0)
    
    # Calculate total metrics for the last 30 days
    total_visitors = monthly_data["Total Visitors"].sum()
    new_visitors = monthly_data["New Users"].sum()
    total_sessions = monthly_data["Sessions"].sum()
    total_leads = monthly_data["Leads"].sum()

    # Calculate average metrics for the last 30 days
    avg_time_on_site = monthly_data["Avg. Session Duration"].mean().round(2)
    
    # Create a summary DataFrame
    summary_df = pd.DataFrame({
        "Metric": ["Total Visitors", "New Visitors", "Total Sessions", "Total Leads", "Avg. Time on Site (seconds)"],
        "Value": [total_visitors, new_visitors, total_sessions, total_leads, avg_time_on_site]
    })
    
    # Summarize acquisition metrics
    acquisition_summary = monthly_data.groupby("Session Source").agg(
        Visitors=("Total Visitors", "sum"),
        Sessions=("Sessions", "sum"),
        Leads=("Leads", "sum")
    ).reset_index()
    
    return summary_df, acquisition_summary

def summarize_last_month_data(acquisition_data):
    # Ensure the Date column is in datetime format, then convert to date
    if 'Date' not in acquisition_data.columns:
        raise ValueError("Data does not contain a 'Date' column.")
    
    acquisition_data['Date'] = pd.to_datetime(acquisition_data['Date'], errors='coerce').dt.date

    # Calculate the first and last day of the previous month
    today = date.today()
    first_day_of_this_month = today.replace(day=1)
    last_day_of_last_month = first_day_of_this_month - timedelta(days=1)
    first_day_of_last_month = last_day_of_last_month.replace(day=1)
    
    # Filter data for the previous month
    last_month_data = acquisition_data[
        (acquisition_data['Date'] >= first_day_of_last_month) & 
        (acquisition_data['Date'] <= last_day_of_last_month)
    ]
    
    # Check if required columns are in the dataframe
    required_cols = ["Total Visitors", "New Users", "Sessions", "Leads", "Avg. Session Duration", "Session Source"]
    if not all(col in last_month_data.columns for col in required_cols):
        raise ValueError("Data does not contain required columns.")
    
    # Convert columns to numeric, if possible, and fill NaNs
    numeric_cols = ["Total Visitors", "New Users", "Sessions", "Leads", "Avg. Session Duration"]
    for col in numeric_cols:
        last_month_data[col] = pd.to_numeric(last_month_data[col], errors='coerce').fillna(0)
    
    # Calculate total metrics for last month
    total_visitors = last_month_data["Total Visitors"].sum()
    new_visitors = last_month_data["New Users"].sum()
    total_sessions = last_month_data["Sessions"].sum()
    total_leads = last_month_data["Leads"].sum()

    # Calculate average metrics for last month
    avg_time_on_site = last_month_data["Avg. Session Duration"].mean().round(2)
    
    # Create a summary dataframe
    summary_df = pd.DataFrame({
        "Metric": ["Total Visitors", "New Visitors", "Total Sessions", "Total Leads", "Average Time on Site"],
        "Value": [total_visitors, new_visitors, total_sessions, total_leads, avg_time_on_site]
    })

    # Summarize acquisition metrics
    acquisition_summary = last_month_data.groupby("Session Source").agg(
        Visitors=("Total Visitors", "sum"),
        Sessions=("Sessions", "sum"),
        Leads=("Leads", "sum")
    ).reset_index()
    
    return summary_df, acquisition_summary
