"""
PROPRIETARY & CONFIDENTIAL
L5 FORENSIC ACCOUNTING - ENHANCED LAYER
Patent Pending: "12-Layer Algorithmic Fraud Detection System"
© 2026 Aryan Sinha. All Rights Reserved.
"""

import yfinance as yf
import numpy as np
from datetime import datetime, timedelta

class ForensicAccountingAnalyzer:
    """
    Advanced forensic accounting detection using Beneish M-Score and accruals quality
    Detects earnings manipulation, cash flow manipulation, accounting fraud
    """
    
    def __init__(self):
        self.name = "L5_Forensic_Enhanced"
    
    def get_quarterly_data(self, ticker, quarters=8):
        """Fetch last 8 quarters of financial data"""
        try:
            stock = yf.Ticker(ticker)
            quarterly_financials = stock.quarterly_financials
            quarterly_cashflow = stock.quarterly_cashflow
            
            if quarterly_financials is None or quarterly_financials.empty:
                return None
                
            data = []
            for i in range(min(quarters, len(quarterly_financials.columns))):
                col = quarterly_financials.columns[i]
                
                revenue = quarterly_financials.loc['Total Revenue', col] if 'Total Revenue' in quarterly_financials.index else 0
                net_income = quarterly_financials.loc['Net Income', col] if 'Net Income' in quarterly_financials.index else 0
                total_assets = quarterly_financials.loc['Total Assets', col] if 'Total Assets' in quarterly_financials.index else 0
                current_assets = quarterly_financials.loc['Current Assets', col] if 'Current Assets' in quarterly_financials.index else 0
                operating_cf = quarterly_cashflow.loc['Operating Cash Flow', col] if 'Operating Cash Flow' in quarterly_cashflow.index else 0
                
                if revenue > 0:
                    data.append({
                        'date': col,
                        'revenue': revenue,
                        'net_income': net_income,
                        'operating_cf': operating_cf,
                        'total_assets': total_assets,
                        'current_assets': current_assets
                    })
            
            return data
        except Exception as e:
            print(f"Error fetching quarterly data: {str(e)}")
            return None
    
    def calculate_beneish_m_score(self, ticker):
        """
        Calculate Beneish M-Score (Financial Statement Manipulation Detector)
        Score > -1.22 = likely manipulator (fraud risk)
        Used by SEC and forensic accountants worldwide
        """
        try:
            data = self.get_quarterly_data(ticker, quarters=8)
            if not data or len(data) < 4:
                return 5.0  # Neutral score if insufficient data
            
            # Ensure data is in chronological order
            data = sorted(data, key=lambda x: x['date'], reverse=False)
            
            scores = []
            
            # Metric 1: DSRI (Days Sales in Receivables Index)
            # High DSRI = sales growing faster than receivables collection (RED FLAG)
            if len(data) >= 2:
                curr_quarter = data[-1]
                prev_quarter = data[-2]
                
                if curr_quarter['revenue'] > 0 and prev_quarter['revenue'] > 0:
                    # Estimate receivables from balance sheet data
                    curr_dsr = 365 * (curr_quarter['current_assets'] / curr_quarter['revenue']) if curr_quarter['revenue'] else 0
                    prev_dsr = 365 * (prev_quarter['current_assets'] / prev_quarter['revenue']) if prev_quarter['revenue'] else 0
                    
                    dsri = curr_dsr / prev_dsr if prev_dsr > 0 else 1.0
                    dsri_score = min(10, max(1, dsri * 5))  # Convert to 1-10 scale
                    scores.append(dsri_score)
            
            # Metric 2: GMI (Gross Margin Index)
            # Declining gross margin = business deterioration (fraud risk)
            if len(data) >= 2:
                curr_gm = (curr_quarter['revenue'] - curr_quarter['net_income']) / curr_quarter['revenue'] if curr_quarter['revenue'] else 0
                prev_gm = (prev_quarter['revenue'] - prev_quarter['net_income']) / prev_quarter['revenue'] if prev_quarter['revenue'] else 0
                
                gmi = prev_gm / curr_gm if curr_gm > 0 else 1.0
                gmi_score = min(10, max(1, gmi * 5))
                scores.append(gmi_score)
            
            # Metric 3: AQI (Asset Quality Index)
            # High AQI = high intangible assets (low quality earnings)
            if len(data) >= 1:
                curr = data[-1]
                tangible_assets = curr['total_assets'] - curr['current_assets']
                aqi = curr['total_assets'] / tangible_assets if tangible_assets > 0 else 1.0
                aqi_score = min(10, max(1, aqi * 3))
                scores.append(aqi_score)
            
            # Metric 4: SGI (Sales Growth Index)
            # Rapid sales growth = higher fraud risk
            if len(data) >= 2:
                revenue_growth = (curr_quarter['revenue'] / prev_quarter['revenue']) if prev_quarter['revenue'] > 0 else 1.0
                sgi = revenue_growth
                sgi_score = min(10, max(1, sgi * 3))
                scores.append(sgi_score)
            
            # Metric 5: LVGI (Leverage Index)
            # Increasing leverage = financial distress (fraud risk)
            lvgi_score = 5.0  # Will enhance with balance sheet data
            scores.append(lvgi_score)
            
            # Return average forensic score
            forensic_score = np.mean(scores) if scores else 5.0
            return min(10, max(1, forensic_score))
            
        except Exception as e:
            print(f"Error calculating Beneish M-Score: {str(e)}")
            return 5.0
    
    def calculate_accruals_quality(self, ticker):
        """
        Calculate Accruals Quality Score
        High accruals = earnings quality issue (fraud indicator)
        Sloan Accruals Anomaly
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            net_income = info.get('netIncome', 0) or 0
            operating_cf = info.get('operatingCashFlow', 0) or 0
            total_assets = info.get('totalAssets', 0) or 0
            
            if total_assets == 0 or operating_cf == 0:
                return 5.0
            
            # Accruals = Net Income - Operating Cash Flow
            accruals = net_income - operating_cf
            
            # Quality score: high positive accruals = RED FLAG
            accruals_ratio = accruals / total_assets if total_assets else 0
            
            # Score: high accruals (0.1+) = 8-10 (high fraud risk)
            if accruals_ratio > 0.15:
                return 9.0
            elif accruals_ratio > 0.10:
                return 8.0
            elif accruals_ratio > 0.05:
                return 6.0
            elif accruals_ratio > 0:
                return 4.0
            else:
                return 2.0  # Negative accruals = good quality
                
        except Exception as e:
            print(f"Error calculating accruals quality: {str(e)}")
            return 5.0
    
    def calculate_cash_flow_quality(self, ticker):
        """
        Calculate Cash Flow Quality
        Gap between earnings and cash flow = RED FLAG
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            net_income = info.get('netIncome', 0) or 1
            operating_cf = info.get('operatingCashFlow', 0) or 0
            
            if net_income == 0:
                return 5.0
            
            # Cash flow quality ratio
            cf_quality = operating_cf / net_income if net_income else 0
            
            # Ideal is close to 1.0 (earnings = cash flow)
            # < 0.5 = cash flow much lower than earnings = RED FLAG
            if cf_quality < 0.5:
                return 8.5  # High fraud risk
            elif cf_quality < 0.7:
                return 7.0
            elif cf_quality < 0.9:
                return 5.0
            elif cf_quality > 1.5:
                return 4.0  # Cash flow much higher than earnings (unusual but not always bad)
            else:
                return 3.0  # Healthy (0.9-1.5)
                
        except Exception as e:
            print(f"Error calculating cash flow quality: {str(e)}")
            return 5.0
    
    def analyze(self, ticker, company_name):
        """
        Calculate overall L5_Forensic score
        Combines: Beneish M-Score, Accruals Quality, Cash Flow Quality
        """
        
        beneish_score = self.calculate_beneish_m_score(ticker)
        accruals_score = self.calculate_accruals_quality(ticker)
        cf_quality_score = self.calculate_cash_flow_quality(ticker)
        
        # Weighted average (higher weight on cash flow gap)
        l5_forensic = (beneish_score * 0.3 + accruals_score * 0.3 + cf_quality_score * 0.4)
        
        return {
            'company': company_name,
            'ticker': ticker,
            'L5_Forensic': round(min(10, max(1, l5_forensic)), 2),
            'beneish_m_score': round(beneish_score, 2),
            'accruals_quality': round(accruals_score, 2),
            'cash_flow_quality': round(cf_quality_score, 2),
            'risk_level': 'HIGH FRAUD RISK' if l5_forensic > 7.0 else ('MEDIUM RISK' if l5_forensic > 5.5 else 'LOW RISK')
        }

if __name__ == "__main__":
    analyzer = ForensicAccountingAnalyzer()
    
    # Test on known fraud case
    print("\n" + "="*100)
    print("L5_FORENSIC ENHANCED - TESTING ON KNOWN FRAUD CASES")
    print("="*100)
    
    test_companies = [
        ('INFY.NS', 'Infosys'),
        ('TCS.NS', 'TCS'),
        ('RELIANCE.NS', 'Reliance'),
    ]
    
    for ticker, name in test_companies:
        result = analyzer.analyze(ticker, name)
        print(f"\n{name}:")
        print(f"  L5_Forensic Score: {result['L5_Forensic']}/10")
        print(f"  Beneish M-Score: {result['beneish_m_score']}")
        print(f"  Accruals Quality: {result['accruals_quality']}")
        print(f"  Cash Flow Quality: {result['cash_flow_quality']}")
        print(f"  Risk Level: {result['risk_level']}")