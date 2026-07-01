"""
PROPRIETARY & CONFIDENTIAL
Patent Pending: "Automated 12-Layer Fraud Detection System"
© 2026 Aryan Sinha. All Rights Reserved.
"""
import json, time
from datetime import datetime

class BatchProcessor:
    def __init__(self):
        self.results = []
        self.stats = {'FRAUD_ALERT': 0, 'HIGH_RISK': 0, 'WARNING': 0, 'NORMAL': 0}
    def detect(self, company, layers):
        avg = sum(layers.values()) / 12
        critical = sum(1 for x in layers.values() if x >= 6.0)
        red = sum(1 for x in layers.values() if x >= 7.0)
        stressed = layers['L6_Amplification'] >= 6.5 or (layers['L3_Network'] >= 5.5 and layers['L5_Forensic'] < 6.0)
        if (avg >= 7.0 and critical >= 8) or (red >= 7 and avg >= 6.0):
            alert = 'FRAUD_ALERT'
        elif (avg >= 6.0 and critical >= 6) or critical >= 7:
            alert = 'HIGH_RISK'
        elif (avg >= 5.0 and critical >= 4) or stressed:
            alert = 'WARNING'
        else:
            alert = 'NORMAL'
        self.stats[alert] += 1
        return {'company': company, 'alert': alert, 'score': round(avg, 2), 'flags': critical}
    def process_batch(self, companies_data):
        for company, layers in companies_data:
            result = self.detect(company, layers)
            self.results.append(result)
        return self.results
    def rank_results(self):
        order = {'FRAUD_ALERT': 0, 'HIGH_RISK': 1, 'WARNING': 2, 'NORMAL': 3}
        return sorted(self.results, key=lambda x: (order[x['alert']], -x['score']))
    def report(self):
        ranked = self.rank_results()
        print("\n" + "="*100)
        print("BATCH RESULTS".center(100))
        print("="*100)
        print(f"Processed: {len(self.results)} | Fraud: {self.stats['FRAUD_ALERT']} | High Risk: {self.stats['HIGH_RISK']} | Warning: {self.stats['WARNING']} | Normal: {self.stats['NORMAL']}")
        print("-"*100)
        for i, r in enumerate(ranked[:20], 1):
            print(f"{i:2d}. {r['company']:<30} {r['alert']:<15} {r['score']:5.2f}/10  {r['flags']}/12 flags")
        print("="*100 + "\n")

if __name__ == "__main__":
    processor = BatchProcessor()
    test_data = [
        ('IndusInd Bank', {'L1_Sentiment': 7.5, 'L2_Macro': 4.0, 'L3_Network': 5.5, 'L4_Behavioral': 8.0, 'L5_Forensic': 8.5, 'L6_Amplification': 7.0, 'L7_Policy': 3.0, 'L8_Regulatory': 8.5, 'L9_Geopolitical': 3.0, 'L10_ESG': 8.0, 'L11_PatentIP': 2.0, 'L12_RegAlerts': 8.5}),
        ('Ramco Systems', {'L1_Sentiment': 2.5, 'L2_Macro': 2.0, 'L3_Network': 2.8, 'L4_Behavioral': 1.5, 'L5_Forensic': 2.0, 'L6_Amplification': 2.2, 'L7_Policy': 2.5, 'L8_Regulatory': 1.8, 'L9_Geopolitical': 3.0, 'L10_ESG': 2.5, 'L11_PatentIP': 2.0, 'L12_RegAlerts': 2.5}),
    ]
    processor.process_batch(test_data)
    processor.report()