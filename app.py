"""Streamlit app for B2B lead finder."""
import streamlit as st
import os
from dotenv import load_dotenv
from main import LeadFinder

def main():
    # Load environment variables
    load_dotenv(override=True)
    
    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key not found. Please make sure it's set in your .env file.")
        return

    st.title("B2B Lead Finder")
    
    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'market_analysis' not in st.session_state:
        st.session_state.market_analysis = None
    if 'stop_requested' not in st.session_state:
        st.session_state.stop_requested = False
    if 'emails' not in st.session_state:
        st.session_state.emails = {}

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Step 1: Product Information")
        
        product_description = st.text_input("What's your product?")
        company_name = st.text_input("What's your company name?")
        
        analyze_button = st.button("Analyze Product")
        if analyze_button and product_description and company_name:
            with st.spinner('Analyzing product...'):
                status_area = st.empty()
                progress_bar = st.progress(0)
                
                try:
                    finder = LeadFinder(api_key)
                    
                    # First analyze the product and target market
                    market_analysis = finder._analyze_target_market(product_description, company_name)
                    st.session_state.market_analysis = market_analysis
                    st.success('Market analysis complete!')
                    st.session_state.step = 2
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    return
        elif analyze_button:
            st.warning("Please enter both product name and company name.")
            
        # Only show Step 2 if market analysis is complete
        if st.session_state.step >= 2 and st.session_state.market_analysis:
            st.subheader("Market Analysis")
            
            # Display and allow editing of market analysis
            edited_analysis = st.text_area("Review and edit the analysis:", 
                                         value=st.session_state.market_analysis, 
                                         height=300)
            st.session_state.market_analysis = edited_analysis
            
            st.subheader("Step 2: Find Prospects")
            
            # Search preferences in expandable section
            with st.expander("", expanded=True):
                col3, col4 = st.columns(2)
                with col3:
                    location_pref = st.text_input("Preferred location (e.g., 'US West Coast', 'Europe'):")
                with col4:
                    company_types = st.text_input("Preferred company types (e.g., 'SaaS', 'Manufacturing'):")
            
            col5, col6 = st.columns(2)
            with col5:
                find_button = st.button("Find Matching Companies")
            with col6:
                stop_button = st.button("Stop Search")
                if stop_button:
                    st.session_state.stop_requested = True
            
            if find_button:
                with st.spinner('Finding matching companies...'):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    def update_progress(current, total):
                        if st.session_state.stop_requested:
                            st.warning("Search stopped by user.")
                            st.stop()
                        progress = int((current / total) * 100)
                        progress_bar.progress(progress)
                        status_text.text(f"Analyzing company {current} of {total}")
                    
                    try:
                        finder = LeadFinder(api_key)
                        matching_companies = finder.find_matching_companies(
                            product_description,
                            company_name,
                            st.session_state.market_analysis,
                            callback=update_progress,
                            location_preference=location_pref if location_pref else None,
                            company_types=company_types if company_types else None
                        )
                        
                        st.session_state.stop_requested = False
                        status_text.text("Analysis complete!")
                        
                        if matching_companies:
                            st.subheader("Matching Companies")
                            for prospect in matching_companies:
                                with st.expander(f"🏢 {prospect['company_name']}", expanded=True):
                                    # Match reasons with reduced padding
                                    st.markdown("""
                                    <div style='background-color: #f8f9fa; padding: 12px; border-radius: 8px; margin-bottom: 12px;'>
                                        <h4 style='color: #2c3e50; margin: 0 0 8px 0;'>Why They're a Good Prospect</h4>
                                        <div style='margin-left: 12px; background-color: white; padding: 10px; border-radius: 5px;'>
                                    """, unsafe_allow_html=True)
                                    
                                    for reason in prospect['match_reasons']:
                                        st.markdown(f"• {reason}")
                                    
                                    st.markdown("</div></div>", unsafe_allow_html=True)
                                    
                                    # Recent signals with reduced padding
                                    st.markdown("""
                                    <div style='background-color: #f8f9fa; padding: 12px; border-radius: 8px; margin-bottom: 12px;'>
                                        <h4 style='color: #2c3e50; margin: 0 0 8px 0;'>Recent Events & Signals</h4>
                                        <div style='margin-left: 12px; background-color: white; padding: 10px; border-radius: 5px;'>
                                    """, unsafe_allow_html=True)
                                    
                                    for signal in prospect['recent_signals']:
                                        st.markdown(f"• {signal}")
                                    
                                    st.markdown("</div></div>", unsafe_allow_html=True)
                                    
                                    # Value proposition
                                    value_prop = prospect['value_proposition']
                                    if value_prop:
                                        st.markdown(f"""
                                        <div style='background-color: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 10px;'>
                                            <h4 style='color: #2c3e50; margin: 0 0 5px 0;'>💡 Value Proposition</h4>
                                            <div style='margin-left: 10px; background-color: white; padding: 8px; border-radius: 5px;'>
                                                <p style='color: #2c3e50; line-height: 1.4; margin: 0;'>{value_prop}</p>
                                            </div>
                                        </div>
                                        """, unsafe_allow_html=True)

                                    # Email Generation - Removed
                                    # if st.button("Generate Email", key=f"btn_{prospect['company_name']}"):
                                    #     with st.spinner('Generating email...'):
                                    #         try:
                                    #             email = finder._generate_email(
                                    #                 prospect['company_name'],
                                    #                 prospect['match_reasons'],
                                    #                 prospect['recent_signals']
                                    #             )
                                    #             if email:
                                    #                 email_parts = email.split('\n', 1)
                                    #                 if len(email_parts) == 2:
                                    #                     subject = email_parts[0].replace('Subject:', '').strip()
                                    #                     body = email_parts[1].strip()
                                    #                     st.markdown(f"""
                                    #                     <div style='background-color: #f8f9fa; padding: 10px; border-radius: 8px;'>
                                    #                         <h4 style='color: #2c3e50; margin: 0 0 5px 0;'>📧 Personalized Email</h4>
                                    #                         <div style='margin-left: 10px; background-color: white; padding: 8px; border-radius: 5px;'>
                                    #                             <p style='color: #2c3e50; margin: 0 0 5px 0;'><strong>Subject:</strong> {subject}</p>
                                    #                             <hr style='margin: 5px 0;'>
                                    #                             <div style='color: #2c3e50; white-space: pre-line; line-height: 1.4;'>{body}</div>
                                    #                         </div>
                                    #                     </div>
                                    #                     """, unsafe_allow_html=True)
                                    #         except Exception as e:
                                    #             st.error(f"Failed to generate email: {str(e)}")
                        else:
                            st.warning("No matching companies found.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                    finally:
                        st.session_state.stop_requested = False

    with col2:
        st.markdown("""
        ### How it works
        
        This tool helps you find and qualify potential B2B leads by:
        
        1. **Analyzing Your Product**
           - Market characteristics
           - Ideal customer profile
           - Key buying signals
        
        2. **Finding Prospects**
           - Company matching
           - Signal detection
           - Fit analysis
        
        3. **Qualifying Leads**
           - Match scoring
           - Recent events
           - Growth signals
        
        4. **Generating Outreach**
           - Value propositions
           - Personalized emails
           - Trigger events
        
        ### Tips for Best Results
        
        - Be specific about your product
        - Review and edit the analysis
        - Use location preferences
        - Filter by company type
        """)

if __name__ == "__main__":
    main()
