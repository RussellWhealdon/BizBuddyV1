from google.ads.googleads.client import GoogleAdsClient
import os

# Load Google Ads client from a configuration file
client = GoogleAdsClient.load_from_storage("google-ads.yaml")

# Customer ID of the test account
CUSTOMER_ID = "INSERT_TEST_ACCOUNT_ID"  # Replace with your test account ID

def create_budget(client, customer_id):
    """Creates a campaign budget."""
    budget_service = client.get_service("CampaignBudgetService")
    budget_operation = client.get_type("CampaignBudgetOperation")
    budget = budget_operation.create
    budget.name = "Test Budget"
    budget.amount_micros = 1000000  # $1.00 daily budget
    budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    response = budget_service.mutate_campaign_budgets(customer_id=customer_id, operations=[budget_operation])
    print(f"Created budget: {response.results[0].resource_name}")
    return response.results[0].resource_name

def create_campaign(client, customer_id, budget_resource_name):
    """Creates a campaign."""
    campaign_service = client.get_service("CampaignService")
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = "Test Campaign"
    campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
    campaign.status = client.enums.CampaignStatusEnum.PAUSED
    campaign.campaign_budget = budget_resource_name
    campaign.manual_cpc.CopyFrom(client.get_type("ManualCpc"))
    campaign.start_date = "2024-01-01"
    campaign.end_date = "2024-12-31"
    response = campaign_service.mutate_campaigns(customer_id=customer_id, operations=[campaign_operation])
    print(f"Created campaign: {response.results[0].resource_name}")
    return response.results[0].resource_name

def create_ad_group(client, customer_id, campaign_resource_name):
    """Creates an ad group."""
    ad_group_service = client.get_service("AdGroupService")
    ad_group_operation = client.get_type("AdGroupOperation")
    ad_group = ad_group_operation.create
    ad_group.name = "Test Ad Group"
    ad_group.campaign = campaign_resource_name
    ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
    ad_group.cpc_bid_micros = 100000  # $0.10 CPC
    response = ad_group_service.mutate_ad_groups(customer_id=customer_id, operations=[ad_group_operation])
    print(f"Created ad group: {response.results[0].resource_name}")
    return response.results[0].resource_name

def add_keywords(client, customer_id, ad_group_resource_name):
    """Adds keywords to the ad group."""
    keywords = ["nutrition counseling", "eating disorder recovery", "dietitian near me"]
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    operations = []
    for keyword in keywords:
        criterion_operation = client.get_type("AdGroupCriterionOperation")
        criterion = criterion_operation.create
        criterion.ad_group = ad_group_resource_name
        criterion.keyword.text = keyword
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        operations.append(criterion_operation)
    response = ad_group_criterion_service.mutate_ad_group_criteria(customer_id=customer_id, operations=operations)
    for result in response.results:
        print(f"Added keyword: {result.resource_name}")

def create_ads(client, customer_id, ad_group_resource_name):
    """Creates ads in the ad group."""
    ad_service = client.get_service("AdGroupAdService")
    ad_operation = client.get_type("AdGroupAdOperation")
    ad = ad_operation.create
    ad.ad_group = ad_group_resource_name
    ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
    ad.ad.expanded_text_ad.headline_part1 = "Affordable Nutrition Counseling"
    ad.ad.expanded_text_ad.headline_part2 = "Personalized Plans"
    ad.ad.expanded_text_ad.description = "Helping adults with eating disorders."
    response = ad_service.mutate_ad_group_ads(customer_id=customer_id, operations=[ad_operation])
    print(f"Created ad: {response.results[0].resource_name}")

def enable_campaign(client, customer_id, campaign_resource_name):
    """Enables the campaign."""
    campaign_service = client.get_service("CampaignService")
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.update
    campaign.resource_name = campaign_resource_name
    campaign.status = client.enums.CampaignStatusEnum.ENABLED
    client.copy_from(campaign_operation.update_mask, client.get_type("FieldMask", message=campaign._pb))
    response = campaign_service.mutate_campaigns(customer_id=customer_id, operations=[campaign_operation])
    print(f"Enabled campaign: {response.results[0].resource_name}")

def main():
    """Main function to run the test campaign setup."""
    budget_resource_name = create_budget(client, CUSTOMER_ID)
    campaign_resource_name = create_campaign(client, CUSTOMER_ID, budget_resource_name)
    ad_group_resource_name = create_ad_group(client, CUSTOMER_ID, campaign_resource_name)
    add_keywords(client, CUSTOMER_ID, ad_group_resource_name)
    create_ads(client, CUSTOMER_ID, ad_group_resource_name)
    enable_campaign(client, CUSTOMER_ID, campaign_resource_name)

if __name__ == "__main__":
    #main()
