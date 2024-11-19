"""Product analyzer agent for evaluating products as potential buyers."""

from typing import Dict, Any, List

class ProductAnalyzer:
    """Agent for analyzing if a product's company would be a good buyer."""
    
    def __init__(self, product_config: Dict[str, Any]):
        """Initialize the product analyzer."""
        self.product_config = product_config
    
    def analyze_product_fit(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze if the product's company would benefit from our lead generation tool."""
        try:
            if not research_data.get('success', False):
                return {
                    'success': False,
                    'error': research_data.get('error', 'Research data not available')
                }
            
            # Initialize scoring
            score = 0
            reasons = []
            
            # Check if it's a B2B product
            is_b2b = False
            
            # Check target audience for B2B indicators
            target_audience = research_data.get('target_audience', [])
            b2b_terms = ['business', 'enterprise', 'company', 'organization', 'corporate', 'professional']
            for audience in target_audience:
                if any(term in audience.lower() for term in b2b_terms):
                    is_b2b = True
                    score += 20
                    reasons.append("Product targets B2B customers")
                    break
            
            # Check features and use cases for B2B indicators
            use_cases = research_data.get('use_cases', [])
            features = research_data.get('features', [])
            all_text = ' '.join(use_cases + features)
            
            b2b_indicators = ['crm', 'enterprise', 'business', 'corporate', 'professional']
            for term in b2b_indicators:
                if term in all_text.lower():
                    is_b2b = True
                    score += 10
                    reasons.append(f"Product has B2B {term} functionality")
                    break
            
            if not is_b2b:
                return {
                    'success': True,
                    'score': 0,
                    'recommendation': "Not a B2B product - Not a potential buyer",
                    'reasons': ["Product does not show clear B2B focus"]
                }
            
            # Analyze if they need lead generation
            # Check for sales/marketing focus
            sales_terms = ['sales', 'crm', 'customer relationship', 'pipeline', 'lead', 'prospect', 'revenue']
            for term in sales_terms:
                if term in all_text.lower():
                    score += 20
                    reasons.append(f"Product involves {term} processes")
                    break
            
            # Check for growth signals
            growth_terms = ['growth', 'expand', 'scale', 'market', 'outreach', 'acquisition']
            for term in growth_terms:
                if term in all_text.lower():
                    score += 20
                    reasons.append(f"Company shows interest in {term}")
                    break
            
            # Check for automation/efficiency needs
            efficiency_terms = ['automation', 'workflow', 'efficiency', 'productivity', 'streamline']
            for term in efficiency_terms:
                if term in all_text.lower():
                    score += 15
                    reasons.append(f"Company values {term}")
                    break
            
            # Check company size from target audience
            company_sizes = ['enterprise', 'large', 'medium', 'small']
            target_size = self.product_config.get('target_company_size', '50-5000')
            for size in company_sizes:
                if any(size in audience.lower() for audience in target_audience):
                    if size in target_size.lower():
                        score += 15
                        reasons.append(f"Company size matches our target ({size} business)")
                        break
            
            # Generate recommendation
            if score >= 75:
                recommendation = "Excellent potential buyer - High need for lead generation"
            elif score >= 50:
                recommendation = "Good potential buyer - Shows clear sales/marketing focus"
            elif score >= 25:
                recommendation = "Possible potential buyer - May need lead generation"
            else:
                recommendation = "Not recommended - Limited sales/marketing focus"
            
            return {
                'success': True,
                'score': min(score, 100),  # Cap score at 100
                'recommendation': recommendation,
                'reasons': reasons
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error in product analysis: {str(e)}"
            }

    @staticmethod
    def create(config: Dict):
        """
        Create a product analyzer agent with specific configuration
        
        Args:
            config (Dict): Product configuration including:
                - name: Product name
                - features: List of key features
                - pain_points: List of pain points
                - industry_keywords: Industry-specific keywords
        """
        product_analyzer = ProductAnalyzer(config)
        
        return {
            'role': "Product Analyzer",
            'goal': "Analyze product fit based on product research and product configuration.",
            'backstory': """You are an expert product analyst with deep experience in:
            1. Understanding product-market fit
            2. Analyzing product features and use cases
            3. Matching product capabilities to business requirements
            4. Evaluating technology adoption potential
            5. Assessing implementation feasibility""",
            'tools': [],
            'verbose': True,
            'allow_delegation': False,
            'memory': True
        }
