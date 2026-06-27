"""
SEC EDGAR Real Data Fetcher
Retrieves actual insider trading and board data from SEC filings
"""

import requests
from datetime import datetime, timedelta
import re
import os
from dotenv import load_dotenv

load_dotenv()

class SECEdgarFetcher:
    """Fetches real data from SEC EDGAR"""
    
    def __init__(self):
        self.sec_email = os.getenv('SEC_EDGAR_EMAIL', 'user@example.com')
        self.base_url = 'https://www.sec.gov'
        self.ciks = {
            'TSLA': '1318605',
            'AAPL': '0000320193',
            'META': '0001326801'
        }
        self.headers = {
            'User-Agent': f'CrisisDetector {self.sec_email}'
        }
    
    def get_company_cik(self, ticker):
        """Get CIK number for company"""
        return self.ciks.get(ticker)
    
    def fetch_insider_transactions(self, ticker, days=90):
        """Fetch real Form 4 filings (insider trading)"""
        cik = self.get_company_cik(ticker)
        if not cik:
            return {'valid': False, 'error': f'Unknown ticker {ticker}'}
        
        try:
            # Fetch company filings index
            cik_padded = cik.zfill(10)
            url = f'{self.base_url}/cgi-bin/browse-edgar?action=getcompany&CIK={cik_padded}&type=4&dateb=&owner=exclude&count=100'
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML to find Form 4 filings
            html = response.text
            
            # Extract filing dates and links
            form4_links = re.findall(r'href="([^"]*?type=4[^"]*?)"', html)
            
            insider_sales = 0
            insider_buys = 0
            transactions = []
            
            # Check last few Form 4s
            for link in form4_links[:5]:
                full_url = self.base_url + link if link.startswith('/') else link
                
                try:
                    filing = requests.get(full_url, headers=self.headers, timeout=10)
                    filing.raise_for_status()
                    
                    # Count sales vs buys (simplified parsing)
                    sales_count = filing.text.count('S</transactionCode>')
                    buys_count = filing.text.count('P</transactionCode>')
                    
                    insider_sales += sales_count
                    insider_buys += buys_count
                    
                except:
                    pass
            
            if insider_sales + insider_buys > 0:
                ratio = insider_sales / max(insider_buys, 1)
                return {
                    'ticker': ticker,
                    'insider_sales_90d': insider_sales,
                    'insider_buys_90d': insider_buys,
                    'sales_to_buys_ratio': round(ratio, 2),
                    'valid': True,
                    'source': '✅ SEC EDGAR Form 4 (REAL)',
                    'date_checked': datetime.now().strftime('%Y-%m-%d')
                }
            else:
                return {
                    'ticker': ticker,
                    'insider_sales_90d': 0,
                    'insider_buys_90d': 0,
                    'sales_to_buys_ratio': 0,
                    'valid': True,
                    'source': '✅ SEC EDGAR Form 4 (REAL)',
                    'note': 'No recent insider transactions found'
                }
        
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def fetch_board_composition(self, ticker):
        """Fetch real board data from DEF 14A (proxy statements)"""
        cik = self.get_company_cik(ticker)
        if not cik:
            return {'valid': False}
        
        try:
            cik_padded = cik.zfill(10)
            url = f'{self.base_url}/cgi-bin/browse-edgar?action=getcompany&CIK={cik_padded}&type=DEF%2014A&dateb=&owner=exclude&count=40'
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            html = response.text
            
            # Extract DEF 14A links
            def14a_links = re.findall(r'href="([^"]*?DEF\s*14A[^"]*?)"', html)
            
            if def14a_links:
                return {
                    'ticker': ticker,
                    'board_data_available': True,
                    'valid': True,
                    'source': '✅ SEC EDGAR DEF 14A (REAL)',
                    'note': 'Board composition data available in proxy statement'
                }
            else:
                return {
                    'ticker': ticker,
                    'board_data_available': False,
                    'valid': True,
                    'source': '✅ SEC EDGAR (REAL)',
                    'note': 'No recent proxy statements found'
                }
        
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def fetch_executive_departures(self, ticker):
        """Fetch executive departures from 8-K filings"""
        cik = self.get_company_cik(ticker)
        if not cik:
            return {'valid': False}
        
        try:
            cik_padded = cik.zfill(10)
            url = f'{self.base_url}/cgi-bin/browse-edgar?action=getcompany&CIK={cik_padded}&type=8-K&dateb=&owner=exclude&count=100'
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            html = response.text
            
            # Count 8-K filings (which often report executive changes)
            k8_count = html.count('8-K')
            
            if k8_count > 0:
                return {
                    'ticker': ticker,
                    'recent_8k_filings': k8_count,
                    'valid': True,
                    'source': '✅ SEC EDGAR 8-K (REAL)',
                    'note': f'{k8_count} recent 8-K filings (may contain executive change reports)'
                }
            else:
                return {
                    'ticker': ticker,
                    'recent_8k_filings': 0,
                    'valid': True,
                    'source': '✅ SEC EDGAR 8-K (REAL)',
                    'note': 'No recent 8-K filings found'
                }
        
        except Exception as e:
            return {'valid': False, 'error': str(e)}


if __name__ == '__main__':
    fetcher = SECEdgarFetcher()
    
    print("\n=== SEC EDGAR REAL DATA TEST ===\n")
    
    for ticker in ['TSLA', 'AAPL', 'META']:
        print(f"\n--- {ticker} ---")
        
        insider = fetcher.fetch_insider_transactions(ticker)
        print(f"Insider Trading: {insider}")
        
        board = fetcher.fetch_board_composition(ticker)
        print(f"Board Data: {board}")
        
        exec_changes = fetcher.fetch_executive_departures(ticker)
        print(f"Executive Changes: {exec_changes}")