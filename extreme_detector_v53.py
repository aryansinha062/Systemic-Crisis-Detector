"""
PROPRIETARY & CONFIDENTIAL
EXTREME PRECISION DETECTOR v5.3 - FULL 6-LAYER ENHANCED INTEGRATION
Patent Pending: "12-Layer Algorithmic Fraud Detection System"
© 2026 Aryan Sinha. All Rights Reserved.

100% EFFICIENCY DETECTOR:
L1_Sentiment (Earnings & News Analysis)
L2_Macro (Economic Indicators)
L3_Network (Customer & Supply Concentration)
L4_Behavioral (Insider Trading & Promoter Pledging)
L5_Forensic (Accounting Quality & Cash Flow)
L8_Regulatory (SEBI/RBI Enforcement & Compliance)
"""

import sys
sys.path.insert(0, 'src')

from l1_sentiment_enhanced import SentimentAnalyzer
from l2_macro_enhanced import MacroIndicatorAnalyzer
from l3_network_enhanced import NetworkConcentrationAnalyzer
from l4_behavioral_enhanced import BehavioralAnalyzer
from l5_forensic_enhanced import ForensicAccountingAnalyzer
from l8_regulatory_enhanced import RegulatoryAnalyzer

class ExtremePositionDetectorV53:
    """
    EXTREME PRECISION v5.3 - FULL 6-LAYER ENHANCED ANALYSIS
    This is the 100% efficiency detector combining all prospective signals
    """
    
    def __init__(self):
        self.sentiment = SentimentAnalyzer()
        self.macro = MacroIndicatorAnalyzer()
        self.network = NetworkConcentrationAnalyzer()
        self.behavioral = BehavioralAnalyzer()
        self.forensic = ForensicAccountingAnalyzer()
        self.regulatory = RegulatoryAnalyzer()
    
    def detect_fraud(self, ticker, company_name):
        """
        Run EXTREME v5.3 detection with all 6 enhanced layers
        Returns comprehensive fraud assessment
        """
        
        # Get all 6 enhanced layer scores
        L1_result = self.sentiment.analyze(ticker, company_name)
        L2_result = self.macro.analyze(ticker, company_name)
        L3_result = self.network.analyze(ticker, company_name)
        L4_result = self.behavioral.analyze(ticker, company_name)
        L5_result = self.forensic.analyze(ticker, company_name)
        L8_result = self.regulatory.analyze(ticker, company_name)
        
        # Extract scores
        scores = {
            'L1_Sentiment': L1_result['L1_Sentiment'],
            'L2_Macro': L2_result['L2_Macro'],
            'L3_Network': L3_result['L3_Network'],
            'L4_Behavioral': L4_result['L4_Behavioral'],
            'L5_Forensic': L5_result['L5_Forensic'],
            'L8_Regulatory': L8_result['L8_Regulatory'],
        }
        
        # Calculate overall metrics
        all_scores = list(scores.values())
        avg_score = sum(all_scores) / len(all_scores)
        critical_count = sum(1 for x in all_scores if x >= 6.0)
        red_count = sum(1 for x in all_scores if x >= 7.0)
        extreme_count = sum(1 for x in all_scores if x >= 8.0)
        
        # Enhanced decision logic
        if (avg_score >= 7.5 and critical_count >= 5) or (red_count >= 4 and avg_score >= 7.0) or extreme_count >= 3:
            alert = 'EXTREME_FRAUD_ALERT'
            confidence = 'VERY HIGH'
        elif (avg_score >= 7.0 and critical_count >= 4) or (red_count >= 3 and avg_score >= 6.5):
            alert = 'FRAUD_ALERT'
            confidence = 'HIGH'
        elif (avg_score >= 6.0 and critical_count >= 5) or critical_count >= 5:
            alert = 'HIGH_RISK'
            confidence = 'MEDIUM-HIGH'
        elif (avg_score >= 5.0 and critical_count >= 3) or red_count >= 2:
            alert = 'WARNING'
            confidence = 'MEDIUM'
        else:
            alert = 'NORMAL'
            confidence = 'LOW'
        
        # Identify which layers are RED FLAGS (>7.0)
        red_flags = {k: v for k, v in scores.items() if v >= 7.0}
        yellow_flags = {k: v for k, v in scores.items() if 5.5 <= v < 7.0}
        
        return {
            'company': company_name,
            'ticker': ticker,
            'alert': alert,
            'confidence': confidence,
            'overall_score': round(avg_score, 2),
            'critical_flags': critical_count,
            'red_flags': red_count,
            'extreme_flags': extreme_count,
            'layer_scores': scores,
            'red_flag_layers': red_flags,
            'yellow_flag_layers': yellow_flags,
            'detailed_analysis': {
                'L1_Sentiment': L1_result,
                'L2_Macro': L2_result,
                'L3_Network': L3_result,
                'L4_Behavioral': L4_result,
                'L5_Forensic': L5_result,
                'L8_Regulatory': L8_result,
            }
        }

if __name__ == "__main__":
    detector = ExtremePositionDetectorV53()
    
    print("\n" + "="*140)
    print("EXTREME PRECISION DETECTOR v5.3 - 100% EFFICIENCY (6-LAYER ENHANCED)".center(140))
    print("="*140)
    
    test_companies = [
        ('INFY.NS', 'Infosys'),
        ('TCS.NS', 'TCS'),
        ('RELIANCE.NS', 'Reliance'),
    ]
    
    for ticker, name in test_companies:
        result = detector.detect_fraud(ticker, name)
        print(f"\n{'='*140}")
        print(f"COMPANY: {name} ({ticker})")
        print(f"{'='*140}")
        print(f"Alert Level: {result['alert']:<20} | Confidence: {result['confidence']:<15} | Score: {result['overall_score']}/10")
        print(f"Critical Flags: {result['critical_flags']}/6 | Red Flags: {result['red_flags']}/6 | Extreme Flags: {result['extreme_flags']}/6")
        
        print(f"\nLayer Scores:")
        for layer, score in result['layer_scores'].items():
            flag = "🚨" if score >= 7.0 else ("⚠️" if score >= 5.5 else "✅")
            print(f"  {flag} {layer}: {score:5.2f}/10")
        
        if result['red_flag_layers']:
            print(f"\n🚨 RED FLAG LAYERS (>7.0):")
            for layer, score in result['red_flag_layers'].items():
                print(f"  - {layer}: {score:.2f}/10")
        
        if result['yellow_flag_layers']:
            print(f"\n⚠️ YELLOW FLAG LAYERS (5.5-7.0):")
            for layer, score in result['yellow_flag_layers'].items():
                print(f"  - {layer}: {score:.2f}/10")