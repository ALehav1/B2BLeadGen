"""Main module for B2B lead finder."""
import re
import json
import requests
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import random
import openai
import os
from dotenv import load_dotenv

class LeadFinder:
    """Main class for finding and analyzing B2B leads."""
    
    def __init__(self, openai_api_key: str):
        """Initialize the LeadFinder with OpenAI API key."""
        if not openai_api_key:
            raise ValueError("OpenAI API key is required")
        if not openai_api_key.startswith("sk-"):
            raise ValueError("Invalid OpenAI API key format")
            
        self.openai_api_key = openai_api_key
        self.openai_client = openai.Client(api_key=openai_api_key)
        self.cache = {}  # Cache for storing analyzed prospects
        self.excluded_companies = [
            "JPMorgan Chase", "Bank of America", "Citigroup", "Wells Fargo",
            "Goldman Sachs", "Morgan Stanley", "HSBC", "Barclays",
            "Deutsche Bank", "UBS", "Credit Suisse", "BNP Paribas"
        ]
        
        # Signal patterns to look for in company news and announcements
        self.signal_patterns = {
            'expansion': [
                r'expand(ing|s|ed)',
                r'grow(ing|s|th)',
                r'scal(ing|e|es)',
                r'new (market|product|service)',
                r'launch(ing|es|ed)'
            ],
            'technology': [
                r'digital transformation',
                r'moderniz(e|ing|ation)',
                r'technology upgrade',
                r'innovation'
            ],
            'funding': [
                r'investment',
                r'funding',
                r'capital raise',
                r'acquisition'
            ],
            'pain_points': [
                r'challenge(s)?',
                r'(operational )?issue(s)?',
                r'inefficien(t|cy)',
                r'problem(s)?',
                r'need(s)? to improve'
            ]
        }
    
    def analyze_product(self, product_description: str, company_name: str) -> Dict[str, Any]:
        """Analyze a product to identify target market and buying signals."""
        try:
            # First, analyze the product and target market
            analysis = self._analyze_target_market(product_description, company_name)
            
            # Split into sections
            sections = analysis.split('2. Key Buying Signals:')
            if len(sections) != 2:
                return {'success': False, 'error': 'Failed to parse analysis'}
                
            market_section = sections[0].replace('1. Target Market Characteristics:', '').strip()
            signals_section = sections[1].strip()
            
            # Extract bullet points
            features = [
                line.strip().strip('-').strip()
                for line in market_section.split('\n')
                if line.strip() and line.strip().startswith('-')
            ]
            
            signals = [
                line.strip().strip('-').strip()
                for line in signals_section.split('\n')
                if line.strip() and line.strip().startswith('-')
            ]

            return {
                'success': True,
                'product_features': features,
                'buying_signals': signals
            }

        except Exception as e:
            print(f"Error in analyze_product: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def find_matching_companies(self, product_description: str, company_name: str, 
                              market_analysis: str, callback=None, 
                              location_preference: str = None, 
                              company_types: str = None) -> List[Dict]:
        """Find companies that match the target market criteria."""
        cache_key = f"{product_description}_{company_name}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            companies = self._get_companies_list(location_preference, company_types)
            matching_companies = []
            total = len(companies)

            for i, company in enumerate(companies):
                if callback:
                    callback(i + 1, total)

                if company in self.excluded_companies:
                    continue

                match_reasons = self._evaluate_company_fit(
                    company, product_description, market_analysis)
                
                if match_reasons:
                    signals = self._get_company_signals(company)
                    value_prop = self._generate_value_proposition(
                        company, match_reasons, signals)
                    email = self._generate_email(
                        company, match_reasons, signals)
                    
                    matching_companies.append({
                        'company_name': company,
                        'match_reasons': match_reasons,
                        'recent_signals': signals,
                        'value_proposition': value_prop,
                        'email': email
                    })

            self.cache[cache_key] = matching_companies
            return matching_companies

        except Exception as e:
            print(f"Error finding matching companies: {e}")
            return []

    def _analyze_target_market(self, product_description: str, company_name: str) -> str:
        """Analyze target market and generate initial analysis."""
        try:
            prompt = f"""Analyze the ideal target market for {company_name}'s product: {product_description}

Please provide a detailed analysis in two parts:

1. Target Market Characteristics:
- Company sizes
- Industry verticals
- Common pain points
- Technical requirements
- Budget considerations

2. Key Buying Signals:
- Trigger events
- Business changes
- Industry trends
- Technology adoption patterns
- Growth indicators

Format as bullet points for each section."""

            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a market research expert specializing in B2B markets."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error analyzing target market: {e}")
            return "Error analyzing target market."

    def _get_companies_list(self, location_preference: str = None, 
                           company_types: str = None) -> List[str]:
        """Get list of companies to analyze based on preferences."""
        try:
            prompt = "Generate a list of 5 potential companies to analyze."
            if location_preference or company_types:
                prompt += "\nPreferences:"
                if location_preference:
                    prompt += f"\n- Location: {location_preference}"
                if company_types:
                    prompt += f"\n- Company Types: {company_types}"
            else:
                prompt += "\nFocus on public companies across different industries."

            prompt += "\nExclude major banks and financial institutions."

            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a B2B market researcher. List only company names, one per line."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            companies = [
                company.strip() 
                for company in response.choices[0].message.content.strip().split('\n')
                if company.strip() and company.strip() not in self.excluded_companies
            ]
            return companies[:5]

        except Exception as e:
            print(f"Error getting companies list: {e}")
            return []

    def _evaluate_company_fit(self, company_name: str, product_description: str, market_analysis: str) -> List[str]:
        """Evaluate how well a company fits the target market criteria."""
        try:
            prompt = f"""Evaluate how well {company_name} fits the target market criteria for {product_description}:

Target Market Analysis:
{market_analysis}

Please provide a list of reasons why {company_name} is a good fit for this product, based on their recent business activities and market position.

Format as bullet points."""

            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a B2B market analyst. Focus on specific, actionable insights."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            reasons = [
                line.strip().strip('-').strip()
                for line in response.choices[0].message.content.strip().split('\n')
                if line.strip() and line.strip().startswith('-')
            ]

            return reasons

        except Exception as e:
            print(f"Error evaluating company fit: {e}")
            return []

    def _get_company_signals(self, company_name: str) -> List[str]:
        """Get recent signals and news about a company that indicate potential fit."""
        try:
            prompt = f"""Analyze {company_name} as a potential customer based on recent business activities and market position.

Please provide a list of recent signals that indicate potential fit, such as:

- Recent announcements or news
- Business changes or initiatives
- Industry trends or adoption patterns
- Growth indicators or financial performance

Format as bullet points."""

            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a B2B sales researcher. Focus on recent, specific evidence of need and concrete reasons for fit. Include dates where possible."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            signals = [
                line.strip().strip('-').strip()
                for line in response.choices[0].message.content.strip().split('\n')
                if line.strip() and line.strip().startswith('-')
            ]

            return signals

        except Exception as e:
            print(f"Error getting company signals: {e}")
            return []

    def _generate_value_proposition(self, company_name: str, match_reasons: List[str], signals: List[str]) -> str:
        """Generate a personalized value proposition based on company signals."""
        try:
            prompt = f"""Generate a compelling value proposition for {company_name} based on:

Match Reasons:
{chr(10).join(f'- {reason}' for reason in match_reasons)}

Recent Signals:
{chr(10).join(f'- {signal}' for signal in signals)}

Requirements:
1. Focus on their specific pain points from the match reasons
2. Explain how we solve their unique challenges
3. Highlight the business value we provide
4. Keep it concise (2-3 sentences)
5. Make it specific to their needs
6. Do NOT start with 'Dear' or any greeting - this is a value proposition, not an email

Example format:
"Our [solution type] helps [company type] like [company name] [achieve specific benefit] by [explanation of how]. This addresses your [specific pain point] while [additional benefit], ultimately [business impact]."
"""

            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a B2B sales expert who writes compelling, focused value propositions. Focus on concrete benefits and specific pain points."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error generating value proposition: {e}")
            return None

    def _generate_email(self, company_name: str, match_reasons: List[str], signals: List[str]) -> str:
        """Generate a personalized email based on company match reasons and signals."""
        return ""  # Email generation removed

    def callback(self, message: str):
        """Callback function for progress updates."""
        print(message)

