"""Tool for detecting business signals in text content."""

import re
import json
from typing import Dict, Any, List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SignalDetector:
    """Tool for detecting and categorizing business signals from text content."""
    
    def __init__(self):
        """Initialize signal detector with signal patterns."""
        self.signal_patterns = {
            'leadership_changes': [
                r'(?i)(new|appoint|hire|join).{0,20}(CEO|CTO|CFO|COO|president|director|executive)',
                r'(?i)(leadership|management).{0,20}(change|transition|update)',
                r'(?i)(promot|step.{0,5}down|resign).{0,20}(executive|leader|director)'
            ],
            'growth_signals': [
                r'(?i)(expand|growth|growing|scale).{0,30}(team|business|company|market)',
                r'(?i)(new|open).{0,20}(office|location|market|region)',
                r'(?i)(hire|hiring|recruit).{0,20}(spree|aggressively|rapidly)',
                r'(?i)(revenue|sales).{0,20}(growth|increase|up|higher)'
            ],
            'technology_signals': [
                r'(?i)(implement|adopt|rollout).{0,30}(technology|platform|system|software)',
                r'(?i)(digital|tech|IT).{0,20}(transformation|modernization|upgrade)',
                r'(?i)(automat|streamline|optimize).{0,20}(process|operation|workflow)',
                r'(?i)(legacy|manual|outdated).{0,20}(system|process|tool)'
            ],
            'financial_signals': [
                r'(?i)(raise|secure|close).{0,20}(funding|investment|round)',
                r'(?i)(revenue|profit).{0,20}(growth|increase|up)',
                r'(?i)(invest|spending).{0,20}(infrastructure|technology|expansion)',
                r'(?i)(budget|allocate).{0,20}(technology|improvement|modernization)'
            ],
            'risk_signals': [
                r'(?i)(compliance|regulatory|security).{0,30}(requirement|challenge|issue)',
                r'(?i)(risk|vulnerab|threat).{0,20}(assessment|management|mitigation)',
                r'(?i)(audit|review).{0,20}(process|system|operation)',
                r'(?i)(manual|error|inefficien).{0,20}(process|operation|workflow)'
            ],
            'operational_signals': [
                r'(?i)(improve|enhance|optimize).{0,30}(efficiency|productivity|performance)',
                r'(?i)(challenge|problem|issue).{0,20}(process|operation|workflow)',
                r'(?i)(bottleneck|pain.?point|friction).{0,20}(process|operation)',
                r'(?i)(manual|repetitive|time.consuming).{0,20}(task|process|work)'
            ]
        }
    
    def analyze_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content for business signals."""
        try:
            if not content.get('success', False):
                return {
                    'error': 'Invalid content data',
                    'success': False
                }
            
            text = content.get('text', '')
            if not text:
                return {
                    'error': 'No text content to analyze',
                    'success': False
                }
            
            # Initialize signals dictionary
            signals = {category: [] for category in self.signal_patterns.keys()}
            
            # Process each category of signals
            for category, patterns in self.signal_patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, text, re.IGNORECASE)
                    for match in matches:
                        signal = text[max(0, match.start() - 50):min(len(text), match.end() + 50)].strip()
                        if signal and signal not in signals[category]:
                            signals[category].append(signal)
            
            # Count total signals
            total_signals = sum(len(sigs) for sigs in signals.values())
            
            return {
                'success': True,
                'signals': signals,
                'total_signals': total_signals,
                'url': content.get('url', '')
            }
            
        except Exception as e:
            logger.error(f"Error analyzing content: {str(e)}")
            return {
                'error': f"Error analyzing content: {str(e)}",
                'success': False
            }
