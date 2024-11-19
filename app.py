import streamlit as st
from main import run_lead_finder, analyze_product_description
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def main():
    st.set_page_config(
        page_title="B2B Lead Finder",
        page_icon="🎯",
        layout="wide"
    )

    st.title("🎯 B2B Lead Finder")
    
    # Mode selection
    mode = st.radio(
        "Choose your mode",
        ["Existing Product", "Product Idea"],
        help="Choose 'Existing Product' to find leads for a real product, or 'Product Idea' to test market fit for a hypothetical product"
    )

    if mode == "Existing Product":
        st.markdown("""
        ### Existing Product Mode
        Describe your product as you would to a potential customer. Focus on what it does and the problems it solves.
        """)
        
        example_description = """
        CreditLens is a cloud-based credit origination and risk assessment platform that helps financial institutions 
        streamline their lending operations. It automates the entire lending process from application to decision, 
        reducing manual work and ensuring consistent risk assessment across all loans.
        """
        
        product_description = st.text_area(
            "Product Description",
            placeholder=example_description,
            height=150,
            help="Describe what your product does and the problems it solves. Be specific about its features and benefits."
        )

    else:  # Product Idea mode
        st.markdown("""
        ### Product Idea Mode
        Describe your product concept and specify your target market to test potential market fit.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            product_description = st.text_area(
                "Product Concept",
                placeholder="Describe your product idea and its key features...",
                height=150
            )
        
        with col2:
            target_market = st.text_area(
                "Target Market Criteria (Optional)",
                placeholder="Describe your ideal customer profile...",
                height=150
            )

    num_leads = st.slider("Number of leads to find", min_value=1, max_value=10, value=3)

    # Process button with loading animation
    if st.button("Find Leads", type="primary"):
        if not product_description:
            st.error("Please provide a product description.")
            return

        # Create a placeholder for the progress bar
        progress_placeholder = st.empty()
        
        # Create placeholders for different stages
        analysis_status = st.empty()
        search_status = st.empty()
        qualification_status = st.empty()

        try:
            with st.spinner():
                # Show progress stages
                analysis_status.info("🔍 Analyzing product description...")
                if mode == "Existing Product":
                    # Analyze product description to determine target market
                    target_market = analyze_product_description(product_description)
                    time.sleep(1)  # Give user time to see the analysis happening
                    
                search_status.info("🌐 Searching for potential leads...")
                results = run_lead_finder(
                    product_description=product_description,
                    target_market=target_market if mode == "Product Idea" else None,
                    num_leads=num_leads
                )
                time.sleep(1)  # Give user time to see the search happening
                
                qualification_status.info("⚖️ Qualifying leads...")
                time.sleep(1)  # Give user time to see the qualification happening

                # Clear status messages
                analysis_status.empty()
                search_status.empty()
                qualification_status.empty()

                # Display results
                if results:
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
                else:
                    st.warning("No leads found. Try adjusting your product description or target market criteria.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Add footer with GitHub link
    st.markdown("---")
    st.markdown(
        "[![GitHub](https://img.shields.io/badge/GitHub-View_Source-lightgrey?logo=github&style=social)](https://github.com/ALehav1/B2BLeadGen)"
    )

if __name__ == "__main__":
    main()
