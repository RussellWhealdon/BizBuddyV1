import streamlit as st

# Set page configuration
st.set_page_config(page_title="Keyword Campaign Builder", layout="wide")

def main():
    # Set up the app title
    st.title("Keyword Campaign Builder")

    # Step 1: Collect information about the business
    st.header("Step 1: Tell us about your business")
    st.write("Enter a short description of your business, the specific services you provide, "
             "and what customers might search for when looking for a business like yours.")

    # Input fields for user description
    business_name = st.text_input("Business Name", placeholder="E.g., Chelsea Whealdon Nutrition")
    business_description = st.text_area("Business Description", 
                                         placeholder="Describe your business, services, and target audience...")
    customer_search_terms = st.text_area("Customer Search Terms",
                                         placeholder="List any words or phrases customers might use to find you...")

    # Button to proceed to the next step
    if st.button("Next Step"):
        st.success("Thank you! Proceeding to the next step...")
        # In the next step, you would add logic to process this input and proceed further

if __name__ == "__main__":
    main()
