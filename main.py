"""Main module for the B2B Lead Finder application."""

import sys
import json
from typing import Dict, List, Any
from tools.web_scraper import WebScraper
from agents.company_researcher import CompanyResearcher
from agents.product_researcher import ProductResearcher

# CreditLens product configuration
product_config = {
    'name': 'CreditLens',
    'description': 'Advanced credit assessment and portfolio management solution',
    'target_industries': [
        'Banking',
        'Financial Services',
        'Credit Unions',
        'Alternative Lenders',
        'Investment Management'
    ],
    'target_company_size': '100+',
    'target_roles': [
        'Chief Risk Officer',
        'Credit Risk Manager',
        'Head of Lending',
        'Portfolio Manager',
        'Chief Technology Officer'
    ],
    'pain_points': [
        'Manual credit assessment process',
        'Complex regulatory compliance',
        'Legacy lending systems',
        'Inefficient portfolio monitoring',
        'Risk management challenges'
    ],
    'industry_keywords': [
        'credit risk',
        'loan portfolio',
        'lending operations',
        'risk management',
        'regulatory compliance',
        'credit assessment',
        'portfolio monitoring',
        'loan origination',
        'credit workflow',
        'risk analytics'
    ]
}

class LeadFinder:
    """Main class for finding potential CreditLens customers."""
    
    def __init__(self, product_config: Dict):
        """Initialize the lead finder with product configuration."""
        self.product_config = product_config
        self.web_scraper = WebScraper()
        self.company_researcher = CompanyResearcher()
        self.product_researcher = ProductResearcher()
    
    def analyze_company(self, company_name: str) -> Dict[str, Any]:
        """Analyze a potential customer for CreditLens fit."""
        try:
            print(f"\nAnalyzing {company_name}...")
            
            # Step 1: Gather company information
            company_data = self.web_scraper.research_company(company_name)
            if not company_data['success']:
                return {
                    'success': False,
                    'error': f"Failed to gather data for {company_name}"
                }
            
            # Step 2: Analyze company signals
            company_analysis = self.company_researcher.analyze_company(company_data)
            if not company_analysis['success']:
                return {
                    'success': False,
                    'error': f"Failed to analyze {company_name}"
                }
            
            # Step 3: Match to CreditLens capabilities
            product_match = self.product_researcher.match_company_needs(company_analysis['signals'])
            if not product_match['success']:
                return {
                    'success': False,
                    'error': f"Failed to match {company_name} to CreditLens"
                }
            
            # Step 4: Generate comprehensive report
            result = {
                'success': True,
                'company_name': company_name,
                'institution_type': company_analysis.get('institution_type', 'unknown'),
                'fit_score': product_match['score'],
                'signals': company_analysis['signals'],
                'signal_details': company_analysis.get('signal_details', {}),
                'insights': company_analysis['insights'],
                'value_props': product_match['value_propositions'],
                'recommendation': product_match['recommendation']
            }
            
            # Print detailed analysis
            self._print_analysis(result)
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error analyzing {company_name}: {str(e)}"
            }
    
    def analyze_companies(self, company_names: List[str]) -> List[Dict[str, Any]]:
        """Analyze multiple companies for CreditLens fit."""
        results = []
        for company in company_names:
            result = self.analyze_company(company)
            if result['success']:
                results.append(result)
        return sorted(results, key=lambda x: x['fit_score'], reverse=True)
    
    def _print_analysis(self, analysis: Dict[str, Any]) -> None:
        """Print formatted analysis results."""
        print("\n" + "="*80)
        print(f"Company Analysis: {analysis['company_name']}")
        print(f"Institution Type: {analysis['institution_type'].replace('_', ' ').title()}")
        print(f"Fit Score: {analysis['fit_score']}/100")
        print("="*80)
        
        # Print signal analysis
        print("\nSignal Analysis:")
        for category, subcats in analysis['signals'].items():
            if any(subcats.values()):
                print(f"\n{category.title()} Signals:")
                for subcat, count in subcats.items():
                    if count > 0:
                        print(f"  - {subcat.replace('_', ' ').title()}: {count} signals")
                        # Print example contexts
                        if analysis['signal_details'].get(category, {}).get(subcat):
                            for i, detail in enumerate(analysis['signal_details'][category][subcat][:2]):
                                context = detail['context']
                                if len(context) > 100:
                                    context = context[:100] + "..."
                                print(f"    Example {i+1}: {context}")
        
        # Print key insights
        print("\nKey Insights:")
        for insight in analysis['insights']:
            print(f"- {insight}")
        
        # Print value propositions
        print("\nRelevant CreditLens Value Propositions:")
        for prop in analysis['value_props']:
            print(f"- {prop}")
        
        print(f"\nRecommendation: {analysis['recommendation']}")
        print("="*80 + "\n")

