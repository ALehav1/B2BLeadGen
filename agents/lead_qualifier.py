from crewai import Agent
from tools.web_scraper import WebScraperTool, WebScraperInput
from langchain.tools import Tool
from typing import Dict, List
import json

class LeadQualifier:
    @staticmethod
    def create():
        # Create the web scraper tool
        web_scraper = WebScraperTool.create()
        
        # Create a LangChain Tool wrapper
        web_scraper_tool = Tool(
            name="Web Scraper",
            func=lambda x: web_scraper.run(x),
            description="""Use this tool to extract content from websites.
            Input should be a URL (e.g., 'https://example.com' or just 'example.com').
            The tool will return the text content from the webpage, including:
            - Page title
            - Main content
            - Meta description
            - Keywords
            - Summary
            
            Example usage:
            Action: Web Scraper
            Action Input: https://example.com
            """
        )
        
        return Agent(
            role='Lead Qualifier',
            goal='Qualify and rank potential leads based on product fit and buying signals',
            backstory="""You are an expert in lead qualification and sales opportunity analysis with 15+ years 
            of experience in B2B sales. Your expertise lies in evaluating potential customers based on their 
            likelihood to purchase, urgency of need, and ability to buy. You excel at:
            1. Evaluating company fit with product use cases
            2. Identifying urgent needs and pain points
            3. Assessing budget and purchasing power
            4. Analyzing decision-making patterns
            5. Scoring and ranking sales opportunities""",
            tools=[web_scraper_tool],
            verbose=True,
            allow_delegation=False,  # Focus on core qualification task
            memory=True
        )

    @staticmethod
    def calculate_lead_score(company: Dict, product_analysis: Dict) -> float:
        """Calculate a lead score based on various signals"""
        score = 0.0
        max_score = 100.0
        
        # Base score weights
        weights = {
            "pain_point": {
                "high": 30,
                "medium": 20,
                "low": 10
            },
            "expansion": {
                "high": 25,
                "medium": 15,
                "low": 5
            },
            "technology": {
                "high": 20,
                "medium": 15,
                "low": 10
            },
            "metadata": {
                "high": 15,
                "medium": 10,
                "low": 5
            }
        }
        
        # Score based on signal types and confidence
        for signal in company.get("signals", []):
            signal_type = signal.get("type")
            confidence = signal.get("confidence", "low")
            
            if signal_type in weights:
                score += weights[signal_type][confidence]
        
        # Normalize score to 0-100
        normalized_score = min((score / max_score) * 100, 100)
        
        return round(normalized_score, 2)

    @staticmethod
    def evaluate_urgency(company: Dict) -> Dict:
        """Evaluate the urgency level based on signals"""
        urgent_signals = []
        moderate_signals = []
        low_signals = []
        
        for signal in company.get("signals", []):
            if signal["type"] == "pain_point" and signal["confidence"] == "high":
                urgent_signals.append(signal["signal"])
            elif signal["type"] in ["pain_point", "expansion"] and signal["confidence"] == "medium":
                moderate_signals.append(signal["signal"])
            else:
                low_signals.append(signal["signal"])
        
        # Determine urgency level
        if len(urgent_signals) >= 2:
            urgency = "High"
            reasons = urgent_signals[:3]  # Top 3 urgent signals
        elif len(urgent_signals) == 1 or len(moderate_signals) >= 2:
            urgency = "Medium"
            reasons = (urgent_signals + moderate_signals)[:3]
        else:
            urgency = "Low"
            reasons = (moderate_signals + low_signals)[:3]
        
        return {
            "level": urgency,
            "reasons": reasons
        }

    @staticmethod
    def qualify_lead(company: Dict, product_analysis: Dict) -> Dict:
        """
        Qualifies a lead based on:
        - Lead score
        - Urgency level
        - Company signals
        - Product fit
        """
        try:
            # Calculate lead score
            score = LeadQualifier.calculate_lead_score(company, product_analysis)
            
            # Evaluate urgency
            urgency = LeadQualifier.evaluate_urgency(company)
            
            # Determine qualification status
            if score >= 80 and urgency["level"] == "High":
                status = "Hot Lead"
            elif score >= 60 or urgency["level"] == "High":
                status = "Warm Lead"
            else:
                status = "Cold Lead"
            
            qualification = {
                "company_name": company.get("company_name", "Unknown"),
                "url": company.get("url"),
                "status": status,
                "score": score,
                "urgency": urgency["level"],
                "urgency_reasons": urgency["reasons"],
                "signal_count": company.get("signal_count", 0),
                "key_signals": [s["signal"] for s in company.get("signals", [])[:5]],
                "success": True
            }
            
            return qualification
            
        except Exception as e:
            return {
                "error": f"Error qualifying lead: {str(e)}",
                "company_url": company.get("url"),
                "success": False
            }
