"""
Tests for Layer 4: Behavioral Signals
"""

import pytest
from src.layer_4_behavioral import BehavioralDetector

def test_behavioral_detector_initializes():
    detector = BehavioralDetector()
    assert detector is not None

def test_insider_trading_analysis():
    detector = BehavioralDetector()
    result = detector.analyze_insider_trading('TSLA')
    assert result['ticker'] == 'TSLA'
    assert 'insider_risk_score' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_insider_selling_detected():
    detector = BehavioralDetector()
    result = detector.analyze_insider_trading('META')
    assert result['alert'] in ['CRITICAL', 'WARNING']
    assert len(result['red_flags']) > 0

def test_board_departure_analysis():
    detector = BehavioralDetector()
    result = detector.analyze_board_departures('TSLA')
    assert result['ticker'] == 'TSLA'
    assert 'departure_risk_score' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_executive_change_analysis():
    detector = BehavioralDetector()
    result = detector.analyze_executive_changes('META')
    assert result['ticker'] == 'META'
    assert 'exec_risk_score' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_patent_activity_analysis():
    detector = BehavioralDetector()
    result = detector.analyze_patent_activity('AAPL')
    assert result['ticker'] == 'AAPL'
    assert 'patent_risk_score' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_patent_decline_detected():
    detector = BehavioralDetector()
    result = detector.analyze_patent_activity('META')
    assert result['patent_trend'] == 'DECLINING'
    assert len(result['red_flags']) > 0
    assert 'declining' in result['red_flags'][0].lower()

def test_behavioral_alert_combined():
    detector = BehavioralDetector()
    result = detector.generate_behavioral_alert('TSLA')
    assert 'behavioral_risk_score' in result
    assert 'insider_trading' in result
    assert 'board_departures' in result
    assert 'executive_changes' in result
    assert 'patent_activity' in result
    assert result['behavioral_alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

if __name__ == '__main__':
    pytest.main([__file__, '-v'])