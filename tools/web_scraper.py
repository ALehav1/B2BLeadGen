"""Web scraping tool for gathering company information."""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List
from urllib.parse import quote
import logging
import time
import random
import json

logger = logging.getLogger(__name__)

class WebScraper:
    """Web scraping tool for gathering company information."""

    def __init__(self):
        """Initialize the web scraper tool."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Test data for different companies
        self.test_data = {
            "JPMorgan Chase": {
                "name": "JPMorgan Chase",
                "description": "Global financial services firm and banking leader",
                "content": """
                Leading global financial institution with significant commercial and consumer lending operations.
                Major initiatives in credit risk management and portfolio monitoring.
                Investing heavily in technology modernization and automation.
                Expanding digital lending capabilities and analytics.
                Focus on regulatory compliance and risk management.
                Growing commercial loan portfolio across multiple sectors.
                """
            },
            "Bank of America": {
                "name": "Bank of America",
                "description": "Multinational investment bank and financial services company",
                "content": """
                Major US bank with extensive lending operations.
                Significant investment in credit technology modernization.
                Focus on commercial and consumer lending growth.
                Enhanced risk management capabilities.
                Digital transformation initiatives.
                Portfolio expansion across multiple segments.
                """
            },
            "PNC Bank": {
                "name": "PNC Bank",
                "description": "Regional banking institution",
                "content": """
                Regional bank expanding commercial lending operations.
                Modernizing credit assessment processes.
                Focus on middle market lending growth.
                Implementing new risk management systems.
                Digital banking transformation.
                Regional expansion initiatives.
                """
            },
            "Fifth Third Bank": {
                "name": "Fifth Third Bank",
                "description": "Regional bank with commercial focus",
                "content": """
                Growing regional bank with commercial focus.
                Expanding commercial lending portfolio.
                Modernizing credit operations.
                Enhanced risk management focus.
                Digital transformation projects.
                Market expansion plans.
                """
            },
            "Navy Federal Credit Union": {
                "name": "Navy Federal Credit Union",
                "description": "Large credit union serving military members",
                "content": """
                Leading credit union with focus on consumer lending.
                Modernizing lending operations.
                Enhanced member services.
                Risk management improvements.
                Digital banking initiatives.
                Growing consumer portfolio.
                """
            },
            "State Employees Credit Union": {
                "name": "State Employees Credit Union",
                "description": "State-focused credit union",
                "content": """
                Large state credit union with consumer focus.
                Expanding consumer lending programs.
                Credit process modernization.
                Risk management enhancement.
                Digital service expansion.
                Member-focused growth.
                """
            },
            "Affirm": {
                "name": "Affirm",
                "description": "Fintech company specializing in lending",
                "content": """
                Leading fintech lender with innovative credit products.
                Advanced technology platform.
                Rapid portfolio growth.
                Data-driven risk management.
                Expanding merchant partnerships.
                New product innovation.
                """
            },
            "OnDeck Capital": {
                "name": "OnDeck Capital",
                "description": "Online small business lender",
                "content": """
                Online lender focused on small business.
                Technology-driven credit assessment.
                Automated lending processes.
                Risk analytics platform.
                Market expansion initiatives.
                Product innovation focus.
                """
            },
            "Goldman Sachs": {
                "name": "Goldman Sachs",
                "description": "Global investment banking leader",
                "content": """
                Global investment bank with significant lending operations.
                Complex credit products.
                Advanced risk management.
                Technology modernization.
                Portfolio expansion.
                Innovation initiatives.
                """
            },
            "Morgan Stanley": {
                "name": "Morgan Stanley",
                "description": "Multinational investment bank",
                "content": """
                Major investment bank with diverse lending operations.
                Sophisticated credit products.
                Advanced risk analytics.
                Technology transformation.
                Business expansion.
                Innovation focus.
                """
            }
        }

    def get_test_companies(self):
        """Get test company data with realistic urgent signals."""
        return [
            {
                'name': 'First Regional Bank of the Midwest',
                'type': 'regional_bank',
                'size': 'medium',
                'description': """
                First Regional Bank of the Midwest announced on 15 June 2023 its acquisition of Community Trust Bank, 
                expanding its presence across three new states. The merger will triple their commercial loan portfolio 
                to $12B. CEO Sarah Johnson highlighted the immediate need to standardize credit assessment processes 
                across all branches and ensure consistent risk management practices. The bank is currently operating 
                separate legacy systems from both institutions, causing delays in credit decisions and raising 
                concerns about risk visibility.
                """,
                'executive_name': 'Sarah Johnson',
                'role': 'Chief Executive Officer'
            },
            {
                'name': 'TechFin Solutions',
                'type': 'alternative_lender',
                'size': 'medium',
                'description': """
                Leading fintech lender TechFin Solutions reported on 1 July 2023 a 300% growth in their commercial 
                lending portfolio over the past quarter. The rapid expansion has highlighted limitations in their 
                current credit assessment infrastructure. Recent regulatory audit on 10 July 2023 identified 
                inconsistencies in their credit risk evaluation process, particularly in handling complex commercial 
                loans. The company is actively seeking solutions to scale their credit operations while ensuring 
                regulatory compliance.
                """,
                'executive_name': 'Michael Chang',
                'role': 'Chief Risk Officer'
            },
            {
                'name': 'Atlantic Credit Union',
                'type': 'credit_union',
                'size': 'large',
                'description': """
                Atlantic Credit Union is experiencing significant challenges with their legacy credit assessment 
                system as of May 2023. Recent regulatory changes requiring enhanced stress testing and portfolio 
                monitoring have put strain on their manual processes. The credit union's board approved a digital 
                transformation initiative on 20 June 2023, with credit operations modernization as a top priority. 
                They're currently evaluating solutions to automate their credit assessment workflow.
                """,
                'executive_name': 'Robert Martinez',
                'role': 'Head of Lending'
            }
        ]

    def research_company(self, company_name: str) -> Dict[str, Any]:
        """Research a company and gather relevant information."""
        try:
            # For testing, use predefined test data
            if company_name in self.test_data:
                return {
                    'success': True,
                    'name': company_name,
                    'description': self.test_data[company_name]['description'],
                    'content': self.test_data[company_name]['content']
                }
            
            # Get company overview
            overview = self._search_company(
                company_name,
                "lending portfolio credit risk management banking"
            )
            if overview:
                company_data = {
                    'success': True,
                    'description': ' '.join(overview),
                    'news': '',
                    'features': [],
                    'use_cases': []
                }
            else:
                return {
                    'success': False,
                    'error': f"Company {company_name} not found in test data"
                }
            
            # Get lending operations news
            lending_news = self._search_company(
                company_name,
                "loan portfolio credit operations lending growth 2024"
            )
            if lending_news:
                company_data['news'] = ' '.join(lending_news)
            
            # Get technology and modernization info
            tech_info = self._search_company(
                company_name,
                "digital transformation technology modernization credit platform"
            )
            if tech_info:
                company_data['features'].extend(tech_info)
            
            # Get risk and compliance info
            risk_info = self._search_company(
                company_name,
                "risk management compliance credit assessment regulatory"
            )
            if risk_info:
                company_data['use_cases'].extend(risk_info)
            
            return company_data
            
        except Exception as e:
            logger.error(f"Error researching {company_name}: {str(e)}")
            return {
                'success': False,
                'error': f"Failed to research company: {str(e)}"
            }
    
    def _search_company(self, company_name: str, keywords: str) -> List[str]:
        """Perform a targeted search about the company."""
        try:
            results = []
            search_query = f'https://www.google.com/search?q={quote(company_name + " " + keywords)}'
            
            response = requests.get(search_query, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract search results
            for result in soup.find_all('div', class_='g')[:3]:
                snippet = result.find('div', class_='VwiC3b')
                if snippet:
                    results.append(snippet.text.strip())
            
            # Add delay to avoid rate limiting
            time.sleep(random.uniform(1, 2))
            
            return results
            
        except Exception as e:
            logger.error(f"Search error for {company_name}: {str(e)}")
            return []
    
    def run(self, query: str) -> str:
        """Run the web scraper tool."""
        try:
            # Research company
            company_data = self.research_company(query)
            if not company_data.get('success'):
                return json.dumps(company_data)
            
            return json.dumps(company_data)
            
        except Exception as e:
            error_msg = {
                "error": f"Error in web scraper: {str(e)}",
                "success": False
            }
            logger.error(error_msg["error"])
            return json.dumps(error_msg)
