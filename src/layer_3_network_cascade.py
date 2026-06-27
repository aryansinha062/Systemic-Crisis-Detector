"""
Layer 3: Financial Network Mapping & Cascade Modeling
"""

from datetime import datetime

class NetworkCascadeDetector:
    
    def __init__(self):
        self.detection_timestamp = datetime.now()
        self.network = self.build_network()
    
    def build_network(self):
        return {
            'TSLA': {'suppliers': ['Panasonic'], 'creditors': ['JPMorgan'], 'counterparties': ['Citadel'], 'systemic': 8.2},
            'AAPL': {'suppliers': ['TSMC'], 'creditors': ['Morgan Stanley'], 'counterparties': ['Berkshire'], 'systemic': 9.5},
            'META': {'suppliers': ['Nvidia'], 'creditors': ['Deutsche Bank'], 'counterparties': ['Blackrock'], 'systemic': 7.8},
            'JPMorgan': {'suppliers': [], 'creditors': ['Federal Reserve'], 'counterparties': ['Goldman'], 'systemic': 9.8},
            'Panasonic': {'suppliers': [], 'creditors': ['MUFG'], 'counterparties': ['Sony'], 'systemic': 6.5},
            'TSMC': {'suppliers': [], 'creditors': [], 'counterparties': ['Intel'], 'systemic': 8.8},
            'Nvidia': {'suppliers': [], 'creditors': [], 'counterparties': ['AMD'], 'systemic': 7.9},
            'Goldman': {'suppliers': [], 'creditors': ['Federal Reserve'], 'counterparties': ['BofA'], 'systemic': 9.3},
            'Federal Reserve': {'suppliers': [], 'creditors': [], 'counterparties': ['JPMorgan'], 'systemic': 10.0}
        }
    
    def analyze_network_structure(self, ticker):
        if ticker not in self.network:
            return {'company': ticker, 'network_risk_score': 0.0, 'alert': 'UNKNOWN'}
        
        data = self.network[ticker]
        risk = 0
        flags = []
        
        if 0 < len(data['suppliers']) < 3:
            risk += 2.0
            flags.append(f'Low supplier diversity: {len(data["suppliers"])}')
        
        if len(data['creditors']) > 5:
            risk += 1.5
            flags.append(f'High creditor count: {len(data["creditors"])}')
        
        if data['systemic'] > 8.0:
            risk += 2.5
            flags.append(f'High systemic importance: {data["systemic"]}/10')
        
        risk = min(risk, 10.0)
        alert = 'CRITICAL' if risk >= 7.0 else 'WARNING' if risk >= 4.0 else 'NORMAL'
        
        return {'company': ticker, 'network_risk_score': risk, 'supplier_count': len(data['suppliers']), 'creditor_count': len(data['creditors']), 'red_flags': flags, 'alert': alert}
    
    def calculate_critical_nodes(self):
        scores = {}
        for company in self.network:
            data = self.network[company]
            connections = len(data['suppliers']) + len(data['creditors']) + len(data['counterparties'])
            scores[company] = data['systemic'] * 0.8 + connections * 0.2
        
        sorted_nodes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return {'critical_nodes': sorted_nodes[:3], 'centrality_scores': scores}
    
    def model_cascade_path(self, trigger, days=30):
        if trigger not in self.network:
            return {'trigger_company': trigger, 'cascade_timeline': [], 'peak_affected': 0, 'cascade_alert': 'UNKNOWN'}
        
        timeline = []
        affected = {trigger}
        failed = {trigger}
        
        timeline.append({'day': 0, 'trigger': trigger, 'newly_affected': [trigger], 'total_affected': 1, 'stage': 'TRIGGER'})
        
        for day in range(1, 8):
            new_affected = []
            for company in list(failed):
                if company in self.network:
                    data = self.network[company]
                    for supplier in data['suppliers']:
                        if supplier not in affected and supplier in self.network:
                            new_affected.append(supplier)
                            affected.add(supplier)
                    for creditor in data['creditors']:
                        if creditor not in affected and creditor in self.network:
                            new_affected.append(creditor)
                            affected.add(creditor)
                    for counterparty in data['counterparties']:
                        if counterparty not in affected and counterparty in self.network:
                            new_affected.append(counterparty)
                            affected.add(counterparty)
            
            stage = 'LOCALIZED' if len(affected) < 3 else 'SPREADING' if len(affected) < 6 else 'SYSTEMIC'
            timeline.append({'day': day, 'newly_affected': new_affected, 'total_affected': len(affected), 'stage': stage})
            
            for comp in new_affected:
                if comp in self.network and self.network[comp]['systemic'] > 7.0:
                    failed.add(comp)
        
        final_stage = timeline[-1]['stage'] if timeline else 'LOCALIZED'
        alert = 'CRITICAL' if final_stage == 'SYSTEMIC' else 'WARNING' if final_stage == 'SPREADING' else 'NORMAL'
        
        return {'trigger_company': trigger, 'cascade_timeline': timeline, 'peak_affected': len(affected), 'cascade_alert': alert}
    
    def estimate_contagion_probability(self, source, target):
        if source not in self.network or target not in self.network:
            return {'source': source, 'target': target, 'contagion_probability': 0.0, 'connection_type': 'NONE'}
        
        source_data = self.network[source]
        if target in source_data['suppliers'] or target in source_data['creditors'] or target in source_data['counterparties']:
            prob = 0.85
            conn = 'DIRECT'
        else:
            prob = 0.35
            conn = 'INDIRECT'
        
        prob = prob * (self.network[target]['systemic'] / 10.0)
        return {'source': source, 'target': target, 'contagion_probability': min(prob, 1.0), 'connection_type': conn}
    
    def generate_network_alert(self):
        critical = self.calculate_critical_nodes()
        cascade = self.model_cascade_path('TSLA', 30)
        contagion = self.estimate_contagion_probability('JPMorgan', 'AAPL')
        return {'critical_nodes': critical, 'cascade': cascade, 'contagion': contagion, 'network_alert': cascade['cascade_alert']}


if __name__ == '__main__':
    detector = NetworkCascadeDetector()
    print(detector.generate_network_alert())