import streamlit as st
from main import run_lead_finder
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    st.set_page_config(
        page_title="B2B Lead Finder",
        page_icon="🎯",
        layout="wide"
    )

    st.title("🎯 B2B Lead Finder")
    st.markdown("""
    This tool helps you find and qualify B2B leads based on your product description 
    and target market criteria.
    """)

    # Input section
    st.header("Input Parameters")
    col1, col2 = st.columns(2)

    with col1:
        product_description = st.text_area(
            "Product Description",
            placeholder="Describe your product or service...",
            height=150
        )

    with col2:
        target_market = st.text_area(
            "Target Market Criteria",
            placeholder="Describe your ideal customer profile...",
            height=150
        )

    num_leads = st.slider("Number of leads to find", min_value=1, max_value=10, value=3)

    # Process button
    if st.button("Find Leads", type="primary"):
        if not product_description or not target_market:
            st.error("Please fill in both the product description and target market criteria.")
            return

        with st.spinner("Finding and analyzing leads... This may take a few minutes..."):
            try:
                results = run_lead_finder(
                    product_description=product_description,
                    target_market=target_market,
                    num_leads=num_leads
                )

                # Display results
                st.header("Results")
                for idx, lead in enumerate(results, 1):
                    with st.expander(f"Lead {idx}: {lead.get('company_name', 'Unknown Company')}"):
                        st.markdown(f"**Company Name:** {lead.get('company_name', 'N/A')}")
                        st.markdown(f"**Website:** {lead.get('website', 'N/A')}")
                        st.markdown(f"**Description:** {lead.get('description', 'N/A')}")
                        st.markdown("**Match Analysis:**")
                        st.markdown(lead.get('match_analysis', 'N/A'))
                        st.markdown("**Contact Information:**")
                        st.markdown(lead.get('contact_info', 'N/A'))

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # Add footer with GitHub link
    st.markdown("---")
    st.markdown(
        "[![GitHub](https://img.shields.io/badge/GitHub-View_Source-lightgrey?logo=github&style=social)](https://github.com/ALehav1/B2BLeadGen)"
    )

if __name__ == "__main__":
    main()
