import json
from datetime import datetime

class RegulatoryAlertSystem:
    def __init__(self):
        self.layer_5_score = 9.5
        self.layer_12_score = 9.2
        self.layer_6_score = 8.2
        self.layer_4_score = 3.0
        self.layer_8_score = 4.0
    
    def calculate_integrated_score(self):
        weighted = (self.layer_5_score * 0.30 + 
                   self.layer_12_score * 0.25 + 
                   self.layer_6_score * 0.15 + 
                   self.layer_4_score * 0.15 + 
                   self.layer_8_score * 0.10)
        return weighted
    
    def generate_alert(self, company_name):
        score = self.calculate_integrated_score()
        
        if score >= 8.5:
            alert_level = "🚨 CRITICAL_FRAUD"
            timeline = "WITHIN 24 HOURS"
            fraud_prob = 99.0
        elif score >= 8.0:
            alert_level = "⚠️ CRITICAL"
            timeline = "WITHIN 48 HOURS"
            fraud_prob = 95.0
        elif score >= 6.5:
            alert_level = "⚠️ HIGH_WARNING"
            timeline = "WITHIN 1 WEEK"
            fraud_prob = 85.0
        else:
            alert_level = "📊 MONITOR"
            timeline = "ROUTINE"
            fraud_prob = 50.0
        
        return {
            'alert_level': alert_level,
            'integrated_score': score,
            'fraud_probability': fraud_prob,
            'investigation_timeline': timeline,
            'company': company_name,
            'layer_breakdown': {
                'L5_Forensic': self.layer_5_score,
                'L12_Alerts': self.layer_12_score,
                'L6_Amplification': self.layer_6_score,
                'L4_Behavioral': self.layer_4_score,
                'L8_Compliance': self.layer_8_score
            }
        }
    
    def generate_investigation_roadmap(self):
        return {
            'Phase_1_Urgent_Actions': [
                'Issue formal inquiry notice within 24 hours',
                'Freeze fund transfers to related parties',
                'Notify stock exchange',
                'Request forensic auditor appointment within 48 hours',
                'Secure company records'
            ],
            'Phase_2_Documentation': [
                'Request 5-year audited financial statements',
                'Request transaction-level documentation',
                'Request ERP system access',
                'Request board meeting minutes'
            ],
            'Phase_3_Verification': [
                'Direct customer verification (top 20)',
                'Cross-border filing reconciliation',
                'Banking data verification',
                'GST & Customs verification'
            ],
            'Phase_4_Investigation': [
                'File formal investigation report',
                'Calculate fraud quantum',
                'Issue provisional order',
                'Impose penalties'
            ],
            'estimated_timeline_weeks': '10-14'
        }

def main():
    print("\n" + "="*80)
    print("LAYER 12: REGULATORY ALERT SYSTEM")
    print("="*80)
    print("Company: Rajesh Exports Limited (NSE: RAJESHEXPO)")
    print("="*80 + "\n")
    
    system = RegulatoryAlertSystem()
    alert = system.generate_alert("Rajesh Exports Limited")
    roadmap = system.generate_investigation_roadmap()
    
    print(f"Alert Level: {alert['alert_level']}")
    print(f"Integrated Risk Score: {alert['integrated_score']:.2f}/10")
    print(f"Fraud Probability: {alert['fraud_probability']:.1f}%")
    print(f"Investigation Timeline: {alert['investigation_timeline']}")
    print()
    
    print("="*80)
    print("LAYER BREAKDOWN")
    print("="*80)
    for layer, score in alert['layer_breakdown'].items():
        print(f"{layer}: {score:.1f}/10")
    print()
    
    print("="*80)
    print("INVESTIGATION ROADMAP")
    print("="*80)
    print(f"\nPhase 1 (Urgent Actions):")
    for action in roadmap['Phase_1_Urgent_Actions']:
        print(f"  • {action}")
    
    print(f"\nPhase 2 (Documentation):")
    for action in roadmap['Phase_2_Documentation']:
        print(f"  • {action}")
    
    print(f"\nPhase 3 (Verification):")
    for action in roadmap['Phase_3_Verification']:
        print(f"  • {action}")
    
    print(f"\nPhase 4 (Investigation):")
    for action in roadmap['Phase_4_Investigation']:
        print(f"  • {action}")
    
    print(f"\nEstimated Timeline: {roadmap['estimated_timeline_weeks']} weeks")
    print("="*80 + "\n")
    
    output = {
        'timestamp': datetime.now().isoformat(),
        'alert': alert,
        'investigation_roadmap': roadmap,
        'recommendation': 'TIER-1 EMERGENCY - MOVE WITHIN 24 HOURS'
    }
    
    with open('output_layer12_regulatory_alert.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("SUCCESS: Results saved to output_layer12_regulatory_alert.json")

if __name__ == "__main__":
    main()