def run_lead_finder(product_name, company_name, num_leads=10, is_existing_product=True):
    """Run the lead finder with the given product description."""
    try:
        # Initialize components
        finder = LeadFinder(os.getenv("OPENAI_API_KEY"))
        
        # Analyze product and find prospects
        result = finder.analyze_product(product_name, company_name)
        
        if result['success']:
            analysis = result
            target_market = analysis['product_features']
            buying_signals = analysis['buying_signals']
            prospects = finder.find_matching_companies(product_name, company_name, 
                              "\n".join(f"- {feature}" for feature in target_market), 
                              callback=finder.callback)
            
            # Print criteria
            print("\nIdeal Prospect Criteria:")
            for category, items in finder._get_ideal_prospect_criteria(target_market).items():
                print(f"\n{category.replace('_', ' ').title()}:")
                for item in items:
                    print(f"- {item}")
            
            # Print prospects
            print("\nTop Matching Prospects:")
            for prospect in prospects:
                print(f"\n{prospect['company_name']}")
                print("Recent Signals:")
                for signal in prospect['recent_signals']:
                    print(f"- {signal}")
                print("\nMatch Reasons:")
                for reason in prospect['match_reasons']:
                    print(f"- {reason}")
                print("\nValue Proposition:")
                print(prospect['value_proposition'])
                print("\nEmail:")
                print(prospect['email'])
                print("\n---")
        else:
            print(f"Error: {result['error']}")
            
    except Exception as e:
        print(f"Error running lead finder: {e}")

def main():
    """Run the lead finder."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python main.py <product_name> <company_name>")
        sys.exit(1)
    
    product_name = sys.argv[1]
    company_name = sys.argv[2]
    
    print("\nB2B Lead Finder")
    print("---------------")
    print(f"\nAnalyzing {product_name} by {company_name}...")
    
    run_lead_finder(product_name, company_name)

if __name__ == "__main__":
    main()
