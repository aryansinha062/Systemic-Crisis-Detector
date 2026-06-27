"""
Layer 1: Company-Specific Risk Detection
Analyzes board, strategy, operations, competition, and news sentiment
"""

import pandas as pd
import numpy as np
from datetime import datetime

class CompanyRiskDetector:
    """
    Detects company-specific risks that precede financial crises
    """
    
    def __init__(self):
        self.company_scores = {}
        self.detection_timestamp = datetime.now()
    
    def analyze_news_sentiment(self, company_ticker):
        """
        Analyze news sentiment for a company
        Mock data for now (will connect to NewsAPI later)
        Returns sentiment trend and alert level
        """
        
        # Mock sentiment database (will be replaced with real API)
        sentiment_data = {
            'TSLA': {
                'recent_articles': 12,
                'negative_articles': 8,
                'positive_articles': 2,
                'neutral_articles': 2,
                'avg_sentiment': -0.45,
                'trend': 'DECLINING'
            },
            'AAPL': {
                'recent_articles': 15,
                'negative_articles': 2,
                'positive_articles': 10,
                'neutral_articles': 3,
                'avg_sentiment': 0.65,
                'trend': 'IMPROVING'
            },
            'META': {
                'recent_articles': 8,
                'negative_articles': 5,
                'positive_articles': 1,
                'neutral_articles': 2,
                'avg_sentiment': -0.35,
                'trend': 'DECLINING'
            }
        }
        
        data = sentiment_data.get(company_ticker, {
            'recent_articles': 0,
            'negative_articles': 0,
            'positive_articles': 0,
            'neutral_articles': 0,
            'avg_sentiment': 0.0,
            'trend': 'UNKNOWN'
        })
        
        if data['recent_articles'] > 0:
            negative_ratio = data['negative_articles'] / data['recent_articles']
        else:
            negative_ratio = 0
        
        if data['avg_sentiment'] < -0.5 and negative_ratio > 0.6:
            alert_level = 'CRITICAL'
        elif data['avg_sentiment'] < -0.2:
            alert_level = 'WARNING'
        else:
            alert_level = 'NORMAL'
        
        return {
            'company': company_ticker,
            'sentiment_trend': data['trend'],
            'sentiment_score': data['avg_sentiment'],
            'negative_articles': data['negative_articles'],
            'recent_articles': data['recent_articles'],
            'alert': alert_level,
            'timestamp': self.detection_timestamp
        }
    
    def analyze_board_governance(self, company_ticker):
        """
        Analyze board composition, changes, and governance risks
        Flags red flags like board departures, insider related-party transactions
        """
        
        # Mock board governance data (will connect to SEC EDGAR later)
        board_data = {
            'TSLA': {
                'board_size': 11,
                'independent_directors': 8,
                'ceo_board_chair': True,  # Red flag: CEO is also board chair
                'recent_board_departures': 2,
                'average_tenure_years': 4.2,
                'related_party_transactions': 3,
                'auditor_changes': 0,
                'restatements_last_3_years': 0
            },
            'AAPL': {
                'board_size': 9,
                'independent_directors': 8,
                'ceo_board_chair': False,  # Good: separate roles
                'recent_board_departures': 0,
                'average_tenure_years': 6.1,
                'related_party_transactions': 0,
                'auditor_changes': 0,
                'restatements_last_3_years': 0
            },
            'META': {
                'board_size': 10,
                'independent_directors': 6,
                'ceo_board_chair': True,  # Red flag
                'recent_board_departures': 3,  # Red flag: multiple departures
                'average_tenure_years': 3.8,
                'related_party_transactions': 2,
                'auditor_changes': 1,  # Red flag
                'restatements_last_3_years': 1  # Red flag
            }
        }
        
        data = board_data.get(company_ticker, {
            'board_size': 0,
            'independent_directors': 0,
            'ceo_board_chair': False,
            'recent_board_departures': 0,
            'average_tenure_years': 0,
            'related_party_transactions': 0,
            'auditor_changes': 0,
            'restatements_last_3_years': 0
        })
        
        # Calculate board risk score (0-10)
        risk_score = 0
        red_flags = []
        
        # Flag 1: CEO is board chair (consolidation of power)
        if data['ceo_board_chair']:
            risk_score += 2.0
            red_flags.append('CEO serves as board chair')
        
        # Flag 2: Low independence ratio
        if data['board_size'] > 0:
            independence_ratio = data['independent_directors'] / data['board_size']
            if independence_ratio < 0.5:
                risk_score += 2.0
                red_flags.append('Board lacks independence (<50%)')
        
        # Flag 3: Recent board departures
        if data['recent_board_departures'] >= 2:
            risk_score += 2.5
            red_flags.append(f'{data["recent_board_departures"]} board departures recently')
        
        # Flag 4: Related-party transactions
        if data['related_party_transactions'] > 0:
            risk_score += 1.5
            red_flags.append(f'{data["related_party_transactions"]} related-party transactions')
        
        # Flag 5: Auditor changes
        if data['auditor_changes'] > 0:
            risk_score += 2.0
            red_flags.append('Recent auditor change')
        
        # Flag 6: Financial restatements
        if data['restatements_last_3_years'] > 0:
            risk_score += 3.0
            red_flags.append(f'{data["restatements_last_3_years"]} restatements in last 3 years')
        
        # Cap at 10
        risk_score = min(risk_score, 10.0)
        
        # Determine alert level
        if risk_score >= 7.0:
            alert_level = 'CRITICAL'
        elif risk_score >= 4.0:
            alert_level = 'WARNING'
        else:
            alert_level = 'NORMAL'
        
        return {
            'company': company_ticker,
            'board_risk_score': risk_score,
            'board_size': data['board_size'],
            'independent_directors': data['independent_directors'],
            'recent_departures': data['recent_board_departures'],
            'red_flags': red_flags,
            'alert': alert_level,
            'timestamp': self.detection_timestamp
        }
    
    def analyze_strategy_risk(self, company_ticker):
        """Strategy & innovation analysis"""
        return {
            'company': company_ticker,
            'strategy_risk_score': None,
            'alert': 'INITIALIZED'
        }
    
    def analyze_operational_health(self, company_ticker):
        """Operational health analysis"""
        return {
            'company': company_ticker,
            'operational_risk_score': None,
            'alert': 'INITIALIZED'
        }
    
    def analyze_competitive_position(self, company_ticker):
        """Competitive position analysis"""
        return {
            'company': company_ticker,
            'competitive_risk_score': None,
            'alert': 'INITIALIZED'
        }
    
    def generate_company_risk_alert(self, company_ticker):
        """Generate complete company risk alert"""
        return {
            'ticker': company_ticker,
            'overall_risk_score': None,
            'alert_level': 'MONITORING',
            'timestamp': self.detection_timestamp
        }


if __name__ == '__main__':
    detector = CompanyRiskDetector()
    result = detector.generate_company_risk_alert('TSLA')
    print("Company Risk Analysis for TSLA:")
    print(result)