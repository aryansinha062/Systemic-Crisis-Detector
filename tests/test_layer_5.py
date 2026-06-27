"""
Tests for Layer 5: Forensic Accounting
"""

import pytest
from src.layer_5_forensic import ForensicDetector

def test_forensic_detector_initializes():
    detector = ForensicDetector()
    assert detector is not None

def test_cash_flow_quality_analysis():
    detector = ForensicDetector()
    result = detector.analyze_cash_flow_quality('TSLA')
    assert result['ticker'] == 'TSLA'
    assert 'cash_flow_risk' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_poor_cash_flow_detected():
    detector = ForensicDetector()
    result = detector.analyze_cash_flow_quality('META')
    assert result['cash_flow_risk'] > 0
    assert len(result['red_flags']) > 0

def test_receivables_quality_analysis():
    detector = ForensicDetector()
    result = detector.analyze_receivables_quality('TSLA')
    assert result['ticker'] == 'TSLA'
    assert 'receivables_risk' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_high_receivables_detected():
    detector = ForensicDetector()
    result = detector.analyze_receivables_quality('META')
    assert result['alert'] in ['CRITICAL', 'WARNING']

def test_inventory_quality_analysis():
    detector = ForensicDetector()
    result = detector.analyze_inventory_quality('AAPL')
    assert result['ticker'] == 'AAPL'
    assert 'inventory_risk' in result

def test_related_party_analysis():
    detector = ForensicDetector()
    result = detector.analyze_related_party_transactions('META')
    assert result['ticker'] == 'META'
    assert 'rpt_risk' in result

def test_forensic_alert_combined():
    detector = ForensicDetector()
    result = detector.generate_forensic_alert('META')
    assert 'forensic_risk_score' in result
    assert 'cash_flow' in result
    assert 'receivables' in result
    assert 'inventory' in result
    assert 'rpt' in result
    assert result['forensic_alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

if __name__ == '__main__':
    pytest.main([__file__, '-v'])