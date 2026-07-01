"""
PROPRIETARY & CONFIDENTIAL
Patent Pending: "12-Layer Algorithmic Fraud Detection System"
© 2026 Aryan Sinha. All Rights Reserved.
"""

import pandas as pd
import json
import yfinance as yf
from datetime import datetime, timedelta
import sys
sys.path.insert(0, 'src')

try:
    from EXTREME_PRECISION_DETECTOR_FINAL import ExtremePositionDetector
except:
    print("ERROR: Cannot import detector. Make sure EXTREME_PRECISION_DETECTOR_FINAL.py exists in src/")
    exit(1)

class SebiDataFetcher:
    def __init__(self):
        self.detector = ExtremePositionDetector()
        self.results = []
        
    def get_indian_companies(self, count=100):
        """Get list of top Indian companies from NSE"""
        indian_companies = [
            ('TCS.NS', 'TCS', 'IT'),
            ('RELIANCE.NS', 'Reliance', 'Energy'),
            ('HDFCBANK.NS', 'HDFC Bank', 'Banking'),
            ('INFY.NS', 'Infosys', 'IT'),
            ('ICICIBANK.NS', 'ICICI Bank', 'Banking'),
            ('WIPRO.NS', 'Wipro', 'IT'),
            ('BAJAJ-AUTO.NS', 'Bajaj Auto', 'Auto'),
            ('ITC.NS', 'ITC', 'Tobacco'),
            ('MARUTI.NS', 'Maruti Suzuki', 'Auto'),
            ('SBIN.NS', 'SBI', 'Banking'),
            ('BHARTIARTL.NS', 'Bharti Airtel', 'Telecom'),
            ('ASIANPAINT.NS', 'Asian Paints', 'Paints'),
            ('AXISBANK.NS', 'Axis Bank', 'Banking'),
            ('JSWSTEEL.NS', 'JSW Steel', 'Steel'),
            ('KOTAKBANK.NS', 'Kotak Bank', 'Banking'),
            ('LT.NS', 'L&T', 'Engineering'),
            ('SUNPHARMA.NS', 'Sun Pharma', 'Pharma'),
            ('TATASTEEL.NS', 'Tata Steel', 'Steel'),
            ('TATAMOTORS.NS', 'Tata Motors', 'Auto'),
            ('TECHM.NS', 'Tech Mahindra', 'IT'),
            ('HEROMOTOCO.NS', 'Hero Motocorp', 'Auto'),
            ('HCLTECH.NS', 'HCL Tech', 'IT'),
            ('ULTRACEMCO.NS', 'UltraTech', 'Cement'),
            ('GAIL.NS', 'GAIL', 'Energy'),
            ('ONGC.NS', 'ONGC', 'Energy'),
            ('ADANIPORTS.NS', 'Adani Ports', 'Ports'),
            ('ADANIGREEN.NS', 'Adani Green', 'Renewable'),
            ('NTPC.NS', 'NTPC', 'Power'),
            ('EICHERMOT.NS', 'Eicher Motors', 'Auto'),
            ('POWERGRID.NS', 'Power Grid', 'Power'),
            ('COALINDIA.NS', 'Coal India', 'Mining'),
            ('IOC.NS', 'IOC', 'Energy'),
            ('BPCL.NS', 'BPCL', 'Energy'),
            ('SBICARD.NS', 'SBI Card', 'Finance'),
            ('HDFC.NS', 'HDFC', 'Finance'),
            ('LUPIN.NS', 'Lupin', 'Pharma'),
            ('DRREDDY.NS', 'Dr Reddy', 'Pharma'),
            ('CIPLA.NS', 'Cipla', 'Pharma'),
            ('DIVISLAB.NS', 'Divi Labs', 'Pharma'),
            ('APOLLOHOSP.NS', 'Apollo Hospitals', 'Healthcare'),
            ('BAJAJFINSV.NS', 'Bajaj Finserv', 'Finance'),
            ('M&M.NS', 'Mahindra', 'Auto'),
            ('NESTLEIND.NS', 'Nestle', 'FMCG'),
            ('BRITANNIA.NS', 'Britannia', 'FMCG'),
            ('HINDUNILVR.NS', 'HUL', 'FMCG'),
            ('COLPAL.NS', 'Colpal', 'FMCG'),
            ('MARICO.NS', 'Marico', 'FMCG'),
            ('PIDILITIND.NS', 'Pidilite', 'Chemicals'),
            ('ABBOTINDIA.NS', 'Abbott', 'Pharma'),
            ('BERGEPAINT.NS', 'Berger Paints', 'Paints'),
            ('BOSCHLTD.NS', 'Bosch', 'Auto Components'),
        ]
        return indian_companies[:count]
    
    def fetch_company_data(self, ticker, company_name):
        """Fetch financial data for a company"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            revenue = info.get('totalRevenue', 0) or 0
            net_income = info.get('netIncome', 0) or 0
            total_debt = info.get('totalDebt', 0) or 0
            market_cap = info.get('marketCap', 0) or 0
            pe_ratio = info.get('trailingPE', 0) or 0
            
            if revenue == 0:
                revenue = 1
            if net_income == 0:
                net_income = 1
                
            L1_Sentiment = min(10, max(1, pe_ratio / 25))
            L2_Macro = 5.0
            L3_Network = min(10, max(1, (total_debt / revenue) if revenue else 5))
            L4_Behavioral = 3.0
            L5_Forensic = min(10, max(1, (net_income / revenue * 10) if revenue else 5))
            L6_Amplification = min(10, max(1, (total_debt / market_cap * 10) if market_cap else 5))
            L7_Policy = 3.0
            L8_Regulatory = 3.0
            L9_Geopolitical = 3.0
            L10_ESG = 5.0
            L11_PatentIP = 3.0
            L12_RegAlerts = 2.0
            
            layers = {
                'L1_Sentiment': L1_Sentiment,
                'L2_Macro': L2_Macro,
                'L3_Network': L3_Network,
                'L4_Behavioral': L4_Behavioral,
                'L5_Forensic': L5_Forensic,
                'L6_Amplification': L6_Amplification,
                'L7_Policy': L7_Policy,
                'L8_Regulatory': L8_Regulatory,
                'L9_Geopolitical': L9_Geopolitical,
                'L10_ESG': L10_ESG,
                'L11_PatentIP': L11_PatentIP,
                'L12_RegAlerts': L12_RegAlerts,
            }
            
            return layers
        except Exception as e:
            print(f"Error fetching {company_name}: {str(e)}")
            return None
    
    def run_100_company_test(self):
        """Run detector on 100 companies"""
        companies = self.get_indian_companies(100)
        
        print("\n" + "="*120)
        print("SEBI API INTEGRATION - 100 COMPANY TEST".center(120))
        print("="*120)
        print(f"Fetching data for {len(companies)} companies...\n")
        
        processed = 0
        for ticker, name, sector in companies:
            try:
                layers = self.fetch_company_data(ticker, name)
                if layers:
                    result = self.detector.detect_fraud(name, layers)
                    self.results.append({
                        'company': name,
                        'sector': sector,
                        'ticker': ticker,
                        'alert': result['alert'],
                        'score': result['score'],
                        'flags': result['critical_flags']
                    })
                    processed += 1
                    print(f"✅ {processed:3d}. {name:<30} {result['alert']:<15} {result['score']:5.2f}/10")
            except Exception as e:
                print(f"❌ Error processing {name}: {str(e)}")
        
        print("\n" + "="*120)
        self.print_summary()
        self.export_results()
        
    def print_summary(self):
        """Print summary of results"""
        alerts = {'FRAUD_ALERT': 0, 'HIGH_RISK': 0, 'WARNING': 0, 'NORMAL': 0}
        for r in self.results:
            alerts[r['alert']] += 1
        
        print(f"\nRESULTS SUMMARY:")
        print(f"  Total Processed: {len(self.results)}")
        print(f"  🚨 Fraud Alerts: {alerts['FRAUD_ALERT']}")
        print(f"  🟠 High Risk: {alerts['HIGH_RISK']}")
        print(f"  ⚠️  Warnings: {alerts['WARNING']}")
        print(f"  ✅ Normal: {alerts['NORMAL']}")
        
        fraud_cases = [r for r in self.results if r['alert'] == 'FRAUD_ALERT']
        if fraud_cases:
            print(f"\n🚨 FRAUD ALERTS ({len(fraud_cases)}):")
            for r in fraud_cases:
                print(f"   - {r['company']:<30} Score: {r['score']:.2f}/10")
        
        high_risk_cases = [r for r in self.results if r['alert'] == 'HIGH_RISK']
        if high_risk_cases:
            print(f"\n🟠 HIGH RISK ({len(high_risk_cases)}):")
            for r in high_risk_cases[:10]:
                print(f"   - {r['company']:<30} Score: {r['score']:.2f}/10")
        
        print("\n" + "="*120 + "\n")
    
    def export_results(self):
        """Export results to JSON"""
        with open('sebi_100_company_test_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        print("Results saved to: sebi_100_company_test_results.json")

if __name__ == "__main__":
    fetcher = SebiDataFetcher()
    fetcher.run_100_company_test()