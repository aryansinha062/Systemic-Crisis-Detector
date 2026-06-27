"""
Layer 2: Macro-Level Risk Detection
Analyzes pandemic, geopolitical, economic, and supply chain risks
"""

from datetime import datetime

class MacroRiskDetector:
    
    def __init__(self):
        self.detection_timestamp = datetime.now()
    
    def analyze_pandemic_risk(self):
        """Analyze pandemic threat level (COVID-like events)"""
        data = {
            'current_cases_trend': 'STABLE',
            'hospitalization_rate': 0.02,
            'new_variants_detected': 1,
            'vaccination_rate': 0.68,
            'supply_chain_disruption': 'LOW',
            'risk_score': 2.5
        }
        
        if data['hospitalization_rate'] > 0.1 and data['current_cases_trend'] == 'RISING':
            alert = 'CRITICAL'
        elif data['hospitalization_rate'] > 0.05 or data['current_cases_trend'] == 'RISING':
            alert = 'WARNING'
        else:
            alert = 'NORMAL'
        
        return {
            'category': 'Pandemic Risk',
            'risk_score': data['risk_score'],
            'hospitalization_rate': data['hospitalization_rate'],
            'vaccination_rate': data['vaccination_rate'],
            'supply_chain_impact': data['supply_chain_disruption'],
            'alert': alert,
            'timestamp': self.detection_timestamp
        }
    
    def analyze_geopolitical_risk(self):
        """Analyze geopolitical threats (wars, sanctions, trade tensions)"""
        data = {
            'active_conflicts': 5,
            'escalation_trend': 'STABLE',
            'sanctions_active': 12,
            'trade_wars': 2,
            'supply_route_disruptions': 3,
            'risk_score': 5.5
        }
        
        if data['escalation_trend'] == 'ESCALATING' and data['active_conflicts'] > 3:
            alert = 'CRITICAL'
        elif data['escalation_trend'] == 'ESCALATING' or data['active_conflicts'] > 2:
            alert = 'WARNING'
        else:
            alert = 'NORMAL'
        
        return {
            'category': 'Geopolitical Risk',
            'risk_score': data['risk_score'],
            'active_conflicts': data['active_conflicts'],
            'escalation_trend': data['escalation_trend'],
            'supply_route_disruptions': data['supply_route_disruptions'],
            'alert': alert,
            'timestamp': self.detection_timestamp
        }
    
    def analyze_economic_risk(self):
        """Analyze economic indicators (yield curve, unemployment, inflation, rates)"""
        data = {
            'yield_curve_inversion': True,
            'yield_spread': -0.15,
            'unemployment_rate': 0.042,
            'unemployment_trend': 'RISING',
            'inflation_rate': 0.038,
            'inflation_trend': 'STABLE',
            'central_bank_rate': 0.045,
            'rate_trend': 'HOLDING',
            'gdp_growth': 0.018,
            'risk_score': 6.0
        }
        
        if data['yield_curve_inversion'] and data['unemployment_trend'] == 'RISING':
            alert = 'CRITICAL'
        elif data['yield_curve_inversion'] or (data['unemployment_rate'] > 0.05 and data['unemployment_trend'] == 'RISING'):
            alert = 'WARNING'
        else:
            alert = 'NORMAL'
        
        return {
            'category': 'Economic Risk',
            'risk_score': data['risk_score'],
            'yield_curve_inverted': data['yield_curve_inversion'],
            'unemployment_rate': data['unemployment_rate'],
            'unemployment_trend': data['unemployment_trend'],
            'inflation_rate': data['inflation_rate'],
            'gdp_growth': data['gdp_growth'],
            'alert': alert,
            'timestamp': self.detection_timestamp
        }
    
    def analyze_supply_chain_risk(self):
        """Analyze supply chain stress (shipping prices, delays, port congestion)"""
        data = {
            'shipping_price_index': 1850,
            'shipping_price_trend': 'RISING',
            'port_congestion_index': 72,
            'average_shipping_delay_days': 8,
            'container_shortage': True,
            'chip_shortage_status': 'EASING',
            'supply_chain_stress': 6.5,
            'risk_score': 5.8
        }
        
        if data['shipping_price_trend'] == 'RISING' and data['port_congestion_index'] > 70:
            alert = 'CRITICAL'
        elif data['shipping_price_trend'] == 'RISING' or data['average_shipping_delay_days'] > 5:
            alert = 'WARNING'
        else:
            alert = 'NORMAL'
        
        return {
            'category': 'Supply Chain Risk',
            'risk_score': data['risk_score'],
            'shipping_price_index': data['shipping_price_index'],
            'shipping_price_trend': data['shipping_price_trend'],
            'port_congestion': data['port_congestion_index'],
            'average_shipping_delay_days': data['average_shipping_delay_days'],
            'container_shortage': data['container_shortage'],
            'alert': alert,
            'timestamp': self.detection_timestamp
        }
    
    def generate_macro_risk_alert(self):
        """Generate combined macro risk alert"""
        pandemic = self.analyze_pandemic_risk()
        geopolitical = self.analyze_geopolitical_risk()
        economic = self.analyze_economic_risk()
        supply_chain = self.analyze_supply_chain_risk()
        
        combined_score = (pandemic['risk_score'] + geopolitical['risk_score'] + economic['risk_score'] + supply_chain['risk_score']) / 4
        
        if combined_score > 7.0:
            overall_alert = 'CRITICAL'
        elif combined_score > 5.0:
            overall_alert = 'WARNING'
        else:
            overall_alert = 'NORMAL'
        
        return {
            'overall_risk_score': combined_score,
            'overall_alert': overall_alert,
            'pandemic': pandemic,
            'geopolitical': geopolitical,
            'economic': economic,
            'supply_chain': supply_chain,
            'timestamp': self.detection_timestamp
        }


if __name__ == '__main__':
    detector = MacroRiskDetector()
    result = detector.generate_macro_risk_alert()
    print("Macro Risk Analysis:")
    print(result)