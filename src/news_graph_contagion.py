"""
PROPRIETARY & CONFIDENTIAL
L9+ NEWS GRAPH - INDIRECT CONTAGION DETECTION
Patent Pending: "12-Layer Algorithmic Fraud Detection System"
© 2026 Aryan Sinha. All Rights Reserved.

CAPTURES: Company relationships through news events
DETECTS: Indirect fraud risk via supply chain & market contagion
"""

import yfinance as yf
from collections import defaultdict
import json
from datetime import datetime, timedelta

class NewsGraphAnalyzer:
    """
    Build graph of company relationships from market events
    Detect contagion: if Company A fails, who else is at risk?
    """
    
    def __init__(self):
        self.name = "NewsGraph_Contagion"
        # Known supply chain relationships (seed data)
        self.supply_chains = {
            'Reliance': {
                'suppliers': ['Tata Steel', 'JSW Steel', 'NTPC', 'ONGC'],
                'customers': ['Adani Ports', 'Bharti Airtel', 'HUL'],
            },
            'TCS': {
                'suppliers': ['Tech Mahindra', 'HCL Tech', 'Infosys'],
                'customers': ['Most Large Indian Companies'],
            },
            'HDFC Bank': {
                'suppliers': ['SBIN', 'ICICI Bank'],
                'customers': ['All listed companies (financing)'],
            },
            'Infosys': {
                'suppliers': ['Tech Mahindra', 'HCL Tech'],
                'customers': ['Global Fortune 500'],
            },
        }
    
    def detect_customer_bankruptcy_contagion(self, ticker, company_name):
        """
        Detect if company's customers are failing
        Customer bankruptcy = RED FLAG (revenue cliff)
        """
        try:
            # Get supply chain relationships
            suppliers = self.supply_chains.get(company_name, {}).get('suppliers', [])
            customers = self.supply_chains.get(company_name, {}).get('customers', [])
            
            # Simulate customer health check
            risk_score = 2.0
            
            # Check if major customers are in distress
            distressed_customers = ['YES Bank', 'IL&FS', 'Bhushan Steel']
            
            for customer in customers:
                if isinstance(customer, str) and customer in distressed_customers:
                    risk_score = 8.5  # Major customer bankruptcy = extreme risk
                    break
            
            # In production: fetch news for "Company X bankruptcy" mentions
            # If found: flag this company
            
            return risk_score
            
        except Exception as e:
            print(f"Error detecting customer bankruptcy: {str(e)}")
            return 2.0
    
    def detect_supplier_disruption_contagion(self, ticker, company_name):
        """
        Detect if company's suppliers are failing
        Supplier bankruptcy = RED FLAG (supply chain disruption)
        """
        try:
            suppliers = self.supply_chains.get(company_name, {}).get('suppliers', [])
            
            risk_score = 2.0
            
            # Check if major suppliers are in distress
            distressed_suppliers = ['Bhushan Steel', 'IL&FS', 'Suzlon Energy']
            
            supplier_distress_count = 0
            for supplier in suppliers:
                if isinstance(supplier, str) and supplier in distressed_suppliers:
                    supplier_distress_count += 1
            
            if supplier_distress_count >= 2:
                risk_score = 8.5  # Multiple suppliers failing = supply chain collapse
            elif supplier_distress_count >= 1:
                risk_score = 7.0  # One major supplier failing = disruption risk
            
            # In production: track supplier health indices
            
            return risk_score
            
        except Exception as e:
            print(f"Error detecting supplier disruption: {str(e)}")
            return 2.0
    
    def detect_competitor_contagion(self, ticker, company_name):
        """
        Detect if competitors are failing
        Competitor fraud = risk spreads to peers (sector contagion)
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            sector = info.get('sector', 'Unknown')
            
            # Map competitors by sector
            sector_competitors = {
                'IT': ['TCS', 'Infosys', 'Wipro', 'Tech Mahindra', 'HCL Tech'],
                'Banking': ['HDFC Bank', 'ICICI Bank', 'Axis Bank', 'SBI', 'Kotak Bank'],
                'Energy': ['Reliance', 'ONGC', 'NTPC', 'GAIL', 'IOC'],
                'Steel': ['Tata Steel', 'JSW Steel', 'Bhushan Steel'],
                'Auto': ['Maruti Suzuki', 'Tata Motors', 'Mahindra', 'Hero Motocorp'],
            }
            
            risk_score = 2.0
            competitors = sector_competitors.get(sector, [])
            
            # Known enforcement/fraud cases
            fraud_cases = {
                'Satyam': 9.0,
                'IL&FS': 9.0,
                'Bhushan Steel': 8.0,
                'YES Bank': 7.5,
                'Suzlon Energy': 7.0,
            }
            
            # Check if any competitors have enforcement
            for competitor in competitors:
                if competitor in fraud_cases:
                    # Peer contagion risk
                    risk_score = max(risk_score, fraud_cases[competitor] * 0.8)
            
            # In production: parse news for "Peer company SEBI enforcement"
            # Track: does peer fraud predict sector-wide stress?
            
            return min(9.0, risk_score)
            
        except Exception as e:
            print(f"Error detecting competitor contagion: {str(e)}")
            return 2.0
    
    def detect_sector_cascade_risk(self, ticker, company_name):
        """
        Detect if sector is experiencing cascade failure
        One failure can trigger others in same sector
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            sector = info.get('sector', 'Unknown')
            
            # Track sector stress levels
            sector_stress = {
                'Energy': 5.5,  # Oil price dependent
                'Auto': 6.0,    # Cyclical, inventory risk
                'Steel': 7.0,   # Commodity crash risk
                'Banking': 6.5, # Credit crisis risk
                'IT': 4.0,      # Stable sector
            }
            
            risk_score = sector_stress.get(sector, 5.0)
            
            # In production: calculate aggregate sector health
            # If multiple companies in sector showing distress:
            # Flag all peers for cascade risk
            
            return risk_score
            
        except Exception as e:
            print(f"Error detecting sector cascade: {str(e)}")
            return 5.0
    
    def detect_regulatory_contagion(self, company_name):
        """
        Detect if regulatory action against one company signals peer risk
        SEBI enforcement in peer = regulatory sweep risk
        """
        try:
            # Known regulatory cases
            sebi_cases = {
                'Satyam': 9.0,
                'IndusInd Bank': 8.5,
                'Suzlon Energy': 8.0,
                'IL&FS': 9.0,
            }
            
            # Regulatory sweep indicators
            # When SEBI acts on one company, similar companies face scrutiny
            
            risk_score = 2.0
            
            # If peer had recent enforcement: flag this company
            for case, severity in sebi_cases.items():
                # In production: check if same sector peer had enforcement
                # within last 6-12 months
                pass
            
            # In production: track regulatory pattern
            # "SEBI enforcement on [Sector] companies" → flag entire sector
            
            return risk_score
            
        except Exception as e:
            print(f"Error detecting regulatory contagion: {str(e)}")
            return 2.0
    
    def detect_geopolitical_contagion(self, company_name):
        """
        Detect if geopolitical events affect supply chains
        Example: US-China tension → supply chain disruption
        """
        try:
            # Current geopolitical risks
            geopolitical_risks = {
                'US-China tension': 6.0,  # Tech export risk
                'Russia sanctions': 7.0,  # Energy/metals risk
                'India-Pakistan': 5.0,    # Local disruption
                'Middle East conflict': 6.5,  # Oil price spike
            }
            
            # Map companies to geopolitical exposure
            exposure_map = {
                'Tech/IT': 'US-China tension',
                'Energy': 'Middle East conflict',
                'Steel/Auto': 'Russia sanctions',
            }
            
            risk_score = 2.0
            
            # In production: track news for geopolitical events
            # Calculate exposure index for each company
            # Flag companies if geopolitical risk to their supply chain
            
            return risk_score
            
        except Exception as e:
            print(f"Error detecting geopolitical contagion: {str(e)}")
            return 2.0
    
    def analyze(self, ticker, company_name):
        """
        Calculate contagion risk from indirect sources
        """
        
        customer_bankruptcy = self.detect_customer_bankruptcy_contagion(ticker, company_name)
        supplier_disruption = self.detect_supplier_disruption_contagion(ticker, company_name)
        competitor_contagion = self.detect_competitor_contagion(ticker, company_name)
        sector_cascade = self.detect_sector_cascade_risk(ticker, company_name)
        regulatory_contagion = self.detect_regulatory_contagion(company_name)
        geopolitical_contagion = self.detect_geopolitical_contagion(company_name)
        
        # Weighted average (customer/supplier failures = highest weight)
        contagion_risk = (
            customer_bankruptcy * 0.25 +
            supplier_disruption * 0.25 +
            competitor_contagion * 0.15 +
            sector_cascade * 0.15 +
            regulatory_contagion * 0.10 +
            geopolitical_contagion * 0.10
        )
        
        return {
            'company': company_name,
            'ticker': ticker,
            'contagion_risk': round(min(10, max(1, contagion_risk)), 2),
            'customer_bankruptcy_risk': round(customer_bankruptcy, 2),
            'supplier_disruption_risk': round(supplier_disruption, 2),
            'competitor_contagion_risk': round(competitor_contagion, 2),
            'sector_cascade_risk': round(sector_cascade, 2),
            'regulatory_contagion_risk': round(regulatory_contagion, 2),
            'geopolitical_contagion_risk': round(geopolitical_contagion, 2),
            'contagion_risk_level': 'EXTREME CONTAGION RISK' if contagion_risk >= 7.5 else (
                'HIGH CONTAGION RISK' if contagion_risk >= 6.5 else (
                'MEDIUM CONTAGION RISK' if contagion_risk >= 5.0 else 'LOW CONTAGION RISK'
            ))
        }

if __name__ == "__main__":
    analyzer = NewsGraphAnalyzer()
    
    print("\n" + "="*120)
    print("NEWS GRAPH - INDIRECT CONTAGION DETECTION")
    print("="*120)
    
    test_companies = [
        ('INFY.NS', 'Infosys'),
        ('TCS.NS', 'TCS'),
        ('RELIANCE.NS', 'Reliance'),
    ]
    
    for ticker, name in test_companies:
        result = analyzer.analyze(ticker, name)
        print(f"\n{name}:")
        print(f"  Overall Contagion Risk: {result['contagion_risk']}/10")
        print(f"  Customer Bankruptcy Risk: {result['customer_bankruptcy_risk']}")
        print(f"  Supplier Disruption Risk: {result['supplier_disruption_risk']}")
        print(f"  Competitor Contagion: {result['competitor_contagion_risk']}")
        print(f"  Sector Cascade Risk: {result['sector_cascade_risk']}")
        print(f"  Regulatory Contagion: {result['regulatory_contagion_risk']}")
        print(f"  Geopolitical Risk: {result['geopolitical_contagion_risk']}")
        print(f"  Risk Level: {result['contagion_risk_level']}")