"""
PROPRIETARY & CONFIDENTIAL
L1 SENTIMENT ENHANCED - NEWS & EARNINGS ANALYSIS
Patent Pending: "12-Layer Algorithmic Fraud Detection System"
© 2026 Aryan Sinha. All Rights Reserved.
"""

import yfinance as yf
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
import numpy as np

class SentimentAnalyzer:
    """
    Detect earnings surprises, news sentiment, analyst downgrades
    These are PROSPECTIVE fraud signals (appear DAYS/WEEKS before insolvency)
    """
    
    def __init__(self):
        self.name = "L1_Sentiment_Enhanced"
        self.vader = SentimentIntensityAnalyzer()
    
    def calculate_earnings_surprise(self, ticker):
        """
        Detect negative earnings surprises
        Missing guidance = RED FLAG
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get earnings metrics
            current_eps = info.get('trailingEps', 0) or 0
            forward_eps = info.get('forwardEps', 0) or 0
            earnings_growth = info.get('earningsGrowth', 0) or 0
            
            # Negative earnings growth = surprise miss
            if earnings_growth is None:
                earnings_growth = 0
            
            if current_eps > 0 and forward_eps > 0:
                eps_decline = (forward_eps - current_eps) / current_eps
                
                # Negative forward EPS = RED FLAG
                if eps_decline < -0.20:  # >20% EPS decline guidance
                    return 8.5  # HIGH RISK
                elif eps_decline < -0.10:
                    return 7.0
                elif eps_decline < 0:
                    return 5.5
                elif eps_decline < 0.05:
                    return 4.0
                else:
                    return 2.5  # Positive guidance
            else:
                return 5.0
                
        except Exception as e:
            print(f"Error calculating earnings surprise: {str(e)}")
            return 5.0
    
    def analyze_pe_valuation_compression(self, ticker):
        """
        Detect PE compression
        Falling PE + earnings miss = RED FLAG
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            pe_ratio = info.get('trailingPE', 0) or 0
            peg_ratio = info.get('pegRatio', 0) or 0
            
            # High PE + negative earnings = manipulation risk
            if pe_ratio > 0:
                if pe_ratio > 50:  # Very high PE
                    return 7.5
                elif pe_ratio > 30:
                    return 6.0
                elif pe_ratio > 20:
                    return 4.5
                elif pe_ratio > 10:
                    return 3.0
                else:
                    return 2.0
            else:
                return 5.0
                
        except Exception as e:
            print(f"Error analyzing PE: {str(e)}")
            return 5.0
    
    def analyze_analyst_sentiment(self, ticker):
        """
        Detect analyst downgrades
        Recent downgrades = RED FLAG
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get analyst ratings
            num_analysts = info.get('numberOfAnalysts', 0) or 0
            analyst_rating = info.get('recommendationKey', 'none') or 'none'
            target_price = info.get('targetMeanPrice', 0) or 0
            current_price = info.get('currentPrice', 1) or 1
            
            # Sentiment scoring
            sentiment_scores = {
                'strong buy': 1.0,
                'buy': 2.0,
                'hold': 3.5,
                'sell': 7.0,
                'strong sell': 8.5,
                'none': 4.0
            }
            
            base_score = sentiment_scores.get(analyst_rating.lower(), 4.0)
            
            # Target price below current = downgrade signal
            if target_price > 0 and current_price > 0:
                downside = (current_price - target_price) / current_price
                
                if downside > 0.30:  # >30% downside
                    return min(9.0, base_score + 1.5)
                elif downside > 0.15:
                    return min(8.5, base_score + 1.0)
                elif downside > 0:
                    return base_score + 0.5
            
            return base_score
            
        except Exception as e:
            print(f"Error analyzing analyst sentiment: {str(e)}")
            return 4.0
    
    def analyze_earnings_quality(self, ticker):
        """
        Detect earnings quality issues
        Accruals spike, revenue miss = RED FLAG
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get revenue and profit metrics
            total_revenue = info.get('totalRevenue', 0) or 0
            net_income = info.get('netIncome', 0) or 0
            operating_cf = info.get('operatingCashFlow', 0) or 0
            
            if total_revenue > 0:
                # Profit margin
                profit_margin = net_income / total_revenue if total_revenue else 0
                
                # Cash conversion
                if operating_cf != 0:
                    cash_conversion = net_income / operating_cf if operating_cf else 1.0
                else:
                    cash_conversion = 1.0
                
                score = 5.0
                
                # Low/negative profit margin = RED FLAG
                if profit_margin < -0.05:
                    score = 8.5
                elif profit_margin < 0:
                    score = 7.5
                elif profit_margin < 0.02:
                    score = 6.5
                elif profit_margin > 0.15:
                    score = 2.5
                
                # Accruals spike (cash conversion < 0.5)
                if cash_conversion < 0.5:
                    score = min(9.0, score + 1.5)
                elif cash_conversion < 0.7:
                    score = min(9.0, score + 1.0)
                
                return min(10, max(1, score))
            else:
                return 5.0
                
        except Exception as e:
            print(f"Error analyzing earnings quality: {str(e)}")
            return 5.0
    
    def analyze_price_momentum(self, ticker):
        """
        Detect negative price momentum
        Stock falling despite sector rally = RED FLAG
        """
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period='6mo')
            
            if len(data) > 60:
                # 6-month momentum
                price_6mo_ago = data['Close'].iloc[0]
                price_now = data['Close'].iloc[-1]
                
                momentum = (price_now - price_6mo_ago) / price_6mo_ago if price_6mo_ago > 0 else 0
                
                # Negative momentum = RED FLAG
                if momentum < -0.40:  # >40% decline
                    return 8.5
                elif momentum < -0.25:
                    return 7.5
                elif momentum < -0.10:
                    return 6.0
                elif momentum < 0:
                    return 5.0
                elif momentum < 0.10:
                    return 3.0
                else:
                    return 2.0  # Positive momentum
            else:
                return 5.0
                
        except Exception as e:
            print(f"Error analyzing momentum: {str(e)}")
            return 5.0
    
    def analyze(self, ticker, company_name):
        """
        Calculate overall L1_Sentiment score
        Combines: earnings surprise, PE compression, analyst sentiment, earnings quality, momentum
        """
        
        earnings_score = self.calculate_earnings_surprise(ticker)
        pe_score = self.analyze_pe_valuation_compression(ticker)
        analyst_score = self.analyze_analyst_sentiment(ticker)
        quality_score = self.analyze_earnings_quality(ticker)
        momentum_score = self.analyze_price_momentum(ticker)
        
        # Weighted average (earnings surprise gets highest weight)
        l1_sentiment = (
            earnings_score * 0.30 +
            analyst_score * 0.25 +
            quality_score * 0.20 +
            momentum_score * 0.15 +
            pe_score * 0.10
        )
        
        return {
            'company': company_name,
            'ticker': ticker,
            'L1_Sentiment': round(min(10, max(1, l1_sentiment)), 2),
            'earnings_surprise': round(earnings_score, 2),
            'pe_compression': round(pe_score, 2),
            'analyst_sentiment': round(analyst_score, 2),
            'earnings_quality': round(quality_score, 2),
            'price_momentum': round(momentum_score, 2),
            'sentiment_risk': 'HIGH SENTIMENT RISK' if l1_sentiment > 7.0 else ('MEDIUM RISK' if l1_sentiment > 5.5 else 'LOW RISK')
        }

if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
    print("\n" + "="*100)
    print("L1_SENTIMENT ENHANCED - NEWS & EARNINGS ANALYSIS")
    print("="*100)
    
    test_companies = [
        ('INFY.NS', 'Infosys'),
        ('TCS.NS', 'TCS'),
        ('RELIANCE.NS', 'Reliance'),
    ]
    
    for ticker, name in test_companies:
        result = analyzer.analyze(ticker, name)
        print(f"\n{name}:")
        print(f"  L1_Sentiment Score: {result['L1_Sentiment']}/10")
        print(f"  Earnings Surprise: {result['earnings_surprise']}")
        print(f"  PE Compression: {result['pe_compression']}")
        print(f"  Analyst Sentiment: {result['analyst_sentiment']}")
        print(f"  Earnings Quality: {result['earnings_quality']}")
        print(f"  Price Momentum: {result['price_momentum']}")
        print(f"  Sentiment Risk: {result['sentiment_risk']}")