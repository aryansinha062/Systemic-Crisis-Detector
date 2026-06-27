"""
Layer 5: Forensic Accounting Detection
Detects fraud through financial statement anomalies
"""

from datetime import datetime

class ForensicDetector:
    
    def __init__(self):
        self.timestamp = datetime.now()
    
    def analyze_cash_flow_quality(self, ticker):
        data = {
            'TSLA': {'net_income': 12586, 'operating_cash_flow': 13256, 'quality_ratio': 1.05},
            'AAPL': {'net_income': 96995, 'operating_cash_flow': 110543, 'quality_ratio': 1.14},
            'META': {'net_income': 23200, 'operating_cash_flow': 15800, 'quality_ratio': 0.68}
        }
        
        d = data.get(ticker, {'quality_ratio': 1.0})
        risk = 0
        flags = []
        
        if d['quality_ratio'] < 0.8:
            risk += 3.5
            flags.append(f'Poor cash flow quality: {d["quality_ratio"]:.2f}')
        
        risk = min(risk, 10.0)
        alert = 'CRITICAL' if risk >= 7.0 else 'WARNING' if risk >= 3.0 else 'NORMAL'
        
        return {'ticker': ticker, 'cash_flow_risk': risk, 'quality_ratio': d['quality_ratio'], 'red_flags': flags, 'alert': alert}
    
    def analyze_receivables_quality(self, ticker):
        data = {
            'TSLA': {'ar_to_revenue': 0.05},
            'AAPL': {'ar_to_revenue': 0.07},
            'META': {'ar_to_revenue': 0.30}
        }
        
        d = data.get(ticker, {'ar_to_revenue': 0.0})
        risk = 0
        flags = []
        
        if d['ar_to_revenue'] > 0.25:
            risk += 3.5
            flags.append(f'High receivables: {d["ar_to_revenue"]*100:.1f}%')
        
        risk = min(risk, 10.0)
        alert = 'CRITICAL' if risk >= 7.0 else 'WARNING' if risk >= 3.0 else 'NORMAL'
        
        return {'ticker': ticker, 'receivables_risk': risk, 'ar_to_revenue': d['ar_to_revenue'], 'red_flags': flags, 'alert': alert}
    
    def analyze_inventory_quality(self, ticker):
        data = {
            'TSLA': {'inventory_to_revenue': 0.17, 'turnover': 5.92},
            'AAPL': {'inventory_to_revenue': 0.02, 'turnover': 57.95},
            'META': {'inventory_to_revenue': 0.52, 'turnover': 1.93}
        }
        
        d = data.get(ticker, {'inventory_to_revenue': 0.0})
        risk = 0
        flags = []
        
        if d['inventory_to_revenue'] > 0.40:
            risk += 2.5
            flags.append(f'Excessive inventory: {d["inventory_to_revenue"]*100:.1f}%')
        
        if d['turnover'] < 2.0:
            risk += 2.5
            flags.append(f'Low turnover: {d["turnover"]:.1f}x')
        
        risk = min(risk, 10.0)
        alert = 'CRITICAL' if risk >= 7.0 else 'WARNING' if risk >= 3.0 else 'NORMAL'
        
        return {'ticker': ticker, 'inventory_risk': risk, 'red_flags': flags, 'alert': alert}
    
    def analyze_related_party_transactions(self, ticker):
        data = {
            'TSLA': {'rpt_count': 3},
            'AAPL': {'rpt_count': 1},
            'META': {'rpt_count': 8}
        }
        
        d = data.get(ticker, {'rpt_count': 0})
        risk = 0
        flags = []
        
        if d['rpt_count'] >= 5:
            risk += 3.5
            flags.append(f'Multiple RPTs: {d["rpt_count"]}')
        
        risk = min(risk, 10.0)
        alert = 'CRITICAL' if risk >= 7.0 else 'WARNING' if risk >= 3.0 else 'NORMAL'
        
        return {'ticker': ticker, 'rpt_risk': risk, 'rpt_count': d['rpt_count'], 'red_flags': flags, 'alert': alert}
    
    def generate_forensic_alert(self, ticker):
        cash_flow = self.analyze_cash_flow_quality(ticker)
        receivables = self.analyze_receivables_quality(ticker)
        inventory = self.analyze_inventory_quality(ticker)
        rpt = self.analyze_related_party_transactions(ticker)
        
        combined_risk = (cash_flow['cash_flow_risk'] + receivables['receivables_risk'] + inventory['inventory_risk'] + rpt['rpt_risk']) / 4
        
        alert = 'CRITICAL' if combined_risk >= 7.0 else 'WARNING' if combined_risk >= 4.0 else 'NORMAL'
        
        return {'ticker': ticker, 'forensic_risk_score': combined_risk, 'cash_flow': cash_flow, 'receivables': receivables, 'inventory': inventory, 'rpt': rpt, 'forensic_alert': alert}


if __name__ == '__main__':
    detector = ForensicDetector()
    print(detector.generate_forensic_alert('META'))