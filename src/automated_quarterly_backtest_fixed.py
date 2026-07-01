import yfinance as yf
import json
import pandas as pd
from datetime import datetime

def fetch_quarterly_data(ticker):
    """Automatically fetch quarterly financial data from Yahoo Finance"""
    
    try:
        stock = yf.Ticker(ticker)
        
        # Get quarterly financials
        quarterly_financials = stock.quarterly_financials
        quarterly_balance = stock.quarterly_balance_sheet
        quarterly_cashflow = stock.quarterly_cashflow
        
        print(f"\n✓ Successfully fetched data for {ticker}")
        print(f"  Quarters available: {len(quarterly_financials.columns)}")
        print(f"  Financials shape: {quarterly_financials.shape}")
        print(f"  Available metrics: {list(quarterly_financials.index[:10])}")
        
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
    """Extract key metrics from quarterly data - FIXED VERSION"""
    
    if not data['success']:
        return None
    
    financials = data['financials']
    balance = data['balance_sheet']
    cashflow = data['cashflow']
    
    quarters_data = []
    
    try:
        # Get all quarters (columns are dates)
        for date in financials.columns:
            try:
                # Try different field names that yfinance might use
                revenue = 0
                if 'Total Revenue' in financials.index:
                    revenue = float(financials.loc['Total Revenue', date]) if pd.notna(financials.loc['Total Revenue', date]) else 0
                elif 'Revenues' in financials.index:
                    revenue = float(financials.loc['Revenues', date]) if pd.notna(financials.loc['Revenues', date]) else 0
                
                # Net Income
                net_income = 0
                if 'Net Income' in financials.index:
                    net_income = float(financials.loc['Net Income', date]) if pd.notna(financials.loc['Net Income', date]) else 0
                elif 'Net Profit' in financials.index:
                    net_income = float(financials.loc['Net Profit', date]) if pd.notna(financials.loc['Net Profit', date]) else 0
                
                # Operating Cash Flow
                ocf = 0
                if 'Operating Cash Flow' in cashflow.index:
                    ocf = float(cashflow.loc['Operating Cash Flow', date]) if pd.notna(cashflow.loc['Operating Cash Flow', date]) else 0
                
                # Receivables
                receivables = 0
                if 'Accounts Receivable' in balance.index:
                    receivables = float(balance.loc['Accounts Receivable', date]) if pd.notna(balance.loc['Accounts Receivable', date]) else 0
                elif 'Current Assets' in balance.index:
                    receivables = float(balance.loc['Current Assets', date]) if pd.notna(balance.loc['Current Assets', date]) else 0
                
                quarter_data = {
                    'date': str(date.date()),
                    'revenue': revenue,
                    'operating_cash_flow': ocf,
                    'net_income': net_income,
                    'receivables': receivables,
                }
                
                quarters_data.append(quarter_data)
                
            except Exception as e:
                print(f"  Error processing quarter {date}: {e}")
                continue
        
        return quarters_data
    except Exception as e:
        print(f"Error extracting metrics: {e}")
        return None

def calculate_forensic_score_for_quarter(quarter_data, prev_quarter=None):
    """Run forensic detector on single quarter"""
    
    if not quarter_data:
        return {'score': 0, 'red_flags': []}
    
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
        elif dso > 180:
            score += 1.0
            red_flags.append(f"DSO: {dso:.0f} days (high)")
    
    # Red Flag 2: OCF/NI mismatch
    if ni > 0 and ocf > 0:
        ratio = ocf / ni
        if ratio < 0.8:
            score += 2.0
            red_flags.append(f"OCF/NI: {ratio:.2f}x")
    
    # Red Flag 3: Revenue declining
    if prev_quarter and prev_quarter.get('revenue', 0) > 0:
        rev_change = (revenue - prev_quarter['revenue']) / prev_quarter['revenue'] * 100
        if rev_change < -10:
            score += 1.5
            red_flags.append(f"Revenue down: {rev_change:.1f}%")
    
    return {
        'score': min(10, score),
        'red_flags': red_flags,
        'details': quarter_data
    }

def run_automated_backtest(ticker):
    """Automatically backtest system on historical quarterly data"""
    
    print("\n" + "="*80)
    print("AUTOMATED QUARTERLY BACKTEST (FIXED)")
    print("="*80)
    print(f"Fetching data for: {ticker}")
    print("="*80 + "\n")
    
    # Step 1: Fetch data
    data = fetch_quarterly_data(ticker)
    
    if not data['success']:
        print("Could not fetch data. System needs:")
        print("  pip install yfinance pandas")
        return
    
    # Step 2: Extract metrics
    quarters = extract_quarterly_metrics(data)
    
    if not quarters or len(quarters) == 0:
        print("Could not extract metrics from available data")
        return
    
    # Step 3: Run detector on each quarter
    print("\nQUARTERLY FRAUD DETECTION TIMELINE")
    print("-" * 80)
    
    results = []
    prev_quarter = None
    
    for quarter in sorted(quarters, key=lambda x: x['date']):
        q_result = calculate_forensic_score_for_quarter(quarter, prev_quarter)
        
        print(f"\n{quarter['date']}")
        print(f"  Revenue: ₹{quarter['revenue']:,.0f}")
        print(f"  Receivables: ₹{quarter['receivables']:,.0f}")
        print(f"  Net Income: ₹{quarter['net_income']:,.0f}")
        print(f"  Fraud Score: {q_result['score']:.2f}/10", end="")
        
        if q_result['score'] >= 7:
            print(" 🚨 CRITICAL FRAUD")
        elif q_result['score'] >= 5:
            print(" ⚠️ HIGH WARNING")
        elif q_result['score'] >= 3:
            print(" ⚠️ WARNING")
        else:
            print(" ✓ NORMAL")
        
        for flag in q_result['red_flags']:
            print(f"    • {flag}")
        
        results.append({
            'date': quarter['date'],
            'score': q_result['score'],
            'red_flags': q_result['red_flags'],
            'revenue': quarter['revenue']
        })
        
        prev_quarter = quarter
    
    print("\n" + "="*80)
    print("DETECTION SUMMARY")
    print("="*80)
    
    # Find when system first flagged
    critical_quarters = [r for r in results if r['score'] >= 5]
    
    if critical_quarters:
        first_flag = critical_quarters[0]['date']
        print(f"\n✓ System first WARNED at: {first_flag}")
        print(f"  Fraud Score: {critical_quarters[0]['score']:.2f}/10")
        print(f"  Red flags: {critical_quarters[0]['red_flags']}")
    else:
        print("\n⚠️ System did not flag critical red flags in this period")
        print("   (May indicate fraud began after these quarters)")
    
    # Save results
    output = {
        'timestamp': datetime.now().isoformat(),
        'ticker': ticker,
        'quarterly_scores': results,
        'first_warning': critical_quarters[0]['date'] if critical_quarters else None,
        'total_quarters_analyzed': len(results)
    }
    
    with open(f'automated_backtest_{ticker}.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✓ Results saved to automated_backtest_{ticker}.json\n")
    print("="*80 + "\n")

if __name__ == "__main__":
    run_automated_backtest('RAJESHEXPO.NS')