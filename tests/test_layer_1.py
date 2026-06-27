"""
Tests for Layer 1: Company Risk Detection
"""

import pytest
from src.layer_1_company_risk import CompanyRiskDetector

def test_detector_initializes():
    """Test that detector initializes"""
    detector = CompanyRiskDetector()
    assert detector is not None

def test_can_analyze_company():
    """Test that we can analyze a company"""
    detector = CompanyRiskDetector()
    result = detector.generate_company_risk_alert('TSLA')
    assert result['ticker'] == 'TSLA'

def test_all_modules_present():
    """Test that all 5 modules are included"""
    detector = CompanyRiskDetector()
    assert hasattr(detector, 'analyze_news_sentiment')
    assert hasattr(detector, 'analyze_board_governance')
    assert hasattr(detector, 'analyze_strategy_risk')
    assert hasattr(detector, 'analyze_operational_health')
    assert hasattr(detector, 'analyze_competitive_position')

def test_news_sentiment_analysis():
    """Test that news sentiment analysis works"""
    detector = CompanyRiskDetector()
    result = detector.analyze_news_sentiment('TSLA')
    
    assert result['company'] == 'TSLA'
    assert 'sentiment_score' in result
    assert 'alert' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']
    assert 'negative_articles' in result

def test_sentiment_triggers_alert():
    """Test that negative sentiment triggers alerts"""
    detector = CompanyRiskDetector()
    result = detector.analyze_news_sentiment('TSLA')
    
    # TSLA has negative sentiment, should trigger alert
    assert result['alert'] in ['CRITICAL', 'WARNING']

def test_board_governance_analysis():
    """Test that board governance analysis works"""
    detector = CompanyRiskDetector()
    result = detector.analyze_board_governance('TSLA')
    
    assert result['company'] == 'TSLA'
    assert 'board_risk_score' in result
    assert 'alert' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']
    assert 'red_flags' in result
    assert isinstance(result['red_flags'], list)

def test_board_red_flags_detected():
    """Test that red flags are properly detected"""
    detector = CompanyRiskDetector()
    result = detector.analyze_board_governance('META')
    
    # META has multiple red flags, should be WARNING or CRITICAL
    assert result['alert'] in ['CRITICAL', 'WARNING']
    assert len(result['red_flags']) > 0

def test_good_governance_detected():
    """Test that good governance gets lower scores"""
    detector = CompanyRiskDetector()
    result = detector.analyze_board_governance('AAPL')
    
    # AAPL has good governance, should be NORMAL
    assert result['alert'] == 'NORMAL'
    assert len(result['red_flags']) == 0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])