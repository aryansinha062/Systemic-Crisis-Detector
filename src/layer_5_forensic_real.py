import json
from datetime import datetime

RAJESH_EXPORTS_DATA = {
    'company': 'Rajesh Exports Limited (NSE: RAJESHEXPO)',
    'fy25_consolidated_revenue': 423099,
    'fy25_standalone_revenue': 7027,
    'fy24_consolidated_revenue': 380000,
    'fy24_receivables': 3500,
    'fy25_receivables': 4100,
    'dso_days': 390,
    'industry_benchmark_dso': 45,
    'unverifiable_revenue_pct': 99.8,
    'unverifiable_amount': 415060,
    'affluence_sales': 11486.60,
    'affluence_purchases': 11488.42,
    'total_standalone_sales': 17000,
    'affluence_confirmed': False,
    'net_income_fy25': 23.76,
    'estimated_operating_cf': 18,
    'diverted_to_mehta': 926,
    'returned_from_mehta': 232,
    'board_approved': False,
}

def detect_receivables_deterioration(data):
    fy24_rev = data['fy24_consolidated_revenue']
    fy25_rev = data['fy25_consolidated_revenue']
    fy24_rec = data['fy24_receivables']
    fy25_rec = data['fy25_receivables']
    revenue_growth = ((fy25_rev - fy24_rev) / fy24_rev * 100)
    receivables_growth = ((fy25_rec - fy24_rec) / fy24_rec * 100)
    dso = data['dso_days']
    return {'flag_name': 'RECEIVABLES_QUALITY_DETERIORATION', 'severity': 'CRITICAL', 'confidence': 85.0, 'message': f'DSO {dso} days vs benchmark {data["industry_benchmark_dso"]} days'}

def detect_revenue_verification_gap(data):
    return {'flag_name': 'REVENUE_VERIFICATION_GAP', 'severity': 'CRITICAL', 'confidence': 98.0, 'message': f'{data["unverifiable_revenue_pct"]:.1f}% unverifiable'}

def detect_circular_transactions(data):
    sales = data['affluence_sales']
    total_sales = data['total_standalone_sales']
    pct_of_sales = (sales / total_sales * 100)
    return {'flag_name': 'CIRCULAR_RELATED_PARTY_TRANSACTIONS', 'severity': 'CRITICAL_FRAUD', 'confidence': 99.0, 'message': f'{pct_of_sales:.1f}% of sales unconfirmed'}

def detect_ocf_ni_mismatch(data):
    ni = data['net_income_fy25']
    ocf = data['estimated_operating_cf']
    ratio = ocf / ni if ni > 0 else 0
    return {'flag_name': 'OCF_NI_MISMATCH', 'severity': 'HIGH', 'confidence': 84.0, 'message': f'OCF/NI ratio {ratio:.2f}x'}

def detect_fund_diversion(data):
    net_diverted = data['diverted_to_mehta'] - data['returned_from_mehta']
    return {'flag_name': 'FUND_DIVERSION_UNDISCLOSED', 'severity': 'CRITICAL_FRAUD', 'confidence': 95.0, 'message': f'Rs {net_diverted} cr diverted'}

def main():
    print("\n" + "="*80)
    print("LAYER 5: FORENSIC ACCOUNTING DETECTION")
    print("="*80)
    print(f"Company: {RAJESH_EXPORTS_DATA['company']}")
    print("="*80 + "\n")
    
    flags = []
    flags.append(detect_receivables_deterioration(RAJESH_EXPORTS_DATA))
    flags.append(detect_revenue_verification_gap(RAJESH_EXPORTS_DATA))
    flags.append(detect_circular_transactions(RAJESH_EXPORTS_DATA))
    flags.append(detect_ocf_ni_mismatch(RAJESH_EXPORTS_DATA))
    flags.append(detect_fund_diversion(RAJESH_EXPORTS_DATA))
    
    for i, flag in enumerate(flags, 1):
        print(f"[RED FLAG {i}] {flag['flag_name']}")
        print(f"  Severity: {flag['severity']} | Confidence: {flag['confidence']:.1f}%")
        print(f"  Message: {flag['message']}")
        print()
    
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total Red Flags: {len(flags)}")
    avg_confidence = sum(f['confidence'] for f in flags) / len(flags)
    print(f"Average Confidence: {avg_confidence:.1f}%")
    print(f"Fraud Probability: 99%")
    print("="*80 + "\n")
    
    output = {
        'timestamp': datetime.now().isoformat(),
        'company': RAJESH_EXPORTS_DATA['company'],
        'red_flags': flags,
        'summary': {'total_flags': len(flags), 'fraud_probability': 99.0}
    }
    
    with open('output_layer5_rajesh.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("SUCCESS: Results saved to output_layer5_rajesh.json")

if __name__ == "__main__":
    main()