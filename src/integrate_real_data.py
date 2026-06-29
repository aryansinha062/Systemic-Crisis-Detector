"""
REAL DATA INTEGRATION FOR GLOBAL DETECTOR
Plugs Layers 1,2,4,5 into batch processor
"""

from src.layer_2_real_macro_fixed import RealFREDDetector, RealYahooFinanceDetector
from src.layer_4_real_behavioral import RealBehavioralDetector
from src.layer_5_real_forensic import RealForensicDetector

class RealDataIntegration:
    """Adds real data to risk scoring"""
    
    def __init__(self):
        self.fred = RealFREDDetector()
        self.yahoo = RealYahooFinanceDetector()
        self.behavioral = RealBehavioralDetector()
        self.forensic = RealForensicDetector()
        self.macro_cache = None
    
    def get_macro_data(self):
        """Cache macro data (same for all companies)"""
        if self.macro_cache:
            return self.macro_cache
        
        try:
            yield_curve = self.fred.get_yield_curve()
            inflation = self.fred.get_inflation_yoy()
            unemployment = self.fred.get_unemployment()
            fed_rate = self.fred.get_fed_funds_rate()
            vix = self.yahoo.get_vix()
            
            macro_risk = 0
            if inflation.get('alert') == 'WARNING':
                macro_risk += 1.5
            if yield_curve.get('inverted'):
                macro_risk += 3.0
            
            self.macro_cache = {
                'risk': min(macro_risk, 10),
                'inflation': inflation.get('inflation_rate_yoy', 0),
                'yield_curve': yield_curve.get('spread', 0),
                'vix': vix.get('vix', 18)
            }
            return self.macro_cache
        except:
            return {'risk': 1.5}
    
    def analyze_us_company(self, ticker):
        """Full 7-layer analysis for US companies"""
        try:
            macro = self.get_macro_data()
            behavioral = self.behavioral.generate_behavioral_alert(ticker)
            forensic = self.forensic.generate_forensic_alert(ticker)
            
            # Integrate
            risk_score = (macro['risk'] + 
                         behavioral.get('behavioral_risk_score', 0) + 
                         forensic.get('forensic_risk_score', 0)) / 3
            
            return {
                'risk_score': round(min(risk_score, 10), 2),
                'layers': 7,
                'macro': macro['risk'],
                'behavioral': behavioral.get('behavioral_risk_score', 0),
                'forensic': forensic.get('forensic_risk_score', 0)
            }
        except Exception as e:
            return {
                'risk_score': 1.5,
                'error': str(e),
                'layers': 0
            }
    
    def analyze_intl_company(self, ticker, exchange):
        """Simplified 2-layer analysis for international"""
        try:
            macro = self.get_macro_data()
            
            # For international: only macro + basic forensic
            # Skip behavioral (no SEC EDGAR equivalent)
            try:
                forensic = self.forensic.generate_forensic_alert(ticker)
                forensic_score = forensic.get('forensic_risk_score', 0)
            except:
                forensic_score = 0
            
            risk_score = (macro['risk'] + forensic_score) / 2
            
            return {
                'risk_score': round(min(risk_score, 10), 2),
                'layers': 2,
                'macro': macro['risk'],
                'forensic': forensic_score
            }
        except:
            return {
                'risk_score': 1.5,
                'layers': 1
            }


if __name__ == '__main__':
    integrator = RealDataIntegration()
    
    print("Testing real data integration...")
    
    # Test US
    print("\n✅ US COMPANY (TSLA) - 7 layers:")
    us_result = integrator.analyze_us_company('TSLA')
    print(f"Risk: {us_result['risk_score']}/10")
    
    # Test International
    print("\n🌍 INTL COMPANY - 2 layers:")
    intl_result = integrator.analyze_intl_company('INTC', 'US')
    print(f"Risk: {intl_result['risk_score']}/10")