import yfinance as yf
import json
from datetime import datetime

def fetch_quarterly_data(ticker):
    """Automatically fetch quarterly financial data from Yahoo Finance"""
    
    try:
        # Fetch stock data
        stock = yf.Ticker(ticker)
        
        # Get quarterly financials
        quarterly_financials = stock.quarterly_financials
        quarterly_balance = stock.quarterly_balance_sheet
        quarterly_cashflow = stock.quarterly_cashflow
        
        print(f"\n✓ Successfully fetched data for {ticker}")
        print(f"  Quarters available: {len(quarterly_financials.columns)}")
        
        return {
            'financials': quarterly_financials,
            'balance_sheet': quarterly_balance,
            'cashflow': quarterly_cashflow,
            'success': True
        }
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return {'success': False, 'error': str(e)}

def extract_quarterly_metrics(data):
    """Extract key metrics from quarterly data"""
    
    if not data['success']:
        return None
    
    financials = data['financials']
    balance = data['balance_sheet']
    cashflow = data['cashflow']
    
    quarters_data = []
    
    try:
        # Get all quarters
        for date in financials.columns:
            quarter_data = {
                'date': str(date.date()),
                'revenue': financials.loc['Total Revenue', date] if 'Total Revenue' in financials.index else 0,
                'operating_cash_flow': cashflow.loc['Operating Cash Flow', date] if 'Operating Cash Flow' in cashflow.index else 0,
                'net_income': financials.loc['Net Income', date] if 'Net Income' in financials.index else 0,
                'current_assets': balance.loc['Total Assets', date] if 'Total Assets' in balance.index else 0,
                'receivables': balance.loc['Accounts Receivable', date] if 'Accounts Receivable' in balance.index else 0,
            }
            quarters_data.append(quarter_data)
        
        return quarters_data
    except Exception as e:
        print(f"Error extracting metrics: {e}")
        return None

def calculate_forensic_score_for_quarter(quarter_data):
    """Run forensic detector on single quarter"""
    
    if not quarter_data:
        return 0
    
    revenue = quarter_data.get('revenue', 0)
    receivables = quarter_data.get('receivables', 0)
    ni = quarter_data.get('net_income', 0)
    ocf = quarter_data.get('operating_cash_flow', 0)
    
    score = 0
    red_flags = []
    
    # Red Flag 1: High receivables vs revenue
    if revenue > 0:
        dso = (receivables / revenue * 365)
        if dso > 300:
            score += 2.5
            red_flags.append(f"DSO: {dso:.0f} days")
    
    # Red Flag 2: OCF/NI mismatch
    if ni > 0:
        ratio = ocf / ni
        if ratio < 0.8:
            score += 2.0
            red_flags.append(f"OCF/NI: {ratio:.2f}x")
    
    return {
        'score': min(10, score),
        'red_flags': red_flags,
        'details': quarter_data
    }

def run_automated_backtest(ticker):
    """Automatically backtest system on historical quarterly data"""
    
    print("\n" + "="*80)
    print("AUTOMATED QUARTERLY BACKTEST")
    print("="*80)
    print(f"Fetching data for: {ticker}")
    print("="*80 + "\n")
    
    # Step 1: Fetch data
    data = fetch_quarterly_data(ticker)
    
    if not data['success']:
        print("Could not fetch data. System needs:")
        print("  pip install yfinance")
        return
    
    # Step 2: Extract metrics
    quarters = extract_quarterly_metrics(data)
    
    if not quarters:
        print("Could not extract metrics")
        return
    
    # Step 3: Run detector on each quarter
    print("QUARTERLY FRAUD DETECTION TIMELINE")
    print("-" * 80)
    
    results = []
    
    for quarter in sorted(quarters, key=lambda x: x['date']):
        q_result = calculate_forensic_score_for_quarter(quarter)
        
        print(f"\n{quarter['date']}")
        print(f"  Revenue: ${quarter['revenue']:.0f}")
        print(f"  Receivables: ${quarter['receivables']:.0f}")
        print(f"  Fraud Score: {q_result['score']:.1f}/10", end="")
        
        if q_result['score'] >= 5:
            print(" ⚠️ WARNING")
        elif q_result['score'] >= 7:
            print(" 🚨 CRITICAL")
        else:
            print()
        
        for flag in q_result['red_flags']:
            print(f"    • {flag}")
        
        results.append({
            'date': quarter['date'],
            'score': q_result['score'],
            'red_flags': q_result['red_flags']
        })
    
    print("\n" + "="*80)
    print("CONCLUSION")
    print("="*80)
    
    # Find when system first flagged
    critical_quarters = [r for r in results if r['score'] >= 6.5]
    
    if critical_quarters:
        first_flag = critical_quarters[0]['date']
        print(f"System first flagged at: {first_flag}")
        print(f"Red flags: {critical_quarters[0]['red_flags']}")
    else:
        print("System did not flag this quarter range as critical")
    
    # Save results
    output = {
        'timestamp': datetime.now().isoformat(),
        'ticker': ticker,
        'quarterly_scores': results,
        'first_critical_flag': critical_quarters[0]['date'] if critical_quarters else None
    }
    
    with open(f'automated_backtest_{ticker}.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✓ Results saved to automated_backtest_{ticker}.json")
    print("="*80 + "\n")

if __name__ == "__main__":
    # Install requirement first
    print("Installing yfinance...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'yfinance'])
    
    # Run backtest
    run_automated_backtest('RAJESHEXPO.NS')