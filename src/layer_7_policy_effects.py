import json
from datetime import datetime

def analyze_policy_effects():
    """Layer 7: Policy Effects - Circuit breakers, trading halts"""
    
    circuit_breaker_pct = 5  # SEBI circuit breaker at 5%
    actual_decline_pct = 56  # Stock declined 56% after SEBI order
    
    # If decline > circuit breaker = policy tools ineffective
    policy_effectiveness = min(10, (circuit_breaker_pct / actual_decline_pct) * 10)
    policy_score = 10 - policy_effectiveness  # Low effectiveness = high risk score
    
    return {
        'score': policy_score,
        'circuit_breaker_threshold': circuit_breaker_pct,
        'actual_decline': actual_decline_pct,
        'policy_effectiveness': policy_effectiveness,
        'message': 'Circuit breakers triggered but could not prevent 56% collapse',
        'conclusion': 'Policy tools manage volatility, not fundamentals'
    }

def main():
    print("\n" + "="*80)
    print("LAYER 7: POLICY EFFECTS")
    print("="*80)
    
    result = analyze_policy_effects()
    print(f"Policy Risk Score: {result['score']:.2f}/10")
    print(f"Circuit Breaker: {result['circuit_breaker_threshold']}%")
    print(f"Actual Decline: {result['actual_decline']}%")
    print(f"Policy Effectiveness: {result['policy_effectiveness']:.1f}%")
    print(f"Message: {result['message']}")
    print(f"Conclusion: {result['conclusion']}")
    print("="*80 + "\n")
    
    output = {
        'timestamp': datetime.now().isoformat(),
        'layer': 'policy',
        'score': result['score']
    }
    
    with open('output_layer7_policy.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("SUCCESS: output_layer7_policy.json")

if __name__ == "__main__":
    main()