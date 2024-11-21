import streamlit as st
from llm_integration import query_gpt_keywordbuilder, initialize_llm_context
import json

# Set page configuration
st.set_page_config(page_title="Keyword Campaign Builder", layout="wide")

def main():
    # Initialize LLM session context
    initialize_llm_context()

    # Set up the app title
    st.title("Keyword Campaign Builder")

    # Step 1: Collect information about the business
    st.header("Step 1: Tell us about your business")
    st.write("Please enter a short prompt about your business, specific services, and what customers might search for "
             "if they were looking for a business like yours.")

    # Input field for user description
    business_description = st.text_area(
        "Business Description", 
        placeholder="E.g., 'A sports psychologist in Boise, Idaho, specializing in 1-on-1 coaching, team workshops, and mental performance plans. Customers might search for terms like 'sports psychologist,' 'sports mental coach,' or 'mental fatigue in athletes.'"
    )

    # Button to process and query LLM
    if st.button("Generate Keywords"):
        if business_description.strip():
            # Query the LLM using the provided description
            with st.spinner("Generating keyword suggestions..."):
                llm_response = query_gpt_keywordbuilder(
                    prompt=(
                        "Generate a list of potential paid search keywords grouped into ad groups based on the following business description. "
                        "Return the response as a JSON-formatted list of dictionaries, where each dictionary has the following structure: "
                        '{"Keyword": "Keyword 1", "Ad Group": "Ad Group 1"}. '
                        "Ensure that the only output is the JSON list of dictionaries with no additional text before or after."
                    ),
                    data_summary=business_description
                )

            # Extract the JSON part of the response
            json_start_index = llm_response.lower().find("json")
            if json_start_index != -1:
                json_text = llm_response[json_start_index + 4:].strip()  # Skip 'json' and trim extra spaces
                try:
                    keyword_list = json.loads(json_text)  # Parse JSON
                    st.success("Keywords generated and parsed successfully!")
                    st.write("Here is the parsed DataFrame:")
                    st.dataframe(keyword_list)  # Display as a DataFrame
                except json.JSONDecodeError:
                    st.error("Failed to parse the response as JSON. Please check the LLM output.")
                    st.write("Raw JSON Text:")
                    st.text_area("LLM Response", value=json_text, height=300)
            else:
                st.error("The response does not contain the keyword 'json'. Please check the LLM output.")
                st.write("Raw LLM Response:")
                st.text_area("LLM Response", value=llm_response, height=300)
        else:
            st.error("Please provide a description of your business before proceeding.")

if __name__ == "__main__":
    main()
