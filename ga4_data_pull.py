from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric, Dimension

def fetch_ga4_metrics(property_id, start_date, end_date):
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="sessions"),
            Metric(name="newUsers"),
            Metric(name="averageSessionDuration"),
            Metric(name="bounceRate"),
            Metric(name="eventCount"),  # For conversions
            Metric(name="sessionsPerUser"),
            Metric(name="pageviews"),
        ],
        dimensions=[
            Dimension(name="sourceMedium"),  # Acquisition metrics
            Dimension(name="pagePath"),      # Content performance
            Dimension(name="exitPagePath"),  # Exit pages
            Dimension(name="eventName"),     # Filter for conversions
        ],
    )

    response = client.run_report(request)
    return response.rows

# Example of how this data could be processed:
def process_ga4_data(rows):
    metrics_data = {}
    for row in rows:
        dimension_values = row.dimension_values
        metric_values = row.metric_values
        
        # Process each metric and store it in a structured way
        # E.g., metrics_data['Total Visitors'] = metric_values[0].value
    return metrics_data
