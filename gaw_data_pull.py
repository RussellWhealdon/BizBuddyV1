import pandas as pd
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import streamlit as st

def fetch_keyword_data(customer_id, location_ids, language_id, page_url):
    # Load credentials from Streamlit secrets
    credentials_dict = {
        "developer_token": st.secrets["google_ads"]["developer_token"],
        "client_id": st.secrets["google_ads"]["client_id"],
        "client_secret": st.secrets["google_ads"]["client_secret"],
        "refresh_token": st.secrets["google_ads"]["refresh_token"],
        "login_customer_id": None,  # Optional for test accounts
        "use_proto_plus": True
    }
    
    # Location and language constants (New York, NY and English as defaults)
    location_ids = ["1014044"]
    language_id = "1000"  # English

    # Website URL for generating keyword ideas
    try:
        client = GoogleAdsClient.load_from_dict(credentials_dict, version="v18")

        # KeywordPlanIdeaService
        keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")

        # Create request
        request = client.get_type("GenerateKeywordIdeasRequest")
        request.customer_id = customer_id
        request.language = client.get_service("GoogleAdsService").language_constant_path(language_id)
        request.geo_target_constants.extend([
            client.get_service("GeoTargetConstantService").geo_target_constant_path(location_id)
            for location_id in location_ids
        ])
        request.url_seed.url = page_url

        # Fetch keyword ideas
        response = keyword_plan_idea_service.generate_keyword_ideas(request=request)

        # Collect data
        data = []
        for idea in response:
            metrics = idea.keyword_idea_metrics
            data.append({
                "Keyword": idea.text,
                "Avg Monthly Searches": metrics.avg_monthly_searches,
                "Competition": metrics.competition.name,
                "Low Top of Page Bid (micros)": metrics.low_top_of_page_bid_micros,
                "High Top of Page Bid (micros)": metrics.high_top_of_page_bid_micros
            })

        # Convert to DataFrame
        return pd.DataFrame(data)

    except GoogleAdsException as ex:
        st.error(f"GoogleAdsException occurred: {ex}")
        return pd.DataFrame()  # Return an empty DataFrame on failure

def generate_seo_insights(search_data):
    # Prepare the search query list
    query_list = search_data["Search Query"].unique()
    formatted_queries = "\n".join(query_list)

    # Define the prompt for the LLM
    prompt = (
        "Here are the search queries this website currently appears for:\n"
        f"{formatted_queries}\n\n"
        "Based on this data, please provide the following:\n"
        "- Target search terms that align with the website's goals.\n"
        "- New niche ideas for search terms that could improve conversions.\n"
        "- A brief explanation of why SEO optimization is critical for this business."
    )

    # Call the LLM using query_gpt
    response = query_gpt(prompt)
    return response
