"""
REAL HISTORICAL CONTAGION DATA COLLECTOR - FINAL WORKING VERSION
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class RealContagionDataCollector:
    
    def __init__(self):
        self.contagion_events = [
            {
                'name': 'YES Bank Crisis (2020)',
                'event_date': datetime(2020, 3, 5),
                'event_type': 'banking_crisis',
                'peer_companies': ['HDFC Bank', 'ICICI Bank', 'Axis Bank'],
                'peer_tickers': ['HDFCBANK.NS', 'ICICIBANK.NS', 'AXISBANK.NS']
            },
            {
                'name': 'IL&FS Financial Crisis (2018)',
                'event_date': datetime(2018, 9, 25),
                'event_type': 'liquidity_crisis',
                'peer_companies': ['HDFC Bank', 'ICICI Bank', 'SBI'],
                'peer_tickers': ['HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS']
            }
        ]
    
    def download_stock_data(self, ticker, start_date, end_date):
        try:
            data = yf.download(ticker, start=start_date, end=end_date, progress=False, timeout=10)
            
            if data is None or data.empty:
                return None
            
            return data
        except Exception as e:
            return None
    
    def calculate_stock_impact(self, stock_data, ticker_name, event_date, weeks_after=12):
        """Calculate ACTUAL stock price impact - FIXED MultiIndex handling"""
        
        try:
            if stock_data is None or stock_data.empty:
                return None
            
            # Handle MultiIndex columns from yfinance
            if isinstance(stock_data.columns, pd.MultiIndex):
                # MultiIndex: ('Close', 'TICKER')
                close_col = [col for col in stock_data.columns if col[0] == 'Close']
                if len(close_col) == 0:
                    return None
                close_prices = stock_data[close_col[0]]
            else:
                # Regular columns: 'Close'
                if 'Close' not in stock_data.columns:
                    return None
                close_prices = stock_data['Close']
            
            # Ensure proper format
            if isinstance(close_prices, pd.DataFrame):
                close_prices = close_prices.iloc[:, 0]
            
            close_prices = close_prices.sort_index()
            close_prices.index = pd.to_datetime(close_prices.index)
            
            # Get price at or before event date
            before_event = close_prices[close_prices.index <= event_date]
            
            if len(before_event) == 0:
                return None
            
            price_at_event = float(before_event.iloc[-1])
            
            if price_at_event <= 0 or np.isnan(price_at_event):
                return None
            
            impacts = []
            
            # Measure returns for next N weeks
            for week in range(0, weeks_after + 1, 1):
                future_date = event_date + timedelta(weeks=week)
                before_future = close_prices[close_prices.index <= future_date]
                
                if len(before_future) == 0:
                    continue
                
                future_price = float(before_future.iloc[-1])
                
                if np.isnan(future_price):
                    continue
                
                return_pct = ((future_price - price_at_event) / price_at_event) * 100
                
                # Convert to risk score
                if return_pct < -30:
                    risk_score = 9.5
                elif return_pct < -20:
                    risk_score = 9.0
                elif return_pct < -15:
                    risk_score = 8.5
                elif return_pct < -10:
                    risk_score = 8.0
                elif return_pct < -5:
                    risk_score = 7.0
                elif return_pct < 0:
                    risk_score = 5.5
                elif return_pct < 5:
                    risk_score = 4.0
                else:
                    risk_score = 2.5
                
                impacts.append({
                    'week': week,
                    'return_pct': round(return_pct, 2),
                    'risk_score': risk_score
                })
            
            return impacts if len(impacts) > 0 else None
        
        except Exception as e:
            return None
    
    def measure_contagion_effect(self, event):
        print(f"\n{'='*120}")
        print(f"EVENT: {event['name']}")
        print(f"Date: {event['event_date'].strftime('%Y-%m-%d')} | Type: {event['event_type']}")
        print(f"{'='*120}")
        
        peer_impacts = {}
        print(f"\nPeer Companies ({len(event['peer_tickers'])} total):")
        
        for peer_name, peer_ticker in zip(event['peer_companies'], event['peer_tickers']):
            print(f"  {peer_ticker}: ", end='', flush=True)
            
            peer_data = self.download_stock_data(
                peer_ticker,
                event['event_date'] - timedelta(days=365),
                event['event_date'] + timedelta(weeks=12)
            )
            
            if peer_data is not None:
                peer_impact = self.calculate_stock_impact(peer_data, peer_ticker, event['event_date'])
                
                if peer_impact is not None and len(peer_impact) > 0:
                    peer_impacts[peer_name] = peer_impact
                    
                    # Extract key weeks
                    week_dict = {p['week']: p['return_pct'] for p in peer_impact}
                    week_0 = week_dict.get(0, 0)
                    week_2 = week_dict.get(2, 0)
                    week_4 = week_dict.get(4, 0)
                    week_8 = week_dict.get(8, 0)
                    
                    max_decline = min([p['return_pct'] for p in peer_impact])
                    peak_risk = max([p['risk_score'] for p in peer_impact])
                    
                    print(f"✓ | W0={week_0:7.2f}% | W2={week_2:7.2f}% | W4={week_4:7.2f}% | W8={week_8:7.2f}% | Max={max_decline:7.2f}% | Peak={peak_risk:.1f}")
                else:
                    print(f"✗ No impacts calculated")
            else:
                print(f"✗ Download failed")
        
        return {
            'event': event['name'],
            'event_date': event['event_date'].isoformat(),
            'event_type': event['event_type'],
            'peer_impacts': peer_impacts
        }
    
    def collect_all_real_data(self):
        print("\n" + "="*120)
        print("REAL HISTORICAL CONTAGION DATA COLLECTION")
        print("Measuring ACTUAL peer company stock impacts after contagion events")
        print("="*120)
        
        all_results = []
        
        for event in self.contagion_events:
            result = self.measure_contagion_effect(event)
            if result and len(result['peer_impacts']) > 0:
                all_results.append(result)
        
        self.save_results(all_results)
        return all_results
    
    def save_results(self, results):
        output = {
            'collection_date': datetime.now().isoformat(),
            'total_events': len(results),
            'data_source': 'yfinance (REAL NSE stock prices)',
            'events': results
        }
        
        with open('real_contagion_data.json', 'w') as f:
            json.dump(output, f, indent=2, default=str)
        
        print(f"\n{'='*120}")
        print("✓ REAL CONTAGION DATA SAVED")
        print(f"  File: real_contagion_data.json")
        print(f"  Events collected: {len(results)}")
        print(f"  Data source: REAL NSE stock prices from yfinance")
        print(f"{'='*120}\n")

if __name__ == "__main__":
    collector = RealContagionDataCollector()
    results = collector.collect_all_real_data()