"""
Tests for Layer 1: Company Risk Detection
"""

import pytest
from src.layer_1_company_risk import CompanyRiskDetector

def test_detector_initializes():
    detector = CompanyRiskDetector()
    assert detector is not None

def test_can_analyze_company():
    detector = CompanyRiskDetector()
    result = detector.generate_company_risk_alert('TSLA')
    assert result['ticker'] == 'TSLA'

def test_all_modules_present():
    detector = CompanyRiskDetector()
    assert hasattr(detector, 'analyze_news_sentiment')
    assert hasattr(detector, 'analyze_board_governance')
    assert hasattr(detector, 'analyze_strategy_risk')
    assert hasattr(detector, 'analyze_operational_health')
    assert hasattr(detector, 'analyze_competitive_position')

def test_news_sentiment_analysis():
    detector = CompanyRiskDetector()
    result = detector.analyze_news_sentiment('TSLA')
    assert result['company'] == 'TSLA'
    assert 'sentiment_score' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_sentiment_triggers_alert():
    detector = CompanyRiskDetector()
    result = detector.analyze_news_sentiment('TSLA')
    assert result['alert'] in ['CRITICAL', 'WARNING']

def test_board_governance_analysis():
    detector = CompanyRiskDetector()
    result = detector.analyze_board_governance('TSLA')
    assert result['company'] == 'TSLA'
    assert 'board_risk_score' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_board_red_flags_detected():
    detector = CompanyRiskDetector()
    result = detector.analyze_board_governance('META')
    assert result['alert'] in ['CRITICAL', 'WARNING']
    assert len(result['red_flags']) > 0

def test_good_governance_detected():
    detector = CompanyRiskDetector()
    result = detector.analyze_board_governance('AAPL')
    assert result['alert'] == 'NORMAL'

def test_strategy_risk_analysis():
    detector = CompanyRiskDetector()
    result = detector.analyze_strategy_risk('TSLA')
    assert result['company'] == 'TSLA'
    assert 'strategy_risk_score' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_strategy_red_flags():
    detector = CompanyRiskDetector()
    result = detector.analyze_strategy_risk('META')
    assert result['alert'] in ['CRITICAL', 'WARNING']
    assert len(result['red_flags']) > 0

def test_operational_health_analysis():
    detector = CompanyRiskDetector()
    result = detector.analyze_operational_health('TSLA')
    assert result['company'] == 'TSLA'
    assert 'operational_risk_score' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_operational_red_flags():
    detector = CompanyRiskDetector()
    result = detector.analyze_operational_health('META')
    assert result['alert'] in ['CRITICAL', 'WARNING']
    assert len(result['red_flags']) > 0

def test_competitive_position_analysis():
    detector = CompanyRiskDetector()
    result = detector.analyze_competitive_position('TSLA')
    assert result['company'] == 'TSLA'
    assert 'competitive_risk_score' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_competitive_risk_detected():
    detector = CompanyRiskDetector()
    result = detector.analyze_competitive_position('META')
    assert result['alert'] in ['CRITICAL', 'WARNING']

def test_all_companies_work():
    detector = CompanyRiskDetector()
    for ticker in ['TSLA', 'AAPL', 'META']:
        sentiment = detector.analyze_news_sentiment(ticker)
        board = detector.analyze_board_governance(ticker)
        strategy = detector.analyze_strategy_risk(ticker)
        operations = detector.analyze_operational_health(ticker)
        competition = detector.analyze_competitive_position(ticker)
        
        assert sentiment['company'] == ticker
        assert board['company'] == ticker
        assert strategy['company'] == ticker
        assert operations['company'] == ticker
        assert competition['company'] == ticker

if __name__ == '__main__':
    pytest.main([__file__, '-v'])