class SalesPitchGenerator:
    def __init__(self):
        self.pitch_templates = {
            'acquisition': """Subject: Streamline Post-Merger Credit Operations with CreditLens

Dear {executive_name},

I noticed {company_name}'s recent acquisition announcement and wanted to reach out. Having worked with several financial institutions during similar transitions, I understand the challenges of integrating credit operations and maintaining consistent risk management practices during this period.

CreditLens has helped organizations like yours:
• Standardize credit assessment across merged entities
• Reduce integration time by 40%
• Maintain regulatory compliance throughout the transition

Would you have 15 minutes this week to discuss how we've helped other institutions navigate similar challenges?

Best regards,
[Your name]""",
            'rapid_growth': """Subject: Scale Your Credit Operations Efficiently with CreditLens

Dear {executive_name},

Congratulations on {company_name}'s impressive growth. As you scale your operations, maintaining efficient credit assessment processes becomes crucial for sustainable expansion.

Our CreditLens platform has helped fast-growing institutions:
• Reduce credit decision time by 60%
• Scale operations without proportionally increasing headcount
• Maintain consistent risk assessment quality

I'd welcome the opportunity to share specific examples of how we've supported similar growth journeys.

Best regards,
[Your name]""",
            'system_integration': """Subject: Modernize Your Credit Operations with CreditLens

Dear {executive_name},

I understand {company_name} is working to standardize credit assessment processes across your organization. Many of our clients have faced similar challenges with legacy systems and found that modernizing their credit assessment infrastructure was key to ensuring operational efficiency.

CreditLens helps institutions:
• Consolidate multiple legacy systems into a single platform
• Reduce credit decision delays by 60%
• Ensure consistent risk assessment across all branches

Would you be interested in seeing how other institutions have solved similar challenges?

Best regards,
[Your name]"""
        }

    def generate_pitch(self, company_data, urgency_signals):
        # Determine primary signal type based on context relevance
        signal_scores = {
            'acquisition': 0,
            'rapid_growth': 0,
            'system_integration': 0
        }
        
        for signal in urgency_signals:
            if signal['type'] in signal_scores:
                signal_scores[signal['type']] += 1
            elif signal['type'] in ['modernization', 'legacy_system']:
                signal_scores['system_integration'] += 1
        
        primary_type = max(signal_scores.items(), key=lambda x: x[1])[0]
        template = self.pitch_templates.get(primary_type, self.pitch_templates['rapid_growth'])
        
        return template.format(
            executive_name=company_data.get('executive_name', 'Chief Risk Officer'),
            company_name=company_data['name']
        )

def analyze_prospects(companies, min_urgency_score=2.0):
    researcher = CompanyResearcher()
    pitch_generator = SalesPitchGenerator()
    
    high_potential_prospects = []
    
    for company in companies:
        analysis = researcher.analyze_company(company)
        if 'urgency_signals' in analysis and analysis['urgency_signals']:
            urgency_score = len(analysis['urgency_signals'])  # Simple scoring based on number of signals
            if urgency_score >= min_urgency_score:
                high_potential_prospects.append({
                    'company': company,
                    'analysis': analysis,
                    'urgency_score': urgency_score,
                    'pitch': pitch_generator.generate_pitch(company, analysis['urgency_signals'])
                })
    
    # Sort by urgency score
    high_potential_prospects.sort(key=lambda x: x['urgency_score'], reverse=True)
    
    return high_potential_prospects

def main():
    """Run the lead finder with test companies."""
    scraper = WebScraper()
    companies = scraper.get_test_companies()
    
    prospects = analyze_prospects(companies)
    
    if not prospects:
        print("No high-urgency prospects found.")
        return
    
    # Display top prospect analysis and pitch
    top_prospect = prospects[0]
    print(f"\nTop Prospect Analysis: {top_prospect['company']['name']}")
    print("-" * 50)
    print(f"Urgency Score: {len(top_prospect['analysis']['urgency_signals'])}")
    print("\nKey Urgency Signals:")
    for signal in top_prospect['analysis']['urgency_signals']:
        print(f"• {signal['type'].title()}: {signal['context']}")
    
    print("\nRecommended Sales Pitch:")
    print("=" * 50)
    print(top_prospect['pitch'])

if __name__ == '__main__':
    main()
