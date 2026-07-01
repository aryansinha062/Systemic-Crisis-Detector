"""
PROPRIETARY & CONFIDENTIAL
REAL-TIME MARKET STRESS INDICATORS
Detect macro conditions favoring fraud/defaults
"""

import yfinance as yf
from datetime import datetime, timedelta
import json
import numpy as np

class RealTimeMarketStressIndicators:
    """
    Monitor market-wide stress for fraud catalysts
    Detects: Liquidity crises, credit stress, sector stress, currency stress
    """
    
    def __init__(self):
        self.name = "MarketStressIndicators_RealTime"
    
    def get_market_stress_metrics(self):
        """Fetch real-time market stress indicators"""
        
        print("\n" + "="*120)
        print("REAL-TIME MARKET STRESS INDICATORS")
        print("="*120)
        print("\nFetching real-time market stress data...\n")
        
        metrics = {}
        
        # 1. VIX (Market Volatility) - Higher = Stress
        print("  1. VIX (Market Volatility)... ", end='', flush=True)
        try:
            vix_data = yf.download('^VIX', start=datetime.now() - timedelta(days=60), 
                                   end=datetime.now(), progress=False)
            if not vix_data.empty:
                current_vix = float(vix_data['Close'].iloc[-1])
                vix_mean = float(vix_data['Close'].mean())
                vix_stress = min(10, (current_vix / 20) * 5)  # 20 = neutral, scale to 5
                metrics['VIX'] = {
                    'current': round(current_vix, 2),
                    'mean_60d': round(vix_mean, 2),
                    'stress_score': round(vix_stress, 2),
                    'interpretation': 'HIGH VOLATILITY STRESS' if vix_stress >= 6 else 'NORMAL'
                }
                print(f"✓ {current_vix:.2f}")
            else:
                metrics['VIX'] = {'stress_score': 3.0}
                print("✓ (using baseline)")
        except:
            metrics['VIX'] = {'stress_score': 3.0}
            print("✓ (using baseline)")
        
        # 2. INR/USD Exchange Rate - Depreciation = Stress
        print("  2. INR/USD (Currency Stress)... ", end='', flush=True)
        try:
            inr_data = yf.download('INRUSD=X', start=datetime.now() - timedelta(days=60),
                                   end=datetime.now(), progress=False)
            if not inr_data.empty:
                current_inr = float(inr_data['Close'].iloc[-1])
                inr_mean = float(inr_data['Close'].mean())
                inr_stress = min(10, ((current_inr - inr_mean) / inr_mean) * 20)  # % depreciation scaled
                metrics['INR_USD'] = {
                    'current': round(current_inr, 4),
                    'mean_60d': round(inr_mean, 4),
                    'stress_score': round(max(1, inr_stress), 2),
                    'interpretation': 'RUPEE DEPRECIATION STRESS' if inr_stress >= 5 else 'NORMAL'
                }
                print(f"✓ {current_inr:.2f}")
            else:
                metrics['INR_USD'] = {'stress_score': 3.0}
                print("✓ (using baseline)")
        except:
            metrics['INR_USD'] = {'stress_score': 3.0}
            print("✓ (using baseline)")
        
        # 3. Nifty 50 Performance - Down = Stress
        print("  3. Nifty 50 Performance... ", end='', flush=True)
        try:
            nifty_data = yf.download('^NSEI', start=datetime.now() - timedelta(days=60),
                                     end=datetime.now(), progress=False)
            if not nifty_data.empty:
                current_nifty = float(nifty_data['Close'].iloc[-1])
                nifty_60d = float(nifty_data['Close'].iloc[0])
                nifty_return = ((current_nifty - nifty_60d) / nifty_60d) * 100
                nifty_stress = min(10, max(1, -nifty_return / 10))  # Negative returns = stress
                metrics['Nifty50'] = {
                    'current': round(current_nifty, 2),
                    '60d_return': round(nifty_return, 2),
                    'stress_score': round(nifty_stress, 2),
                    'interpretation': 'MARKET DOWNTURN STRESS' if nifty_stress >= 5 else 'NORMAL'
                }
                print(f"✓ {nifty_return:.2f}%")
            else:
                metrics['Nifty50'] = {'stress_score': 3.0}
                print("✓ (using baseline)")
        except:
            metrics['Nifty50'] = {'stress_score': 3.0}
            print("✓ (using baseline)")
        
        # 4. US 10-Year Yield - Higher = Stress
        print("  4. US 10-Year Yield (^TNX)... ", end='', flush=True)
        try:
            yield_data = yf.download('^TNX', start=datetime.now() - timedelta(days=60),
                                     end=datetime.now(), progress=False)
            if not yield_data.empty:
                current_yield = float(yield_data['Close'].iloc[-1])
                yield_mean = float(yield_data['Close'].mean())
                yield_stress = min(10, (current_yield / 4) * 5)  # 4% = neutral
                metrics['US10Y'] = {
                    'current': round(current_yield, 2),
                    'mean_60d': round(yield_mean, 2),
                    'stress_score': round(yield_stress, 2),
                    'interpretation': 'GLOBAL YIELD STRESS' if yield_stress >= 6 else 'NORMAL'
                }
                print(f"✓ {current_yield:.2f}%")
            else:
                metrics['US10Y'] = {'stress_score': 3.0}
                print("✓ (using baseline)")
        except:
            metrics['US10Y'] = {'stress_score': 3.0}
            print("✓ (using baseline)")
        
        # 5. Crude Oil Price - Volatility = Stress
        print("  5. Crude Oil (CL=F)... ", end='', flush=True)
        try:
            oil_data = yf.download('CL=F', start=datetime.now() - timedelta(days=60),
                                   end=datetime.now(), progress=False)
            if not oil_data.empty:
                current_oil = float(oil_data['Close'].iloc[-1])
                oil_mean = float(oil_data['Close'].mean())
                oil_volatility = float(oil_data['Close'].std())
                oil_stress = min(10, (oil_volatility / oil_mean) * 20)
                metrics['CrudeOil'] = {
                    'current': round(current_oil, 2),
                    'volatility': round(oil_volatility, 2),
                    'stress_score': round(oil_stress, 2),
                    'interpretation': 'OIL PRICE VOLATILITY' if oil_stress >= 5 else 'NORMAL'
                }
                print(f"✓ ${current_oil:.2f}")
            else:
                metrics['CrudeOil'] = {'stress_score': 3.0}
                print("✓ (using baseline)")
        except:
            metrics['CrudeOil'] = {'stress_score': 3.0}
            print("✓ (using baseline)")
        
        # 6. S&P 500 Volatility
        print("  6. S&P 500 Volatility (^GSPC)... ", end='', flush=True)
        try:
            sp500_data = yf.download('^GSPC', start=datetime.now() - timedelta(days=60),
                                     end=datetime.now(), progress=False)
            if not sp500_data.empty:
                sp500_returns = sp500_data['Close'].pct_change()
                sp500_volatility = float(sp500_returns.std() * np.sqrt(252)) * 100
                sp500_stress = min(10, (sp500_volatility / 15) * 5)
                metrics['SP500'] = {
                    'volatility': round(sp500_volatility, 2),
                    'stress_score': round(sp500_stress, 2),
                    'interpretation': 'US MARKET STRESS' if sp500_stress >= 5 else 'NORMAL'
                }
                print(f"✓ {sp500_volatility:.2f}%")
            else:
                metrics['SP500'] = {'stress_score': 3.0}
                print("✓ (using baseline)")
        except:
            metrics['SP500'] = {'stress_score': 3.0}
            print("✓ (using baseline)")
        
        return metrics
    
    def calculate_overall_market_stress(self, metrics):
        """Calculate overall market stress score"""
        scores = [m.get('stress_score', 3.0) for m in metrics.values()]
        overall_stress = np.mean(scores)
        
        return {
            'overall_stress_score': round(overall_stress, 2),
            'stress_level': 'EXTREME MARKET STRESS' if overall_stress >= 7.0 else (
                'HIGH MARKET STRESS' if overall_stress >= 5.5 else (
                'MEDIUM MARKET STRESS' if overall_stress >= 4.0 else 'NORMAL MARKET CONDITIONS'
            ))
        }
    
    def get_all_market_stress_data(self):
        """Get comprehensive market stress assessment"""
        metrics = self.get_market_stress_metrics()
        overall = self.calculate_overall_market_stress(metrics)
        
        # Display results
        print("\n" + "="*120)
        print("MARKET STRESS ASSESSMENT")
        print("="*120)
        
        print(f"\nOverall Market Stress: {overall['overall_stress_score']}/10")
        print(f"Level: {overall['stress_level']}")
        
        print(f"\nIndividual Stress Indicators:")
        for indicator, data in metrics.items():
            score = data.get('stress_score', 3.0)
            interpretation = data.get('interpretation', 'N/A')
            emoji = "🚨" if score >= 6 else ("⚠️" if score >= 4 else "✅")
            print(f"  {emoji} {indicator:<20}: {score:5.2f}/10 | {interpretation}")
        
        self.save_market_stress_data(metrics, overall)
        return metrics, overall
    
    def save_market_stress_data(self, metrics, overall):
        """Save market stress data"""
        output = {
            'assessment_time': datetime.now().isoformat(),
            'metrics': metrics,
            'overall': overall
        }
        
        with open('real_time_market_stress.json', 'w') as f:
            json.dump(output, f, indent=2, default=str)
        
        print(f"\n{'='*120}")
        print("✓ MARKET STRESS DATA SAVED")
        print(f"  File: real_time_market_stress.json")
        print(f"{'='*120}\n")

if __name__ == "__main__":
    monitor = RealTimeMarketStressIndicators()
    metrics, overall = monitor.get_all_market_stress_data()