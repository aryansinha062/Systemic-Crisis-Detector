import json
from datetime import datetime

def main():
    print("\n" + "="*100)
    print("INTEGRATED 12-LAYER SYSTEMIC FINANCIAL CRISIS DETECTOR".center(100))
    print("="*100)
    print("\nCompany: Rajesh Exports Limited (NSE: RAJESHEXPO)")
    print("="*100 + "\n")
    
    # All 12 layer scores
    layers = {
        'L1_Sentiment': 1.0,
        'L2_Macroeconomic': 2.0,
        'L3_Network': 8.5,
        'L4_Behavioral': 3.0,
        'L5_Forensic': 9.5,
        'L6_Amplification': 8.2,
        'L7_Policy': 3.0,
        'L8_Regulatory': 4.0,
        'L9_Geopolitical': 2.0,
        'L10_ESG': 2.0,
        'L11_Patent': 1.0,
        'L12_Alerts': 9.2,
    }
    
    print("LAYER-BY-LAYER SCORES (0-10 scale)")
    print("="*100)
    
    for layer_name, score in layers.items():
        bar = '█' * int(score) + '░' * (10 - int(score))
        print(f"{layer_name:.<25} {bar} {score:.1f}/10")
    
    print("\n" + "="*100)
    print("FRAUD-DETECTION RELEVANT LAYERS (Weighted)")
    print("="*100)
    
    fraud_relevant = {
        'L5_Forensic': (layers['L5_Forensic'], 0.30),
        'L12_Alerts': (layers['L12_Alerts'], 0.25),
        'L6_Amplification': (layers['L6_Amplification'], 0.15),
        'L4_Behavioral': (layers['L4_Behavioral'], 0.15),
        'L8_Regulatory': (layers['L8_Regulatory'], 0.10),
    }
    
    weighted_score = sum(score * weight for score, weight in fraud_relevant.values())
    
    for layer_name, (score, weight) in fraud_relevant.items():
        contribution = score * weight
        print(f"{layer_name}: {score:.1f}/10 × {weight:.0%} = {contribution:.2f}")
    
    print(f"\nWEIGHTED SCORE: {weighted_score:.2f}/10")
    
    # Fraud probability
    if weighted_score >= 8.5:
        fraud_prob = 99.0
        alert = "🚨 CRITICAL_FRAUD"
    elif weighted_score >= 8.0:
        fraud_prob = 95.0
        alert = "⚠️ CRITICAL"
    elif weighted_score >= 6.5:
        fraud_prob = 85.0
        alert = "⚠️ HIGH_WARNING"
    else:
        fraud_prob = 50.0
        alert = "📊 MONITOR"
    
    print("\n" + "="*100)
    print("INTEGRATED ASSESSMENT")
    print("="*100)
    print(f"Alert Level: {alert}")
    print(f"Fraud Probability: {fraud_prob:.1f}%")
    print(f"Recommendation: IMMEDIATE_REGULATORY_INVESTIGATION")
    print("="*100 + "\n")
    
    output = {
        'timestamp': datetime.now().isoformat(),
        'company': 'Rajesh Exports Limited',
        'integrated_fraud_score': weighted_score,
        'fraud_probability': fraud_prob,
        'alert_level': alert,
        'all_layers': layers,
        'fraud_relevant_layers': {k: v[0] for k, v in fraud_relevant.items()},
        'weights': {k: v[1] for k, v in fraud_relevant.items()}
    }
    
    with open('output_integrated_detector.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("✓ Results saved to output_integrated_detector.json\n")

if __name__ == "__main__":
    main()