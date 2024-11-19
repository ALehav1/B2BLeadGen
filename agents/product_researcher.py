"""Product researcher agent for matching company needs to CreditLens capabilities."""

from typing import Dict, List, Any

class ProductResearcher:
    """Agent for matching company needs to CreditLens capabilities."""

    def __init__(self):
        """Initialize the product researcher agent."""
        self.value_propositions = {
            "lending": {
                "commercial_lending": [
                    "Streamlined commercial loan origination workflow",
                    "Automated financial spreading and analysis",
                    "Industry-specific credit assessment templates"
                ],
                "consumer_lending": [
                    "Automated retail credit decisioning",
                    "Consumer loan portfolio analytics",
                    "Standardized credit assessment workflow"
                ],
                "specialty_lending": [
                    "Customizable lending workflows",
                    "Specialized industry risk assessment",
                    "Complex deal structure support"
                ]
            },
            "risk_management": {
                "credit_risk": [
                    "Advanced credit risk modeling",
                    "Portfolio risk analytics",
                    "Early warning system integration"
                ],
                "regulatory_compliance": [
                    "Regulatory reporting automation",
                    "Compliance workflow management",
                    "Audit trail documentation"
                ],
                "portfolio_monitoring": [
                    "Real-time portfolio monitoring",
                    "Automated covenant tracking",
                    "Portfolio health analytics"
                ]
            },
            "technology": {
                "modernization": [
                    "Modern cloud-based architecture",
                    "API-first integration approach",
                    "Scalable technology platform"
                ],
                "automation": [
                    "End-to-end process automation",
                    "Automated data collection",
                    "Workflow automation engine"
                ],
                "analytics": [
                    "Advanced analytics capabilities",
                    "Machine learning integration",
                    "Predictive modeling tools"
                ]
            },
            "growth": {
                "expansion": [
                    "Multi-entity support",
                    "Geographic expansion ready",
                    "Scalable user management"
                ],
                "portfolio_growth": [
                    "Portfolio management tools",
                    "Growth analytics dashboard",
                    "Capacity planning features"
                ],
                "innovation": [
                    "Regular feature updates",
                    "Innovation enablement",
                    "Modern API ecosystem"
                ]
            }
        }

        self.recommendations = {
            "traditional_bank": {
                "high": "Immediate implementation recommended for comprehensive credit lifecycle management",
                "medium": "Strong fit for modernizing credit operations with phased implementation",
                "low": "Consider targeted implementation for specific lending areas"
            },
            "regional_bank": {
                "high": "Excellent fit for regional growth and modernization goals",
                "medium": "Good fit with focused implementation approach",
                "low": "Consider starting with core lending functionality"
            },
            "credit_union": {
                "high": "Strong fit for member-focused lending modernization",
                "medium": "Good fit with emphasis on consumer lending capabilities",
                "low": "Consider targeted implementation for key lending areas"
            },
            "alternative_lender": {
                "high": "Ideal fit for innovative lending approach with full capabilities",
                "medium": "Strong fit with focus on automation and analytics",
                "low": "Consider targeted implementation for specific needs"
            },
            "investment_bank": {
                "high": "Excellent fit for complex credit operations",
                "medium": "Strong fit with focus on sophisticated risk management",
                "low": "Consider focused implementation for key areas"
            }
        }

    def match_company_needs(self, signals: Dict[str, Dict[str, int]]) -> Dict[str, Any]:
        """Match company signals to CreditLens value propositions."""
        try:
            # Collect relevant value propositions
            value_props = []
            for category, subcategories in signals.items():
                for subcategory, count in subcategories.items():
                    if count > 0:
                        # Add relevant value propositions based on signal strength
                        props = self.value_propositions[category][subcategory]
                        if count >= 4:  # Strong signal
                            value_props.extend(props)
                        elif count >= 2:  # Medium signal
                            value_props.extend(props[:2])
                        else:  # Weak signal
                            value_props.append(props[0])

            # Remove duplicates while preserving order
            value_props = list(dict.fromkeys(value_props))

            # Calculate fit score
            score = self._calculate_fit_score(signals)

            # Generate recommendation
            recommendation = self._generate_recommendation(score)

            return {
                'success': True,
                'score': score,
                'value_propositions': value_props,
                'recommendation': recommendation
            }

        except Exception as e:
            return {
                'success': False,
                'error': f"Error matching company needs: {str(e)}"
            }

    def _calculate_fit_score(self, signals: Dict[str, Dict[str, int]]) -> int:
        """Calculate overall fit score based on signals."""
        total_points = 0
        max_points = 0

        # Weights for different categories
        weights = {
            'lending': 0.35,
            'risk_management': 0.25,
            'technology': 0.25,
            'growth': 0.15
        }

        for category, subcategories in signals.items():
            category_points = sum(subcategories.values())
            category_max = len(subcategories) * 5  # Assuming max 5 signals per subcategory
            
            # Apply category weight
            total_points += category_points * weights[category]
            max_points += category_max * weights[category]

        # Convert to 0-100 scale
        if max_points > 0:
            score = int((total_points / max_points) * 100)
            return min(100, max(0, score))
        return 0

    def _generate_recommendation(self, score: int) -> str:
        """Generate recommendation based on fit score."""
        if score >= 80:
            return "High priority implementation recommended. Strong alignment across multiple areas suggests significant value potential."
        elif score >= 60:
            return "Medium priority implementation recommended. Good alignment in key areas indicates strong value potential."
        else:
            return "Evaluate specific needs and use cases. Consider targeted implementation for highest value areas."
