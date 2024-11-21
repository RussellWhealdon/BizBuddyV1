import streamlit as st
from llm_integration import query_gpt_keywordbuilder, initialize_llm_context
import json
import re
import pandas as pd

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

    # Generate Keywords Button
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
                try:
                    keyword_list = json.loads(extracted_json)  # Parse JSON
                    st.session_state["keywords_df"] = pd.DataFrame(keyword_list)  # Save DataFrame in session state
                    st.session_state["selected_keywords"] = st.session_state["keywords_df"]["Keyword"].tolist()  # Initialize selected keywords
                except json.JSONDecodeError:
                    st.error("Failed to parse the extracted content as JSON. Please check the output.")
            else:
                st.error("Could not extract content inside brackets. Please check the LLM response.")

    # Display and allow editing of keywords if they exist in session state
    if "keywords_df" in st.session_state:
        st.header("Refine Keyword List")

        # Allow user to add new keywords
        st.subheader("Add a New Keyword")
        new_keyword = st.text_input("Enter a new keyword:")
        new_ad_group = st.selectbox("Select an ad group:", st.session_state["keywords_df"]["Ad Group"].unique())

        if st.button("Add Keyword"):
            if new_keyword.strip() and new_ad_group.strip():
                new_row = {"Keyword": new_keyword.strip(), "Ad Group": new_ad_group.strip()}
                updated_df = pd.concat([st.session_state["keywords_df"], pd.DataFrame([new_row])], ignore_index=True)
                st.session_state["keywords_df"] = updated_df
                st.session_state["selected_keywords"].append(new_keyword.strip())
                st.success(f"Added new keyword: '{new_keyword}' to Ad Group: '{new_ad_group}'!")
            else:
                st.error("Please enter a valid keyword and select an ad group.")

            # Multiselect widget for refining keywords with improved formatting
            st.subheader("Select Keywords to Keep")
            keyword_adgroup_pairs = [
                f"{kw} ({ad})" for kw, ad in zip(
                    st.session_state["keywords_df"]["Keyword"],
                    st.session_state["keywords_df"]["Ad Group"]
                )
            ]
            
            selected_keywords = st.multiselect(
                "Check keywords to include in the final list:",
                options=keyword_adgroup_pairs,
                default=[f"{kw} ({ad})" for kw, ad in zip(
                    st.session_state["selected_keywords"],
                    st.session_state["keywords_df"]["Ad Group"]
                )],
                help="The format is 'Keyword (Ad Group)'. Uncheck a term to remove it."
            )
            
            # Update the selected keywords in session state
            selected_keywords_cleaned = [kw.split(" (")[0] for kw in selected_keywords]  # Extract just the keywords
            st.session_state["selected_keywords"] = selected_keywords_cleaned

        # Filter the DataFrame based on the user's selection
        refined_df = st.session_state["keywords_df"][
            st.session_state["keywords_df"]["Keyword"].isin(st.session_state["selected_keywords"])
        ]

        st.dataframe(refined_df, use_container_width=True)

        # Button to accept the keywords
        if st.button("Okay"):
            st.success("Keywords accepted! Here is your final list:")
            st.dataframe(refined_df, use_container_width=True)

if __name__ == "__main__":
    main()
