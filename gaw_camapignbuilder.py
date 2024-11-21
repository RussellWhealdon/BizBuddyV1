import streamlit as st
import llm_integration

# Set page configuration
st.set_page_config(page_title="Keyword Campaign Builder", layout="wide")

def main():

    # Set up the app title
    st.title("Keyword Campaign Builder")

    # Step 1: Collect information about the business
    st.header("Step 1: Tell us about your business")
    st.write("Please enter a short prompt about your business, specific services, and what customers might search for "
             "if they were looking for a business like yours.")

    # Input field for user description
    business_description = st.text_area(
        "Business Description", 
        placeholder="E.g., 'A nutrition counseling service specializing in eating disorder recovery, intuitive eating, and chronic disease management. Customers might search for terms like 'nutritionist near me,' 'eating disorder dietitian,' or 'virtual dietitian.'"
    )

    # Button to process and query LLM
    if st.button("Generate Keywords"):
        if business_description.strip():
            # Query the LLM using the provided description
            with st.spinner("Generating keyword suggestions..."):
                llm_response = query_gpt_keywordbuilder(
                    prompt=(
                        "Generate a list of potential paid search keywords grouped into ad groups based on the following business description. "
                        "At the end of the response, include all keywords in the campaign, separated by commas, and prefixed by a '|' character. "
                        "The grouped keywords should be clear for campaign use, and the final list of all keywords should allow easy extraction."
                    ),
                    data_summary=business_description
                )
            # Display the LLM response
            st.success("Keywords generated successfully!")
            st.write("Here are the keyword suggestions grouped into ad groups:")
            st.write(llm_response)

            # Extract keywords if the response includes a "|"
            if "|" in llm_response:
                all_keywords = llm_response.split("|")[-1].strip()
                st.write("Extracted Keywords for Campaign:")
                st.write(all_keywords)
        else:
            st.error("Please provide a description of your business before proceeding.")

if __name__ == "__main__":
    main()
