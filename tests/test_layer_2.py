"""
Tests for Layer 2: Macro Risk Detection
"""

import pytest
from src.layer_2_macro_risk import MacroRiskDetector

def test_macro_detector_initializes():
    detector = MacroRiskDetector()
    assert detector is not None

def test_pandemic_risk_analysis():
    detector = MacroRiskDetector()
    result = detector.analyze_pandemic_risk()
    assert result['category'] == 'Pandemic Risk'
    assert 'risk_score' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_geopolitical_risk_analysis():
    detector = MacroRiskDetector()
    result = detector.analyze_geopolitical_risk()
    assert result['category'] == 'Geopolitical Risk'
    assert 'risk_score' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_economic_risk_analysis():
    detector = MacroRiskDetector()
    result = detector.analyze_economic_risk()
    assert result['category'] == 'Economic Risk'
    assert 'risk_score' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_supply_chain_risk_analysis():
    detector = MacroRiskDetector()
    result = detector.analyze_supply_chain_risk()
    assert result['category'] == 'Supply Chain Risk'
    assert 'risk_score' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_combined_macro_alert():
    detector = MacroRiskDetector()
    result = detector.generate_macro_risk_alert()
    assert 'overall_risk_score' in result
    assert 'overall_alert' in result
    assert 'pandemic' in result
    assert 'geopolitical' in result
    assert 'economic' in result
    assert 'supply_chain' in result

def test_all_macro_categories_work():
    detector = MacroRiskDetector()
    pandemic = detector.analyze_pandemic_risk()
    geo = detector.analyze_geopolitical_risk()
    econ = detector.analyze_economic_risk()
    supply = detector.analyze_supply_chain_risk()
    
    assert pandemic['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']
    assert geo['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']
    assert econ['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']
    assert supply['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

if __name__ == '__main__':
    pytest.main([__file__, '-v'])