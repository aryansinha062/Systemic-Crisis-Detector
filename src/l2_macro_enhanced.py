"""
PROPRIETARY & CONFIDENTIAL
L2 MACRO ENHANCED - REAL ECONOMIC INDICATORS (FIXED)
Patent Pending: "12-Layer Algorithmic Fraud Detection System"
© 2026 Aryan Sinha. All Rights Reserved.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class MacroIndicatorAnalyzer:
    """
    Detect macro stress signals using REAL economic data
    Global yields, currency stress, inflation, credit conditions
    """
    
    def __init__(self):
        self.name = "L2_Macro_Enhanced"
    
    def get_rbi_stress_indicator(self):
        """
        Get RBI stress from INR depreciation
        INR weakness = RBI rate hikes = credit crunch
        """
        try:
            inr_usd = yf.Ticker('INRUSD=X')
            data = inr_usd.history(period='1y')
            
            if len(data) > 30:
                recent_30d = data['Close'].tail(30).mean()
                year_ago = data['Close'].head(30).mean()
                
                # INR depreciation = RBI stress
                depreciation = (recent_30d - year_ago) / year_ago
                
                if depreciation > 0.08:  # >8% depreciation
                    return 8.5  # High stress
                elif depreciation > 0.05:
                    return 7.0
                elif depreciation > 0.02:
                    return 5.5
                else:
                    return 3.0  # INR stable
            else:
                return 5.0
        except Exception as e:
            print(f"Error getting RBI stress: {str(e)}")
            return 5.0
    
    def get_global_yield_stress(self):
        """
        Get US 10-year yield trend
        Rising yields = capital flight = EM stress
        """
        try:
            # US 10-year bond yield (proxy for global rates)
            ust10y = yf.Ticker('^TNX')
            data = ust10y.history(period='1y')
            
            if len(data) > 30:
                recent = data['Close'].tail(30).mean()
                prev = data['Close'].iloc[-120:-90].mean()
                
                # Rising yields
                yield_rise = recent - prev
                
                if yield_rise > 0.5:  # >50bps rise
                    return 8.0
                elif yield_rise > 0.25:
                    return 6.5
                elif yield_rise > 0:
                    return 5.0
                else:
                    return 3.0
            else:
                return 5.0
        except Exception as e:
            print(f"Error getting yield stress: {str(e)}")
            return 5.0
    
    def get_corporate_credit_stress(self):
        """
        Get corporate credit stress from volatility
        High volatility = credit stress = fraud risk
        """
        try:
            # S&P 500 (global risk barometer)
            sp500 = yf.Ticker('^GSPC')
            data = sp500.history(period='1y')
            
            if len(data) > 30:
                recent_vol = data['Close'].tail(30).pct_change().std()
                annual_vol = data['Close'].pct_change().std()
                
                vol_ratio = recent_vol / annual_vol if annual_vol > 0 else 1.0
                
                if vol_ratio > 1.8:  # High volatility
                    return 8.5
                elif vol_ratio > 1.5:
                    return 7.0
                elif vol_ratio > 1.2:
                    return 5.5
                else:
                    return 3.0
            else:
                return 5.0
        except Exception as e:
            print(f"Error getting credit stress: {str(e)}")
            return 5.0
    
    def get_inflation_pressure(self):
        """
        Detect inflation from commodity prices
        Crude oil price = inflation proxy
        """
        try:
            crude = yf.Ticker('CL=F')
            data = crude.history(period='1y')
            
            if len(data) > 30:
                recent = data['Close'].tail(30).mean()
                year_ago = data['Close'].head(30).mean()
                
                inflation_rate = (recent - year_ago) / year_ago if year_ago > 0 else 0
                
                if inflation_rate > 0.25:  # >25% inflation
                    return 8.5
                elif inflation_rate > 0.15:
                    return 7.0
                elif inflation_rate > 0.05:
                    return 5.0
                else:
                    return 3.0
            else:
                return 5.0
        except Exception as e:
            print(f"Error getting inflation: {str(e)}")
            return 5.0
    
    def get_sector_specific_stress(self, ticker):
        """
        Get sector stress from individual stock volatility
        Used as proxy for sector health
        """
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period='6mo')
            
            if len(data) > 30:
                recent_vol = data['Close'].tail(30).pct_change().std()
                
                # Annualize volatility
                annual_vol = recent_vol * np.sqrt(252)
                
                if annual_vol > 0.50:  # >50% annualized vol
                    return 8.0
                elif annual_vol > 0.35:
                    return 6.5
                elif annual_vol > 0.20:
                    return 5.0
                else:
                    return 3.0
            else:
                return 5.0
        except Exception as e:
            print(f"Error getting sector stress: {str(e)}")
            return 5.0
    
    def analyze(self, ticker, company_name):
        """
        Calculate overall L2_Macro score
        Combines: RBI stress, global yields, credit stress, inflation, sector vol
        """
        
        rbi_score = self.get_rbi_stress_indicator()
        yield_score = self.get_global_yield_stress()
        credit_score = self.get_corporate_credit_stress()
        inflation_score = self.get_inflation_pressure()
        sector_score = self.get_sector_specific_stress(ticker)
        
        # Weighted average
        l2_macro = (
            rbi_score * 0.25 +
            yield_score * 0.20 +
            credit_score * 0.20 +
            inflation_score * 0.20 +
            sector_score * 0.15
        )
        
        return {
            'company': company_name,
            'ticker': ticker,
            'L2_Macro': round(min(10, max(1, l2_macro)), 2),
            'rbi_stress': round(rbi_score, 2),
            'global_yields': round(yield_score, 2),
            'credit_stress': round(credit_score, 2),
            'inflation': round(inflation_score, 2),
            'sector_volatility': round(sector_score, 2),
            'macro_risk': 'HIGH MACRO STRESS' if l2_macro > 7.0 else ('MEDIUM STRESS' if l2_macro > 5.5 else 'LOW STRESS')
        }

if __name__ == "__main__":
    analyzer = MacroIndicatorAnalyzer()
    
    print("\n" + "="*100)
    print("L2_MACRO ENHANCED - REAL ECONOMIC INDICATORS (FIXED)")
    print("="*100)
    
    test_companies = [
        ('INFY.NS', 'Infosys'),
        ('TCS.NS', 'TCS'),
        ('RELIANCE.NS', 'Reliance'),
    ]
    
    for ticker, name in test_companies:
        result = analyzer.analyze(ticker, name)
        print(f"\n{name}:")
        print(f"  L2_Macro Score: {result['L2_Macro']}/10")
        print(f"  RBI Stress: {result['rbi_stress']}")
        print(f"  Global Yields: {result['global_yields']}")
        print(f"  Credit Stress: {result['credit_stress']}")
        print(f"  Inflation: {result['inflation']}")
        print(f"  Sector Volatility: {result['sector_volatility']}")
        print(f"  Macro Risk: {result['macro_risk']}")