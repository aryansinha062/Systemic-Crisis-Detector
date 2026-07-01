"""
PROPRIETARY & CONFIDENTIAL
SEBI API INTEGRATION v2.0 - WITH EXTREME v5.2 DETECTOR
Patent Pending: "12-Layer Algorithmic Fraud Detection System"
© 2026 Aryan Sinha. All Rights Reserved.
"""

import json
import yfinance as yf
import sys
sys.path.insert(0, 'src')

from extreme_detector_v52 import ExtremePositionDetectorV52

class SebiDataFetcherV2:
    def __init__(self):
        self.detector = ExtremePositionDetectorV52()
        self.results = []
        
    def get_indian_companies(self, count=100):
        """Get list of top 51 Indian companies from NSE"""
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
    
    def run_100_company_test_extreme(self):
        """Run EXTREME detector on 100 companies"""
        companies = self.get_indian_companies(100)
        
        print("\n" + "="*120)
        print("EXTREME DETECTOR v5.2 - 100 COMPANY TEST WITH ENHANCED LAYERS".center(120))
        print("="*120)
        print(f"Processing {len(companies)} companies with L4, L5, L8 enhanced analysis...\n")
        
        processed = 0
        fraud_alerts = []
        high_risk = []
        warnings = []
        
        for ticker, name, sector in companies:
            try:
                result = self.detector.detect_fraud(ticker, name)
                self.results.append({
                    'company': name,
                    'sector': sector,
                    'ticker': ticker,
                    'alert': result['alert'],
                    'score': result['score'],
                    'enhanced_layer_avg': result['enhanced_layer_avg'],
                    'enhanced_risk': result['enhanced_risk'],
                    'L4_Behavioral': result['enhanced_layers']['L4_Behavioral']['L4_Behavioral'],
                    'L5_Forensic': result['enhanced_layers']['L5_Forensic']['L5_Forensic'],
                    'L8_Regulatory': result['enhanced_layers']['L8_Regulatory']['L8_Regulatory'],
                })
                
                processed += 1
                
                # Categorize
                if result['enhanced_layer_avg'] >= 7.0:
                    fraud_alerts.append(name)
                elif result['enhanced_layer_avg'] >= 5.5:
                    high_risk.append(name)
                else:
                    warnings.append(name)
                
                print(f"✅ {processed:3d}. {name:<30} {result['enhanced_risk']:<20} L4:{result['enhanced_layers']['L4_Behavioral']['L4_Behavioral']:5.2f} L5:{result['enhanced_layers']['L5_Forensic']['L5_Forensic']:5.2f} L8:{result['enhanced_layers']['L8_Regulatory']['L8_Regulatory']:5.2f}")
                
            except Exception as e:
                print(f"❌ Error processing {name}: {str(e)}")
        
        print("\n" + "="*120)
        self.print_summary(fraud_alerts, high_risk, warnings)
        self.export_results()
        
    def print_summary(self, fraud_alerts, high_risk, warnings):
        """Print summary of enhanced results"""
        total = len(self.results)
        
        print(f"\nEXTREME DETECTION RESULTS:")
        print(f"  Total Processed: {total}")
        print(f"  🚨 Extreme Fraud Risk (≥7.0): {len(fraud_alerts)}")
        print(f"  🟠 High Risk (5.5-6.9): {len(high_risk)}")
        print(f"  ⚠️  Medium/Low Risk (<5.5): {len(warnings)}")
        
        if fraud_alerts:
            print(f"\n🚨 EXTREME FRAUD RISK COMPANIES:")
            for company in fraud_alerts:
                r = next(r for r in self.results if r['company'] == company)
                print(f"   - {company:<30} Enhanced Avg: {r['enhanced_layer_avg']:5.2f}/10 (L4:{r['L4_Behavioral']:5.2f} L5:{r['L5_Forensic']:5.2f} L8:{r['L8_Regulatory']:5.2f})")
        
        if high_risk:
            print(f"\n🟠 HIGH RISK COMPANIES (Top 10):")
            for company in high_risk[:10]:
                r = next(r for r in self.results if r['company'] == company)
                print(f"   - {company:<30} Enhanced Avg: {r['enhanced_layer_avg']:5.2f}/10 (L4:{r['L4_Behavioral']:5.2f} L5:{r['L5_Forensic']:5.2f} L8:{r['L8_Regulatory']:5.2f})")
        
        print("\n" + "="*120 + "\n")
    
    def export_results(self):
        """Export results to JSON"""
        with open('extreme_100_company_test_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        print("Results saved to: extreme_100_company_test_results.json")

if __name__ == "__main__":
    fetcher = SebiDataFetcherV2()
    fetcher.run_100_company_test_extreme()