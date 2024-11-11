import pandas as pd
from datetime import date
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
import streamlit as st

# Load the secrets for the service account path and property ID
service_account_info = st.secrets["google_service_account"]
property_id = st.secrets["google_service_account"]["property_id"]

# Initialize GA Client using the service account JSON
client = BetaAnalyticsDataClient.from_service_account_info(service_account_info)

# Get today's date
today = date.today().strftime("%Y-%m-%d")

# Function to fetch GA4 data with all key metrics
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
            Dimension(name="eventName"),
            Dimension(name="exitPagePath")              # For exit pages
        ],
        metrics=[
            Metric(name="activeUsers"),                # Total visitors (unique users)
            Metric(name="sessions"),                   # Total sessions
            Metric(name="screenPageViews"),            # Total pageviews
            Metric(name="pagesPerSession"),            # Pages per session
            Metric(name="bounceRate"),                 # Bounce rate
            Metric(name="averageSessionDuration"),     # Avg. session duration
            Metric(name="newUsers"),                   # New visitors
            Metric(name="eventCount"),                 # Event counts (e.g., leads)
            Metric(name="exits")                       # Exit count for each page
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
        exit_page = row.dimension_values[7].value
            
        active_users = row.metric_values[0].value
        sessions = row.metric_values[1].value
        pageviews = row.metric_values[2].value
        pages_per_session = row.metric_values[3].value
        bounce_rate = row.metric_values[4].value
        avg_session_duration = row.metric_values[5].value
        new_users = row.metric_values[6].value
        event_count = row.metric_values[7].value
        exits = row.metric_values[8].value
        
        rows.append([
            date, page_path, session_source, campaign_name, source_medium, lp_query, event_name, exit_page,
            active_users, sessions, pageviews, pages_per_session, bounce_rate, avg_session_duration, 
            new_users, event_count, exits
        ])
    
    # Create DataFrame
    df = pd.DataFrame(rows, columns=[
        'Date', 'Page Path', 'Session Source', 'Campaign Name', 'Source/Medium', 'Lp/Query', 'Event Name', 'Exit Page',
        'Total Visitors', 'Sessions', 'Pageviews', 'Pages per Session', 'Bounce Rate', 'Avg. Session Duration',
        'New Users', 'Event Count', 'Exits'
    ])
    
    # Process date columns for easier handling
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)

    # Create new 'Leads' column based on "generate_lead"
    df['Leads'] = df.apply(lambda row: float(row['Event Count']) if row['Event Name'] == "generate_lead" else 0, axis=1)

    return df

# Updated summary functions remain the same, ensuring all metrics are grouped and aggregated appropriately.
