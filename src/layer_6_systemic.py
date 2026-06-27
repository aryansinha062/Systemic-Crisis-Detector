"""
Layer 6: Systemic Crisis Detection
Combines all 5 layers into comprehensive risk scoring
"""

from datetime import datetime
from src.layer_1_company_risk import CompanyRiskDetector
from src.layer_2_macro_risk import MacroRiskDetector
from src.layer_3_network_cascade import NetworkCascadeDetector
from src.layer_4_behavioral import BehavioralDetector
from src.layer_5_forensic import ForensicDetector

class SystemicCrisisDetector:
    
    def __init__(self):
        self.timestamp = datetime.now()
        self.layer1 = CompanyRiskDetector()
        self.layer2 = MacroRiskDetector()
        self.layer3 = NetworkCascadeDetector()
        self.layer4 = BehavioralDetector()
        self.layer5 = ForensicDetector()
    
    def calculate_vulnerability_score(self, ticker):
        if ticker not in self.layer3.network:
            return 0.5
        
        network_data = self.layer3.network[ticker]
        supplier_count = len(network_data['suppliers'])
        creditor_count = len(network_data['creditors'])
        systemic_importance = network_data['systemic']
        
        vulnerability = 0.0
        
        if supplier_count < 3 and supplier_count > 0:
            vulnerability += 0.2
        
        if creditor_count > 5:
            vulnerability += 0.15
        
        if systemic_importance > 8.0:
            vulnerability += 0.25
        
        return min(vulnerability, 1.0)
    
    def combine_all_layers(self, ticker):
        layer1 = self.layer1.analyze_news_sentiment(ticker)
        layer1_sentiment = layer1['alert']
        
        layer2 = self.layer2.analyze_pandemic_risk()
        layer2_alert = layer2['alert']
        
        layer3_network = self.layer3.analyze_network_structure(ticker)
        layer3_network_risk = layer3_network['network_risk_score']
        
        layer4_behavioral = self.layer4.analyze_insider_trading(ticker)
        layer4_behavioral_risk = layer4_behavioral['alert']
        
        layer5_forensic = self.layer5.analyze_cash_flow_quality(ticker)
        layer5_forensic_risk = layer5_forensic['alert']
        
        vulnerability = self.calculate_vulnerability_score(ticker)
        
        risk_scores = []
        risk_scores.append(layer1['sentiment_score'] if 'sentiment_score' in layer1 else 0)
        risk_scores.append(layer3_network_risk)
        risk_scores.append(4.0 if layer4_behavioral_risk in ['CRITICAL', 'WARNING'] else 2.0)
        risk_scores.append(4.0 if layer5_forensic_risk in ['CRITICAL', 'WARNING'] else 2.0)
        
        base_risk = sum(risk_scores) / len(risk_scores)
        combined_risk = base_risk * (0.8 + vulnerability * 0.2)
        combined_risk = min(combined_risk, 10.0)
        
        if combined_risk >= 7.5:
            alert = 'CRITICAL'
        elif combined_risk >= 5.0:
            alert = 'WARNING'
        else:
            alert = 'NORMAL'
        
        return {'ticker': ticker, 'systemic_risk_score': combined_risk, 'vulnerability_score': vulnerability, 'layer1_alert': layer1_sentiment, 'layer3_risk': layer3_network_risk, 'layer4_alert': layer4_behavioral_risk, 'layer5_alert': layer5_forensic_risk, 'systemic_alert': alert}
    
    def rank_critical_companies(self, tickers):
        results = []
        for ticker in tickers:
            result = self.combine_all_layers(ticker)
            results.append((ticker, result['systemic_risk_score']))
        
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
        return {'ranked_companies': sorted_results}
    
    def generate_systemic_alert(self, ticker):
        combined = self.combine_all_layers(ticker)
        cascade = self.layer3.model_cascade_path(ticker, 30)
        
        return {'ticker': ticker, 'combined_analysis': combined, 'cascade': cascade, 'systemic_alert': combined['systemic_alert']}


if __name__ == '__main__':
    detector = SystemicCrisisDetector()
    print(detector.generate_systemic_alert('TSLA'))