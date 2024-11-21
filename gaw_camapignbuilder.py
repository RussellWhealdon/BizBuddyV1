import streamlit as st

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
    business_description = st.text_area("Business Description", 
                                         placeholder="E.g., 'A nutrition counseling service specializing in eating disorder recovery, intuitive eating, and chronic disease management. Customers might search for terms like 'nutritionist near me,' 'eating disorder dietitian,' or 'virtual dietitian.'")

    # Button to proceed to the next step
    if st.button("Next Step"):
        if business_description.strip():
            st.success("Thank you! Proceeding to the next step...")
            # In the next step, you would add logic to process this input and proceed further
        else:
            st.error("Please provide a description of your business before proceeding.")

if __name__ == "__main__":
    main()
