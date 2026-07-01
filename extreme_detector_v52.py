"""
PROPRIETARY & CONFIDENTIAL
EXTREME PRECISION DETECTOR v5.2 - WITH ENHANCED LAYERS
Patent Pending: "12-Layer Algorithmic Fraud Detection System"
© 2026 Aryan Sinha. All Rights Reserved.
"""

import sys
sys.path.insert(0, 'src')

from EXTREME_PRECISION_DETECTOR_FINAL import ExtremePositionDetector
from l5_forensic_enhanced import ForensicAccountingAnalyzer
from l4_behavioral_enhanced import BehavioralAnalyzer
from l8_regulatory_enhanced import RegulatoryAnalyzer

class ExtremePositionDetectorV52:
    """
    EXTREME PRECISION v5.2 with enhanced L4, L5, L8 layers
    Uses: Forensic Accounting, Insider Trading, Regulatory Enforcement
    """
    
    def __init__(self):
        self.base_detector = ExtremePositionDetector()
        self.forensic_analyzer = ForensicAccountingAnalyzer()
        self.behavioral_analyzer = BehavioralAnalyzer()
        self.regulatory_analyzer = RegulatoryAnalyzer()
    
    def detect_fraud(self, ticker, company_name):
        """
        Run enhanced detection with L4, L5, L8 analysis
        """
        
        # Get base 12 layers (simplified)
        base_layers = {
            'L1_Sentiment': 3.0,
            'L2_Macro': 5.0,
            'L3_Network': 3.5,
            'L4_Behavioral': 0,  # Will override
            'L5_Forensic': 0,  # Will override
            'L6_Amplification': 3.0,
            'L7_Policy': 3.0,
            'L8_Regulatory': 0,  # Will override
            'L9_Geopolitical': 3.0,
            'L10_ESG': 5.0,
            'L11_PatentIP': 3.0,
            'L12_RegAlerts': 2.0,
        }
        
        # OVERRIDE with enhanced L4 (Behavioral)
        behavioral_result = self.behavioral_analyzer.analyze(ticker, company_name)
        base_layers['L4_Behavioral'] = behavioral_result['L4_Behavioral']
        
        # OVERRIDE with enhanced L5 (Forensic)
        forensic_result = self.forensic_analyzer.analyze(ticker, company_name)
        base_layers['L5_Forensic'] = forensic_result['L5_Forensic']
        
        # OVERRIDE with enhanced L8 (Regulatory)
        regulatory_result = self.regulatory_analyzer.analyze(ticker, company_name)
        base_layers['L8_Regulatory'] = regulatory_result['L8_Regulatory']
        
        # Run base detector with enhanced layers
        result = self.base_detector.detect_fraud(company_name, base_layers)
        
        # Add enhanced layer details
        result['enhanced_layers'] = {
            'L4_Behavioral': behavioral_result,
            'L5_Forensic': forensic_result,
            'L8_Regulatory': regulatory_result,
        }
        
        # Calculate risk level based on enhanced layers
        enhanced_avg = (
            behavioral_result['L4_Behavioral'] +
            forensic_result['L5_Forensic'] +
            regulatory_result['L8_Regulatory']
        ) / 3
        
        result['enhanced_layer_avg'] = round(enhanced_avg, 2)
        result['enhanced_risk'] = (
            'EXTREME FRAUD RISK' if enhanced_avg > 8.0 else
            'HIGH FRAUD RISK' if enhanced_avg > 7.0 else
            'MEDIUM RISK' if enhanced_avg > 5.5 else
            'LOW RISK'
        )
        
        return result

if __name__ == "__main__":
    detector = ExtremePositionDetectorV52()
    
    print("\n" + "="*120)
    print("EXTREME PRECISION DETECTOR v5.2 - ENHANCED LAYER TESTING".center(120))
    print("="*120)
    
    test_companies = [
        ('INFY.NS', 'Infosys'),
        ('TCS.NS', 'TCS'),
        ('RELIANCE.NS', 'Reliance'),
    ]
    
    for ticker, name in test_companies:
        result = detector.detect_fraud(ticker, name)
        print(f"\n{name}:")
        print(f"  Base Alert: {result['alert']}")
        print(f"  Base Score: {result['score']}/10")
        print(f"  Enhanced Layer Avg: {result['enhanced_layer_avg']}/10")
        print(f"  Enhanced Risk: {result['enhanced_risk']}")
        print(f"    - L4 Behavioral: {result['enhanced_layers']['L4_Behavioral']['L4_Behavioral']}/10")
        print(f"    - L5 Forensic: {result['enhanced_layers']['L5_Forensic']['L5_Forensic']}/10")
        print(f"    - L8 Regulatory: {result['enhanced_layers']['L8_Regulatory']['L8_Regulatory']}/10")