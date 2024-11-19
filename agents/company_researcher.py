"""Company research agent for analyzing potential customers."""

from typing import Dict, List, Any
import random
import re
from datetime import datetime, timedelta

class CompanyResearcher:
    """Agent for researching and analyzing companies."""

    def __init__(self):
        """Initialize the company researcher agent."""
        # Signal patterns to look for in company data
        self.signal_patterns = {
            "lending": {
                "commercial_lending": [
                    r'commercial\s+lending',
                    r'commercial\s+loan',
                    r'business\s+lending',
                    r'middle\s+market'
                ],
                "consumer_lending": [
                    r'consumer\s+lending',
                    r'retail\s+lending',
                    r'personal\s+loan',
                    r'consumer\s+credit'
                ],
                "specialty_lending": [
                    r'specialty\s+lending',
                    r'specialized\s+finance',
                    r'equipment\s+leasing',
                    r'project\s+finance'
                ]
            },
            "risk_management": {
                "credit_risk": [
                    r'credit\s+risk',
                    r'risk\s+management',
                    r'risk\s+assessment',
                    r'risk\s+analytics'
                ],
                "regulatory_compliance": [
                    r'regulatory\s+compliance',
                    r'compliance\s+requirements',
                    r'regulatory\s+reporting',
                    r'compliance\s+framework'
                ],
                "portfolio_monitoring": [
                    r'portfolio\s+monitoring',
                    r'portfolio\s+management',
                    r'portfolio\s+analytics',
                    r'portfolio\s+health'
                ]
            },
            "technology": {
                "modernization": [
                    r'modernization',
                    r'digital\s+transformation',
                    r'technology\s+upgrade',
                    r'legacy\s+system'
                ],
                "automation": [
                    r'automation',
                    r'automated\s+process',
                    r'workflow\s+automation',
                    r'process\s+efficiency'
                ],
                "analytics": [
                    r'analytics',
                    r'data\s+driven',
                    r'machine\s+learning',
                    r'predictive\s+model'
                ]
            },
            "growth": {
                "expansion": [
                    r'expansion',
                    r'market\s+growth',
                    r'geographic\s+expansion',
                    r'new\s+market'
                ],
                "portfolio_growth": [
                    r'portfolio\s+growth',
                    r'asset\s+growth',
                    r'growing\s+portfolio',
                    r'portfolio\s+expansion'
                ],
                "innovation": [
                    r'innovation',
                    r'new\s+product',
                    r'digital\s+innovation',
                    r'fintech'
                ]
            }
        }

        # Institution type characteristics
        self.institution_types = {
            "traditional_bank": [
                r'global\s+financial',
                r'major\s+bank',
                r'multinational\s+bank'
            ],
            "regional_bank": [
                r'regional\s+bank',
                r'middle\s+market',
                r'community\s+bank'
            ],
            "credit_union": [
                r'credit\s+union',
                r'member\s+service',
                r'member\s+focused'
            ],
            "alternative_lender": [
                r'fintech',
                r'online\s+lender',
                r'alternative\s+lending'
            ],
            "investment_bank": [
                r'investment\s+bank',
                r'securities',
                r'capital\s+markets'
            ]
        }

    def analyze_company(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze company data for signals and insights."""
        try:
            description = company_data.get('description', '')
            
            # Detect urgency signals
            urgency_signals = self._detect_urgency_signals(description)
            
            return {
                'success': True,
                'urgency_signals': urgency_signals,
                'company_name': company_data.get('name', ''),
                'executive_name': company_data.get('executive_name', '')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _detect_urgency_signals(self, content):
        urgency_patterns = {
            'acquisition': r'(?i)(announced.*acquisition|merger with|acquiring|merging with)',
            'rapid_growth': r'(?i)(rapid growth|300% growth|tripl.*portfolio|significant.*increase)',
            'regulatory': r'(?i)(regulatory.*audit|compliance.*mandate|regulatory.*changes)',
            'modernization': r'(?i)(legacy system|digital transformation|modernization initiative)',
            'risk_issues': r'(?i)(inconsistencies.*risk|challenges.*credit|limitations.*infrastructure)',
            'system_integration': r'(?i)(separate.*systems|integration.*needed|standardize.*processes)'
        }
        
        urgency_signals = []
        for signal_type, pattern in urgency_patterns.items():
            matches = re.finditer(pattern, content)
            for match in matches:
                # Get surrounding context (100 chars before and after)
                start = max(0, match.start() - 100)
                end = min(len(content), match.end() + 100)
                context = content[start:end].strip()
                
                urgency_signals.append({
                    'type': signal_type,
                    'context': context
                })
        
        return urgency_signals

    def _detect_institution_type(self, text: str) -> str:
        """Detect the institution type based on text patterns."""
        type_scores = {}
        
        for inst_type, patterns in self.institution_types.items():
            score = 0
            for pattern in patterns:
                score += len(re.findall(pattern, text))
            type_scores[inst_type] = score
        
        # Return the type with highest score, default to 'unknown'
        if any(type_scores.values()):
            return max(type_scores.items(), key=lambda x: x[1])[0]
        return 'unknown'

    def _get_context(self, text: str, start: int, end: int, context_size: int = 100) -> str:
        """Get context around a match."""
        start_ctx = max(0, start - context_size)
        end_ctx = min(len(text), end + context_size)
        return text[start_ctx:end_ctx].strip()

    def _generate_insights(self, signals: Dict[str, Dict[str, int]], institution_type: str) -> List[str]:
        """Generate insights based on signals and institution type."""
        insights = []
        
        # Institution type specific insights
        type_insights = {
            "traditional_bank": "Large-scale operations with complex needs across lending, risk, and compliance",
            "regional_bank": "Growing institution with focus on regional market expansion and modernization",
            "credit_union": "Member-focused organization with emphasis on consumer lending and service",
            "alternative_lender": "Technology-driven lender with innovative approaches to credit",
            "investment_bank": "Sophisticated institution with complex risk management needs"
        }
        
        if institution_type in type_insights:
            insights.append(type_insights[institution_type])

        # Signal-based insights
        for category, subcategories in signals.items():
            strong_signals = [
                subcat.replace('_', ' ').title()
                for subcat, count in subcategories.items()
                if count >= 2
            ]
            if strong_signals:
                insights.append(
                    f"Strong focus on {', '.join(strong_signals)} in {category.replace('_', ' ')} area"
                )

        return insights

    def _extract_timestamp(self, text):
        # Simple timestamp extraction, you may need to improve this
        date_pattern = r'\d{1,2} [A-Za-z]+ \d{4}'
        match = re.search(date_pattern, text)
        if match:
            return datetime.strptime(match.group(), '%d %B %Y')
        return None

    def _is_recent(self, timestamp):
        if timestamp is None:
            return False
        return timestamp > datetime.now() - timedelta(days=30)

    def _calculate_urgency_score(self, signals):
        score = 0
        recent_signals = [s for s in signals if self._is_recent(s.get('timestamp'))]
        
        # Weight recent signals more heavily
        score += len(recent_signals) * 2
        
        # Additional points for multiple signal types
        signal_types = set(s['type'] for s in recent_signals)
        score += len(signal_types) * 1.5
        
        return min(score, 10)  # Cap at 10
