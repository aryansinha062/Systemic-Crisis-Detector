"""
Layer 4: Behavioral Signal Detection
Insider trading, board departures, executive changes, patent activity
"""

from datetime import datetime

class BehavioralDetector:
    
    def __init__(self):
        self.timestamp = datetime.now()
    
    def analyze_insider_trading(self, ticker):
        data = {
            'TSLA': {'insider_sales_90d': 45, 'insider_buys_90d': 3, 'sales_to_buys_ratio': 15.0, 'avg_sale_price': 245.0, 'current_price': 250.0, 'prediction_power': 92},
            'AAPL': {'insider_sales_90d': 8, 'insider_buys_90d': 12, 'sales_to_buys_ratio': 0.67, 'avg_sale_price': 180.0, 'current_price': 185.0, 'prediction_power': 88},
            'META': {'insider_sales_90d': 62, 'insider_buys_90d': 2, 'sales_to_buys_ratio': 31.0, 'avg_sale_price': 380.0, 'current_price': 420.0, 'prediction_power': 91}
        }
        
        d = data.get(ticker, {'insider_sales_90d': 0, 'insider_buys_90d': 0, 'sales_to_buys_ratio': 0, 'prediction_power': 85})
        risk = 0
        flags = []
        
        if d['sales_to_buys_ratio'] > 5.0:
            risk += 2.5
            flags.append(f'Heavy insider selling: {d["sales_to_buys_ratio"]:.1f}x ratio')
        
        if d['insider_sales_90d'] > 50:
            risk += 2.0
            flags.append(f'Massive insider sales: {d["insider_sales_90d"]} transactions')
        
        risk = min(risk, 10.0)
        alert = 'CRITICAL' if risk >= 7.0 else 'WARNING' if risk >= 4.0 else 'NORMAL'
        
        return {'ticker': ticker, 'insider_risk_score': risk, 'insider_sales_90d': d['insider_sales_90d'], 'sales_to_buys_ratio': d['sales_to_buys_ratio'], 'red_flags': flags, 'alert': alert, 'prediction_power': d['prediction_power']}
    
    def analyze_board_departures(self, ticker):
        data = {
            'TSLA': {'departures_12m': 4, 'departure_rate': 0.36, 'avg_tenure_departed': 3.2, 'reason_unknown_count': 2},
            'AAPL': {'departures_12m': 1, 'departure_rate': 0.11, 'avg_tenure_departed': 5.1, 'reason_unknown_count': 0},
            'META': {'departures_12m': 6, 'departure_rate': 0.60, 'avg_tenure_departed': 2.8, 'reason_unknown_count': 3}
        }
        
        d = data.get(ticker, {'departures_12m': 0, 'departure_rate': 0.0, 'reason_unknown_count': 0})
        risk = 0
        flags = []
        
        if d['departures_12m'] >= 3:
            risk += 2.5
            flags.append(f'Multiple board departures: {d["departures_12m"]} in 12 months')
        
        if d['reason_unknown_count'] >= 2:
            risk += 2.0
            flags.append(f'Unexplained departures: {d["reason_unknown_count"]} without public reason')
        
        risk = min(risk, 10.0)
        alert = 'CRITICAL' if risk >= 7.0 else 'WARNING' if risk >= 4.0 else 'NORMAL'
        
        return {'ticker': ticker, 'departure_risk_score': risk, 'departures_12m': d['departures_12m'], 'departure_rate': d['departure_rate'], 'red_flags': flags, 'alert': alert}
    
    def analyze_executive_changes(self, ticker):
        data = {
            'TSLA': {'ceo_changes_3y': 0, 'cfo_changes_3y': 1, 'cto_changes_3y': 2, 'key_exec_departures': 5},
            'AAPL': {'ceo_changes_3y': 0, 'cfo_changes_3y': 0, 'cto_changes_3y': 1, 'key_exec_departures': 2},
            'META': {'ceo_changes_3y': 0, 'cfo_changes_3y': 1, 'cto_changes_3y': 1, 'key_exec_departures': 8}
        }
        
        d = data.get(ticker, {'ceo_changes_3y': 0, 'cfo_changes_3y': 0, 'cto_changes_3y': 0, 'key_exec_departures': 0})
        risk = 0
        flags = []
        
        if d['ceo_changes_3y'] >= 1:
            risk += 3.0
            flags.append('CEO change in last 3 years')
        
        if d['key_exec_departures'] >= 5:
            risk += 2.5
            flags.append(f'High executive turnover: {d["key_exec_departures"]} key departures')
        
        risk = min(risk, 10.0)
        alert = 'CRITICAL' if risk >= 7.0 else 'WARNING' if risk >= 4.0 else 'NORMAL'
        
        return {'ticker': ticker, 'exec_risk_score': risk, 'key_departures': d['key_exec_departures'], 'ceo_changes': d['ceo_changes_3y'], 'red_flags': flags, 'alert': alert}
    
    def analyze_patent_activity(self, ticker):
        data = {
            'TSLA': {'patents_filed_12m': 156, 'patents_granted_12m': 89, 'patent_trend': 'STABLE', 'citations_per_patent': 2.3},
            'AAPL': {'patents_filed_12m': 892, 'patents_granted_12m': 645, 'patent_trend': 'GROWING', 'citations_per_patent': 3.8},
            'META': {'patents_filed_12m': 234, 'patents_granted_12m': 145, 'patent_trend': 'DECLINING', 'citations_per_patent': 1.9}
        }
        
        d = data.get(ticker, {'patents_filed_12m': 0, 'patent_trend': 'UNKNOWN', 'citations_per_patent': 0})
        risk = 0
        flags = []
        
        if d['patent_trend'] == 'DECLINING':
            risk += 2.0
            flags.append('Patent filing activity declining')
        
        if d['citations_per_patent'] < 2.0:
            risk += 1.5
            flags.append('Low patent citation rate (weak innovation)')
        
        risk = min(risk, 10.0)
        alert = 'CRITICAL' if risk >= 7.0 else 'WARNING' if risk >= 4.0 else 'NORMAL'
        
        return {'ticker': ticker, 'patent_risk_score': risk, 'patents_filed_12m': d['patents_filed_12m'], 'patent_trend': d['patent_trend'], 'red_flags': flags, 'alert': alert}
    
    def generate_behavioral_alert(self, ticker):
        insider = self.analyze_insider_trading(ticker)
        departures = self.analyze_board_departures(ticker)
        exec_changes = self.analyze_executive_changes(ticker)
        patents = self.analyze_patent_activity(ticker)
        
        combined_risk = (insider['insider_risk_score'] + departures['departure_risk_score'] + exec_changes['exec_risk_score'] + patents['patent_risk_score']) / 4
        
        alert = 'CRITICAL' if combined_risk >= 7.0 else 'WARNING' if combined_risk >= 4.0 else 'NORMAL'
        
        return {'ticker': ticker, 'behavioral_risk_score': combined_risk, 'insider_trading': insider, 'board_departures': departures, 'executive_changes': exec_changes, 'patent_activity': patents, 'behavioral_alert': alert}


if __name__ == '__main__':
    detector = BehavioralDetector()
    print(detector.generate_behavioral_alert('TSLA'))