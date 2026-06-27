"""
Tests for Layer 6: Systemic Crisis Detection
"""

import pytest
from src.layer_6_systemic import SystemicCrisisDetector

def test_systemic_detector_initializes():
    detector = SystemicCrisisDetector()
    assert detector is not None
    assert detector.layer1 is not None

def test_vulnerability_score_calculation():
    detector = SystemicCrisisDetector()
    vuln = detector.calculate_vulnerability_score('TSLA')
    assert 0.0 <= vuln <= 1.0

def test_combine_all_layers():
    detector = SystemicCrisisDetector()
    result = detector.combine_all_layers('TSLA')
    assert result['ticker'] == 'TSLA'
    assert 'systemic_risk_score' in result
    assert result['systemic_alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_systemic_risk_tsla():
    detector = SystemicCrisisDetector()
    result = detector.combine_all_layers('TSLA')
    assert result['systemic_risk_score'] >= 0

def test_rank_critical_companies():
    detector = SystemicCrisisDetector()
    result = detector.rank_critical_companies(['TSLA', 'AAPL', 'META'])
    assert 'ranked_companies' in result
    assert len(result['ranked_companies']) == 3

def test_generate_systemic_alert():
    detector = SystemicCrisisDetector()
    result = detector.generate_systemic_alert('TSLA')
    assert result['ticker'] == 'TSLA'
    assert 'combined_analysis' in result
    assert 'cascade' in result
    assert result['systemic_alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_all_companies_work():
    detector = SystemicCrisisDetector()
    for ticker in ['TSLA', 'AAPL', 'META']:
        result = detector.combine_all_layers(ticker)
        assert result['ticker'] == ticker
        assert result['systemic_alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

if __name__ == '__main__':
    pytest.main([__file__, '-v'])