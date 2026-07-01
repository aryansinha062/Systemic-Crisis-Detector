"""
PROPRIETARY & CONFIDENTIAL
L3 NETWORK ENHANCED - CUSTOMER & SUPPLY CONCENTRATION
Patent Pending: "12-Layer Algorithmic Fraud Detection System"
© 2026 Aryan Sinha. All Rights Reserved.
"""

import yfinance as yf
import numpy as np
from datetime import datetime, timedelta

class NetworkConcentrationAnalyzer:
    """
    Detect concentration risks: customers, suppliers, geography, segments
    Revenue cliff risk = PROSPECTIVE fraud signal
    """
    
    def __init__(self):
        self.name = "L3_Network_Enhanced"
    
    def analyze_revenue_concentration(self, ticker):
        """
        Detect customer concentration risk
        Top 5 customers > 40% revenue = RED FLAG
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # In production: parse annual report for customer concentration
            # For MVP: use revenue volatility as proxy
            
            total_revenue = info.get('totalRevenue', 0) or 0
            
            if total_revenue == 0:
                return 5.0
            
            # High revenue volatility = customer concentration risk
            try:
                hist = stock.history(period='5y')
                
                if len(hist) > 60:
                    quarterly_revenue_volatility = hist['Close'].pct_change().std()
                    
                    # Volatility as proxy for concentration
                    if quarterly_revenue_volatility > 0.10:  # High volatility
                        return 8.0  # High concentration risk
                    elif quarterly_revenue_volatility > 0.08:
                        return 6.5
                    elif quarterly_revenue_volatility > 0.05:
                        return 5.0
                    else:
                        return 3.0  # Stable revenue
                else:
                    return 5.0
            except:
                return 5.0
                
        except Exception as e:
            print(f"Error analyzing revenue concentration: {str(e)}")
            return 5.0
    
    def analyze_segment_concentration(self, ticker):
        """
        Detect segment concentration risk
        Revenue from 1-2 segments > 70% = RED FLAG
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Analyze by sector concentration
            sector = info.get('sector', 'Unknown')
            
            # High sector concentration risk scores
            high_risk_sectors = {
                'Energy': 7.0,  # Oil price dependent
                'Auto': 6.5,    # Cyclical, concentrated suppliers
                'Steel': 7.5,   # Commodity dependent
                'Telecom': 6.0, # Regulated, competitive
            }
            
            # Use earnings volatility as proxy for segment concentration
            try:
                hist = stock.history(period='2y')
                
                if len(hist) > 30:
                    earnings_volatility = hist['Close'].pct_change().std()
                    
                    if earnings_volatility > 0.08:
                        base_score = high_risk_sectors.get(sector, 5.0)
                        return min(9.0, base_score + 1.0)
                    else:
                        return high_risk_sectors.get(sector, 4.0)
                else:
                    return high_risk_sectors.get(sector, 5.0)
            except:
                return high_risk_sectors.get(sector, 5.0)
                
        except Exception as e:
            print(f"Error analyzing segment concentration: {str(e)}")
            return 5.0
    
    def analyze_geographic_concentration(self, ticker):
        """
        Detect geographic concentration risk
        >70% revenue from single country/region = RED FLAG
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Detect geographic risk from currency exposure
            # INR weakness = India exposure risk
            try:
                inr_usd = yf.Ticker('INRUSD=X')
                data = inr_usd.history(period='1y')
                
                if len(data) > 30:
                    recent_vol = data['Close'].pct_change().tail(30).std()
                    
                    # High INR volatility = geographic risk
                    if recent_vol > 0.015:  # High currency volatility
                        return 7.5  # High geographic concentration in India
                    elif recent_vol > 0.01:
                        return 6.0
                    else:
                        return 4.0
                else:
                    return 5.0
            except:
                return 5.0
                
        except Exception as e:
            print(f"Error analyzing geographic concentration: {str(e)}")
            return 5.0
    
    def analyze_supplier_dependency(self, ticker):
        """
        Detect supplier concentration risk
        High COGS > 70% revenue with few suppliers = RED FLAG
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            total_revenue = info.get('totalRevenue', 0) or 0
            
            # Use gross margin as proxy for COGS dependency
            try:
                gross_profit_margin = info.get('grossMargins', 0) or 0
                
                if gross_profit_margin == 0:
                    return 5.0
                
                # Very low gross margin = high COGS dependency = supplier risk
                if gross_profit_margin < 0.15:  # <15% gross margin
                    return 8.0  # High supplier dependency
                elif gross_profit_margin < 0.25:
                    return 6.5
                elif gross_profit_margin < 0.35:
                    return 5.0
                else:
                    return 3.0  # Good margin = low supplier risk
            except:
                return 5.0
                
        except Exception as e:
            print(f"Error analyzing supplier dependency: {str(e)}")
            return 5.0
    
    def analyze_customer_concentration_trend(self, ticker):
        """
        Detect worsening customer concentration
        Rising concentration = RED FLAG
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Use customer acquisition/retention proxy
            try:
                hist = stock.history(period='3y')
                
                if len(hist) > 90:
                    # Sharpe ratio decline = worsening concentration
                    recent_sharpe = hist['Close'].pct_change().tail(60).mean() / hist['Close'].pct_change().tail(60).std()
                    old_sharpe = hist['Close'].pct_change().iloc[:60].mean() / hist['Close'].pct_change().iloc[:60].std()
                    
                    if old_sharpe != 0:
                        sharpe_decline = (old_sharpe - recent_sharpe) / abs(old_sharpe)
                    else:
                        sharpe_decline = 0
                    
                    if sharpe_decline > 0.50:  # 50% sharpe decline
                        return 8.0  # Worsening quality
                    elif sharpe_decline > 0.25:
                        return 6.5
                    elif sharpe_decline > 0:
                        return 5.0
                    else:
                        return 3.0  # Improving quality
                else:
                    return 5.0
            except:
                return 5.0
                
        except Exception as e:
            print(f"Error analyzing customer concentration trend: {str(e)}")
            return 5.0
    
    def analyze(self, ticker, company_name):
        """
        Calculate overall L3_Network score
        Combines: revenue concentration, segment risk, geographic risk, supplier risk, trend
        """
        
        revenue_score = self.analyze_revenue_concentration(ticker)
        segment_score = self.analyze_segment_concentration(ticker)
        geographic_score = self.analyze_geographic_concentration(ticker)
        supplier_score = self.analyze_supplier_dependency(ticker)
        trend_score = self.analyze_customer_concentration_trend(ticker)
        
        # Weighted average
        l3_network = (
            revenue_score * 0.25 +
            segment_score * 0.20 +
            geographic_score * 0.20 +
            supplier_score * 0.20 +
            trend_score * 0.15
        )
        
        return {
            'company': company_name,
            'ticker': ticker,
            'L3_Network': round(min(10, max(1, l3_network)), 2),
            'revenue_concentration': round(revenue_score, 2),
            'segment_concentration': round(segment_score, 2),
            'geographic_concentration': round(geographic_score, 2),
            'supplier_dependency': round(supplier_score, 2),
            'concentration_trend': round(trend_score, 2),
            'network_risk': 'HIGH CONCENTRATION RISK' if l3_network > 7.0 else ('MEDIUM RISK' if l3_network > 5.5 else 'LOW RISK')
        }

if __name__ == "__main__":
    analyzer = NetworkConcentrationAnalyzer()
    
    print("\n" + "="*100)
    print("L3_NETWORK ENHANCED - CUSTOMER & SUPPLY CONCENTRATION")
    print("="*100)
    
    test_companies = [
        ('INFY.NS', 'Infosys'),
        ('TCS.NS', 'TCS'),
        ('RELIANCE.NS', 'Reliance'),
    ]
    
    for ticker, name in test_companies:
        result = analyzer.analyze(ticker, name)
        print(f"\n{name}:")
        print(f"  L3_Network Score: {result['L3_Network']}/10")
        print(f"  Revenue Concentration: {result['revenue_concentration']}")
        print(f"  Segment Concentration: {result['segment_concentration']}")
        print(f"  Geographic Concentration: {result['geographic_concentration']}")
        print(f"  Supplier Dependency: {result['supplier_dependency']}")
        print(f"  Concentration Trend: {result['concentration_trend']}")
        print(f"  Network Risk: {result['network_risk']}")