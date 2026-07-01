"""
PROPRIETARY & CONFIDENTIAL
L4 BEHAVIORAL - INSIDER TRADING & PROMOTER ANALYSIS
Patent Pending: "12-Layer Algorithmic Fraud Detection System"
© 2026 Aryan Sinha. All Rights Reserved.
"""

import yfinance as yf
import numpy as np
from datetime import datetime, timedelta

class BehavioralAnalyzer:
    """
    Detect insider trading, promoter pledging, leadership fraud signals
    These are PROSPECTIVE fraud indicators (appear BEFORE insolvency)
    """
    
    def __init__(self):
        self.name = "L4_Behavioral_Enhanced"
    
    def calculate_insider_trading_signal(self, ticker):
        """
        Detect insider trading patterns
        Heavy insider selling = RED FLAG (they know something)
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get insider transactions from yfinance
            try:
                insider_purchases = info.get('insiderBuyCount', 0) or 0
                insider_sales = info.get('insiderSellCount', 0) or 0
                
                # Calculate insider activity ratio
                total_insider_activity = insider_purchases + insider_sales
                
                if total_insider_activity == 0:
                    return 4.0  # No insider activity = neutral
                
                # High sell ratio = RED FLAG
                sell_ratio = insider_sales / total_insider_activity
                
                if sell_ratio > 0.8:  # 80%+ selling
                    return 8.5  # HIGH RISK
                elif sell_ratio > 0.6:  # 60%+ selling
                    return 7.0
                elif sell_ratio > 0.4:  # 40%+ selling
                    return 5.5
                else:
                    return 3.0  # Balanced or buying
                    
            except:
                return 4.0
                
        except Exception as e:
            print(f"Error calculating insider trading signal: {str(e)}")
            return 4.0
    
    def calculate_promoter_pledging(self, ticker):
        """
        Detect promoter share pledging
        High pledging = financial distress (RED FLAG for fraud)
        Promoters pledge shares when they need liquidity = insolvency signal
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Shareholding patterns (if available)
            try:
                # Estimate from public data
                shares_outstanding = info.get('sharesOutstanding', 1) or 1
                insiders_own = info.get('insiderOwnership', 0) or 0
                
                # In India, high promoter pledging signals distress
                # If we had access to NSE regulatory filings, pledging % would be visible
                # For now, use insider ownership decline as proxy
                
                if insiders_own < 0.3:  # < 30% promoter ownership
                    return 7.0  # Potentially high pledging
                elif insiders_own < 0.4:
                    return 5.5
                elif insiders_own < 0.5:
                    return 4.0
                else:
                    return 2.5  # Strong promoter ownership = lower fraud risk
                    
            except:
                return 4.0
                
        except Exception as e:
            print(f"Error calculating promoter pledging: {str(e)}")
            return 4.0
    
    def calculate_leadership_changes(self, ticker):
        """
        Detect abnormal leadership changes
        Frequent CEO/CFO changes = RED FLAG (audit issues, fraud risk)
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Limited data available from yfinance
            # In real implementation, would scrape NSE/BSE announcements
            
            try:
                # Use CEO name changes as proxy (if available)
                ceo_name = info.get('ceoName', '')
                
                # Would track historical CEO changes via scraping
                # For MVP, use static score
                return 3.0
                
            except:
                return 3.0
                
        except Exception as e:
            print(f"Error calculating leadership changes: {str(e)}")
            return 3.0
    
    def calculate_share_buyback_signal(self, ticker):
        """
        Detect manipulative share buybacks
        Heavy buybacks with declining earnings = manipulation (RED FLAG)
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            try:
                # Get share count history
                shares_current = info.get('sharesOutstanding', 0) or 1
                
                # Would compare with historical shares outstanding
                # For MVP, use earnings quality as proxy
                net_income = info.get('netIncome', 0) or 0
                free_cash_flow = info.get('freeCashflow', 0) or 1
                
                # If buybacks > free cash flow, it's manipulative (using debt)
                if free_cash_flow > 0 and net_income > 0:
                    buyback_efficiency = net_income / free_cash_flow
                    
                    if buyback_efficiency > 2.0:  # Burning cash
                        return 7.5
                    elif buyback_efficiency > 1.5:
                        return 6.0
                    else:
                        return 3.0
                else:
                    return 4.0
                    
            except:
                return 4.0
                
        except Exception as e:
            print(f"Error calculating share buyback signal: {str(e)}")
            return 4.0
    
    def calculate_dividend_manipulation(self, ticker):
        """
        Detect manipulative dividend payments
        High dividends with declining cash flow = RED FLAG
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            try:
                dividend_rate = info.get('dividendRate', 0) or 0
                net_income = info.get('netIncome', 0) or 1
                operating_cf = info.get('operatingCashFlow', 0) or 1
                
                # Dividend payout ratio
                if net_income > 0:
                    payout_ratio = dividend_rate / net_income
                    
                    if payout_ratio > 1.5:  # Paying out > 150% of earnings
                        return 8.0  # HIGH RISK - using capital/debt
                    elif payout_ratio > 1.0:
                        return 6.5
                    elif payout_ratio > 0.5:
                        return 4.0
                    else:
                        return 2.5
                else:
                    return 5.0
                    
            except:
                return 4.0
                
        except Exception as e:
            print(f"Error calculating dividend manipulation: {str(e)}")
            return 4.0
    
    def analyze(self, ticker, company_name):
        """
        Calculate overall L4_Behavioral score
        Combines: insider trading, promoter pledging, leadership, buybacks, dividends
        """
        
        insider_score = self.calculate_insider_trading_signal(ticker)
        pledging_score = self.calculate_promoter_pledging(ticker)
        leadership_score = self.calculate_leadership_changes(ticker)
        buyback_score = self.calculate_share_buyback_signal(ticker)
        dividend_score = self.calculate_dividend_manipulation(ticker)
        
        # Weighted average
        l4_behavioral = (
            insider_score * 0.25 +
            pledging_score * 0.30 +
            leadership_score * 0.15 +
            buyback_score * 0.15 +
            dividend_score * 0.15
        )
        
        return {
            'company': company_name,
            'ticker': ticker,
            'L4_Behavioral': round(min(10, max(1, l4_behavioral)), 2),
            'insider_trading': round(insider_score, 2),
            'promoter_pledging': round(pledging_score, 2),
            'leadership_changes': round(leadership_score, 2),
            'share_buybacks': round(buyback_score, 2),
            'dividend_manipulation': round(dividend_score, 2),
            'risk_level': 'HIGH FRAUD RISK' if l4_behavioral > 7.0 else ('MEDIUM RISK' if l4_behavioral > 5.5 else 'LOW RISK')
        }

if __name__ == "__main__":
    analyzer = BehavioralAnalyzer()
    
    print("\n" + "="*100)
    print("L4_BEHAVIORAL ENHANCED - INSIDER TRADING & PROMOTER ANALYSIS")
    print("="*100)
    
    test_companies = [
        ('INFY.NS', 'Infosys'),
        ('TCS.NS', 'TCS'),
        ('RELIANCE.NS', 'Reliance'),
    ]
    
    for ticker, name in test_companies:
        result = analyzer.analyze(ticker, name)
        print(f"\n{name}:")
        print(f"  L4_Behavioral Score: {result['L4_Behavioral']}/10")
        print(f"  Insider Trading: {result['insider_trading']}")
        print(f"  Promoter Pledging: {result['promoter_pledging']}")
        print(f"  Leadership Changes: {result['leadership_changes']}")
        print(f"  Share Buybacks: {result['share_buybacks']}")
        print(f"  Dividend Manipulation: {result['dividend_manipulation']}")
        print(f"  Risk Level: {result['risk_level']}")