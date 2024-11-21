import streamlit as st
from llm_integration import query_gpt_keywordbuilder, initialize_llm_context
import json
import re

# Set page configuration
st.set_page_config(page_title="Keyword Campaign Builder", layout="wide")

def extract_json_like_content(response):
    """
    Extracts the content inside the first matched brackets: [ ... ].
    Returns the content including the brackets.
    """
    try:
        # Use regex to find the first occurrence of [ ... ]
        match = re.search(r"\[.*?\]", response, re.DOTALL)
        if match:
            return match.group(0)  # Return the matched string, including brackets
        else:
            return None
    except Exception as e:
        return None

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
                        "Generate a list of exactly 15 paid search keywords grouped into 3 ad groups based on the following business description. "
                        "Each ad group should contain 5 keywords. "
                        "Return the response as a JSON-formatted list of dictionaries, where each dictionary has the following structure: "
                        '{"Keyword": "Keyword 1", "Ad Group": "Ad Group 1"}. '
                        "Ensure that the only output is the JSON list of dictionaries with no additional text before or after."
                    ),
                    data_summary=business_description
                )

            # Extract content inside brackets
            extracted_json = extract_json_like_content(llm_response)

            if extracted_json:
                st.success("Keywords extracted successfully!")
                st.write("Extracted Content:")
                st.text_area("Extracted JSON-Like Content", value=extracted_json, height=300)

                # Attempt to parse the JSON-like content
                try:
                    keyword_list = json.loads(extracted_json)  # Parse JSON
                    st.write("Parsed DataFrame:")
                    st.dataframe(keyword_list, use_container_width=True)  # Display as a DataFrame with full width
                except json.JSONDecodeError:
                    st.error("Failed to parse the extracted content as JSON. Please check the output.")
            else:
                st.error("Could not extract content inside brackets. Please check the LLM response.")
                st.write("Raw LLM Response:")
                st.text_area("LLM Response", value=llm_response, height=300)

        else:
            st.error("Please provide a description of your business before proceeding.")

if __name__ == "__main__":
    main()
