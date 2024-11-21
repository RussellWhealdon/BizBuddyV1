import streamlit as st
from llm_integration import query_gpt_keywordbuilder, initialize_llm_context

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
                        "Format the output as follows to make it easy to turn into a data frame: "
                        "'Keyword, Ad Group' on each line, where 'Keyword' is the search term, and 'Ad Group' is the group it belongs to. "
                        "The grouped keywords should be clear for campaign use, and the format should ensure easy processing into a DataFrame."
                    ),
                    data_summary=business_description
                )
            # Display the LLM response
            st.success("Keywords generated successfully!")
            st.write("Here are the keyword suggestions grouped into ad groups:")
            st.write(llm_response)

        else:
            st.error("Please provide a description of your business before proceeding.")

if __name__ == "__main__":
    main()
