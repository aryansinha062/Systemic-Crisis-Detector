"""
PROPRIETARY & CONFIDENTIAL
L8 REGULATORY - SEBI/RBI ENFORCEMENT & ALERT DETECTION
Patent Pending: "12-Layer Algorithmic Fraud Detection System"
© 2026 Aryan Sinha. All Rights Reserved.
"""

import yfinance as yf
import requests
from datetime import datetime, timedelta
import json

class RegulatoryAnalyzer:
    """
    Detect SEBI enforcement actions, RBI alerts, regulatory violations
    These are PROSPECTIVE fraud signals (appear MONTHS BEFORE insolvency)
    """
    
    def __init__(self):
        self.name = "L8_Regulatory_Enhanced"
        # Known regulatory action companies (for MVP testing)
        self.regulatory_blacklist = {
            'IndusInd Bank': 8.5,  # SEBI fraud case
            'YES Bank': 7.5,  # RBI supervisory action
            'Bhushan Steel': 8.0,  # SEBI enforcement
            'IL&FS': 9.0,  # Major enforcement
            'Satyam Computers': 9.5,  # Historic fraud
        }
    
    def check_sebi_enforcement_actions(self, company_name):
        """
        Check if company has SEBI enforcement actions
        SEBI maintains public list of enforcement cases
        RED FLAG = SEBI order against company
        """
        try:
            # Check against known enforcement cases
            if company_name in self.regulatory_blacklist:
                return self.regulatory_blacklist[company_name]
            
            # In production: scrape SEBI website for enforcement orders
            # https://www.sebi.gov.in/enforcement/
            
            # For MVP, use heuristics:
            # - Company in news for regulatory issues
            # - Recent SEBI warnings
            
            return 2.0  # No known enforcement
            
        except Exception as e:
            print(f"Error checking SEBI enforcement: {str(e)}")
            return 2.0
    
    def check_rbi_supervisory_actions(self, ticker):
        """
        Check if company has RBI supervisory actions
        RBI supervises banking sector
        RED FLAG = RBI Prompt Corrective Action (PCA) framework
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Check if banking sector
            sector = info.get('sector', '')
            
            if 'Bank' not in sector:
                return 2.0  # Non-bank, no RBI supervision
            
            # For banks, check metrics that trigger PCA:
            # - Net NPA > 6%
            # - CRAR < 9%
            # - ROA < 0%
            
            try:
                roa = info.get('returnOnAssets', 0) or 0
                
                if roa < 0:  # Negative ROA
                    return 8.0  # High risk - PCA candidate
                elif roa < 0.3:
                    return 6.5
                else:
                    return 3.0
                    
            except:
                return 3.0
                
        except Exception as e:
            print(f"Error checking RBI supervisory actions: {str(e)}")
            return 3.0
    
    def check_audit_qualifications(self, ticker):
        """
        Detect audit qualifications and going concern warnings
        RED FLAG = auditor qualifies opinion (red flag for fraud)
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Look for audit committee details
            try:
                audit_committee = info.get('auditCommittee', {}) or {}
                
                # Would parse audit report for:
                # - Going concern warnings
                # - Opinion qualifications
                # - Restatements
                
                # For MVP, use financial distress metrics as proxy
                current_ratio = info.get('currentRatio', 1.0) or 1.0
                quick_ratio = info.get('quickRatio', 1.0) or 1.0
                
                if current_ratio < 0.5 or quick_ratio < 0.3:
                    return 8.5  # Liquidity crisis = audit concern
                elif current_ratio < 1.0 or quick_ratio < 0.5:
                    return 6.5
                else:
                    return 2.5
                    
            except:
                return 3.0
                
        except Exception as e:
            print(f"Error checking audit qualifications: {str(e)}")
            return 3.0
    
    def check_stock_exchange_warnings(self, company_name):
        """
        Check NSE/BSE warnings and suspensions
        RED FLAG = stock exchange warnings (non-compliance, filing delays)
        """
        try:
            # Known exchange warnings/suspensions
            exchange_warnings = {
                'IL&FS': 9.0,
                'Satyam': 9.5,
                'Suzlon Energy': 7.5,
            }
            
            if company_name in exchange_warnings:
                return exchange_warnings[company_name]
            
            # In production: check NSE/BSE website for:
            # - Delisting notices
            # - Trading halts
            # - Filing compliance issues
            
            return 2.0
            
        except Exception as e:
            print(f"Error checking exchange warnings: {str(e)}")
            return 2.0
    
    def check_regulatory_violations(self, ticker):
        """
        Check for regulatory violations and compliance issues
        RED FLAG = repeat violations, fines, enforcement
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Check various regulatory metrics
            try:
                # Debt compliance
                total_debt = info.get('totalDebt', 0) or 0
                total_assets = info.get('totalAssets', 1) or 1
                
                debt_ratio = total_debt / total_assets
                
                # High leverage = compliance risk
                if debt_ratio > 0.8:
                    return 7.5
                elif debt_ratio > 0.6:
                    return 6.0
                else:
                    return 3.0
                    
            except:
                return 3.0
                
        except Exception as e:
            print(f"Error checking regulatory violations: {str(e)}")
            return 3.0
    
    def check_director_disqualifications(self, company_name):
        """
        Check if directors have been disqualified
        RED FLAG = director disqualification (fraud/governance issue)
        """
        try:
            # Known disqualification cases
            disqualification_cases = {
                'Satyam Computers': 9.0,
                'IL&FS': 8.5,
                'Bhushan Steel': 8.0,
            }
            
            if company_name in disqualification_cases:
                return disqualification_cases[company_name]
            
            # In production: check MCA database for director disqualifications
            # https://www.mca.gov.in/
            
            return 2.0
            
        except Exception as e:
            print(f"Error checking director disqualifications: {str(e)}")
            return 2.0
    
    def analyze(self, ticker, company_name):
        """
        Calculate overall L8_Regulatory score
        Combines: SEBI actions, RBI supervision, audit issues, exchange warnings, violations
        """
        
        sebi_score = self.check_sebi_enforcement_actions(company_name)
        rbi_score = self.check_rbi_supervisory_actions(ticker)
        audit_score = self.check_audit_qualifications(ticker)
        exchange_score = self.check_stock_exchange_warnings(company_name)
        violations_score = self.check_regulatory_violations(ticker)
        disqualification_score = self.check_director_disqualifications(company_name)
        
        # Weighted average (SEBI and RBI get highest weight - most prospective)
        l8_regulatory = (
            sebi_score * 0.25 +
            rbi_score * 0.25 +
            audit_score * 0.15 +
            exchange_score * 0.15 +
            violations_score * 0.10 +
            disqualification_score * 0.10
        )
        
        return {
            'company': company_name,
            'ticker': ticker,
            'L8_Regulatory': round(min(10, max(1, l8_regulatory)), 2),
            'sebi_enforcement': round(sebi_score, 2),
            'rbi_supervision': round(rbi_score, 2),
            'audit_issues': round(audit_score, 2),
            'exchange_warnings': round(exchange_score, 2),
            'violations': round(violations_score, 2),
            'director_disqualifications': round(disqualification_score, 2),
            'risk_level': 'HIGH REGULATORY RISK' if l8_regulatory > 7.0 else ('MEDIUM RISK' if l8_regulatory > 5.5 else 'LOW RISK')
        }

if __name__ == "__main__":
    analyzer = RegulatoryAnalyzer()
    
    print("\n" + "="*100)
    print("L8_REGULATORY ENHANCED - SEBI/RBI ENFORCEMENT DETECTION")
    print("="*100)
    
    test_companies = [
        ('INFY.NS', 'Infosys'),
        ('TCS.NS', 'TCS'),
        ('RELIANCE.NS', 'Reliance'),
    ]
    
    for ticker, name in test_companies:
        result = analyzer.analyze(ticker, name)
        print(f"\n{name}:")
        print(f"  L8_Regulatory Score: {result['L8_Regulatory']}/10")
        print(f"  SEBI Enforcement: {result['sebi_enforcement']}")
        print(f"  RBI Supervision: {result['rbi_supervision']}")
        print(f"  Audit Issues: {result['audit_issues']}")
        print(f"  Exchange Warnings: {result['exchange_warnings']}")
        print(f"  Violations: {result['violations']}")
        print(f"  Director Disqualifications: {result['director_disqualifications']}")
        print(f"  Risk Level: {result['risk_level']}")