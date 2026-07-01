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

if __name__ == '__main__':
    pytest.main([__file__, '-v'])